# Sotto Salon implementation planning

This backlog follows Scripta's roadmap and story format. It describes future work; no application, provider approval, legal opinion, or production deployment exists yet. All stories start as `planned`.

- [Roadmap](roadmap.yaml): status, dependencies, decisions, release gates, planned and actual file changes.
- [Implementation sequence](implementation-plan.md): phases, staffing assumptions, critical path and release evidence.
- [Stories](stories/): independently reviewable requirements and acceptance criteria.
- [Product brief](../docs/product/mvp.md): subscription model and scope.
- [Architecture](../docs/architecture/mvp-architecture.md): proposed implementation and security boundaries.
- [Compliance assessment](../docs/compliance/launch-assessment.md): sourced legal questions and implementation mapping.
- [Provider assessment](../docs/providers/selection.md): researched candidates and underwriting requirements.

Read the product brief and applicable story before implementation. Select work whose dependencies are done; synthetic prototypes may proceed earlier with the dependency recorded as a constraint. An open decision blocks the production use described in its `blocks` field, not unrelated local development. Record the actual decision, decision maker, date, evidence reference and review date when resolving it. Do not store identity documents or confidential contracts in Git.

Statuses are `planned`, `in_progress`, `blocked`, `in_review`, `done`, and `cancelled`. Keep YAML and story scope aligned. Update `code_impact.actual` with exact files actually changed, and `verification.evidence` with actual commands, results or reviewed evidence references. Requirements files are not implementation evidence. A story is done only when all acceptance criteria and its definition of done hold. Split broad stories before assigning them if needed.

Paths are workspace-relative and mostly proposed. This backlog does not authorize purchases, provider outreach, live identity checks, commits, pushes, or deployment. Release approval is a later operational gate, not a request to approve these planning files.

Run `python planning/validate_backlog.py` from the root. Requires Python 3 and `PyYAML` (`python -m pip install -r planning/requirements-validation.txt` if missing). Validation checks references, cycles, story sections and file-impact consistency; it cannot establish legal compliance or test nonexistent software.
