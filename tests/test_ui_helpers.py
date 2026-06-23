from pathlib import Path

from next_ops.ui_helpers import (
    build_score_dataframe,
    format_list_as_badges,
    format_priority_badge,
    load_sample_workflows,
    safe_join,
)


def test_load_sample_workflows_uses_fallback_for_missing_file():
    samples = load_sample_workflows(Path("missing_sample_file.csv"))
    assert len(samples) == 1
    assert samples.iloc[0]["workflow_id"] == "WF-FALLBACK"
    assert "workflow_description" in samples.columns


def test_safe_join_and_badges_handle_empty_values():
    assert safe_join([]) == "Not detected"
    assert safe_join(["Email", "WeChat"]) == "Email, WeChat"
    assert "Not detected" in format_list_as_badges([])
    assert "&lt;script&gt;" in format_list_as_badges(["<script>"])


def test_format_priority_badge_and_score_dataframe():
    assert "priority-high" in format_priority_badge("High Priority")
    score_table = build_score_dataframe(
        [
            {
                "bottleneck_name": "Manual follow-up",
                "category": "Customer Follow-up",
                "total_score": 91.2,
                "priority_level": "High Priority",
                "recommended_solution_type": "Reminder Automation",
                "implementation_difficulty": "Easy",
            }
        ]
    )
    assert list(score_table.columns) == [
        "Bottleneck",
        "Category",
        "Total Score",
        "Priority",
        "Solution Type",
        "Difficulty",
    ]
    assert score_table.iloc[0]["Solution Type"] == "Reminder Automation"
