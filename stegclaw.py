"""
StegClaw v1.0 — Personal Entity Upgrade
Extends STEGCLAW.md audit agent to full governed personal entity.
Reads Knowledge Vault context, evaluates actions via Triad, emits next_action.json.
Designed to run from GitHub Actions (iPhone-deployable) or locally.
"""

import json
import hashlib
import uuid
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# ── Imports with graceful fallback ───────────────────────────────────────────
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "knowledge-vault"))
    sys.path.insert(0, str(Path(__file__).parent.parent / "stegid"))
    sys.path.insert(0, str(Path(__file__).parent.parent / "llm-adapter"))
    from knowledge_vault import KnowledgeVault
    from stegid import StegIDRegistry
    from llm_adapter import LLMAdapter
    FULL_MODE = True
except ImportError:
    FULL_MODE = False

SCHEMA = "stegverse_stegclaw.v1"

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ── StegClaw Entity ───────────────────────────────────────────────────────────

class StegClaw:
    """
    Personal AI entity with governed action evaluation.
    Three activation tiers: observe | assist | stegclaw
    All actions pass through Triad gate before execution.
    Memory persists across sessions via Knowledge Vault.
    """

    def __init__(
        self,
        user_id: str,
        entity_subject_id: str,
        activation_tier: str = "assist",    # observe | assist | stegclaw
        vault_root: str = "./vault_data",
        registry_path: str = "./stegid_registry.jsonl",
        output_dir: str = "./brain_reports",
        triad_path: str = None,
    ):
        self.user_id = user_id
        self.subject_id = entity_subject_id
        self.tier = activation_tier
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.receipts_path = self.output_dir / "stegclaw_receipts.jsonl"

        if FULL_MODE:
            self.vault   = KnowledgeVault(vault_root)
            self.stegid  = StegIDRegistry(registry_path)
            self.adapter = LLMAdapter(triad_validator_path=triad_path)
        else:
            self.vault = self.stegid = self.adapter = None

        self.session_id  = str(uuid.uuid4())
        self.session_log = []
        self.context     = {}

    # ── Session lifecycle ─────────────────────────────────────────────────

    def start_session(self) -> dict:
        """Load vault context. Emit session-start receipt."""
        if FULL_MODE and self.vault:
            self.context = self.vault.load_entity_context(
                self.user_id, actor=self.subject_id
            )
        else:
            self.context = {"user_id": self.user_id, "working_memory": [], "consent_ledger": []}

        receipt = self._make_receipt("ALLOW", "Session started.", "session_start")
        self._emit(receipt)
        return {"session_id": self.session_id, "tier": self.tier, "receipt": receipt}

    def end_session(self) -> dict:
        """Save session summary to vault. Emit session-end receipt."""
        summary = {
            "session_id": self.session_id,
            "tier": self.tier,
            "actions_evaluated": len(self.session_log),
            "actions_allowed": sum(1 for a in self.session_log if a.get("decision") == "ALLOW"),
            "ended_at": now(),
        }
        if FULL_MODE and self.vault:
            self.vault.save_session_summary(self.user_id, summary, actor=self.subject_id)

        receipt = self._make_receipt("ALLOW", "Session ended and summary saved.", "session_end")
        self._emit(receipt)
        return {"summary": summary, "receipt": receipt}

    # ── Action evaluation ─────────────────────────────────────────────────

    def propose_action(self, intent: str, payload: dict = None) -> dict:
        """
        Evaluate a proposed action through the Triad gate.
        Returns ALLOW/DENY/FAIL_CLOSED with receipt.
        Does NOT execute — caller decides whether to proceed.
        """
        if FULL_MODE and self.adapter:
            result = self.adapter.evaluate_action(
                prompt=intent,
                user_id=self.user_id,
                entity_subject_id=self.subject_id,
                action_intent=intent,
                activation_tier=self.tier,
                context=payload,
            )
        else:
            # Offline fallback: conservative inline evaluation
            result = self._offline_evaluate(intent)

        self.session_log.append({
            "intent": intent,
            "decision": result["decision"],
            "action_class": result.get("action_class"),
            "timestamp": now(),
        })
        return result

    def _offline_evaluate(self, intent: str) -> dict:
        """Conservative fallback when Triad not available."""
        safe_intents = ["read", "check", "view", "list", "show", "get", "observe"]
        is_safe = any(w in intent.lower() for w in safe_intents)
        decision = "ALLOW" if (is_safe and self.tier in ["assist", "stegclaw"]) else "FAIL_CLOSED"
        return {
            "decision": decision,
            "action_class": "observe" if is_safe else "unknown",
            "reason": "Offline evaluation — Triad not available.",
            "receipt": self._make_receipt(decision, f"Offline: {intent}", "offline_eval"),
        }

    # ── StegBrain next-action loop ────────────────────────────────────────

    def produce_next_action(self, ecosystem_state: dict = None) -> dict:
        """
        Read ecosystem state, produce next_action.json.
        This is the StegBrain loop operating at entity level.
        """
        state = ecosystem_state or self._read_ecosystem_state()

        # Determine blockers
        blockers = []
        if not state.get("core_lite_healthy"):
            blockers.append("Core-Lite CGE not healthy")
        if not state.get("vault_provisioned"):
            blockers.append("Knowledge Vault not provisioned")
        if not state.get("stegid_registered"):
            blockers.append("StegID not registered")

        # Determine next action
        if blockers:
            next_action = {
                "action": "BLOCKED",
                "reason": "; ".join(blockers),
                "blockers": blockers,
                "suggested_resolution": "Complete infrastructure prerequisites before entity activation.",
            }
        elif not state.get("triad_validated"):
            next_action = {
                "action": "RUN_TRIAD_VALIDATION",
                "description": "Run triad_validator.py against candidate vectors to confirm gate is operational.",
                "command": "python triad_validator.py --vectors candidate_vectors/ --report triad_report.json",
                "expected_output": "triad_report.json with ALLOW outcomes for valid candidates.",
            }
        elif not state.get("session_loop_active"):
            next_action = {
                "action": "ACTIVATE_SESSION_LOOP",
                "description": "Wire LLM Adapter to session start/end and vault read/write.",
                "steps": [
                    "1. Call stegclaw.start_session() at conversation start",
                    "2. Call stegclaw.propose_action(intent) before any write",
                    "3. Execute only if decision == ALLOW",
                    "4. Call stegclaw.end_session() at conversation end",
                ],
            }
        else:
            next_action = {
                "action": "OPERATE",
                "description": "Entity is active and governed. Proceed with user requests.",
                "tier": self.tier,
            }

        output = {
            "schema": "stegverse_next_action.v1",
            "generated_at": now(),
            "session_id": self.session_id,
            "entity_subject_id": self.subject_id,
            "user_id": self.user_id,
            "tier": self.tier,
            "ecosystem_state": state,
            "blockers": blockers,
            "next_action": next_action,
            "unknowns": [],
        }

        # Write next_action.json
        na_path = self.output_dir / "next_action.json"
        with open(na_path, "w") as f:
            json.dump(output, f, indent=2)

        receipt = self._make_receipt("ALLOW", f"next_action produced: {next_action['action']}", "next_action")
        self._emit(receipt)
        output["receipt"] = receipt
        return output

    def _read_ecosystem_state(self) -> dict:
        """
        Read current ecosystem health from available signals.
        In production: reads CGE fingerprint, run summaries, StegID, vault.
        """
        state = {
            "core_lite_healthy": False,
            "vault_provisioned": False,
            "stegid_registered": False,
            "triad_validated": False,
            "session_loop_active": False,
        }

        # Check vault
        if FULL_MODE and self.vault:
            try:
                ctx = self.vault.load_entity_context(self.user_id, actor=self.subject_id)
                state["vault_provisioned"] = len(ctx.get("working_memory", [])) > 0
            except Exception:
                pass

        # Check StegID
        if FULL_MODE and self.stegid:
            identity = self.stegid.lookup(self.subject_id)
            state["stegid_registered"] = identity is not None

        # Check for CGE fingerprint
        cge_paths = [
            Path(".stegverse/cge_fingerprint.json"),
            Path("../core_lite/.stegverse/cge_fingerprint.json"),
        ]
        for p in cge_paths:
            if p.exists():
                try:
                    with open(p) as f:
                        cge = json.load(f)
                    state["core_lite_healthy"] = cge.get("status") == "healthy"
                    break
                except Exception:
                    pass

        # Check for triad results
        triad_paths = [
            Path("../triad/brain_reports/triad_receipts.jsonl"),
            Path("brain_reports/triad_receipts.jsonl"),
        ]
        for p in triad_paths:
            if p.exists() and p.stat().st_size > 0:
                state["triad_validated"] = True
                break

        return state

    # ── Vault convenience ─────────────────────────────────────────────────

    def remember(self, key: str, value: dict, evidence_grade: str = "B") -> dict:
        """Write to working memory if ALLOW'd."""
        result = self.propose_action(f"vault_write:{key}")
        if result["decision"] != "ALLOW":
            return result

        if FULL_MODE and self.vault:
            return self.vault.write(
                self.user_id, "working_memory", key, value,
                actor=self.subject_id, evidence_grade=evidence_grade
            )
        return {"status": "vault_unavailable", "key": key}

    def recall(self, key: str = None) -> dict:
        """Read from working memory."""
        result = self.propose_action("vault_read")
        if result["decision"] != "ALLOW":
            return result

        if FULL_MODE and self.vault:
            return self.vault.read(
                self.user_id, "working_memory", key=key, actor=self.subject_id
            )
        return {"status": "vault_unavailable"}

    def add_genealogy(self, cid: str, data: dict, evidence_grade: str, privacy: str = "private") -> dict:
        """Write a genealogy record if ALLOW'd."""
        result = self.propose_action(f"vault_write:genealogy:{cid}")
        if result["decision"] != "ALLOW":
            return result

        if FULL_MODE and self.vault:
            return self.vault.write_genealogy_record(
                self.user_id, cid, data, evidence_grade,
                actor=self.subject_id, privacy=privacy
            )
        return {"status": "vault_unavailable"}

    # ── Receipt helpers ───────────────────────────────────────────────────

    def _make_receipt(self, decision: str, reason: str, ref: str) -> dict:
        return {
            "schema": "stegverse_stegclaw_receipt.v1",
            "generated_at": now(),
            "engine": "stegclaw",
            "input_ref": f"{self.session_id}:{ref}",
            "actor_or_source": self.subject_id,
            "decision": decision,
            "reason": reason,
            "hashes": {"session_hash": sha256(self.session_id)},
            "unknowns": [],
            "next_route": "vault_write" if decision == "ALLOW" else "quarantine",
        }

    def _emit(self, receipt: dict):
        with open(self.receipts_path, "a") as f:
            f.write(json.dumps(receipt) + "\n")


