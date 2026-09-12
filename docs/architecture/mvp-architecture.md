# Proposed MVP architecture

Status: design proposal, not existing code or an approved provider choice.

Use a containerized modular monolith with a web frontend, API and separate worker process. Proposed baseline: TypeScript web UI, Python API, PostgreSQL, private S3-compatible object storage and a transactional outbox/job queue. Confirm frameworks and supported versions in SAL-007; pin them then. Avoid Kubernetes and a separate search engine until operational evidence justifies them. PostgreSQL handles initial directory search over approved projections.

## Modules and trust boundaries

`identity` handles accounts and roles; `verification` stores provider references and minimal assertions; `profiles` owns immutable revisions; `media` quarantines and sanitizes uploads; `moderation` owns cases and decisions; `directory` exposes approved data; `billing` manages the platform subscription; `compliance` handles notices, appeals and disclosure; `operations` handles audit, recovery and deletion.

Public responses never join directly onto verification or billing records. Staff access is role-scoped; moderators see verification outcome rather than documents. Exceptional evidence access requires a reason, short-lived authorization and audit. Billing support has no identity-document access. Privileged staff require MFA. All ownership checks are server-side.

Core records: Account, RoleGrant, VerificationAttempt, CountryPolicy, Profile, ProfileRevision, MediaAsset, ConsentRecord, ModerationCase, ModerationDecision, Notice, Appeal, Subscription, SubscriptionEvent, Entitlement, OutboxEvent, AuditEvent and DeletionRequest. Each has opaque identifiers; revisions, policies and decisions are versioned. Store only necessary legal identity fields in a separately restricted area when a documented obligation requires them. Prefer provider-hosted document capture, short raw-data retention and no biometric templates in the app.

## Publication invariant

A listing is visible only when the account is enabled, advertiser verification is valid for the country, the selected profile revision and each asset are approved, required consents remain valid, subscription entitlement is current, the country is enabled and no safety restriction exists. Enforce this on page, API, search, contact and media delivery. Payment never overrides a restriction. Revocation must invalidate cached projections and media access within the tested bound (proposed maximum 60 seconds; emergency origin denial immediate).

Profile states: draft → submitted → in_review → approved → published, with rejected, paused, suspended and archived transitions. An edit creates a new revision; it cannot mutate the approved payload. Existing approved content may remain visible while an ordinary edit is reviewed; safety-related identity, country or consent changes hide the profile until resolved. Concurrency checks prevent approval or payment for an obsolete revision from publishing new content.

Verification states: not_started, pending, verified, failed, expired, revoked, manual_review. Subscription states: pending, active, past_due, cancel_at_period_end, expired, suspended and refunded. Model financial state and content eligibility separately. Country thresholds can exceed the universal platform minimum of 18.

## Integration design

Define adapters for identity verification, visitor age assurance, payment checkout/subscriptions, moderation signals and storage. Signed server callbacks are authenticated, replay-protected, durably recorded and processed idempotently. Reconcile with providers after missing or out-of-order events. Browser success redirects do not grant rights. Provider outages keep new listings pending, with bounded retries and staff alerts; they do not silently mark checks successful.

Uploads land in private quarantine; enforce MIME/size/dimension limits, malware checks, image decoding/re-encoding and metadata removal before moderation. Deny public originals. Filters combine text normalization, multilingual rules, OCR, image signals and vetted hash matching if access is available. Human pre-publication review remains required. No filter claims to determine legality perfectly. Do not send real abuse imagery to unapproved services or store it in test fixtures.

Use hosted payment pages and provider tokens; never store card data. Sotto Salon is the seller of advertising unless the signed processor contract explicitly establishes another role. No connected accounts, split payments, worker payouts or booking entities. Country and subscription policy are configurable with audited changes.

## Operations and privacy

Use isolated development/staging/production, production secrets management, encrypted private networking/storage, restricted egress and scrubbed telemetry. Synthetic data only outside approved production processing. No ad text, identity documents, contact details or raw webhook payloads in analytics and error logs. Media storage, CDN, email, support tools, backup and moderation providers all need eligibility review.

Proposed pilot recovery targets: RPO 24 hours, RTO 8 hours, subject to ARC-006. Encrypt backups, test restoration and replay deletion/suppression ledgers before restored services become public. A country kill switch, publication freeze and provider-loss runbook must work without redeploying the application. Emergency reports remain reachable during directory shutdown.
