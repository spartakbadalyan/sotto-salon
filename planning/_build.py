# WARNING: one-time bootstrap scaffolder. Re-running this OVERWRITES planning/roadmap.yaml
# and every planning/stories/SAL-*.md, discarding any recorded code_impact.actual,
# verification.evidence, status changes, and implementation notes. The roadmap is now the
# living source of truth; edit it directly instead of re-running this script.
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
STORIES = []

def add(n, epic, title, deps, decisions, paths, outcome, requirements, api, failure, criteria):
    sid = f'SAL-{n:03}'
    paths = paths.split('|')
    verification = [f'Acceptance walkthrough for {sid} with recorded results', 'Relevant negative-path integration tests using lawful synthetic fixtures' if n > 6 and n < 29 else 'Named specialist review and evidence references; record any no-go outcome']
    story = dict(id=sid, epic_id=f'EPIC-{epic:02}', title=title, status='planned', priority='P1' if n > 30 else 'P0', assignee=None, depends_on=[f'SAL-{d:03}' for d in deps], blocked_by_decisions=[f'ARC-{d:03}' for d in decisions], requirements_file=f'planning/stories/{sid}.md', code_impact={'planned':[{'path':p,'action':'create'} for p in paths], 'actual':[]}, verification={'planned':verification,'evidence':[]}, implementation={'pull_request':None,'commits':[],'notes':[]})
    STORIES.append(story)
    sections = [f'# {sid}: {title}', f'Epic: EPIC-{epic:02}. Tracking: `planning/roadmap.yaml`.', '## Outcome', outcome, '## Scope', f'{title}. Follow `docs/product/mvp.md` and the roadmap dependencies. No service payments, commissions or booking functionality.', '## Requirements', '\n'.join('- '+s for s in requirements.split('|')), '## Data and API', api, '## Failure and Security', failure, '## Acceptance Criteria', '\n'.join(f'- {sid}-AC{i:02}: {s}' for i,s in enumerate(criteria.split('|'),1)), '## Verification', '\n'.join('- '+s for s in verification), '## Code Impact', '\n'.join(f'- Create `{p}`.' for p in paths), '## Definition of Done', 'Acceptance criteria have actual evidence, failure paths are reviewed, and applicable decisions are resolved before live use. Update actual files and results in the roadmap. An investigation may conclude no-go without approving its associated release decision.']
    (ROOT/story['requirements_file']).write_text('\n\n'.join(sections)+'\n',encoding='utf-8')

(ROOT/'planning/stories').mkdir(parents=True,exist_ok=True)

