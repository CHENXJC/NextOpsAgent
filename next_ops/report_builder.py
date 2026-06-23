"""Build consultant-style workflow diagnosis reports."""

from html import escape


DISCLAIMER = (
    "This report is for educational and workflow planning purposes only. "
    "It does not replace professional operational, legal, financial, or cybersecurity advice."
)


def _format_range(minimum: float, maximum: float, prefix: str = "") -> str:
    return f"{prefix}{minimum:,.1f}–{prefix}{maximum:,.1f}"


def _roadmap_section(title: str, tasks: list[dict]) -> list[str]:
    lines = [f"### {title}", ""]
    for task in tasks:
        lines.extend(
            [
                f"#### {task.get('task', 'Workflow task')}",
                "",
                f"- **Why it matters:** {task.get('why_it_matters', 'Supports workflow improvement.')}",
                f"- **Related bottleneck:** {task.get('related_bottleneck', 'General workflow')}",
                f"- **Difficulty:** {task.get('difficulty', 'Medium')}",
                "",
            ]
        )
    return lines


def _html(value: object) -> str:
    """Escape a value for safe HTML report rendering."""
    return escape(str(value), quote=True)


def _html_list(items: list[str], fallback: str) -> str:
    """Render escaped list items for the HTML report."""
    values = items or [fallback]
    return "\n".join(f"<li>{_html(item)}</li>" for item in values)


def _summary_card(label: str, value: object) -> str:
    """Render a small escaped summary card."""
    return (
        '<div class="summary-card">'
        f'<div class="label">{_html(label)}</div>'
        f'<div class="value">{_html(value)}</div>'
        "</div>"
    )


def _roadmap_html(title: str, tasks: list[dict]) -> str:
    """Render a roadmap phase for the HTML report."""
    cards = []
    if not tasks:
        tasks = [
            {
                "task": "No roadmap task available.",
                "why_it_matters": "Add more workflow detail to generate a stronger plan.",
                "related_bottleneck": "General workflow",
                "difficulty": "Medium",
            }
        ]
    for task in tasks:
        cards.append(
            f"""
            <div class="card compact">
                <h4>{_html(task.get("task", "Workflow task"))}</h4>
                <p>{_html(task.get("why_it_matters", "Supports workflow improvement."))}</p>
                <p>
                    <span class="badge">{_html(task.get("related_bottleneck", "General workflow"))}</span>
                    <span class="badge">{_html(task.get("difficulty", "Medium"))} Difficulty</span>
                </p>
            </div>
            """
        )
    return f"<h3>{_html(title)}</h3>{''.join(cards)}"


