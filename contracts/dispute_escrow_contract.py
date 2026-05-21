"""GenLayer-style Intelligent Contract sketch for subjective escrow disputes.

Real GenLayer deployment would use gl.Contract decorators and validator/LLM
reasoning over evidence. This sketch keeps the settlement interface explicit.
"""

from __future__ import annotations

from dispute_escrow.core import DisputeCase, DisputeDecision, decide_dispute


class DisputeEscrowContract:
    def __init__(self):
        self.decisions: dict[str, DisputeDecision] = {}

    def settle_dispute(self, dispute: DisputeCase) -> DisputeDecision:
        decision = decide_dispute(dispute)
        self.decisions[dispute.dispute_id] = decision
        return decision

    def get_decision(self, dispute_id: str) -> DisputeDecision | None:
        return self.decisions.get(dispute_id)
