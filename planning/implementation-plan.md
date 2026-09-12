# Implementation sequence

Build one-country, individually owned listings first. Phases follow story dependencies; estimates are planning ranges, not delivery commitments.

| Phase | Stories | Indicative window | Exit evidence |
| --- | --- | --- | --- |
| 0 — Feasibility | SAL-001–006 | 2–6+ weeks; external response time unbounded | Country memo, compliance design, exact-model provider eligibility and priced operations |
| 1 — Foundation | SAL-007–009 | 2–3 weeks | Reproducible app, CI/staging and account security using synthetic data |
| 2 — Identity and profiles | SAL-010–016 | 4–6 weeks | Verification, country/visitor controls, quarantine, review and revocable publication |
| 3 — Subscription and redress | SAL-017–023 | 3–5 weeks, partly alongside phase 2 | Subscription lifecycle, notices, appeals and authority workflows |
| 4 — Operational readiness | SAL-024–029 | 3–4 weeks | Privacy, monitoring, recovery, independent security review and launch evidence |
| 5 — Observe and expand | SAL-030, then SAL-031/032 independently | 4–6 weeks observation; expansion separately estimated | Continue/narrow/stop decision; per-territory approval before enabling |

Assume two experienced full-stack engineers, part-time product/design and QA/security support, an accountable trust-and-safety lead with staffed reviewer/on-call rota, specialist local counsel and an accountant. Legal review and underwriting can run alongside synthetic foundation work. Initial planning envelope: roughly 12–20+ calendar weeks to a restricted paid pilot after feasibility starts, potentially extended materially by approvals. Re-estimate after phase 0 and the first end-to-end slice.

## Critical path and first slice

Resolve merchant/country eligibility and payment acceptance early. In parallel, establish repository/CI and stub provider contracts. Demonstrate a synthetic advertiser through verification, approved revision, sandbox payment and publication; revoke consent or verification and prove disappearance everywhere. Build notices/appeals before real onboarding.

Country memo → provider acceptance/data terms → integrations → publication/subscriptions → redress/privacy/recovery/security → pilot readiness is the release critical path. No approved acquirer means no paid pilot. Contracts and operational coverage are launch dependencies alongside software.

## Release controls

- Feasibility: SAL-001–006 produce reviewed outcomes. A rejected provider investigation can be completed while its associated launch decision remains unresolved.
- Synthetic staging: SAL-007–009, with no real IDs or payments.
- Paid pilot: SAL-029 and all transitive dependencies; ARC-001–008 approved for pilot scope; named operator release approval. Proposed cap: 25 advertisers in one approved territory, reduced if moderation capacity requires it.
- Pilot review: SAL-030 observes use after launch; it is not a prerequisite for starting that same pilot.
- Expansion: SAL-031 and SAL-032 are independent optional P1 releases requiring renewed territory, provider, language, privacy and tax evidence.

Rehearse failed/underage verification, unverifiable consent, unsafe media, outages, late payment events, paid-but-suspended profiles, cancellation, notice/appeal, urgent escalation, account takeover, withdrawal, restored-deleted data and country shutdown. Use lawful synthetic fixtures and provider-authorized test identities. Keep sensitive evidence outside Git.

## Economics and review

Monthly contribution per advertiser = subscription revenue excluding tax − processing fees − allocated verification cost − moderation/support − disputes/refunds − variable infrastructure. Cash planning includes reserves and settlement delays. Break-even advertiser count is fixed monthly cost divided by positive contribution; non-positive contribution has no viable break-even.

Measure onboarding abandonment without identity-content logs, review time, urgent coverage, appeal reversals, withdrawal latency, renewal/cancellation defects, publication failures, subscription retention and contribution. Set commercial thresholds after quotes. Zero known critical access defects, tested withdrawal bounds and staffed urgent response are readiness requirements regardless of demand.
