"""Apply an approved challenge-text proposal to canonical curriculum JSON.

Purpose:
    Update every canonical prompt surface while respecting suite overrides.
Key Components:
    Stale-base validation, synchronized record edits, and dry-run reporting.
Dependencies:
    Canonical curriculum records and shared effective-record patching.
Used By:
    Maintainers applying an approved manifest review proposal.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from lesson_compiler.paths import CONFIG_PATH, RECORDS_ROOT
from lesson_compiler.support import patch_standard_record


def _load_object(path: Path) -> dict[str, Any]:
    """Load a JSON object or fail with source context."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def _challenge_number(field: object) -> int:
    """Return a supported challenge number from a proposal field."""
    if not isinstance(field, str) or not field.startswith("challenge_"):
        raise ValueError(f"unsupported proposal field: {field!r}")
    try:
        number = int(field.removeprefix("challenge_"))
    except ValueError as error:
        raise ValueError(f"invalid challenge field: {field}") from error
    if number not in {1, 2, 3}:
        raise ValueError(f"unsupported challenge number: {number}")
    return number


def _override_changes(config: dict[str, Any]) -> dict[tuple[int, int], str]:
    """Convert configured dotted challenge keys to tuple keys."""
    changes: dict[tuple[int, int], str] = {}
    for key, value in config["challenge_changes"].items():
        lesson_text, challenge_text = key.split(".")
        changes[(int(lesson_text), int(challenge_text))] = str(value)
    return changes


def _set_record_prompt(
    record: dict[str, Any], challenge: int, old_value: str, new_value: str
) -> None:
    """Update every prompt surface in one canonical lesson record."""
    targets = (
        record["primm"][challenge + 3],
        record["worksheet"]["page2"]["challenges"][challenge - 1],
        record["slides"][5 + (challenge - 1) * 2],
    )
    keys = ("prompt", "prompt", "body")
    actual = [target[key] for target, key in zip(targets, keys, strict=True)]
    if any(value != old_value for value in actual):
        raise ValueError(
            f"canonical prompt surfaces disagree for lesson "
            f"{record['lesson']['number']} challenge {challenge}: {actual}"
        )
    for target, key in zip(targets, keys, strict=True):
        target[key] = new_value

    contracts = record.get("challenge_contracts")
    if isinstance(contracts, list) and len(contracts) >= challenge:
        contract = contracts[challenge - 1]
        if contract.get("observable_outcome") == old_value:
            contract["observable_outcome"] = new_value
        test_cases = contract.get("test_cases")
        if isinstance(test_cases, list):
            contract["test_cases"] = [
                new_value if value == old_value else value for value in test_cases
            ]


def apply_prompt_proposal(
    proposal_path: Path,
    *,
    config_path: Path = CONFIG_PATH,
    records_root: Path = RECORDS_ROOT,
    write: bool = False,
) -> dict[str, object]:
    """Validate and optionally apply one approved prompt proposal.

    Args:
        proposal_path: Approved ``lesson_manifest_change_proposal`` JSON.
        config_path: Suite override configuration to inspect and update.
        records_root: Directory containing canonical lesson records.
        write: Whether to persist changes after complete validation.

    Returns:
        Application report listing record and override updates.

    Raises:
        ValueError: If proposal data is malformed, stale, or inconsistent.
    """
    proposal = _load_object(proposal_path)
    if proposal.get("kind") != "lesson_manifest_change_proposal":
        raise ValueError(f"unsupported proposal kind in {proposal_path}")
    raw_changes = proposal.get("changes")
    if not isinstance(raw_changes, list) or not raw_changes:
        raise ValueError("proposal must contain at least one change")

    config = _load_object(config_path)
    overrides = _override_changes(config)
    records: dict[int, dict[str, Any]] = {}
    validated: list[tuple[int, int, str, str]] = []
    seen: set[tuple[int, int]] = set()

    for change in raw_changes:
        if not isinstance(change, dict):
            raise ValueError("every proposal change must be an object")
        lesson = int(change["lesson_number"])
        challenge = _challenge_number(change.get("field"))
        key = (lesson, challenge)
        if key in seen:
            raise ValueError(f"duplicate proposal change: {lesson}.{challenge}")
        seen.add(key)
        old_value = change.get("old_value")
        new_value = change.get("new_value")
        if not isinstance(old_value, str) or not isinstance(new_value, str):
            raise ValueError(f"proposal values must be text for {lesson}.{challenge}")
        if not new_value.strip() or new_value == old_value:
            raise ValueError(f"proposal has no usable change for {lesson}.{challenge}")

        if lesson not in records:
            record_path = records_root / f"lesson{lesson:02d}.json"
            records[lesson] = _load_object(record_path)
        effective = patch_standard_record(
            deepcopy(records[lesson]), overrides, deepcopy(config)
        )
        current = effective["worksheet"]["page2"]["challenges"][challenge - 1][
            "prompt"
        ]
        if current != old_value:
            raise ValueError(
                f"stale proposal base for {lesson}.{challenge}: "
                f"expected {old_value!r}, found {current!r}"
            )
        validated.append((lesson, challenge, old_value, new_value))

    record_updates: set[int] = set()
    override_updates: list[str] = []
    for lesson, challenge, old_value, new_value in validated:
        dotted = f"{lesson}.{challenge}"
        if dotted in config["challenge_changes"]:
            config["challenge_changes"][dotted] = new_value
            override_updates.append(dotted)
        else:
            _set_record_prompt(records[lesson], challenge, old_value, new_value)
            record_updates.add(lesson)

    if write:
        if override_updates:
            config_path.write_text(
                json.dumps(config, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        for lesson in sorted(record_updates):
            path = records_root / f"lesson{lesson:02d}.json"
            path.write_text(
                json.dumps(records[lesson], indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    return {
        "passed": True,
        "write": write,
        "change_count": len(validated),
        "record_lessons": sorted(record_updates),
        "override_keys": sorted(override_updates),
    }
