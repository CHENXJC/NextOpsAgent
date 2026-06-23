"""Small presentation helpers for the Streamlit dashboard.

The core diagnosis engine stays independent from Streamlit. These helpers keep
the UI readable while staying simple enough for beginners to inspect.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


REQUIRED_SAMPLE_COLUMNS = {
    "workflow_id",
    "business_type",
    "workflow_description",
    "expected_main_bottleneck",
}

FALLBACK_SAMPLE_WORKFLOW = {
    "workflow_id": "WF-FALLBACK",
    "business_type": "Tutoring business",
    "workflow_description": (
        "A tutoring business receives student enquiries from WeChat, records "
        "lead details in Excel, sends course information manually, follows up "
        "after 3 days, and prepares weekly reports by copying spreadsheet data."
    ),
    "expected_main_bottleneck": "Manual follow-up",
}

PRIORITY_BADGE_CLASS = {
    "High Priority": "priority-high",
    "Medium Priority": "priority-medium",
    "Low Priority": "priority-low",
    "Not Recommended": "priority-muted",
}


def load_sample_workflows(sample_path: Path) -> pd.DataFrame:
    """Load fictional sample workflows with a safe fallback row."""
    try:
        samples = pd.read_csv(sample_path)
        if REQUIRED_SAMPLE_COLUMNS.issubset(samples.columns) and not samples.empty:
            return samples
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        pass
    return pd.DataFrame([FALLBACK_SAMPLE_WORKFLOW])


def safe_join(values: list[str] | tuple[str, ...] | None, empty: str = "Not detected") -> str:
    """Join display values while handling missing or empty lists."""
    if not values:
        return empty
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return empty
    return ", ".join(cleaned)


def badge(label: str, css_class: str = "badge") -> str:
    """Return escaped HTML for a small dashboard badge."""
    return f'<span class="{escape(css_class)}">{escape(str(label))}</span>'


def format_list_as_badges(values: list[str] | tuple[str, ...] | None) -> str:
    """Render a list as escaped badge HTML, or a muted placeholder."""
    if not values:
        return badge("Not detected", "badge badge-muted")
    return " ".join(badge(value) for value in values if str(value).strip())


def format_priority_badge(priority_level: str) -> str:
    """Return a color-coded priority badge for a score row."""
    css_class = PRIORITY_BADGE_CLASS.get(priority_level, "priority-muted")
    return badge(priority_level or "Unknown", f"priority-badge {css_class}")


def build_score_dataframe(scored_opportunities: list[dict]) -> pd.DataFrame:
    """Create a compact score table for Streamlit display."""
    rows = []
    for opportunity in scored_opportunities:
        rows.append(
            {
                "Bottleneck": opportunity.get("bottleneck_name", "Unknown"),
                "Category": opportunity.get("category", "Unknown"),
                "Total Score": opportunity.get("total_score", 0),
                "Priority": opportunity.get("priority_level", "Unknown"),
                "Solution Type": opportunity.get(
                    "recommended_solution_type", "SOP Automation"
                ),
                "Difficulty": opportunity.get("implementation_difficulty", "Medium"),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "Bottleneck",
            "Category",
            "Total Score",
            "Priority",
            "Solution Type",
            "Difficulty",
        ],
    )
