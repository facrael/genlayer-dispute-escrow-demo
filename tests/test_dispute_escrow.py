from dispute_escrow.core import EvidenceItem, DisputeCase, decide_dispute, summarize_decision


def test_clear_delivery_evidence_releases_funds_to_seller():
    case = DisputeCase(
        dispute_id="d_001",
        buyer_claim="Item was not delivered",
        seller_claim="Item was delivered and accepted",
        evidence=[
            EvidenceItem(party="seller", kind="tracking", content="Carrier shows delivered to buyer address", credibility=0.9),
            EvidenceItem(party="seller", kind="buyer_message", content="Buyer confirmed receipt", credibility=0.8),
            EvidenceItem(party="buyer", kind="text", content="I do not remember receiving it", credibility=0.3),
        ],
        escrow_amount_usd=250,
    )

    decision = decide_dispute(case)

    assert decision.outcome == "release_to_seller"
    assert decision.confidence >= 0.70
    assert decision.payouts == {"buyer_usd": 0, "seller_usd": 250}


def test_ambiguous_evidence_splits_escrow():
    case = DisputeCase(
        dispute_id="d_002",
        buyer_claim="Delivered item was materially different from listing",
        seller_claim="Item matched the listing",
        evidence=[
            EvidenceItem(party="buyer", kind="photo", content="Photo shows model mismatch", credibility=0.65),
            EvidenceItem(party="seller", kind="listing", content="Listing description is somewhat ambiguous", credibility=0.55),
        ],
        escrow_amount_usd=100,
    )

    decision = decide_dispute(case)

    assert decision.outcome == "split_escrow"
    assert decision.payouts == {"buyer_usd": 50, "seller_usd": 50}


def test_insufficient_evidence_requests_more_information():
    case = DisputeCase(
        dispute_id="d_003",
        buyer_claim="Service was not completed",
        seller_claim="Service was completed",
        evidence=[EvidenceItem(party="buyer", kind="text", content="No proof attached", credibility=0.2)],
        escrow_amount_usd=400,
    )

    decision = decide_dispute(case)

    assert decision.outcome == "request_more_evidence"
    assert decision.payouts == {"buyer_usd": 0, "seller_usd": 0}


def test_summary_contains_portal_ready_reasoning():
    case = DisputeCase(
        dispute_id="d_004",
        buyer_claim="Work incomplete",
        seller_claim="Work complete",
        evidence=[EvidenceItem(party="buyer", kind="milestone", content="Missing final deliverable", credibility=0.75)],
        escrow_amount_usd=1000,
    )

    decision = decide_dispute(case)
    summary = summarize_decision(case, decision)

    assert "d_004" in summary
    assert decision.outcome in summary
    assert "evidence" in summary.lower()
