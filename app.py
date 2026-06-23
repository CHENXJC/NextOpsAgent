"""Streamlit product dashboard for the NextOpsAgent local MVP."""

from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

from next_ops.automation_scorer import score_automation_opportunities
from next_ops.bottleneck_detector import detect_bottlenecks
from next_ops.report_builder import build_html_report, build_markdown_report
from next_ops.roadmap_builder import build_implementation_roadmap
from next_ops.roi_estimator import estimate_roi
from next_ops.ui_helpers import (
    build_score_dataframe,
    format_list_as_badges,
    format_priority_badge,
    load_sample_workflows,
    safe_join,
)
from next_ops.workflow_parser import parse_workflow


PROJECT_ROOT = Path(__file__).parent
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample_workflows.csv"
PAGE_ICON = "🧭"

EXAMPLE_HINT = (
    "A tutoring business receives student inquiries from WeChat, records them "
    "in Excel, sends course info manually, follows up after 3 days, and "
    "prepares weekly reports."
)


st.set_page_config(
    page_title="NextOpsAgent",
    page_icon=PAGE_ICON,
    layout="wide",
)


def inject_global_css() -> None:
    """Add screenshot-friendly dashboard styling."""
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6f7fb;
            --card: #ffffff;
            --text: #172033;
            --muted: #667085;
            --border: #e6e9f0;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
            --blue: #2563eb;
            --blue-soft: #eff6ff;
            --green: #15803d;
            --green-soft: #ecfdf3;
            --amber: #b45309;
            --amber-soft: #fff7ed;
            --red: #b42318;
            --red-soft: #fef3f2;
            --gray-soft: #f8fafc;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28rem),
                radial-gradient(circle at top right, rgba(20, 184, 166, 0.08), transparent 26rem),
                var(--bg);
            color: var(--text);
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }

        .hero-card,
        .metric-card,
        .soft-card,
        .step-card,
        .roadmap-card,
        .disclaimer-box {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: var(--shadow);
        }

        .hero-card {
            padding: 2rem 2.2rem;
            margin-bottom: 1rem;
        }

        .hero-eyebrow {
            color: var(--blue);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--text);
            font-size: clamp(2.35rem, 5vw, 4.2rem);
            font-weight: 800;
            letter-spacing: -0.065em;
            line-height: 0.95;
            margin: 0 0 0.7rem;
        }

        .hero-subtitle {
            color: #344054;
            font-size: 1.25rem;
            font-weight: 650;
            margin-bottom: 0.65rem;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.02rem;
            max-width: 760px;
            margin-bottom: 1.1rem;
        }

        .metric-card {
            min-height: 124px;
            padding: 1.05rem 1.1rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--text);
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.035em;
            margin-top: 0.35rem;
        }

        .metric-caption {
            color: var(--muted);
            font-size: 0.86rem;
            margin-top: 0.2rem;
        }

        .soft-card,
        .step-card,
        .roadmap-card,
        .disclaimer-box {
            padding: 1.1rem 1.2rem;
            margin-bottom: 0.9rem;
        }

        .section-kicker {
            color: var(--blue);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }

        .section-title {
            color: var(--text);
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            margin-bottom: 0.35rem;
        }

        .section-copy,
        .muted {
            color: var(--muted);
        }

        .badge,
        .priority-badge {
            display: inline-block;
            border: 1px solid var(--border);
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            line-height: 1;
            margin: 0.18rem 0.22rem 0.18rem 0;
            padding: 0.43rem 0.62rem;
            white-space: nowrap;
        }

        .badge {
            background: var(--gray-soft);
            color: #344054;
        }

        .badge-muted,
        .priority-muted {
            background: var(--gray-soft);
            color: #667085;
        }

        .priority-high {
            background: var(--red-soft);
            border-color: #fecdca;
            color: var(--red);
        }

        .priority-medium {
            background: var(--amber-soft);
            border-color: #fedf89;
            color: var(--amber);
        }

        .priority-low {
            background: var(--blue-soft);
            border-color: #bfdbfe;
            color: var(--blue);
        }

        .severity-high {
            background: var(--red-soft);
            border-color: #fecdca;
            color: var(--red);
        }

        .severity-medium {
            background: var(--amber-soft);
            border-color: #fedf89;
            color: var(--amber);
        }

        .severity-low {
            background: var(--green-soft);
            border-color: #bbf7d0;
            color: var(--green);
        }

        .step-card {
            display: flex;
            gap: 0.85rem;
            align-items: flex-start;
        }

        .step-number {
            align-items: center;
            background: var(--blue-soft);
            border-radius: 999px;
            color: var(--blue);
            display: inline-flex;
            font-weight: 800;
            height: 2rem;
            justify-content: center;
            min-width: 2rem;
        }

        .roadmap-card.featured {
            border-color: #bfdbfe;
            box-shadow: 0 22px 56px rgba(37, 99, 235, 0.12);
        }

        .disclaimer-box {
            background: #fffbeb;
            border-color: #fde68a;
            box-shadow: none;
            color: #92400e;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 18px;
            min-height: 235px;
        }

        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {
            border-radius: 999px;
            font-weight: 750;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_samples() -> object:
    """Load bundled fictional workflow examples for the sidebar."""
    return load_sample_workflows(SAMPLE_DATA_PATH)


def analyze_workflow(
    text: str,
    business_size: str,
    hourly_cost_aud: float,
    workflow_frequency: str,
) -> dict:
    """Run the complete local diagnosis pipeline with configurable ROI inputs."""
    parsed = parse_workflow(text)
    bottlenecks = detect_bottlenecks(parsed)
    scores = score_automation_opportunities(bottlenecks)
    roi = estimate_roi(
        scores,
        business_size=business_size,
        hourly_cost_aud=hourly_cost_aud,
        workflow_frequency=workflow_frequency,
    )
    roadmap = build_implementation_roadmap(scores)
    report = build_markdown_report(parsed, bottlenecks, scores, roi, roadmap)
    html_report = build_html_report(parsed, bottlenecks, scores, roi, roadmap)
    return {
        "parsed": parsed,
        "bottlenecks": bottlenecks,
        "scores": scores,
        "roi": roi,
        "roadmap": roadmap,
        "report": report,
        "html_report": html_report,
        "generated_at": datetime.now(),
    }


def render_metric_card(label: str, value: str, caption: str = "") -> None:
    """Render one custom metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(label)}</div>
            <div class="metric-value">{escape(str(value))}</div>
            <div class="metric-caption">{escape(caption)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(kicker: str, title: str, body: str) -> None:
    """Render a lightweight explanatory card."""
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="section-kicker">{escape(kicker)}</div>
            <div class="section-title">{escape(title)}</div>
            <div class="section-copy">{escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_card(index: int, step: str) -> None:
    """Render a numbered workflow step card."""
    st.markdown(
        f"""
        <div class="step-card">
            <span class="step-number">{index}</span>
            <div>{escape(step)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_badge(severity: str) -> str:
    """Return a severity badge with a stable class name."""
    normalized = (severity or "Medium").lower()
    if normalized not in {"high", "medium", "low"}:
        normalized = "medium"
    return (
        f'<span class="badge severity-{normalized}">'
        f'{escape(severity or "Medium")} Severity</span>'
    )


def confidence_badge(confidence: str) -> str:
    """Return a neutral confidence badge."""
    return f'<span class="badge">{escape(confidence or "Medium")} Confidence</span>'


def render_roadmap_task(task: dict, featured: bool = False) -> None:
    """Render one roadmap task as a card."""
    card_class = "roadmap-card featured" if featured else "roadmap-card"
    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="section-title">{escape(task.get("task", "Roadmap task"))}</div>
            <div class="section-copy">{escape(task.get("why_it_matters", ""))}</div>
            <br>
            <span class="badge">{escape(task.get("related_bottleneck", "Workflow"))}</span>
            <span class="badge">{escape(task.get("difficulty", "Medium"))} Difficulty</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_hours_range(roi: dict) -> str:
    """Return monthly hours saved as a readable range."""
    return (
        f"{roi['estimated_monthly_hours_saved_min']}–"
        f"{roi['estimated_monthly_hours_saved_max']}"
    )


def format_cost_range(roi: dict) -> str:
    """Return monthly cost saved as a readable AUD range."""
    return (
        f"AUD {roi['estimated_monthly_cost_saved_min']:,.0f}–"
        f"{roi['estimated_monthly_cost_saved_max']:,.0f}"
    )


def get_top_score(scores: list[dict]) -> str:
    """Return the highest automation score or a placeholder."""
    if not scores:
        return "—"
    return f"{max(item.get('total_score', 0) for item in scores):.1f}/100"


def render_empty_state(message: str) -> None:
    """Render a calm empty state message."""
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="section-title">Nothing to show yet</div>
            <div class="section-copy">{escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_global_css()
samples = load_samples()

if "workflow_text" not in st.session_state:
    st.session_state.workflow_text = samples.iloc[0]["workflow_description"]


with st.sidebar:
    st.markdown("## NextOpsAgent")
    st.caption("Productized local workflow diagnosis demo")
    st.divider()

    st.markdown("**Project Stage:** NEXT-OPS-006")
    st.markdown("**Mode:** Local Demo")
    st.markdown("**Data:** Sample / user-provided text only")
    st.markdown("**API:** Not required")
    st.divider()

    st.markdown("### Analysis settings")
    business_size = st.selectbox(
        "Business size",
        ["micro", "small", "medium"],
        index=1,
        help="Used only for the directional ROI estimate.",
    )
    hourly_cost_aud = st.number_input(
        "Hourly cost assumption (AUD)",
        min_value=0.0,
        value=30.0,
        step=5.0,
        help="Approximate internal labour cost for planning.",
    )
    workflow_frequency = st.selectbox(
        "Workflow frequency",
        ["daily", "weekly", "monthly", "ad_hoc"],
        index=1,
    )
    st.divider()

    st.markdown("### Fictional sample workflow")
    selected_index = st.selectbox(
        "Choose a sample",
        list(range(len(samples))),
        format_func=lambda index: (
            f"{samples.iloc[index]['business_type']} "
            f"({samples.iloc[index]['workflow_id']})"
        ),
    )
    selected_sample = samples.iloc[selected_index]
    st.caption(f"Expected signal: {selected_sample['expected_main_bottleneck']}")
    if st.button("Use Selected Sample", type="secondary", width="stretch"):
        st.session_state.workflow_text = selected_sample["workflow_description"]
        st.session_state.pop("analysis", None)
        st.rerun()

    st.divider()
    st.markdown("### Safe demo rules")
    st.info(
        "Use fictional or anonymised workflow text. Do not enter names, contact "
        "details, credentials, private chats, or real customer records.",
        icon="🔒",
    )


analysis = st.session_state.get("analysis")
parsed = analysis["parsed"] if analysis else None
bottlenecks = analysis["bottlenecks"] if analysis else []
scores = analysis["scores"] if analysis else []
roi = analysis["roi"] if analysis else None
roadmap = analysis["roadmap"] if analysis else None


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-eyebrow">Local-first SME operations diagnosis</div>
        <div class="hero-title">NextOpsAgent</div>
        <div class="hero-subtitle">AI workflow diagnosis agent for SME operations</div>
        <div class="hero-copy">
            Turn messy business workflows into automation priorities, ROI estimates,
            and implementation roadmaps.
        </div>
        <span class="badge">Local-first</span>
        <span class="badge">Explainable scoring</span>
        <span class="badge">Consultant-style report</span>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    render_metric_card(
        "Workflow Complexity",
        parsed["workflow_complexity_level"] if parsed else "—",
        "Simple / Moderate / Complex",
    )
with metric_cols[1]:
    render_metric_card(
        "Bottlenecks Found",
        str(len(bottlenecks)) if analysis else "—",
        "Detected operational constraints",
    )
with metric_cols[2]:
    render_metric_card(
        "Top Priority Score",
        get_top_score(scores),
        "Highest automation fit",
    )
with metric_cols[3]:
    render_metric_card(
        "Estimated Monthly Hours Saved",
        format_hours_range(roi) if roi else "—",
        "Directional planning range",
    )


st.markdown("## Input Center")
input_col, guidance_col = st.columns([1.55, 1])
with input_col:
    workflow_text = st.text_area(
        "Describe your current business workflow",
        key="workflow_text",
        height=245,
        help=(
            "Paste a workflow description such as lead intake, customer follow-up, "
            "reporting, order processing, or admin operations."
        ),
    )
    analyze_clicked = st.button(
        "Analyze Workflow",
        type="primary",
        width="stretch",
    )

with guidance_col:
    render_info_card(
        "Example",
        "What to paste",
        EXAMPLE_HINT,
    )
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>Local demo boundary:</strong> This app uses rule-based local
            analysis only. It does not call OpenAI, scrape websites, or store
            private customer records.
        </div>
        """,
        unsafe_allow_html=True,
    )


if analyze_clicked:
    if len(workflow_text.strip()) < 30:
        st.warning("Please add more workflow detail before running the diagnosis.")
    else:
        with st.spinner("Diagnosing workflow signals, bottlenecks, ROI, and roadmap..."):
            st.session_state.analysis = analyze_workflow(
                workflow_text,
                business_size,
                hourly_cost_aud,
                workflow_frequency,
            )
        st.rerun()


analysis = st.session_state.get("analysis")
parsed = analysis["parsed"] if analysis else None
bottlenecks = analysis["bottlenecks"] if analysis else []
scores = analysis["scores"] if analysis else []
roi = analysis["roi"] if analysis else None
roadmap = analysis["roadmap"] if analysis else None

overview_tab, diagnosis_tab, score_tab, roadmap_tab, report_tab = st.tabs(
    ["Overview", "Diagnosis", "Scores & ROI", "Roadmap", "Report"]
)


with overview_tab:
    st.markdown("### Overview")
    st.caption("Understand what the agent saw before reading the detailed diagnosis.")

    about_cols = st.columns(3)
    with about_cols[0]:
        render_info_card(
            "What this agent does",
            "Workflow diagnosis",
            "Finds repeated work, manual handoffs, response delays, fragmented records, and reporting effort.",
        )
    with about_cols[1]:
        render_info_card(
            "Who it is for",
            "Small business teams",
            "Designed for tutoring, clinics, agencies, ecommerce, real estate, and other SME operations.",
        )
    with about_cols[2]:
        render_info_card(
            "What it outputs",
            "Prioritized action plan",
            "Produces explainable scores, ROI estimates, staged roadmap tasks, and a Markdown report.",
        )

    st.markdown("### Workflow Summary")
    if parsed:
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.markdown(
                f"""
                <div class="soft-card">
                    <div class="section-kicker">Detected profile</div>
                    <div class="section-title">{escape(parsed["detected_business_type"])}</div>
                    <p class="muted">Complexity: {escape(parsed["workflow_complexity_level"])}</p>
                    <p><strong>Channels</strong><br>{format_list_as_badges(parsed["detected_channels"])}</p>
                    <p><strong>Tools</strong><br>{format_list_as_badges(parsed["detected_tools"])}</p>
                    <p><strong>Frequency terms</strong><br>{format_list_as_badges(parsed["detected_frequency_terms"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with summary_cols[1]:
            st.markdown("#### Evidence snippets preview")
            for snippet in parsed["evidence_snippets"][:3]:
                st.info(snippet)
    else:
        render_empty_state("Run a workflow diagnosis to see summary.")


with diagnosis_tab:
    st.markdown("### Diagnosis")
    st.caption("Review detected workflow steps and the operational bottlenecks behind the score.")

    st.markdown("#### Detected Workflow Steps")
    if parsed and parsed["detected_steps"]:
        for index, step in enumerate(parsed["detected_steps"], 1):
            render_step_card(index, step)
    else:
        render_empty_state("Detected steps will appear after analysis.")

    st.markdown("#### Bottleneck Diagnosis")
    if bottlenecks:
        for index, item in enumerate(bottlenecks):
            with st.expander(
                f"{item['bottleneck_name']} · {item['category']}",
                expanded=index == 0,
            ):
                st.markdown(
                    f"""
                    {severity_badge(item.get("severity", "Medium"))}
                    {confidence_badge(item.get("confidence", "Medium"))}
                    <span class="badge">{escape(item.get("category", "Workflow"))}</span>
                    """,
                    unsafe_allow_html=True,
                )
                st.write(item["description"])
                st.markdown(f"**Evidence:** {item['evidence']}")
                st.markdown(f"**Impact:** {item['impact']}")
                st.markdown(f"**Suggested fix:** {item['suggested_fix']}")
                st.markdown(f"**Automation pattern:** {item['automation_pattern']}")
    elif analysis:
        st.info(
            "No major bottlenecks detected. Consider adding more operational details."
        )
    else:
        render_empty_state("Bottleneck cards will appear after analysis.")


with score_tab:
    st.markdown("### Scores & ROI")
    st.caption("Prioritize automation opportunities with explainable scoring and directional savings.")

    st.markdown("#### Automation Scores")
    if scores:
        score_table = build_score_dataframe(scores)
        st.dataframe(score_table, hide_index=True, width="stretch")

        st.markdown("#### Priority guide")
        guide_cols = st.columns(4)
        priority_guides = [
            ("High Priority", "Strong fit for early automation planning."),
            ("Medium Priority", "Useful candidate after the first pilot."),
            ("Low Priority", "Document or simplify before automating."),
            ("Not Recommended", "Do not automate until the workflow is clearer."),
        ]
        for column, (priority, explanation) in zip(guide_cols, priority_guides):
            with column:
                st.markdown(
                    f"""
                    <div class="soft-card">
                        {format_priority_badge(priority)}
                        <div class="muted">{escape(explanation)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("#### Score Explanation")
        for item in scores:
            with st.expander(
                f"{item['bottleneck_name']} · {item['total_score']}/100 · {item['priority_level']}"
            ):
                explanation = item.get("score_explanation", {})
                st.markdown(f"- {explanation.get('repetition_reason', '')}")
                st.markdown(f"- {explanation.get('manual_effort_reason', '')}")
                st.markdown(f"- {explanation.get('error_risk_reason', '')}")
                st.markdown(f"- {explanation.get('response_delay_reason', '')}")
                st.markdown(f"- {explanation.get('automation_fit_reason', '')}")
    else:
        render_empty_state("Automation scores will appear after analysis.")

    st.markdown("#### ROI Estimate")
    if roi:
        roi_cols = st.columns(3)
        with roi_cols[0]:
            render_metric_card("Monthly Hours Saved", format_hours_range(roi), "Low–high range")
        with roi_cols[1]:
            render_metric_card("Monthly Cost Saved AUD", format_cost_range(roi), "Labour-cost estimate")
        with roi_cols[2]:
            render_metric_card("Confidence Level", roi["confidence_level"], "Evidence quality")

        detail_cols = st.columns(3)
        with detail_cols[0]:
            render_metric_card("Hourly Cost Assumption", f"AUD {roi['hourly_cost_aud']:,.0f}", "Editable in sidebar")
        with detail_cols[1]:
            render_metric_card("Business Size", roi["business_size"], "ROI multiplier")
        with detail_cols[2]:
            render_metric_card("Workflow Frequency", roi["workflow_frequency"], "ROI multiplier")

        st.markdown(
            f"""
            <div class="disclaimer-box">
                <strong>ROI notes:</strong> {escape(roi["assumption"])}
                <ul>
                    {"".join(f"<li>{escape(note)}</li>" for note in roi["roi_notes"])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        render_empty_state("ROI estimate cards will appear after analysis.")


with roadmap_tab:
    st.markdown("### Roadmap")
    st.caption("Turn the highest-scoring opportunities into a staged implementation plan.")

    if roadmap:
        st.markdown("#### 7-Day MVP")
        st.caption("Start here. Keep the first pilot small, visible, and measurable.")
        for task in roadmap["seven_day_mvp"]:
            render_roadmap_task(task, featured=True)

        roadmap_cols = st.columns(2)
        with roadmap_cols[0]:
            st.markdown("#### 30-Day Optimization")
            for task in roadmap["thirty_day_optimization"]:
                render_roadmap_task(task)
        with roadmap_cols[1]:
            st.markdown("#### 90-Day Systemization")
            for task in roadmap["ninety_day_systemization"]:
                render_roadmap_task(task)
    else:
        render_empty_state("Roadmap tasks will appear after analysis.")


with report_tab:
    st.markdown("### Report")
    st.caption("Preview Markdown and download Markdown or HTML diagnosis reports.")

    if analysis:
        generated_at = analysis["generated_at"].strftime("%Y-%m-%d %H:%M:%S")
        file_timestamp = analysis["generated_at"].strftime("%Y%m%d_%H%M%S")
        html_report = analysis.get("html_report") or build_html_report(
            parsed, bottlenecks, scores, roi, roadmap
        )
        st.markdown(f"Report generated: `{generated_at}`")
        st.download_button(
            "Download Markdown Report",
            data=analysis["report"],
            file_name=f"nextops_workflow_report_{file_timestamp}.md",
            mime="text/markdown",
            width="stretch",
        )
        st.download_button(
            "Download HTML Report",
            data=html_report,
            file_name=f"nextops_workflow_report_{file_timestamp}.html",
            mime="text/html",
            width="stretch",
        )
        st.markdown("#### Markdown report preview")
        st.markdown(analysis["report"])
    else:
        render_empty_state("Run an analysis to preview and download the report.")
