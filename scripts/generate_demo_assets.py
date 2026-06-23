"""Generate fictional demo reports for NextOpsAgent showcase review."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from next_ops.automation_scorer import score_automation_opportunities
from next_ops.bottleneck_detector import detect_bottlenecks
from next_ops.export_utils import ensure_output_dir
from next_ops.report_builder import build_html_report, build_markdown_report
from next_ops.roadmap_builder import build_implementation_roadmap
from next_ops.roi_estimator import estimate_roi
from next_ops.workflow_parser import parse_workflow


SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample_workflows.csv"
DEMO_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "demo_reports"


def run_workflow_pipeline(workflow_text: str) -> dict:
    """Run the complete local diagnosis pipeline for one workflow text."""
    parsed = parse_workflow(workflow_text)
    bottlenecks = detect_bottlenecks(parsed)
    scores = score_automation_opportunities(bottlenecks)
    roi = estimate_roi(scores)
    roadmap = build_implementation_roadmap(scores)
    markdown_report = build_markdown_report(parsed, bottlenecks, scores, roi, roadmap)
    html_report = build_html_report(parsed, bottlenecks, scores, roi, roadmap)
    return {
        "parsed": parsed,
        "bottlenecks": bottlenecks,
        "scores": scores,
        "roi": roi,
        "roadmap": roadmap,
        "markdown_report": markdown_report,
        "html_report": html_report,
    }


def build_demo_readme(generated_reports: list[dict]) -> str:
    """Create README content describing the generated fictional demo reports."""
    lines = [
        "# NextOpsAgent Demo Reports",
        "",
        "These demo reports are generated from the bundled fictional SME sample workflows.",
        "They are intended for local review, portfolio preparation, and report QA.",
        "",
        "## Generated reports",
        "",
    ]
    for report in generated_reports:
        lines.extend(
            [
                f"- `{report['workflow_id']}_report.md` - {report['business_type']}",
                f"- `{report['workflow_id']}_report.html` - {report['business_type']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Safety and privacy note",
            "",
            "- All workflows are fictional sample data.",
            "- Do not place real customer, employee, phone, email, payment, or private chat data here.",
            "- The reports are educational workflow planning artifacts, not legal, financial, cybersecurity, or operational advice.",
            "- This folder is generated under `outputs/`, which is excluded from Git except `outputs/.gitkeep`.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_demo_assets() -> list[Path]:
    """Generate Markdown and HTML demo reports from fictional sample workflows."""
    samples = pd.read_csv(SAMPLE_DATA_PATH)
    output_dir = ensure_output_dir(str(DEMO_OUTPUT_DIR))
    written_files = []
    generated_reports = []

    for _, sample in samples.iterrows():
        workflow_id = str(sample["workflow_id"])
        business_type = str(sample["business_type"])
        workflow_text = str(sample["workflow_description"])
        result = run_workflow_pipeline(workflow_text)

        markdown_path = output_dir / f"{workflow_id}_report.md"
        html_path = output_dir / f"{workflow_id}_report.html"
        markdown_path.write_text(result["markdown_report"], encoding="utf-8")
        html_path.write_text(result["html_report"], encoding="utf-8")

        written_files.extend([markdown_path, html_path])
        generated_reports.append(
            {
                "workflow_id": workflow_id,
                "business_type": business_type,
            }
        )

    readme_path = output_dir / "README.md"
    readme_path.write_text(build_demo_readme(generated_reports), encoding="utf-8")
    written_files.append(readme_path)
    return written_files


if __name__ == "__main__":
    files = generate_demo_assets()
    print("Generated demo assets:")
    for file_path in files:
        print(f"- {file_path.relative_to(PROJECT_ROOT)}")