add(1,1,'Confirm business model and first-country eligibility',[],[],
'docs/legal/country-matrix.md|docs/legal/merchant-model.md',
'Identify a legally reviewed territory for an advertising-only paid pilot.',
'Review entity domicile and exact ad/contact flows with local counsel.|Evaluate Belgium first as a proposal; document Dutch and Swiss expansion questions including local permits, ages, advertising restrictions and operator classification.|Record self-advertising, fixed fees, exploitation/reporting obligations and review dates.',
'Country matrix: territory/locality, legal source/effective date, reviewer, minimum age, evidence requirements and enablement decision.',
'Unknown or adverse findings keep the territory disabled; privileged advice stays outside Git.',
'Reviewed memo covers the exact entity and advertiser subscription/external-contact flows.|Each candidate has an explicit approved, rejected or unresolved assessment.|Pilot conditions include local age/permit, content and reporting requirements.|Named decision maker records first-territory go/no-go and review date.')
add(2,1,'Establish compliance, privacy and commercial policies',[1],[],
'docs/legal/obligations-register.md|docs/privacy/dpia.md|docs/legal/subscription-policy.md',
'Convert applicable duties into owned controls before sensitive-data processing.',
'Map DSA classification, Articles 15/19/29 exemptions, Articles 30-32 scope, representative and regulator; no blanket exemption from absent checkout.|Document purpose-level GDPR bases, Article 9 conditions, DPIA, biometrics, transfers, retention and DPO assessment.|Review renewals, cancellation/refunds, tax/VAT, business-user status, Swiss law, accessibility and reporting obligations.|Resolve ad beneficiary/payer disclosure against pseudonymity and visitor-age requirements.',
'Versioned obligations record applicability, source, owner, control/story, evidence, review trigger and deadline.',
'Unresolved lawful processing or public-disclosure design blocks the affected live flow.',
'DSA matrix distinguishes hosting duties, size exemptions and conditional marketplace rules.|DPIA covers profile, contact, identity, notices, billing, logs and providers.|Subscription policy defines price/tax, renewal, withdrawal/cancellation, suspension and refunds.|Each unresolved topic has an owner and launch impact; public-identity policy is resolved before publication.')
add(3,1,'Evaluate advertiser identity and visitor age providers',[1,2],[],
'docs/providers/identity-evaluation.md|contracts/verification-provider.md',
'Choose a privacy-conscious advertiser identity and visitor age design.',
'Evaluate Yoti with exact-model acceptance, document-country coverage, liveness and accessible alternatives.|Separate advertiser identity from minimal visitor age assertions; facial age estimation alone is insufficient KYC.|Review account binding, fraud appeals, expiration/revocation, biometrics, retention/deletion, subprocessors, non-training terms and cost.',
'Adapter specifies session creation, signed results, provider reference, threshold, freshness, failure and revocation; documents remain provider-hosted by default.',
'Marketing is not contractual approval. Any required local identity retention needs a separately restricted design.',
'Scored evaluation covers business acceptance, documents, privacy, fraud and cost.|Sandbox proves success, failure, timeout and authenticated callback handling.|Advertiser and visitor outputs contain only purpose-required fields.|Written acceptance/data terms are recorded or the live-provider decision remains open.')
add(4,1,'Obtain subscription acquiring feasibility and economics',[1,2],[],
'docs/providers/payment-underwriting.md|docs/finance/unit-economics.md|contracts/billing-provider.md',
'Establish an approved route for this exact advertising subscription.',
'Prepare truthful underwriting dossier for CCBill and alternatives; explicitly describe ads for in-person services.|Record acquiring approval/category, merchant role, recurring/SCA support, currencies, bank acceptance, reserves, termination and webhook/reconciliation capabilities.|Model quoted processing, verification, moderation, disputes/refunds, tax and cash reserves; no invented rates.',
'Contract covers checkout, subscription lookup/cancel, refund and signed events; excludes payouts and bookings.',
'No merchant-category disguise or prohibited-provider workaround. No accepted acquirer means paid launch blocked.',
'Underwriting outcome explicitly covers fixed monthly advertiser fees and proposed content.|Economics use quotes or clearly marked unknowns, including reserves.|Contract supports renewal, cancellation, refunds and authoritative reconciliation.|ARC-004 contains selected-provider evidence or an explicit no-go condition.')
add(5,1,'Confirm hosting and supporting service eligibility',[1,2],[],
'docs/providers/hosting-evaluation.md|docs/operations/provider-exit.md',
'Choose an operable infrastructure chain with explicit use-case acceptance.',
'Evaluate Infomaniak and Leaseweb with service-specific written acceptance.|Cover compute, database, objects, CDN/WAF, DNS, email, backup, logs and support tooling.|Record processing/support regions, DPA/transfers, subprocessors, abuse response, patch ownership, export and termination terms.',
'Service inventory maps data category, region, operator, retention, AUP evidence and exit format.',
'One product approval does not approve every dependent service; preserve reporting during provider loss.',
'Every service has a named operator and explicit eligibility status.|Data locations/transfers match privacy assessment.|Portable database/object export and replacement architecture are documented.|Written acceptance exists or live hosting remains gated.')
add(6,1,'Define content rules and staffed moderation operations',[1,2],[],
'docs/safety/content-policy.md|docs/safety/moderation-runbook.md|evaluation/moderation-policy/',
'Create enforceable rules backed by trained review and urgent response.',
'Separate illegal content from stricter platform/provider rules; cover minors/minor-coded themes, coercion, trafficking, nonconsensual media, impersonation, doxxing and links.|Define individual self-ads, non-explicit still photos, consent evidence and private review where public faces are obscured.|Evaluate eligible text/OCR/image/hash and human services; define pilot-language coverage, false-positive review and lawful test cases.|Set on-call rota, training/wellbeing, reporting deadlines and capacity limits.',
'Taxonomy includes rule ID, jurisdiction, severity, action, review path and evidence-handling policy.',
'Filters cannot guarantee legality; KYC cannot establish free consent. Missing urgent coverage blocks launch.',
'Every prohibited category has examples, actions and appeal/escalation guidance.|Every pilot language has trained coverage and urgent on-call staffing.|Lawful benchmark measures misses/false positives per category.|Legal/provider deadlines and internal service targets are distinguished and approved.')
add(7,2,'Create modular application and reproducible development',[],[],
'apps/web/|backend/|contracts/openapi/|compose.yaml|docs/development.md',
'Establish a repeatable local app and domain boundaries.',
'Confirm supported runtimes/frameworks and pin dependencies for the proposed monolith.|Create migrations, config validation, health endpoints, API contracts and synthetic seeds.|Document startup/check commands and environment-specific configuration.',
'Health/build metadata excludes secrets; migrations establish opaque IDs and UTC conventions.',
'Production rejects synthetic identity/payment adapters and authentication bypasses.',
'Clean checkout starts web/API/database with documented commands.|Empty-database migrations and deterministic contract generation succeed.|Missing settings fail with redacted diagnostics.|Production configuration refuses fake verification/payment adapters.')
add(8,2,'Create CI and isolated deployment foundation',[7],[],
'infra/|.github/workflows/ci.yml|docs/operations/environments.md',
'Build traceable artifacts and isolated staging.',
'Automate lint/types/tests, immutable images and dependency/secret checks.|Define TLS, private database/storage, least-privilege accounts and secret injection.|Provision live services only after ARC-005 approval; local synthetic CI can proceed.',
'Deployment inventory binds image digest, config version and secret references without values.',
'Untrusted changes get no deployment secrets. Migrations need rollback/forward-repair planning.',
'CI catches failing tests and excludes secrets from untrusted jobs.|Staging uses traceable images and private database/storage.|TLS and least-privilege access are verified in approved staging.|Production release is separately gated from normal CI.')
add(9,2,'Implement advertiser accounts and staff authorization',[7],[],
'backend/salon/identity/|apps/web/src/features/auth/|backend/tests/identity/',
'Protect advertiser ownership and privileged operations.',
'Implement verified registration, sessions, logout/recovery, rate limits and advertiser MFA option; require staff MFA.|Separate moderator, appeals, billing support and security permissions.|Reauthenticate security/contact changes; audit role grants and use safe account recovery.',
'Account, Session and RoleGrant models; minimal current-user endpoint.',
'Prevent enumeration, CSRF, session fixation and cross-account access; no ID attachments in support email.',
'Advertiser A cannot read or mutate advertiser B private records.|Staff without MFA cannot access privileged endpoints.|Recovery/logout/revocation invalidate sessions within 60 seconds.|CSRF, replay, enumeration and brute-force cases fail safely without credential leakage.')
add(10,3,'Integrate advertiser KYC and consent-aware onboarding',[3,8,9],[2,3,5],
'backend/salon/verification/|apps/web/src/features/verification/|backend/tests/verification/',
'Bind a verified eligible adult to the advertiser account.',
'Use hosted document/liveness capture, minimal assertions and country age/freshness rules.|Authenticate/deduplicate callbacks and reconcile missing events; no raw-document logs.|Provide retry/manual review and re-verification after security-sensitive changes; never label KYC as proof of safety/consent.',
'VerificationAttempt: account/provider binding, result, threshold, timestamps, expiry and policy version.',
'Failed, unknown, underage, expired or revoked checks never grant publication.',
'Eligible verified result binds only to the intended account.|Forged, replayed and wrong-account callbacks cannot grant status.|Expiry/revocation suppresses publication and exposes reviewed recovery.|Raw IDs/biometric templates never appear in public API, logs or ordinary staff views.')
add(11,3,'Enforce jurisdiction and local eligibility policies',[1,9],[1],
'backend/salon/countries/|backend/tests/countries/|apps/web/src/features/location/',
'Enable only reviewed territories under their own rules.',
'Implement disabled-by-default country/locality policy, ages, required permit evidence, content rules and approval expiry.|Separate service location/evidence from visitor policy; IP does not prove residency/eligibility.|Audit policy changes and implement immediate country shutdown without redeployment.',
'Versioned CountryPolicy carries enabled localities, approval evidence and effective/review dates.',
'Unknown/expired policies deny new publication and trigger reviewed existing-listing suppression; document geolocation limits.',
'Unknown/disabled territories cannot publish via UI or API.|Local thresholds/evidence override global defaults.|Service-location changes force eligibility and content review.|Country shutdown removes listing, contact and media access within 60 seconds.')
add(12,3,'Implement privacy-preserving visitor age access',[2,3,8,11],[1,2,3,5],
'backend/salon/access/|apps/web/src/features/age-access/|backend/tests/access/',
'Apply reviewed age rules without creating visitor identity profiles.',
'Use approved threshold/proof by territory/content, not a checkbox.|Bind short-lived assertions to audience/session; gate pages, APIs, search, contact and media server-side.|Offer accessible fallback and neutral pre-gate/help pages; no tracking profiles.',
'Minimal AgeAssertion: threshold, issuer/audience, expiry and bounded anti-replay data, separate from advertiser identity.',
'Unverifiable proof/provider outage denies restricted content while reporting/help remain available.',
'Deep links, API and direct media cannot bypass required checks.|Expired, replayed and wrong-audience proofs fail.|Only necessary age outcome is retained for approved lifetime.|Anonymous reporting/help work during age-provider outage.')
add(13,4,'Build privately owned profile drafts and revisions',[9,11],[],
'backend/salon/profiles/|apps/web/src/features/profiles/|backend/tests/profiles/',
'Let advertisers control one profile without exposing private identity.',
'Allow pseudonym, biography, city/region, languages and opted-in external contact; no exact home/live location.|Implement one active profile per verified advertiser, immutable revisions and consent records.|Provide immediate unpublish/consent withdrawal; distinguish visibility from billing and review sensitive edits.',
'Profile/ProfileRevision with owner, policy version, allowed fields and optimistic-concurrency token.',
'Sanitize rendering and contact schemes; protect drafts/previews from unauthorized access and caches.',
'Owner can save/preview/submit; another account cannot access drafts.|Concurrent edits cannot overwrite submitted revisions silently.|Public preview excludes legal identity, birth date and KYC data.|Withdrawal/unpublish denies origin immediately and schedules full invalidation.')
add(14,4,'Implement quarantined image ingestion and consent records',[6,8,13],[2,5,7],
'backend/salon/media/|backend/workers/media.py|backend/tests/media/',
'Keep every image private until scanned, consented and approved.',
'Limit MIME, bytes, dimensions/count; reject animation/video; isolate decoding, re-encode, strip EXIF and malware-scan.|Bind consent/ownership to each asset; only verified advertiser depicted, no other people; support privately reviewed obscured faces.|Separate quarantine from approved derivatives and use only approved scanning services.',
'MediaAsset states include quarantined, scanned, review_required, approved, rejected, withdrawn; scoped uploads and gated delivery.',
'Parser bombs, spoofing, missing consent and failed scans stay quarantined; original retention is bounded.',
'Unapproved originals/derivatives cannot be accessed through direct object URLs.|Delivered derivatives contain no EXIF coordinates or identifying metadata.|Malformed/oversize/scan-timeout files cannot reach publication.|Withdrawal removes every linked asset/projection/cache within 60 seconds.')
add(15,4,'Implement moderation filters and human review console',[6,9,13,14],[7],
'backend/salon/moderation/|apps/web/src/features/moderation/|backend/tests/moderation/',
'Require explainable human approval of each submitted revision.',
'Combine normalization, multilingual rules, OCR/image signals and lawful hash access where available; version signals and route uncertainty.|Human pre-publication review covers initial profiles and material edits; high-risk queue has priority.|Record reason/rule, reviewer and exact revision; minimize KYC access and prohibit own-case approval.',
'ModerationCase/Decision bind exact profile/assets, policy, signal summary, human reviewer and action.',
'Scanner outage stays pending; low risk score never auto-publishes. Urgent harm enters escalation.',
'Each publish candidate has human approval for exact content/assets.|Obfuscated text/OCR and multilingual cases route per policy benchmark.|Late approval of old revision cannot approve changed content.|Reviewers cannot access raw KYC by default or approve own profile.')
add(16,4,'Build revocable publication and directory discovery',[10,11,12,13,14,15],[],
'backend/salon/directory/|apps/web/src/features/directory/|backend/tests/directory/',
'Expose only currently eligible approved revisions.',
'Enforce account, KYC, country, consent, asset, moderation and entitlement invariant on every public path.|Use approved projections and country/city/language search with fair documented rotation; no paid boosts or sensitive profiling.|Gate contact/media, limit enumeration and invalidate caches/search on all eligibility changes; production billing arrives in SAL-019.',
'PublishedProjection references immutable revision; entitlement interface is deny-by-default, with synthetic tests only until billing integration.',
'Unknown entitlement denies access; outages cannot resurrect restricted ads. Do not promise complete scraping prevention.',
'Removing any eligibility condition hides pages, search, API, contact and media.|Unreviewed edits/direct publish requests cannot change approved public data.|Origin enforces suppression immediately and cached delivery within 60 seconds.|Search returns only permitted projections with documented ordering.')
add(17,5,'Define plans and transparent subscription purchase terms',[2,4,9],[8],
'backend/salon/billing/plans.py|apps/web/src/features/subscriptions/|backend/tests/billing/test_plans.py',
'Offer a clearly priced monthly advertising subscription.',
'One fixed monthly plan per approved currency with versioned tax presentation.|Show total, renewal interval, cancellation/refunds and seller identity before affirmative purchase consent.|First checkout requires KYC and content approval; preserve terms version and reject browser price manipulation.',
'PlanVersion/PurchaseConsent: integer minor units, currency, interval, tax policy and accepted terms.',
'No floating-point money, hidden renewals or default opt-ins; price changes follow approved notice/consent policy.',
'Purchase summary matches server amount, tax, currency and renewal.|Manipulated amounts and inactive plan IDs are rejected.|Consent identifies exact price/terms accepted.|Unverified or unapproved advertisers cannot start first checkout.')
add(18,5,'Integrate hosted subscription checkout and event ingestion',[4,8,17],[4,5,8],
'backend/salon/billing/provider.py|backend/salon/billing/events.py|backend/tests/billing/test_checkout.py',
'Collect platform subscription fees through the approved processor.',
'Use hosted checkout/tokenization, server order IDs and signed callbacks; never collect card data.|Durably store events before processing, deduplicate and implement bounded retries/reconciliation.|Handle SCA, abandonment, outages and sandbox/live credential separation; validate account, amount and currency.',
'CheckoutSession and immutable SubscriptionEvent map advertiser/order to provider identifiers; no worker payouts.',
'Browser success redirect grants no entitlement. Redact raw payloads/secrets and reject forged events.',
'Authorized sandbox purchase creates one correctly bound event.|Forged/replayed/mismatched callbacks cannot duplicate purchase or grant rights.|Success redirect without authoritative payment grants no access.|Lost callback can be replayed/reconciled without loss or duplication.')
add(19,5,'Implement renewal, cancellation and entitlement reconciliation',[16,18],[4,8],
'backend/salon/billing/lifecycle.py|backend/workers/billing.py|backend/tests/billing/test_lifecycle.py',
'Align advertising rights with the complete subscription lifecycle.',
'Model active, past_due, paid-through expiry, cancel-at-period-end, refund and dispute states.|Reconcile missing/out-of-order events; prevent duplicate subscriptions and double charges.|Make cancellation easy/confirmed with receipts and reviewed suspension/refund rules; stop renewals for ineligible accounts as policy requires.|KYC, consent and moderation always override payment.',
'Subscription and Entitlement are separate projections; cancel/refund operations are idempotent and auditable.',
'Provider cancel failure stays pending with alert, never falsely confirmed; stale events cannot reactivate restrictions.',
'Renewal extends rights once; failed/expired payment removes rights at reviewed deadline.|Cancellation stops future renewal and applies disclosed remaining-period policy.|Late success cannot restore suspended/withdrawn/invalid-KYC profiles.|Refund/dispute/reconciliation matrix converges without duplicate charges or hidden renewals.')
add(20,6,'Implement notice intake and reasoned moderation decisions',[2,9,15,16],[],
'backend/salon/compliance/notices.py|apps/web/src/features/reporting/|backend/tests/compliance/test_notices.py',
'Offer traceable reporting without requiring an account.',
'Accessible localized form collects content location, explanation, good-faith declaration and reviewed contact requirements/anonymous exceptions.|Acknowledge, triage and communicate action/no-action with reasons and redress; do not solicit illegal imagery.|Validate trusted-flagger status where applicable; priority is not automatic removal; use proportionate rate limits.',
'Notice: URL/revision, category, minimal reporter details, timestamps, decision and safe tracking token. Reasons include rule/legal basis and automation used.',
'Keep reporter details out of advertiser notifications/public outputs; duplicates must not erase legitimate reports.',
'Unauthenticated person reports a precise listing and receives safe acknowledgement.|Urgent reports immediately enter escalation; ordinary cases retain triage deadlines.|Restrictions and no-action outcomes have reasons and appropriate notifications.|Reporter details/evidence are absent from public reasons and advertiser responses.')
add(21,6,'Implement human appeals and dispute escalation',[20],[],
'backend/salon/compliance/appeals.py|apps/web/src/features/appeals/|backend/tests/compliance/test_appeals.py',
'Provide meaningful review of restrictions and notice outcomes.',
'Free internal complaints for covered decisions with at least six months to submit; qualified different reviewer and no solely automated outcome.|Expose decision history and applicable certified out-of-court redress information.|Use proportionate misuse warnings; reversal restores only if current publication conditions hold.',
'Appeal: decision, eligible party, deadline, reviewer, outcome and private notifications.',
'Overturning a decision never bypasses expired billing, consent withdrawal or another restriction.',
'Eligible parties can submit throughout the minimum complaint window.|Original reviewer cannot decide their own appeal.|Every appeal has human reasoning and applicable further-redress information.|Reversal restores only eligible revisions, never withdrawn content.')
add(22,6,'Build DSA transparency and advertisement disclosures',[2,16,20,21],[],
'backend/salon/compliance/transparency.py|apps/web/src/features/transparency/|backend/tests/compliance/test_transparency.py',
'Produce privacy-safe outputs according to reviewed DSA applicability.',
'Label paid ads and implement approved beneficiary/payer disclosure and ordering explanation.|Aggregate moderation/complaint metrics and active recipients with defined methodology and applicability review triggers.|Gate reporting/database submission by signed applicability register; verify current required schema in sandbox.|Redact all public free text, identities, contacts and identifying locations.',
'TransparencyExport/ApplicabilitySnapshot track period, methodology, source decisions and review without raw personal content.',
'Exemptions require evidence; failed mandatory submission is retryable/visible and cannot be silently skipped.',
'Paid listings show approved disclosure and ordering consistently.|Known synthetic dataset yields reconciled period/count outputs.|Public exports contain no personal data or raw notices.|Applicability changes activate required outputs and notify responsible owner.')
add(23,6,'Implement urgent escalation and authority request handling',[1,2,6,20],[],
'backend/salon/compliance/authority.py|docs/operations/urgent-response.md|backend/tests/compliance/test_authority.py',
'Handle urgent harm and legal requests with minimal accountable disclosure.',
'Separate immediate danger, DSA serious-offence, Belgian suspected exploitation/abuse and contractual reporting triggers.|Verify authority identity, jurisdiction and request scope; track deadlines, legal holds and notifications/exceptions.|Use authorized operators and secure evidence channels; no automatic police disclosure from classifier scores.',
'AuthorityCase: verified recipient, legal basis, scope, due time, authorized action and restricted evidence reference.',
'No suspected illegal media in Git, routine email or support tools; unverified requests get reviewed, not fulfilled.',
'Urgent drills reach on-call within approved target.|Belgian and DSA scenarios follow distinct reviewed procedures.|Forged or excessive requests cannot obtain records.|Every preservation/disclosure is scoped, authorized, audited and retention-reviewed.')
add(24,7,'Implement privacy rights and retention enforcement',[2,10,14,19,20],[2,6],
'backend/salon/operations/privacy.py|backend/workers/retention.py|backend/tests/operations/test_privacy.py',
'Fulfil rights and minimize data lifetime across application and providers.',
'Implement access/export, correction, withdrawal, deletion and scoped legal holds with proportionate authentication.|Separate retained billing records from public removal; track provider deletion and closure/cancellation.|Version retention for failed KYC, originals, evidence, logs and backups; maintain restore suppression ledger.',
'DeletionRequest/RetentionPolicy track scope, deadline, provider status and hold basis; exports are private and short-lived.',
'Do not claim full deletion while justified retention/backups remain; no unnecessary identity checks for rights requests.',
'Closure hides content and invokes reviewed cancellation policy.|Export excludes other users and protected reporter identities.|Each retention class expires and downstream failures are retried.|Hold/deletion evidence distinguishes immediate public removal from backup expiry.')
add(25,7,'Implement privacy-safe monitoring and operational controls',[8,10,15,19,20],[],
'backend/salon/operations/telemetry.py|infra/monitoring/|docs/operations/on-call.md',
'Detect broken verification, billing, moderation and publication promptly.',
'Collect scrubbed logs, latency/errors, queues, urgent deadlines and publication-invariant alerts.|Route to staffed owners, expose provider health and audit publication freeze/country kill switch.|Use minimal aggregate metrics; no sensitive tracking pixels, contact/ad text or raw payloads in telemetry.',
'Opaque correlation IDs permit restricted audit lookup with reviewed retention.',
'Alert tests use synthetic cases and no real emergency dispatch; logging failures cannot leak payloads.',
'Injected outages and overdue urgent cases alert named owners.|Logs/traces/errors exclude IDs, contacts, ads, credentials and card data.|Publication freeze blocks new ads while help/reporting remain available.|On-call can identify and retry jobs without duplicate side effects.')
add(26,7,'Prove backup recovery, deletion replay and provider exit',[5,8,24,25],[5,6],
'infra/recovery/|docs/operations/restore.md|backend/tests/operations/test_recovery.py',
'Restore service without republishing deleted or restricted content.',
'Encrypt backups and test approved RPO/RTO in isolation.|Replay deletion/safety ledgers before public access; reconcile external verification/billing after restoration.|Exercise portable export, credential loss, rollback and replacement-provider assumptions.',
'Recovery manifest includes timestamp, key reference, suppression checkpoint and consistency results.',
'Never restore real data into ordinary development; missing suppression state keeps directory offline.',
'Measured restore meets approved RPO/RTO or fails release gate.|Restoring old backup leaves deleted/suspended profiles unavailable.|Reconciliation prevents stale eligibility and duplicate billing.|Exit rehearsal proves data export and identifies replacement dependencies.')
add(27,7,'Complete security and safety boundary assessment',[12,16,19,21,22,23,24,25,26],[],
'backend/tests/security/|apps/web/tests/security/|docs/security/launch-assessment.md',
'Prove cross-module controls under attacks, races and outages.',
'Test account takeover, ownership/roles, staff abuse, callback replay, uploads, age bypass and caches/media.|Cover concurrent consent/KYC/billing changes, export leaks and restored suppression.|Commission independent scoped review, fix release blockers and record residual risks.',
'Findings map affected data/endpoint, synthetic reproduction, severity, fix and retest evidence.',
'No intrusive third-party production testing; critical/high launch-blocking findings prevent release.',
'Private endpoints pass cross-account and staff-boundary tests.|Publication invariant survives concurrent edit/suspension/payment.|Age/media/cache bypass and malicious uploads fail safely.|Independent review has no unresolved critical/high launch-blocking findings under agreed severity policy.')
add(28,7,'Complete localized accessible advertiser and visitor journeys',[12,16,19,20,21,22,23],[],
'apps/web/src/locales/|apps/web/tests/journeys/|docs/product/pilot-usability.md',
'Make the complete pilot understandable and usable in approved languages.',
'Localize onboarding, verification, directory, billing/cancel, notices/appeals and legal copy; proposed Belgian languages are French/Dutch with English support.|Test keyboard, screen reader, errors and mobile; professionally review legal translations.|Publish operator/contact, policies, versioned terms and ranking explanation; no misleading safety guarantee.',
'Locale catalogue covers date/currency/fallback and policy versions; decisions/purchases bind displayed terms.',
'Missing critical translations and inaccessible reporting block launch; contact sharing stays deliberate.',
'Advertiser completes verification-to-publication and cancellation in each pilot language.|Visitor discovers, reveals contact and reports via keyboard/screen reader.|Usability review confirms renewal, pause-versus-cancel and verification limits are clear.|Required legal/contact/help pages work before sign-in and age checks.')
add(29,8,'Approve supervised paid-pilot readiness',list(range(1,29)),list(range(1,9)),
'docs/pilot/readiness.md|docs/pilot/measurement-plan.md|docs/operations/release.md',
'Produce a concrete release package for a capped one-territory pilot.',
'Collect scoped legal/provider decisions, staffing/support/refund readiness, recovery and security evidence.|Set proposed 25-advertiser cap, capacity/stop thresholds and rollback before launch.|Rehearse full journeys and failure cases with authorized test identities; require named operator go/no-go separately from story completion.',
'Readiness links immutable build, territory, policy/provider versions, owners and non-sensitive evidence references.',
'Unmet mandatory decisions, staffing or security gates block real onboarding and payments.',
'Every P0 prerequisite and pilot decision has traceable accepted evidence.|Publication/cancel/withdrawal/report/appeal/urgent rehearsal succeeds.|Rollback, country shutdown and capacity limits are demonstrated.|Accountable operator records go/no-go with build, territory and conditions.')
add(30,8,'Observe pilot safety, retention and unit economics',[29],[],
'docs/pilot/observation.md|docs/pilot/review.md',
'Decide whether to continue, narrow, stop or prepare expansion.',
'Observe proposed four-to-six-week period after actual launch; document cohort size/uncertainty.|Measure moderation/urgent targets, appeals, withdrawals, renewal/cancel defects, retention and real contribution.|Reassess DSA size, country and provider conditions; changes can require renewed review.',
'Aggregate cohorts/incidents use redaction and minimum-group rules; no raw browsing or identities in reports.',
'Small samples do not prove safety/viability; stop thresholds suspend affected activity.',
'Observation dates follow actual launch and define cohort.|Safety/service/economic results use actual costs and uncertainty.|Incidents and missed targets have owners/actions.|Recorded continue/narrow/stop decision gates expansion.')
add(31,8,'Prepare Netherlands expansion',[30],[9],
'docs/launch/netherlands.md|backend/salon/countries/policies/nl.yaml|apps/web/tests/launch/nl.spec.ts',
'Enable specifically approved Dutch localities after independent review.',
'Review current national/municipal rules, local ages/permits and platform classification.|Confirm provider, tax, notices, languages and reviewer/reporting coverage.|Test local policy, documents and visitor controls before enabling disabled rollout flags.',
'NL policy records locality-specific evidence, effective/review dates and scope.',
'Unresolved municipalities stay disabled; no inherited Belgian approval or reliance on future proposals as law.',
'Legal memo approves exact flow and enabled localities.|Provider/operations acceptance explicitly covers Dutch expansion.|Dutch journey and eligibility/age/withdrawal tests pass.|Separate scoped release decision and rollback precede enablement.')
add(32,8,'Prepare Switzerland expansion',[30],[10],
'docs/launch/switzerland.md|backend/salon/countries/policies/ch.yaml|apps/web/tests/launch/ch.spec.ts',
'Enable approved Swiss localities with appropriate privacy and billing.',
'Review federal/cantonal/municipal advertising/operator/registration and privacy/cross-border rules.|Confirm documents, providers, settlement/CHF decision, taxes and local language/support.|Test each permitted locality and reporting path; no blanket inference from Geneva.',
'CH policy records canton/locality, source, dates, language/currency and reviewer.',
'Unapproved cantons stay disabled; Swiss hosting does not establish operating eligibility or remove EU duties.',
'Legal memo identifies approved localities and obligations.|Providers/accounting accept exact Swiss subscription flow.|Language/currency/document/locality tests pass end-to-end.|Separate scoped approval and rollback rehearsal precede enablement.')

