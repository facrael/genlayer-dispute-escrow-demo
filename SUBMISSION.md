# GenLayer Builder Submission — Dispute Escrow Demo

Topic: Projects & Milestones

Title: Dispute Escrow Demo for GenLayer Intelligent Contracts

Notes / Description:

I built a small dispute-resolution escrow demo for GenLayer-style Intelligent Contracts. The demo models a buyer/seller escrow where both sides submit claims and evidence, then the contract returns a settlement outcome: release to seller, refund buyer, split escrow, or request more evidence.

The repo includes a Python evidence schema, deterministic scoring helpers, a GenLayer-style Intelligent Contract sketch, sample dispute data, and tests for clear seller win, ambiguous evidence split, insufficient evidence, and portal-ready decision summaries.

The main technical gotcha is that dispute resolution has two layers: deterministic evidence structure and subjective judgment. The schema can be strict, but deciding whether evidence is credible, relevant, or sufficient is exactly where GenLayer’s adjudication model is useful.

Next milestone: connect this to a small frontend using genlayer-js and turn it into a “From Zero to GenLayer” tutorial around a practical dispute module.

Evidence Description: GitHub repository / dispute escrow MVP

URL: https://github.com/facrael/genlayer-dispute-escrow-demo
