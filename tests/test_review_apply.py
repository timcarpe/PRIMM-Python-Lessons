"""Tests for applying an approved challenge-text proposal."""

from __future__ import annotations

import json
import shutil

from lesson_compiler.paths import CONFIG_PATH, RECORDS_ROOT
from lesson_compiler.review_tool.apply import apply_prompt_proposal


def test_apply_prompt_proposal_updates_record_and_override(tmp_path) -> None:
    """Raw records and existing suite overrides use their canonical sources."""
    # Arrange
    records = tmp_path / "records"
    records.mkdir()
    for lesson in (4, 9):
        shutil.copy2(RECORDS_ROOT / f"lesson{lesson:02d}.json", records)
    config = tmp_path / "suite.json"
    shutil.copy2(CONFIG_PATH, config)
    proposal = tmp_path / "proposal.json"
    record_old = json.loads((records / "lesson04.json").read_text())["worksheet"][
        "page2"
    ]["challenges"][1]["prompt"]
    suite_data = json.loads(config.read_text())
    override_old = suite_data["challenge_changes"]["9.1"]
    proposal.write_text(
        json.dumps(
            {
                "kind": "lesson_manifest_change_proposal",
                "changes": [
                    {
                        "lesson_number": 4,
                        "field": "challenge_2",
                        "old_value": record_old,
                        "new_value": "Revised record prompt.",
                    },
                    {
                        "lesson_number": 9,
                        "field": "challenge_1",
                        "old_value": override_old,
                        "new_value": "Revised override prompt.",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    # Act
    report = apply_prompt_proposal(
        proposal, config_path=config, records_root=records, write=True
    )
    record = json.loads((records / "lesson04.json").read_text())
    updated_config = json.loads(config.read_text())

    # Assert
    assert report["change_count"] == 2
    assert record["primm"][5]["prompt"] == "Revised record prompt."
    assert record["worksheet"]["page2"]["challenges"][1]["prompt"] == (
        "Revised record prompt."
    )
    assert record["slides"][7]["body"] == "Revised record prompt."
    assert updated_config["challenge_changes"]["9.1"] == (
        "Revised override prompt."
    )