# ── GitHub Actions entrypoint ─────────────────────────────────────────────────

def run_github_actions_mode():
    """
    Entrypoint for GitHub Actions workflow.
    Reads environment variables, produces brain_reports/ artifacts.
    """
    user_id    = os.environ.get("STEGCLAW_USER_ID", "user_001")
    subject_id = os.environ.get("STEGCLAW_SUBJECT_ID", "steg:agent/personal:default")
    tier       = os.environ.get("STEGCLAW_TIER", "assist")
    output_dir = os.environ.get("STEGCLAW_OUTPUT_DIR", "brain_reports")
    vault_root = os.environ.get("STEGCLAW_VAULT_ROOT", "./vault_data")

    print(f"StegClaw starting: user={user_id} tier={tier}")

    entity = StegClaw(
        user_id=user_id,
        entity_subject_id=subject_id,
        activation_tier=tier,
        vault_root=vault_root,
        output_dir=output_dir,
    )

    session = entity.start_session()
    print(f"Session started: {session['session_id']}")

    next_action = entity.produce_next_action()
    print(f"Next action: {next_action['next_action']['action']}")
    print(json.dumps(next_action['next_action'], indent=2))

    summary = entity.end_session()
    print(f"Session ended. Actions evaluated: {summary['summary']['actions_evaluated']}")

    # Write result report
    report = {
        "schema": "stegverse_stegclaw_run_report.v1",
        "generated_at": now(),
        "user_id": user_id,
        "tier": tier,
        "session_id": session["session_id"],
        "next_action": next_action["next_action"],
        "blockers": next_action["blockers"],
        "ecosystem_state": next_action["ecosystem_state"],
    }
    report_path = Path(output_dir) / "stegclaw_run_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    if os.environ.get("GITHUB_ACTIONS"):
        run_github_actions_mode()
    else:
        # Local demo
        print("=== StegClaw Local Demo ===")
        entity = StegClaw(
            user_id="user_001",
            entity_subject_id="steg:agent/personal:demo001",
            activation_tier="assist",
            vault_root="./vault_demo",
            output_dir="./brain_reports_demo",
        )

        session = entity.start_session()
        print(f"Session: {session['session_id']}")

        for intent in ["read my genealogy", "save session note", "deploy new workflow", "pay 100 StegCoin"]:
            r = entity.propose_action(intent)
            print(f"  [{r['decision']:<12}] {intent!r}")

        entity.remember("demo_goal", {"text": "Complete Genesis activation", "priority": "high"})

        na = entity.produce_next_action()
        print(f"\nNext action: {na['next_action']['action']}")

        entity.end_session()
        print("Demo complete.")