def build_markdown_report(
    parsed_workflow: dict,
    bottlenecks: list[dict],
    scored_opportunities: list[dict],
    roi_estimate: dict,
    roadmap: dict,
) -> str:
    """Return a complete evidence-based Markdown workflow diagnosis report."""
    top = scored_opportunities[0] if scored_opportunities else None
    top_priority = (
        f"{top['bottleneck_name']} — {top['total_score']}/100 ({top['priority_level']})"
        if top
        else "No scored opportunity"
    )
    hours_range = _format_range(
        roi_estimate.get("estimated_monthly_hours_saved_min", 0),
        roi_estimate.get("estimated_monthly_hours_saved_max", 0),
    )
    lines = [
        "# NextOpsAgent Workflow Diagnosis Report",
        "",
        "## Executive Summary",
        "",
        f"- **Business Type:** {parsed_workflow.get('detected_business_type', 'General SME')}",
        f"- **Workflow Complexity:** {parsed_workflow.get('workflow_complexity_level', 'Simple')}",
        f"- **Number of Bottlenecks:** {len(bottlenecks)}",
        f"- **Top Automation Priority:** {top_priority}",
        f"- **Estimated Monthly Time Saved:** {hours_range} hours",
        "",
        "## Original Workflow",
        "",
        parsed_workflow.get("original_text") or "No workflow text provided.",
        "",
        "## Detected Workflow Steps",
        "",
    ]
    steps = parsed_workflow.get("detected_steps", []) or ["No steps detected."]
    lines.extend(f"{index}. {step}" for index, step in enumerate(steps, 1))

    lines.extend(["", "## Evidence Snippets", ""])
    snippets = parsed_workflow.get("evidence_snippets", []) or [
        "No evidence snippets available."
    ]
    lines.extend(f"- {snippet}" for snippet in snippets)

    lines.extend(["", "## Bottleneck Diagnosis", ""])
    if not bottlenecks:
        lines.append("No rule-based bottlenecks were detected. Add more operational detail.")
    for item in bottlenecks:
        lines.extend(
            [
                f"### {item['bottleneck_name']}",
                "",
                f"- **Category:** {item['category']}",
                f"- **Severity:** {item['severity']}",
                f"- **Evidence:** {item['evidence']}",
                f"- **Impact:** {item['impact']}",
                f"- **Suggested Fix:** {item['suggested_fix']}",
                f"- **Automation Pattern:** {item['automation_pattern']}",
                f"- **Confidence:** {item['confidence']}",
                "",
            ]
        )

    lines.extend(["## Automation Opportunity Scores", ""])
    if not scored_opportunities:
        lines.append("No automation opportunities are available to score.")
    for item in scored_opportunities:
        explanation = item.get("score_explanation", {})
        lines.extend(
            [
                f"### {item['bottleneck_name']}",
                "",
                f"- **Total Score:** {item['total_score']}/100",
                f"- **Priority Level:** {item['priority_level']}",
                f"- **Recommended Solution Type:** {item['recommended_solution_type']}",
                f"- **Implementation Difficulty:** {item['implementation_difficulty']}",
                "- **Score Explanation:**",
                f"  - Repetition: {explanation.get('repetition_reason', 'Not available.')}",
                f"  - Manual effort: {explanation.get('manual_effort_reason', 'Not available.')}",
                f"  - Error risk: {explanation.get('error_risk_reason', 'Not available.')}",
                f"  - Response delay: {explanation.get('response_delay_reason', 'Not available.')}",
                f"  - Automation fit: {explanation.get('automation_fit_reason', 'Not available.')}",
                "",
            ]
        )

    cost_range = _format_range(
        roi_estimate.get("estimated_monthly_cost_saved_min", 0),
        roi_estimate.get("estimated_monthly_cost_saved_max", 0),
        "AUD ",
    )
    lines.extend(
        [
            "## ROI Estimate",
            "",
            f"- **Monthly Hours Saved:** {hours_range} hours",
            f"- **Monthly Cost Saved:** {cost_range}",
            f"- **Hourly Cost Assumption:** AUD {roi_estimate.get('hourly_cost_aud', 30):,.2f}/hour",
            f"- **Business Size:** {roi_estimate.get('business_size', 'small')}",
            f"- **Workflow Frequency:** {roi_estimate.get('workflow_frequency', 'weekly')}",
            f"- **Confidence Level:** {roi_estimate.get('confidence_level', 'Low')}",
            f"- **Assumption:** {roi_estimate.get('assumption', 'Rule-based estimate only.')}",
            "",
            "### ROI Notes",
            "",
        ]
    )
    lines.extend(
        f"- {note}" for note in roi_estimate.get("roi_notes", [])
    )

    lines.extend(["", "## Implementation Roadmap", ""])
    lines.extend(_roadmap_section("7-Day MVP", roadmap.get("seven_day_mvp", [])))
    lines.extend(
        _roadmap_section(
            "30-Day Optimization", roadmap.get("thirty_day_optimization", [])
        )
    )
    lines.extend(
        _roadmap_section(
            "90-Day Systemization", roadmap.get("ninety_day_systemization", [])
        )
    )
    lines.extend(
        [
            "## Consultant Notes",
            "",
            "- Start with high-priority, low-difficulty workflow fixes.",
            "- Avoid automating a broken process without first standardizing it.",
            "- Track before/after metrics for response time, manual hours, and lead conversion.",
            "",
            "## Disclaimer",
            "",
            DISCLAIMER,
        ]
    )
    return "\n".join(lines)


