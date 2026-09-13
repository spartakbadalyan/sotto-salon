# Frontend preview handoff

Status reviewed: 2026-09-13 on `feature/sal-008-ci-deployment-foundation`.

## When the app becomes previewable

The backlog currently defines several different preview milestones:

| Preview | Scheduled work | Current state | What it demonstrates |
| --- | --- | --- | --- |
| Local technical preview | EPIC-02 / SAL-007 | `in_review`; implemented | A Next.js page can call `GET /api/v1/meta` and display the environment and synthetic adapter configuration. |
| Hosted synthetic staging | EPIC-02 / SAL-007–009 release gate | SAL-008 is `in_progress`; SAL-009 is `planned` | Reproducible app, CI/staging, and account security with synthetic data and no real IDs or payments. |
| Recognizable advertiser/profile preview | EPIC-03 and EPIC-04 / especially SAL-010–016 | `planned` | Onboarding, location and age controls, profile editing, media review, moderation, publication, and public directory discovery. |
| Restricted paid pilot | EPIC-08 / SAL-029 and all transitive dependencies | `planned` | The complete reviewed MVP with provider, legal, privacy, security, moderation, and operational approvals. |

The implementation plan assigns 2–3 weeks to Phase 1 (SAL-007–009) and 4–6 weeks to Phase 2 (SAL-010–016). These are planning ranges, not calendar commitments. Phase 0 has a separate 2–6+ week range and external approvals can extend it without a bound. The overall restricted paid-pilot estimate is 12–20+ weeks after feasibility starts.

The repository already has the local technical preview. A hosted staging preview is not ready because SAL-008 is incomplete and SAL-009 has not started. Approved live staging for SAL-008 also depends on hosting decision ARC-005. A useful design prototype can proceed earlier with synthetic fixtures if its dependency constraints are recorded, as allowed by the planning guide.

## Current frontend

The frontend is a minimal Next.js 15 and React 19 application in `apps/web`. It contains only:

- `src/app/layout.tsx`: document metadata and basic inline body styling.
- `src/app/page.tsx`: a client-rendered developer status page.
- `src/lib/api.ts`: the API base URL and typed `GET /api/v1/meta` client.

There is no product visual language, navigation, route structure, directory, listing card, profile detail, advertiser workflow, authentication UI, responsive shell, component library, or frontend test suite yet. The page is useful as an end-to-end connectivity check, but it is not a representative product preview.

Run the current preview with synthetic configuration only:

```powershell
# terminal 1
cd backend
.venv\Scripts\python -m uvicorn salon.api.main:app --reload --port 8000

# terminal 2
cd apps/web
npm run dev
```

Then open `http://localhost:3000`. See `docs/development.md` for full setup.

## Frontend ownership in the backlog

| Experience | Story | Epic |
| --- | --- | --- |
| Application shell and web/API foundation | SAL-007 | EPIC-02 |
| Advertiser and staff sign-in/security | SAL-009 | EPIC-02 |
| Advertiser verification onboarding | SAL-010 | EPIC-03 |
| Country and location selection | SAL-011 | EPIC-03 |
| Visitor age access | SAL-012 | EPIC-03 |
| Advertiser profile drafts and revisions | SAL-013 | EPIC-04 |
| Image upload and consent UX | SAL-014, although no frontend path is listed in its current code impact | EPIC-04 |
| Human moderation console | SAL-015 | EPIC-04 |
| Public directory, search, profile, contact, and media access | SAL-016 | EPIC-04 |
| Plan and renewal disclosure | SAL-017 | EPIC-05 |
| Visitor reporting, advertiser notices, and appeals | SAL-020–022 | EPIC-06 |
| Localization, accessibility, and complete journeys | SAL-028 | EPIC-07 |
| Visitor consent controls | SAL-034, currently present as a story file but not indexed in the roadmap | EPIC-03 in the story file |

No current story explicitly owns a design-first, synthetic product preview. If work must be tracked against acceptance criteria before implementation, add or index a small preview story under EPIC-02. Keep later production behavior owned by its existing functional story.

## Assignment for a frontend agent

Create a polished, responsive, synthetic-only product preview inside `apps/web` that makes the proposed MVP tangible while preserving the existing web/API foundation.

Represent these core journeys with clearly labelled fictional data:

1. Visitor: location/age entry, directory browsing, filters, paid-ad disclosure, profile details, guarded contact reveal, and report entry point.
2. Advertiser: sign-in entry, onboarding progress, profile draft/editor, still-image upload states, review status, publication status, subscription terms, pause, and cancellation entry points.
3. Moderator: a small review queue and exact-revision decision view, only if time permits after the two public journeys.

Use the product brief and SAL-009–022 as behavior references. For this preview:

- Use local typed fixtures and deterministic UI states. Do not connect real identity, age, payment, media, email, analytics, or hosting providers.
- Do not collect or embed real personal data. Use fictional names, coarse locations, neutral placeholder imagery, and non-explicit content.
- Preserve the current `GET /api/v1/meta` connectivity check, but move it to a low-prominence development/system view if the home route becomes the directory.
- Make paid-ad labelling, external-contact boundaries, immediate unpublish language, easy cancellation, reporting access, and unavailable/denied states visible in the design.
- Keep service booking, chat, reviews, maps with precise pins, behavioural recommendations, tips, ranking boosts, and service-payment flows out of scope.
- Design for French and Dutch pilot content with English support copy, while placeholder translations may be used for the preview.
- Meet keyboard, focus, contrast, semantic-heading, form-label, error-state, responsive-layout, loading, empty, and unavailable-state basics.
- Prefer a small reusable component and token layer over page-specific inline styling.

Expected handoff artifacts:

- A route map and short note explaining which states are interactive versus illustrative.
- The implemented responsive preview in `apps/web`.
- A short mapping from each screen to its owning SAL story so production work remains traceable.
- `npm run lint`, `npm run type-check`, and `npm run build` results.
- Screenshots at desktop and mobile widths if the agent's environment supports browser capture.

The preview must be described as a synthetic design/interaction prototype. It does not satisfy the functional stories, release gates, provider approvals, or paid-pilot readiness.

## Source references

- `planning/implementation-plan.md`
- `planning/roadmap.yaml`
- `planning/README.md`
- `docs/product/mvp.md`
- `docs/architecture/mvp-architecture.md`
- `docs/development.md`
- `planning/stories/SAL-007.md`
- `planning/stories/SAL-009.md` through `planning/stories/SAL-022.md`
- `planning/stories/SAL-028.md`
- `planning/stories/SAL-034.md`
