from next_ops.automation_scorer import score_automation_opportunities
from next_ops.bottleneck_detector import detect_bottlenecks
from next_ops.report_builder import build_html_report, build_markdown_report
from next_ops.roi_estimator import estimate_roi
from next_ops.roadmap_builder import build_implementation_roadmap
from next_ops.workflow_parser import parse_workflow


def test_build_markdown_report_contains_required_sections():
    parsed = parse_workflow(
        "A consulting team uses email and Excel. Staff manually prepare a weekly report."
    )
    bottlenecks = detect_bottlenecks(parsed)
    scores = score_automation_opportunities(bottlenecks)
    roi = estimate_roi(scores)
    roadmap = build_implementation_roadmap(scores)
    report = build_markdown_report(parsed, bottlenecks, scores, roi, roadmap)

    assert "Executive Summary" in report
    assert "Automation Opportunity Scores" in report
    assert "Implementation Roadmap" in report
    assert "Consultant Notes" in report
    assert "Evidence Snippets" in report
    assert "Disclaimer" in report
    assert "This report is for educational and workflow planning purposes only." in report


def test_build_html_report_contains_required_sections_and_disclaimer():
    parsed = parse_workflow(
        "A consulting team uses email and Excel. Staff manually prepare a weekly report."
    )
    bottlenecks = detect_bottlenecks(parsed)
    scores = score_automation_opportunities(bottlenecks)
    roi = estimate_roi(scores)
    roadmap = build_implementation_roadmap(scores)
    report = build_html_report(parsed, bottlenecks, scores, roi, roadmap)

    assert "<html" in report.lower()
    assert "Executive Summary" in report
    assert "Automation Opportunity Scores" in report
    assert "Implementation Roadmap" in report
    assert "This report is for educational and workflow planning purposes only." in report


def test_build_html_report_escapes_user_workflow_text():
    parsed = parse_workflow(
        "A team copies Excel data manually. <script>alert(1)</script>"
    )
    bottlenecks = detect_bottlenecks(parsed)
    scores = score_automation_opportunities(bottlenecks)
    roi = estimate_roi(scores)
    roadmap = build_implementation_roadmap(scores)
    report = build_html_report(parsed, bottlenecks, scores, roi, roadmap)

    assert "<script>alert(1)</script>" not in report
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in report
