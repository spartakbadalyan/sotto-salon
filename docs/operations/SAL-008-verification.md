# SAL-008 verification — 2026-09-13

Scope: local synthetic foundation and review fixes. No provider resources were provisioned,
no registry image was published, and no GitHub protection settings were changed.

| Check | Result |
| --- | --- |
| Backend Ruff | Passed |
| `python -m mypy --no-incremental` in backend | Passed, 26 source files |
| Backend pytest | Passed, 24 tests; two existing dependency deprecation warnings |
| `python -m unittest discover -s infra/deployment/tests -v` | Passed, 7 tests |
| Staging and production template validation | Passed |
| Baseline Alembic upgrade head / downgrade base on temporary SQLite | Passed |
| Workflow YAML parsing | Passed; does not prove GitHub Actions execution |
| Docker build | Blocked fetching dependencies: container PyPI TLS certificate verification failed |
| Hosted CI, vulnerability audits and secret scan | Not executed locally; require hosted run |
| Release tag resolution, approval and registry/artifact publication | Code reviewed; hosted execution pending |

Local Python is 3.14; CI targets 3.12. Mypy checks against Python 3.12 semantics. Initial
sandboxed pytest attempts could not access temporary directories; the unrestricted local
rerun passed. Docker verification reached dependency installation and failed on certificate
trust. TLS verification was not disabled. The base image manifest resolved successfully
and is pinned in the Dockerfile; final image build verification remains outstanding.

Negative inventory tests reject unknown secret fields at the root, image and reference
levels; malformed field types and provisioning modes; a placeholder live digest; and a
digest different from the expected published image. They verify diagnostics do not include
synthetic secret values, and that recording replaces the template digest and configuration
version without changing the template or losing secret references. Invalid templates and
invalid published digests fail recording.

AC01 has local test evidence and a workflow with no deployment secrets/environment; an
actual hosted failing-test run and untrusted PR run remain pending. AC02 has a digest-bound
candidate inventory implementation, but no running staging service or private resource
verification. AC03 is pending ARC-005 and the live checks in environments.md. AC04 has a
separate release workflow targeting production; required reviewers must still be configured
and demonstrated in GitHub. SAL-008 therefore remains in progress, not accepted for live use.
