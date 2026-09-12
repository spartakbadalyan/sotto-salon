# Sotto Salon

A planned subscription-funded directory for verified adults to publish moderated profile advertisements in approved jurisdictions. Fixed monthly advertising fees; no service payments, commissions or reservations.

Start with the [planning guide](planning/README.md), [roadmap](planning/roadmap.yaml) and [implementation sequence](planning/implementation-plan.md).

## Status

Phase 1 foundation in progress. **SAL-007** (modular application and reproducible development) is implemented as a **synthetic-only** skeleton: a FastAPI backend with domain-module boundaries, a Next.js web app, generated OpenAPI contract types, database migrations, and a local development stack. No real identity verification, payments, or customer data are involved, and production configuration refuses the synthetic provider adapters.

Feasibility work (SAL-001–006: legal/country, provider, DSA/GDPR and content-policy decisions) and any live processing remain gated — see the roadmap's release gates and open `ARC-*` decisions.

See [docs/development.md](docs/development.md) to run it locally.
