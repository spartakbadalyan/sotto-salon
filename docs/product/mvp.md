# Sotto Salon product brief

Status: proposed MVP, 2026-09-12. The user's fixed requirements are subscription-funded profile ads, advertiser identity verification, moderation, suitable payment processing and hosting, and DSA compliance.

Sotto Salon lets an eligible adult publish their own moderated profile advertisement for a fixed monthly price. Visitors discover approved listings and use the advertiser's chosen external contact method. The platform sells advertising subscriptions to advertisers. It takes no percentage of their earnings and handles no service payments, deposits, payouts, escrow, booking, calendars or meeting reservations. The payment provider may still charge percentage-based processing fees on the platform's subscription revenue.

## Proposed MVP boundaries

- One verified natural person, one profile, one monthly plan; no agency accounts, third-party managers, group profiles, reviews, internal chat, live streaming, video, tips, affiliate schemes or paid ranking boosts.
- Public pseudonyms, coarse city/region location, moderated text and still photos. No public legal identity, birth date, identity documents, residential address, live location or mandatory face display. Only the verified advertiser may appear in photos; reject other people and synthetic identities.
- Initially non-explicit profile images; exact image and text rules require the country and provider reviews. This restriction does not itself establish legal or provider eligibility. No sexual-minor themes, coercion, trafficking, nonconsensual imagery, impersonation, illegal offers, doxxing or prohibited external links.
- Country allowlist with local rules. Belgium is a proposed first pilot candidate, not an approved launch. Netherlands and Switzerland are separate expansion candidates. No additional countries enabled by default.
- Advertisers complete identity/age checks and content review before first checkout. Approval reserves an immutable revision; successful subscription payment permits publication only while every eligibility condition remains valid.
- Visitors do not need a profile account. Any required visitor age assurance is distinct from advertiser KYC and must protect directory APIs, media, contact details and caches as well as pages.
- Basic discovery by country, city and advertiser-declared language, with a documented fair rotation. No behavioural advertising, sensitive-trait targeting, precise map pins or visitor tracking profiles.
- Advertiser pause/unpublish is immediate; subscription cancellation is separate, prominent and easy. Explain continued billing when voluntarily paused; policy suspensions have a defined renewal/refund process.
- Proposed pilot languages: French and Dutch for a Belgian launch, with English support copy. Additional local languages and currencies are expansion work; legal notices need professional review.

## User journeys

Advertiser: register and secure account → review publishing/privacy rules → verify identity and age → draft profile and upload own photos → consent and moderation → approve price/renewal terms and pay → eligible listing goes live → edit, pause, cancel or delete.

Visitor: satisfy access/age rules → select supported location → browse labelled paid advertisements → read approved profile → voluntarily reveal chosen external contact → report content without creating an account.

Moderator: triage risk → inspect quarantined revision and minimal verification status → approve or restrict with a reason → notify affected user → handle an appeal with a different reviewer → escalate urgent cases through the applicable protocol. Verification is not proof of consent or absence of exploitation.

## Commercial decisions

Monthly price, tax treatment, merchant entity, settlement currency, renewal reminders, refunds, verification cost allocation and moderation budget remain open. Default assumption is EUR for the first EU pilot; CHF is considered for Swiss expansion. No invented processor rates or launch date. Account for acquiring fees, rolling reserves, disputes, verification retries, human moderation, legal reviews, infrastructure and support when setting price.

Success means eligible ads can reliably publish and be withdrawn, serious reports are acted on promptly, identity data remains separated, cancellations stop renewals, and subscription contribution margin can sustain moderation. Raw listing growth does not override safety or release gates.
