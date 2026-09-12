# Launch compliance assessment

Research snapshot: 2026-09-12. This is a planning assessment, not a jurisdictional legal opinion. SAL-001 and SAL-002 obtain a current review for the actual entity, product flows and launch territory. Recheck sources at procurement and launch.

## Country eligibility

| Candidate | Primary-source finding | Required launch evidence |
| --- | --- | --- |
| Belgium | Official guidance permits adult self-advertising and purpose-built advertising platforms, and identifies immediate reporting duties for suspected abuse/exploitation. [SPF Justice](https://www.justice.belgium.be/fr/themes/securite_et_criminalite/travail_du_sexe) | Review current criminal-code provisions, platform conditions, verification, reporting recipients and local restrictions; obtain a signed launch memo. |
| Netherlands | Government guidance describes consensual adult prostitution as legal; this is not a platform licence. [Government](https://www.government.nl/themes/justice-security-and-defence/prostitution) | Check national and municipality rules, applicable minimum ages, permits and whether this directory is regulated as an operator. |
| Switzerland | Geneva requires sex workers to register with the relevant police unit. This example cannot be extrapolated to every canton. [Geneva](https://www.ge.ch/prostitution-geneve) | Review federal, cantonal and municipal advertising/operator rules, eligibility, privacy and cross-border targeting for each enabled territory. |

Use a versioned country/locality registry, disabled by default, with scoped approvals and review dates. Legality of the underlying service does not establish platform eligibility. No booking or commission reduces product scope; it does not establish exemption from advertising or intermediary rules.

## DSA applicability and control map

Working classification: hosting service and likely an online platform disseminating user-provided advertisements. Confirm EU establishment/targeting, competent Digital Services Coordinator, representative where needed and enterprise-size status. The DSA has separate small-enterprise exemptions; there is no blanket startup exemption. SAL-002 records article-level applicability, reasoning, owner and review trigger. [DSA text](https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng).

These are proposed engineering controls; applicability remains subject to review.

| Area | Implementation | Stories |
| --- | --- | --- |
| Articles 9–14: orders, contacts, representation and terms | Authority intake, contacts, versioned rules | SAL-002, SAL-023, SAL-028 |
| Articles 16–18: notices, reasons and serious-offence escalation | Reporting, reasoned decisions, urgent escalation | SAL-020, SAL-023 |
| Articles 15/19: size-related exemptions | Evidence-based applicability register | SAL-002 |
| Articles 20–23: complaints, disputes, trusted flaggers and misuse | Human appeals, priority handling, proportionate anti-abuse controls | SAL-020, SAL-021 |
| Articles 24–28: reporting, interface, ads, ranking and minors | Redacted reporting, paid-ad labels, ordering explanation, age controls | SAL-012, SAL-022, SAL-028 |
| Articles 29–32: distance-contract marketplace provisions | Assess actual contact/contract flow; absent checkout alone does not settle scope | SAL-002 |
| VLOP-specific duties | Monitor scale/designation; separate programme if triggered | SAL-022, SAL-030 |

Size-sensitive transparency duties include user-count publication, reporting and database submissions. Separate notifying an affected user of a moderation reason from external publication of a redacted statement. SAL-022 enables outputs based on the applicability register, retains exemption evidence and reassesses on growth or business changes. [Commission transparency overview](https://digital-strategy.ec.europa.eu/en/policies/dsa-brings-transparency), [database guidance](https://digital-strategy.ec.europa.eu/en/faqs/dsa-transparency-database-questions-and-answers).

Proposed voluntary baseline: complaints and human appeals for restrictions even where exempt. Allow at least six months for covered internal complaints. There is no blanket 24-hour DSA removal promise; deadlines come from the reviewed obligations register. [Commission DSA Q&A](https://digital-strategy.ec.europa.eu/en/faqs/digital-services-act-questions-and-answers).

Assess advertising beneficiary/payer disclosure against pseudonymity before launch. Paid listings may trigger transparency requirements; public legal-name disclosure cannot be silently assumed away. If a lawful disclosure design cannot coexist with promised privacy, revise the promise or hold launch. No sensitive-data profiling or targeted advertising is planned. [Commission DSA overview](https://digital-strategy.ec.europa.eu/en/policies/digital-services-act).

An 18+ checkbox is not the planned age-assurance system. Assess visitor access independently of advertiser KYC against the content and local rules. Use the Commission's minors guidance as an evaluation input without assuming identical applicability to every small platform. [Minors guidance](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors).

## Privacy and additional legal work

Profiles may reveal sex-life/sexual-orientation data; biometric matching may involve special-category processing. Record Article 6 basis and any necessary Article 9 condition by purpose. Complete a DPIA; assess DPO/representative obligations, processors/transfers, automated-decision safeguards, rights and breaches before real processing. Public posting does not authorize every reuse or indefinite identity retention. [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng).

SAL-002 also commissions review of Swiss privacy law, recurring-subscription consumer/business status, tax/VAT/invoicing, business-user platform rules, accessibility, cookies and any platform reporting obligations. These are unresolved topics, not findings of applicability. Receipts concern advertising only. Requested identity checks are not automatically a statutory AML programme.

## Safety operations

The proposed MVP bans minors and sexual-minor representations, coercion, exploitation, nonconsensual media, impersonation and illegal offers. Filters route risk; trained people review every initial listing and material change. Identity checks alone cannot establish free consent. Provide confidential withdrawal/reporting, language coverage and urgent on-call escalation.

Separate immediate danger, country-specific duties, provider reporting and ordinary policy breaches. Preserve only legally justified evidence in restricted systems; never attach suspected illegal imagery to routine email or tickets. Authority reporting needs a reviewed local procedure and authorized operator. Explicitly implement the Belgian reporting duty above.

Proposed service targets: urgent alerts immediately reach on-call, acknowledgement within 15 minutes; ordinary notices triaged within one business day; appeals reviewed within seven calendar days. These are operational targets, not statutory deadlines. Shorter applicable obligations prevail. Inadequate staffing blocks launch.
