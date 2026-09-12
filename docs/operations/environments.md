# Environment and release operations

SAL-008 provides synthetic CI and candidate image publication. ARC-005 (hosting and
supporting services) remains open: no live staging, production, database, object storage,
or secret manager has been provisioned or approved. The inventories are explicitly
synthetic. They are not evidence of a running deployment.

## Isolation and access contract

After ARC-005 approval, provision staging and production in separate provider projects,
networks, databases, buckets, secret namespaces and service accounts. Never copy production
data or credentials into staging. Staging verification uses lawful synthetic fixtures.

Only the ingress endpoint is public. Terminate TLS at an approved managed ingress with
automatic certificate renewal, HTTPS redirects and TLS 1.2 or newer. Restrict API ingress
to the proxy; restrict PostgreSQL ingress to API/worker and migration identities over the
private network. Require certificate-verified TLS for database connections. Do not expose
PostgreSQL, administration ports, or bucket listing to the internet. Object storage must
disable public access and use private endpoints where supported; grant access only to
the relevant service identity and environment-specific bucket/prefix. Downloads require
application authorization and short-lived signed URLs when that feature is implemented.

The container runs as UID 10001. Runtime accounts must not have provider administration,
IAM modification, database ownership/DDL, or access to other environments. The API database
role gets only required table DML and sequence privileges. A separate migration role owns
schema changes and is available only to the approved migration job. Separate API, worker,
release publisher and operator identities; disable shared permanent administrator keys.

Inject SALON_DATABASE_URL and SALON_SESSION_SECRET at process start from the approved
secret manager using workload identity where available. Production must set
SALON_ENVIRONMENT=production in the process environment. No dotenv files, build arguments,
image layers, logs or inventories may contain secret values. Inventory name/source/path
fields are locators only; schema validation cannot determine whether an arbitrary string
is a real credential. Review locators and retain secret scanning. Rotate secrets through
new manager versions and restart consumers; record references, never values.

## CI and release gates

Normal CI uses a read-only repository token, no deployment environment, and no deployment
secrets. It runs lint, Python/TypeScript checks, backend tests, schema and inventory checks,
container build, dependency audits and secret scanning. Configure these jobs as required
branch checks, protect main, and restrict version tag creation to release maintainers.

Before enabling Release, create the GitHub production environment, configure required
reviewers and prevent self-review. Restrict eligible release refs and disable administrator
bypass where supported. Merely naming an environment in YAML does not establish approval
rules. Verify these repository settings with a trial run awaiting approval before publishing.
Do not add deployment credentials until these protections and ARC-005 are approved.

Release accepts an existing vMAJOR.MINOR.PATCH tag (optional prerelease suffix). Both tag
pushes and manual dispatch resolve that tag to a commit; checkout and image labels use the
resolved commit. Publish only a commit whose required CI checks passed. The production
environment approval must include checking that commit's CI results. The workflow builds
and publishes a candidate, then records the registry digest, tag, repository, configuration
commit and secret references in the release-inventory artifact. Missing or invalid templates
fail; the record is validated against the published digest. Artifacts are retained for 90
days; archive approved release records in the approved audit store before expiry.

No deployment is performed. The production template has no live secret references and
remains synthetic. After provider approval, create a live configuration and real locator
references, resolve the candidate digest, and deploy by repository@sha256 digest. Record
the applied configuration version and verify the runtime digest before declaring success.
Never use a tag alone as a deployment identity. A failed inventory upload can leave a
published candidate; treat it as unreleased until its validated record is retained.

## Migration and recovery procedure

CI upgrades and downgrades the baseline on throwaway SQLite. This only verifies the
baseline migration mechanics; it is not PostgreSQL recovery evidence. Before a live
schema change, test it against the approved PostgreSQL version using synthetic data,
record the current/target revision, backup reference, compatible app digest, rollback or
forward-repair script, owner and expected interruption. Follow ARC-006 for approved backup
and recovery objectives; that decision remains open.

Use expand/contract migrations so the previous image remains compatible during rollout.
Stop on failed migration, retain the previous serving image where compatible, and apply
the reviewed repair plan. Never automatically downgrade production: the baseline downgrade
drops system_metadata and destroys its contents. A destructive rollback requires the
approved backup/restore procedure and explicit operator review. Verify schema revision,
health/readiness and data integrity before resuming traffic.

## Required live acceptance evidence (pending ARC-005)

- AC02: runtime image digest matches the retained inventory; staging and production
  resources are isolated; external database connection and anonymous bucket access fail.
- AC03: record certificate hostname/chain/expiry and HTTPS redirect checks; reject obsolete
  TLS; prove runtime identities cannot change IAM, execute DDL or access another environment.
- Verify secret injection and rotation without logging values, and record only secret IDs.
- AC04: demonstrate an unauthorized/unapproved release cannot publish; record the reviewer,
  approved commit, successful required CI checks and retained inventory artifact.

Record dated results and provider configuration references in the roadmap. Do not mark
live acceptance complete based on templates or local tests.