epic_defs = [
 ('Feasibility and provider diligence',range(1,7),'Prove exact-model eligibility before live commitments'),
 ('Application and security foundation',range(7,10),'Create a reproducible isolated authorized application'),
 ('Identity and jurisdiction access',range(10,13),'Verify advertisers and enforce territory/visitor controls'),
 ('Profiles, media and publication',range(13,17),'Publish only eligible consented approved revisions'),
 ('Platform subscription billing',range(17,20),'Charge fixed monthly ad fees with reliable cancellation'),
 ('DSA redress and safety operations',range(20,24),'Provide reports, appeals, transparency and escalation'),
 ('Privacy, reliability and launch quality',range(24,29),'Prove rights fulfilment, recovery, security and usability'),
 ('Pilot and territorial expansion',range(29,33),'Launch deliberately and expand on renewed evidence')]
dec_specs = [
 ('Pilot entity and jurisdiction','Belgium first candidate; disabled until reviewed','Real onboarding and first-territory launch'),
 ('Legal applicability and sensitive-data design','Article-level DSA register, DPIA and reviewed disclosure/billing terms','Real personal-data processing and public advertising'),
 ('Identity and age provider','Evaluate Yoti; exact-model acceptance required','Live advertiser KYC and visitor age processing'),
 ('Subscription acquiring','Evaluate CCBill and alternatives; none approved yet','Live subscription collection'),
 ('Hosting and supporting services','Evaluate Infomaniak and Leaseweb; service-specific acceptance','Cloud procurement and live hosting/data processing'),
 ('Retention and recovery policy','Data-class schedule; proposed RPO 24h and RTO 8h','Production retention, backups and restoration'),
 ('Content policy and moderation capacity','Non-explicit self-ads; human review and urgent rota','Real uploads and publication'),
 ('Price, tax and renewal policy','One fixed monthly plan; price and terms unresolved','Live price offers and recurring billing'),
 ('Netherlands expansion eligibility','Independent local legal/provider/operations review','Netherlands territory activation'),
 ('Switzerland expansion eligibility','Independent canton/locality legal/provider/operations review','Switzerland territory activation')]
