"""Validate planning documents, not application implementation or legal compliance."""

from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit(
        "PyYAML is required; install planning/requirements-validation.txt."
    )


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise yaml.YAMLError("Mapping keys must be strings")
        if key in result:
            raise yaml.YAMLError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def load_yaml(text):
    return yaml.load(text, Loader=UniqueKeyLoader)


SECTIONS = (
    "Outcome", "Scope", "Requirements", "Data and API", "Failure and Security",
    "Acceptance Criteria", "Verification", "Code Impact", "Definition of Done",
)
STATUSES = {"planned", "in_progress", "blocked", "in_review", "done", "cancelled"}
ACTIONS = {"create", "modify", "delete"}


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and not PureWindowsPath(value).drive
        and ".." not in path.parts
        and path.parts != ()
        and path != PurePosixPath(".")
    )


def validate(data, root):
    errors = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["Expected mapping with schema_version: 1"]
    for key in ("epics", "stories", "decisions"):
        entries = data.get(key)
        if not isinstance(entries, list) or not entries:
            errors.append(f"{key}: expected a nonempty list")
        elif not all(isinstance(item, dict) and isinstance(item.get("id"), str)
                     for item in entries):
            errors.append(f"{key}: entries must be mappings with string IDs")
    if errors:
        return errors

    for key, pattern in (("epics", r"EPIC-\d{2}"),
                         ("stories", r"SAL-\d{3}"),
                         ("decisions", r"ARC-\d{3}")):
        counts = Counter(item["id"] for item in data[key])
        errors.extend(f"Duplicate {key} ID: {item}" for item, n in counts.items() if n > 1)
        errors.extend(f"Invalid {key} ID: {item}" for item in counts
                      if not re.fullmatch(pattern, item))

    stories = {item["id"]: item for item in data["stories"]}
    epics = {item["id"]: item for item in data["epics"]}
    decisions = {item["id"]: item for item in data["decisions"]}
    graph = {}
    memberships = Counter()
    linked_files = set()
    acceptance_ids = []

    def document(value, label):
        if not safe_path(value):
            errors.append(f"{label}: unsafe or missing workspace-relative path")
            return None
        path = root / value
        if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(f"{label}: missing or out-of-workspace file: {value}")
            return None
        return path

    for key in ("architecture_file", "product_file", "tracking_guide"):
        document(data.get(key), key)
    for item in decisions.values():
        if item.get("status") not in {"open", "approved", "rejected"}:
            errors.append(f"{item['id']}: invalid decision status")

    for epic_id, epic in epics.items():
        members = epic.get("stories")
        if epic.get("status") not in STATUSES:
            errors.append(f"{epic_id}: invalid status")
        if not isinstance(members, list) or not all(isinstance(x, str) for x in members):
            errors.append(f"{epic_id}: stories must be a string list")
            continue
        for member in members:
            memberships[member] += 1
            if member not in stories or stories[member].get("epic_id") != epic_id:
                errors.append(f"{epic_id}: incorrect story membership: {member}")
            elif epic.get("status") == "done" and stories[member].get("status") != "done":
                errors.append(f"{epic_id}: done epic has unfinished story: {member}")

    for story_id, story in stories.items():
        if story.get("status") not in STATUSES or story.get("priority") not in {"P0", "P1"}:
            errors.append(f"{story_id}: invalid status or priority")
        if not isinstance(story.get("title"), str) or not story["title"].strip():
            errors.append(f"{story_id}: missing title")
        if story.get("epic_id") not in epics or memberships[story_id] != 1:
            errors.append(f"{story_id}: must belong to exactly one matching epic")

        for field, known in (("depends_on", stories), ("blocked_by_decisions", decisions)):
            values = story.get(field)
            if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
                errors.append(f"{story_id}: {field} must be a string list")
                values = []
            if len(set(values)) != len(values):
                errors.append(f"{story_id}: duplicate {field} entries")
            for value in values:
                if value not in known:
                    errors.append(f"{story_id}: unknown {field}: {value}")
                elif story.get("status") == "done":
                    required = "done" if field == "depends_on" else "approved"
                    if known[value].get("status") != required:
                        errors.append(f"{story_id}: done with unresolved prerequisite {value}")
            if field == "depends_on":
                graph[story_id] = [value for value in values if value in stories]

        verification = story.get("verification", {})
        implementation = story.get("implementation", {})
        if not isinstance(verification, dict) or not all(
            isinstance(verification.get(key), list) for key in ("planned", "evidence")
        ):
            errors.append(f"{story_id}: invalid verification record")
        elif story.get("status") == "done" and not verification["evidence"]:
            errors.append(f"{story_id}: done without verification evidence")
        if not isinstance(implementation, dict) or not all(
            key in implementation for key in ("pull_request", "commits", "notes")
        ) or not isinstance(implementation.get("commits"), list):
            errors.append(f"{story_id}: invalid implementation record")

        impact = story.get("code_impact", {})
        planned_paths = set()
        if not isinstance(impact, dict):
            errors.append(f"{story_id}: invalid code impact")
            impact = {}
        for field in ("planned", "actual"):
            entries = impact.get(field)
            if not isinstance(entries, list) or (field == "planned" and not entries):
                errors.append(f"{story_id}: invalid {field} code impact")
                continue
            seen = set()
            for entry in entries:
                if not isinstance(entry, dict) or not safe_path(entry.get("path")) \
                        or entry.get("action") not in ACTIONS:
                    errors.append(f"{story_id}: invalid {field} code impact entry")
                    continue
                path = entry["path"]
                if path in seen:
                    errors.append(f"{story_id}: duplicate {field} path: {path}")
                seen.add(path)
                if field == "planned":
                    planned_paths.add((entry["action"], path))
                elif entry["action"] != "delete" and not (root / path).is_file():
                    errors.append(f"{story_id}: actual change is not an existing exact file: {path}")

        path = document(story.get("requirements_file"), story_id)
        if path is None:
            continue
        if path in linked_files:
            errors.append(f"{story_id}: requirements file reused by another story")
        linked_files.add(path)
        text = path.read_text(encoding="utf-8")
        if not text.startswith(f"# {story_id}: ") or f"Epic: {story.get('epic_id')}." not in text:
            errors.append(f"{story_id}: Markdown identity/epic mismatch")
        for section in SECTIONS:
            if f"\n## {section}\n" not in text:
                errors.append(f"{story_id}: missing section: {section}")
        ids = re.findall(r"(?m)^- (SAL-\d{3}-AC\d{2}):", text)
        if len(ids) < 4 or any(not item.startswith(story_id + "-") for item in ids):
            errors.append(f"{story_id}: requires at least four correctly scoped acceptance IDs")
        acceptance_ids.extend(ids)
        match = re.search(r"\n## Code Impact\n(.*?)(?=\n## |\Z)", text, re.S)
        if match:
            documented = {(action.lower(), value) for action, value in re.findall(
                r"(?m)^- (Create|Modify|Delete) `([^`]+)`\.", match.group(1)
            )}
            if documented != planned_paths:
                errors.append(f"{story_id}: Markdown/YAML code impact mismatch")

    counts = Counter(acceptance_ids)
    errors.extend(f"Duplicate acceptance ID: {item}" for item, n in counts.items() if n > 1)
    for path in (root / "planning/stories").glob("SAL-*.md"):
        if path not in linked_files:
            errors.append(f"Unindexed story file: {path.name}")

    active, visited = [], set()

    def visit(node):
        if node in active:
            errors.append("Dependency cycle: " + " -> ".join(active + [node]))
            return
        if node in visited:
            return
        active.append(node)
        for dependency in graph.get(node, []):
            visit(dependency)
        active.pop()
        visited.add(node)

    for story_id in stories:
        visit(story_id)
    gates = data.get("release_gates")
    if not isinstance(gates, dict) or not gates:
        errors.append("Missing release gates")
    else:
        for name, gate in gates.items():
            if not isinstance(gate, dict):
                errors.append(f"{name}: invalid release gate")
                continue
            for field, known in (("stories", stories), ("decisions", decisions)):
                refs = gate.get(field)
                if not isinstance(refs, list) or not all(isinstance(x, str) and x in known for x in refs):
                    errors.append(f"{name}: invalid release {field}")
            if not isinstance(gate.get("approvals"), list) or not gate["approvals"]:
                errors.append(f"{name}: missing explicit release approvals")
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        data = load_yaml((root / "planning/roadmap.yaml").read_text(encoding="utf-8"))
        errors = validate(data, root)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("Backlog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(data['epics'])} epics, {len(data['stories'])} stories, "
          f"and {len(data['decisions'])} architecture decisions.")
    print("Links, dependencies, story sections, acceptance IDs, and code impacts are consistent.")
    print("This validates planning artifacts only; application tests have not been executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