def build_html_report(
    parsed_workflow: dict,
    bottlenecks: list[dict],
    scored_opportunities: list[dict],
    roi_estimate: dict,
    roadmap: dict,
) -> str:
    """Return a complete escaped HTML workflow diagnosis report."""
    top = scored_opportunities[0] if scored_opportunities else None
    top_priority = (
        f"{top['bottleneck_name']} — {top['total_score']}/100 ({top['priority_level']})"
        if top
        else "No scored opportunity"
    )
    hours_range = _format_range(
        roi_estimate.get("estimated_monthly_hours_saved_min", 0),
        roi_estimate.get("estimated_monthly_hours_saved_max", 0),
    )
    cost_range = _format_range(
        roi_estimate.get("estimated_monthly_cost_saved_min", 0),
        roi_estimate.get("estimated_monthly_cost_saved_max", 0),
        "AUD ",
    )

    summary_cards = "".join(
        [
            _summary_card(
                "Business Type",
                parsed_workflow.get("detected_business_type", "General SME"),
            ),
            _summary_card(
                "Workflow Complexity",
                parsed_workflow.get("workflow_complexity_level", "Simple"),
            ),
            _summary_card("Bottlenecks Found", len(bottlenecks)),
            _summary_card("Top Automation Priority", top_priority),
            _summary_card("Estimated Monthly Time Saved", f"{hours_range} hours"),
        ]
    )

    steps = parsed_workflow.get("detected_steps", []) or ["No steps detected."]
    evidence = parsed_workflow.get("evidence_snippets", []) or [
        "No evidence snippets available."
    ]

    bottleneck_cards = []
    if not bottlenecks:
        bottleneck_cards.append(
            '<div class="card"><p>No rule-based bottlenecks were detected. '
            "Add more operational detail.</p></div>"
        )
    for item in bottlenecks:
        bottleneck_cards.append(
            f"""
            <div class="card">
                <h3>{_html(item.get("bottleneck_name", "Workflow bottleneck"))}</h3>
                <p>
                    <span class="badge">{_html(item.get("category", "Workflow"))}</span>
                    <span class="badge">{_html(item.get("severity", "Medium"))} Severity</span>
                    <span class="badge">{_html(item.get("confidence", "Medium"))} Confidence</span>
                </p>
                <p>{_html(item.get("description", ""))}</p>
                <ul>
                    <li><strong>Evidence:</strong> {_html(item.get("evidence", "Not available."))}</li>
                    <li><strong>Impact:</strong> {_html(item.get("impact", "Not available."))}</li>
                    <li><strong>Suggested Fix:</strong> {_html(item.get("suggested_fix", "Not available."))}</li>
                    <li><strong>Automation Pattern:</strong> {_html(item.get("automation_pattern", "Not available."))}</li>
                </ul>
            </div>
            """
        )

    score_rows = []
    score_explanations = []
    for item in scored_opportunities:
        score_rows.append(
            f"""
            <tr>
                <td>{_html(item.get("bottleneck_name", "Workflow bottleneck"))}</td>
                <td>{_html(item.get("category", "Workflow"))}</td>
                <td>{_html(item.get("total_score", 0))}/100</td>
                <td><span class="badge">{_html(item.get("priority_level", "Unknown"))}</span></td>
                <td>{_html(item.get("recommended_solution_type", "SOP Automation"))}</td>
                <td>{_html(item.get("implementation_difficulty", "Medium"))}</td>
            </tr>
            """
        )
        explanation = item.get("score_explanation", {})
        score_explanations.append(
            f"""
            <div class="card compact">
                <h4>{_html(item.get("bottleneck_name", "Workflow bottleneck"))}</h4>
                <ul>
                    <li>{_html(explanation.get("repetition_reason", "Not available."))}</li>
                    <li>{_html(explanation.get("manual_effort_reason", "Not available."))}</li>
                    <li>{_html(explanation.get("error_risk_reason", "Not available."))}</li>
                    <li>{_html(explanation.get("response_delay_reason", "Not available."))}</li>
                    <li>{_html(explanation.get("automation_fit_reason", "Not available."))}</li>
                </ul>
            </div>
            """
        )
    if not score_rows:
        score_rows.append(
            """
            <tr>
                <td colspan="6">No automation opportunities are available to score.</td>
            </tr>
            """
        )

    roi_notes = roi_estimate.get("roi_notes", []) or [
        "No ROI notes available."
    ]

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>NextOpsAgent Workflow Diagnosis Report</title>
    <style>
        body {{
            margin: 0;
            background: #f6f7fb;
            color: #172033;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1080px;
            margin: 0 auto;
            padding: 48px 24px 72px;
        }}
        .hero {{
            background: #ffffff;
            border: 1px solid #e6e9f0;
            border-radius: 28px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
            padding: 36px;
            margin-bottom: 22px;
        }}
        h1 {{
            font-size: 42px;
            letter-spacing: -0.04em;
            line-height: 1;
            margin: 0 0 12px;
        }}
        h2 {{
            font-size: 26px;
            letter-spacing: -0.025em;
            margin: 36px 0 14px;
        }}
        h3 {{
            margin: 0 0 10px;
        }}
        h4 {{
            margin: 0 0 8px;
        }}
        .subtitle {{
            color: #667085;
            font-size: 18px;
            margin: 0;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 14px;
        }}
        .summary-card,
        .card {{
            background: #ffffff;
            border: 1px solid #e6e9f0;
            border-radius: 22px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.06);
            padding: 20px;
            margin-bottom: 14px;
        }}
        .compact {{
            box-shadow: none;
        }}
        .label {{
            color: #667085;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        .value {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-top: 6px;
        }}
        .badge {{
            display: inline-block;
            background: #f8fafc;
            border: 1px solid #e6e9f0;
            border-radius: 999px;
            color: #344054;
            font-size: 12px;
            font-weight: 700;
            margin: 2px 4px 2px 0;
            padding: 6px 9px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border: 1px solid #e6e9f0;
            border-radius: 18px;
            overflow: hidden;
        }}
        th,
        td {{
            border-bottom: 1px solid #e6e9f0;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background: #f8fafc;
            color: #344054;
            font-size: 12px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        pre {{
            background: #ffffff;
            border: 1px solid #e6e9f0;
            border-radius: 18px;
            overflow-x: auto;
            padding: 18px;
            white-space: pre-wrap;
        }}
        .note {{
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 20px;
            color: #92400e;
            padding: 18px 20px;
        }}
        .footer {{
            color: #667085;
            font-size: 13px;
            margin-top: 34px;
        }}
    </style>
</head>
<body>
    <main class="container">
        <section class="hero">
            <h1>NextOpsAgent Workflow Diagnosis Report</h1>
            <p class="subtitle">
                A local-first workflow automation diagnosis for SME operations.
            </p>
            <p>
                <span class="badge">Local-first</span>
                <span class="badge">Explainable scoring</span>
                <span class="badge">Consultant-style report</span>
            </p>
        </section>

        <section>
            <h2>Executive Summary</h2>
            <div class="grid">{summary_cards}</div>
        </section>

        <section>
            <h2>Original Workflow</h2>
            <pre>{_html(parsed_workflow.get("original_text") or "No workflow text provided.")}</pre>
        </section>

        <section>
            <h2>Detected Workflow Steps</h2>
            <div class="card">
                <ol>{_html_list(steps, "No steps detected.")}</ol>
            </div>
        </section>

        <section>
            <h2>Evidence Snippets</h2>
            <div class="card">
                <ul>{_html_list(evidence, "No evidence snippets available.")}</ul>
            </div>
        </section>

        <section>
            <h2>Bottleneck Diagnosis</h2>
            {''.join(bottleneck_cards)}
        </section>

        <section>
            <h2>Automation Opportunity Scores</h2>
            <table>
                <thead>
                    <tr>
                        <th>Bottleneck</th>
                        <th>Category</th>
                        <th>Total Score</th>
                        <th>Priority</th>
                        <th>Solution Type</th>
                        <th>Difficulty</th>
                    </tr>
                </thead>
                <tbody>{''.join(score_rows)}</tbody>
            </table>
            {''.join(score_explanations)}
        </section>

        <section>
            <h2>ROI Estimate</h2>
            <div class="grid">
                {_summary_card("Monthly Hours Saved", f"{hours_range} hours")}
                {_summary_card("Monthly Cost Saved", cost_range)}
                {_summary_card("Hourly Cost Assumption", f"AUD {roi_estimate.get('hourly_cost_aud', 30):,.2f}/hour")}
                {_summary_card("Business Size", roi_estimate.get("business_size", "small"))}
                {_summary_card("Workflow Frequency", roi_estimate.get("workflow_frequency", "weekly"))}
                {_summary_card("Confidence Level", roi_estimate.get("confidence_level", "Low"))}
            </div>
            <div class="note">
                <strong>Assumption:</strong> {_html(roi_estimate.get("assumption", "Rule-based estimate only."))}
                <ul>{_html_list(roi_notes, "No ROI notes available.")}</ul>
            </div>
        </section>

        <section>
            <h2>Implementation Roadmap</h2>
            {_roadmap_html("7-Day MVP", roadmap.get("seven_day_mvp", []))}
            {_roadmap_html("30-Day Optimization", roadmap.get("thirty_day_optimization", []))}
            {_roadmap_html("90-Day Systemization", roadmap.get("ninety_day_systemization", []))}
        </section>

        <section>
            <h2>Consultant Notes</h2>
            <div class="card">
                <ul>
                    <li>Start with high-priority, low-difficulty workflow fixes.</li>
                    <li>Avoid automating a broken process without first standardizing it.</li>
                    <li>Track before/after metrics for response time, manual hours, and lead conversion.</li>
                </ul>
            </div>
        </section>

        <section>
            <h2>Disclaimer</h2>
            <div class="note">{_html(DISCLAIMER)}</div>
        </section>

        <p class="footer">
            Generated by NextOpsAgent from fictional or user-provided workflow text.
        </p>
    </main>
</body>
</html>"""