data = dict(schema_version=1,project='Sotto Salon',scope='Subscription-funded adult profile advertising; one-territory pilot then gated expansion',architecture_file='docs/architecture/mvp-architecture.md',product_file='docs/product/mvp.md',tracking_guide='planning/README.md',allowed_statuses=['planned','in_progress','blocked','in_review','done','cancelled'],allowed_file_actions=['create','modify','delete'],priorities={'P0':'Required for first paid pilot','P1':'Optional independent territory expansion'},tracking_policy={'paths':'Workspace-relative; proposed files may not exist yet','actual_changes':'Record exact files after implementation','verification':'Record actual results, not planned test names','commits':'No commit or push authorized by this backlog','completion':'Requirements documents do not constitute completed implementation','decisions':'Open decisions block the live activity in blocks; synthetic work can proceed'},decisions=[dict(id=f'ARC-{i:03}',title=t,status='open',proposed_default=p,blocks=b) for i,(t,p,b) in enumerate(dec_specs,1)],release_gates={
 'synthetic_staging':dict(decisions=[],stories=['SAL-007','SAL-008','SAL-009'],approvals=['Engineering review of synthetic-only deployment'],note='No customer IDs, content or real charges'),
 'paid_pilot':dict(decisions=[f'ARC-{i:03}' for i in range(1,9)],stories=['SAL-029'],approvals=['Country legal review accepted','Exact-model provider contracts approved','Privacy/security assessments accepted','Moderation and support coverage staffed','Accountable operator release approval'],note='All transitive dependencies done; decisions approved for pilot scope'),
 'pilot_review':dict(decisions=[],stories=['SAL-030'],approvals=['Recorded continue narrow or stop decision'],note='Observation occurs after launch'),
 'netherlands':dict(decisions=['ARC-009'],stories=['SAL-031'],approvals=['Dutch territory launch with renewed provider/operations evidence'],note='Depends on pilot review; does not require Switzerland'),
 'switzerland':dict(decisions=['ARC-010'],stories=['SAL-032'],approvals=['Swiss locality launch with renewed provider/operations evidence'],note='Depends on pilot review; does not require Netherlands')},epics=[dict(id=f'EPIC-{i:02}',title=t,status='planned',goal=g,stories=[f'SAL-{n:03}' for n in ns]) for i,(t,ns,g) in enumerate(epic_defs,1)],stories=STORIES)
(ROOT/'planning/roadmap.yaml').write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=110),encoding='utf-8')
source=Path(r'C:\Users\BE125858\projects\git\scripta\planning\validate_backlog.py').read_text(encoding='utf-8')
(ROOT/'planning/validate_backlog.py').write_text(source.replace('SCR-', 'SAL-'),encoding='utf-8')
print(f'Created {len(STORIES)} stories, roadmap and adapted Scripta validator.')
