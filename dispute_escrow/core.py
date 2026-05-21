"""Deterministic dispute-resolution helpers for a GenLayer-style escrow demo.

The scoring model is intentionally simple and reviewable. In a real GenLayer
Intelligent Contract, LLM/validator judgment would evaluate evidence quality;
this module keeps the policy transparent for tests and reproducible examples.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceItem:
    party: str
    kind: str
    content: str
    credibility: float

    def __post_init__(self) -> None:
        if self.party not in {"buyer", "seller"}:
            raise ValueError("party must be buyer or seller")
        if not 0 <= self.credibility <= 1:
            raise ValueError("credibility must be between 0 and 1")


@dataclass(frozen=True)
class DisputeCase:
    dispute_id: str
    buyer_claim: str
    seller_claim: str
    evidence: list[EvidenceItem]
    escrow_amount_usd: int


@dataclass(frozen=True)
class DisputeDecision:
    outcome: str
    confidence: float
    buyer_score: float
    seller_score: float
    payouts: dict[str, int]
    rationale: str


def _party_scores(evidence: list[EvidenceItem]) -> tuple[float, float]:
    buyer = sum(item.credibility for item in evidence if item.party == "buyer")
    seller = sum(item.credibility for item in evidence if item.party == "seller")
    return buyer, seller


def decide_dispute(case: DisputeCase) -> DisputeDecision:
    buyer_score, seller_score = _party_scores(case.evidence)
    total = buyer_score + seller_score

    if total < 0.75 or len(case.evidence) < 2:
        return DisputeDecision(
            outcome="request_more_evidence",
            confidence=round(total / 2, 2),
            buyer_score=round(buyer_score, 2),
            seller_score=round(seller_score, 2),
            payouts={"buyer_usd": 0, "seller_usd": 0},
            rationale="Evidence is too weak or one-sided to settle escrow safely.",
        )

    diff = seller_score - buyer_score
    if diff >= 0.55:
        return DisputeDecision(
            outcome="release_to_seller",
            confidence=round(min(0.99, diff / total + 0.5), 2),
            buyer_score=round(buyer_score, 2),
            seller_score=round(seller_score, 2),
            payouts={"buyer_usd": 0, "seller_usd": case.escrow_amount_usd},
            rationale="Seller evidence is materially stronger than buyer evidence.",
        )
    if diff <= -0.55:
        return DisputeDecision(
            outcome="refund_buyer",
            confidence=round(min(0.99, abs(diff) / total + 0.5), 2),
            buyer_score=round(buyer_score, 2),
            seller_score=round(seller_score, 2),
            payouts={"buyer_usd": case.escrow_amount_usd, "seller_usd": 0},
            rationale="Buyer evidence is materially stronger than seller evidence.",
        )

    buyer_payout = case.escrow_amount_usd // 2
    seller_payout = case.escrow_amount_usd - buyer_payout
    return DisputeDecision(
        outcome="split_escrow",
        confidence=round(1 - abs(diff) / total, 2),
        buyer_score=round(buyer_score, 2),
        seller_score=round(seller_score, 2),
        payouts={"buyer_usd": buyer_payout, "seller_usd": seller_payout},
        rationale="Evidence is credible on both sides but not decisive enough for a full payout.",
    )


def summarize_decision(case: DisputeCase, decision: DisputeDecision) -> str:
    return (
        f"Dispute {case.dispute_id}: {decision.outcome}. "
        f"Buyer evidence score={decision.buyer_score}; seller evidence score={decision.seller_score}. "
        f"Confidence={decision.confidence}. Rationale: {decision.rationale}"
    )
