# Provider selection and procurement plan

Public-source screening on 2026-09-12. No provider has been contacted or approved. Marketing support for adult media is not contractual acceptance of paid advertisements for in-person sexual services. Quotes, acquiring approval, processing locations and current service-specific contracts remain unverified.

## Payment processing for platform subscriptions

| Candidate | Evidence | Planning disposition |
| --- | --- | --- |
| CCBill | Markets adult-business processing; merchant AUP imposes content restrictions. [Adult business](https://ccbill.com/industries/adult-business), [AUP](https://ccbill.com/cs/client/policies/ccbill/acceptable_use.html) | Underwriting inquiry candidate only. Exact classified-ad model and recurring advertiser fees need written acceptance. |
| Segpay | Publishes adult-merchant complaint and reporting requirements. [Disclosures](https://gethelp.segpay.com/docs/Content/ComplianceDocs/Disclosures.htm), [content violations](https://gethelp.segpay.com/docs/Content/MPDocs/MyWebsites/WebsiteContentViolations.htm) | Secondary eligibility inquiry only; these pages do not establish acceptance of escort advertising. Do not build against it until confirmed. |
| Stripe | Adult services are on its prohibited/restricted businesses page. [Policy](https://stripe.com/legal/restricted-businesses) | Exclude from the default architecture for this model. Calling the charge an advertising subscription does not cure eligibility. |

SAL-004 must produce a truthful business-model dossier and documented underwriting outcome before choosing an integration. Include sample moderated profiles, merchant domicile, countries served, advertiser-only billing, monthly renewal/cancellation flow, identity checks, content rules, complaint process and the absence of service transactions. Do not disguise the business or choose an inaccurate merchant category.

Obtain exact accepted activities and territories; acquiring bank and merchant category; merchant-of-record role; currencies and settlement bank compatibility; recurring-payment/SCA support; hosted checkout and PCI responsibilities; webhook signing/reconciliation; refunds and chargebacks; descriptor; reserves, payout delays and termination terms; tax/invoicing responsibility; and all moderation/identity/record-retention rules. Calculate economics from a written quote. Processor percentage fees are a platform cost, distinct from taking a share of advertiser earnings.

If no acquirer accepts the exact model, the paid launch remains blocked. A bank-approved invoiced subscription could be assessed separately, but is not a confirmed fallback and must not bypass restrictions. No crypto or personal-account workaround is planned.

## Hosting and supporting services

| Candidate | Evidence | Planning disposition |
| --- | --- | --- |
| Infomaniak | Terms describe pornography being accessible with effective over-18 controls. Offers cloud hosting. [Terms](https://welcome.infomaniak.com/api/components/cgu/latest?id=1&locale=en_GB), [Public Cloud](https://www.infomaniak.com/en/hosting/public-cloud) | First hosting diligence candidate; confirm exact classifieds use, selected cloud service, Swiss processing, abuse handling and all dependent services in writing. Conditional content permission is not approval of this app. |
| Leaseweb | Publishes entity-specific contracts and abuse handling. [Legal](https://www.leaseweb.com/en/about-us/legal), [abuse handling](https://www.leaseweb.com/abuse-prevention) | Alternative infrastructure diligence candidate; no affirmative acceptance of this model established by this review. Confirm EU region, service scope and operational responsibility. |

SAL-005 covers compute, database, object storage, CDN/WAF, DNS/registrar, transactional email, logs, backups and support tooling. Record every subprocessor, data/support geography, DPA, deletion/export capability, security terms and termination notice. Swiss location alone does not resolve GDPR transfer or EU-targeting questions. Budget managed operations or name the operator for self-managed database patching and recovery. Preserve portable container/database/object exports and test exit.

## Identity, age and content services

Yoti is the first evaluation candidate because it explicitly offers adult-content age verification, including creators and visitors. Its age assurance offering is not by itself the full advertiser identity/consent solution. Evaluate document authenticity, liveness, verified age, account binding, supported documents, accessible alternatives and exact business acceptance. [Adult-sector offering](https://www.yoti.com/adult-content-age-verification/), [developer overview](https://developers.yoti.com/age-verification), [age-check privacy](https://www.yoti.com/privacy/age-verification/).

SAL-003 must separate full advertiser identity checks from minimal visitor age proofs. Require signed callbacks, expiration/revocation, retention/deletion proof, non-training terms, subprocessors, appeal handling, biometric legal basis and a clear identity-data access model. Face age estimation alone does not establish advertiser identity or consent. Additional candidates require the same documented evaluation; none is implicitly approved.

No content-scanning supplier is selected. SAL-006 compares adult-eligible text/OCR/image services, lawful hash-matching access and a human moderation provider against the proposed policy using lawful synthetic examples. Confirm handling of suspected illegal media before sending any real uploads. A general-purpose model is not a complete moderation system. Vendor outage and false-positive recovery must be tested.
