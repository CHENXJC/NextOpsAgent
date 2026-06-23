"""Detect explainable SME workflow bottlenecks from parsed local text."""


def _first_evidence(parsed_workflow: dict, terms: list[str]) -> str:
    """Return the first evidence snippet containing a relevant term."""
    snippets = parsed_workflow.get("evidence_snippets", []) or []
    for snippet in snippets:
        if any(term.lower() in snippet.lower() for term in terms):
            return snippet
    return (parsed_workflow.get("cleaned_text") or "No evidence available.")[:160]


def _confidence(signal_count: int, explicit_phrase: bool = False) -> str:
    if explicit_phrase or signal_count >= 2:
        return "High"
    if signal_count == 1:
        return "Medium"
    return "Low"


def _add_bottleneck(
    results: list[dict],
    parsed_workflow: dict,
    *,
    name: str,
    description: str,
    category: str,
    severity: str,
    terms: list[str],
    impact: str,
    suggested_fix: str,
    automation_pattern: str,
    signal_count: int,
    explicit_phrase: bool = False,
) -> None:
    """Append one consistently structured bottleneck record."""
    results.append(
        {
            "bottleneck_name": name,
            "description": description,
            "category": category,
            "severity": severity,
            "evidence": _first_evidence(parsed_workflow, terms),
            "impact": impact,
            "suggested_fix": suggested_fix,
            "automation_pattern": automation_pattern,
            "confidence": _confidence(signal_count, explicit_phrase),
        }
    )


def detect_bottlenecks(parsed_workflow: dict) -> list[dict]:
    """Return detailed bottlenecks supported by parsed workflow evidence."""
    text = str(
        parsed_workflow.get("cleaned_text")
        or parsed_workflow.get("original_text", "")
    ).lower()
    tools = {item.lower() for item in parsed_workflow.get("detected_tools", [])}
    channels = {
        item.lower() for item in parsed_workflow.get("detected_channels", [])
    }
    pain = {
        item.lower() for item in parsed_workflow.get("detected_pain_keywords", [])
    }
    results: list[dict] = []

    table_tools = {"excel", "spreadsheet", "google sheets"}
    manual_signals = pain.intersection({"manually", "manual", "copy", "paste"})
    if tools.intersection(table_tools) and manual_signals:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Manual Data Entry",
            description="Staff repeatedly transfer operational information into spreadsheets by hand.",
            category="Data Entry",
            severity="High",
            terms=["manual", "copy", "paste", "excel", "spreadsheet"],
            impact="May create duplicated work and increase data-entry error risk.",
            suggested_fix="Capture required fields once and write them to a structured shared record.",
            automation_pattern="Structured intake form",
            signal_count=len(manual_signals) + len(tools.intersection(table_tools)),
        )

    follow_up_terms = ["follow-up", "follow up", "after 3 days", "跟进", "三天后"]
    follow_up_matches = [term for term in follow_up_terms if term in text]
    if follow_up_matches:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Manual Follow-up",
            description="Follow-up timing depends on staff memory and repeated manual actions.",
            category="Customer Follow-up",
            severity="High",
            terms=follow_up_terms,
            impact="May delay customer response and reduce conversion rate.",
            suggested_fix="Assign an owner, next-action date, and reminder rule to each active lead.",
            automation_pattern="Automated follow-up reminder",
            signal_count=len(follow_up_matches),
            explicit_phrase="after 3 days" in text,
        )

    reporting_terms = ["weekly report", "weekly summary", "monthly report", "report", "summary", "周报", "报告"]
    reporting_matches = [term for term in reporting_terms if term in text]
    if reporting_matches:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Manual Reporting",
            description="Recurring reports require manual collection, checking, and formatting.",
            category="Reporting",
            severity="Medium",
            terms=reporting_terms,
            impact="May make weekly reporting slow and inconsistent.",
            suggested_fix="Standardize metric fields and generate the recurring summary from source data.",
            automation_pattern="Weekly report generator",
            signal_count=len(reporting_matches),
            explicit_phrase="weekly report" in text or "weekly summary" in text,
        )

    messaging_channels = channels.intersection({"wechat", "whatsapp", "email"})
    explicit_no_crm = any(
        phrase in text
        for phrase in ["no crm", "without crm", "do not use a crm", "没有crm", "没有 crm"]
    )
    has_crm = ("crm" in tools or "crm" in text) and not explicit_no_crm
    if messaging_channels and not has_crm:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Scattered Customer Information",
            description="Customer context is distributed across messaging and email channels without a shared CRM record.",
            category="Information Management",
            severity="High" if len(messaging_channels) >= 2 else "Medium",
            terms=[*messaging_channels, "scattered", "chat records"],
            impact="May hide customer history, weaken handovers, and create inconsistent service.",
            suggested_fix="Create one customer record with channel, status, owner, and last-contact fields.",
            automation_pattern="Centralized customer database",
            signal_count=len(messaging_channels),
        )

    lead_terms = ["inquiry", "inquiries", "enquiry", "enquiries", "lead", "customer", "咨询", "线索", "客户"]
    lead_matches = [term for term in lead_terms if term in text]
    explicit_no_tracking = any(
        phrase in text
        for phrase in [
            "no tracking",
            "no structured lead tracking",
            "no crm or structured lead tracking",
            "not tracked",
            "without tracking",
            "没有跟踪",
            "没有记录",
        ]
    )
    structured_tracking = has_crm or (
        "tracking" in text and not explicit_no_tracking
    )
    if lead_matches and not structured_tracking:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="No Structured Lead Tracking",
            description="Leads or enquiries have no consistent owner, status, next action, or shared history.",
            category="Lead Tracking",
            severity="High",
            terms=[*lead_terms, "no tracking", "missed leads"],
            impact="May cause missed leads, inconsistent follow-up, and lower conversion visibility.",
            suggested_fix="Introduce a lightweight lead tracker with required ownership and status fields.",
            automation_pattern="CRM-lite lead tracker",
            signal_count=len(lead_matches) + int(explicit_no_tracking),
            explicit_phrase=explicit_no_tracking,
        )

    delay_terms = ["one by one", "customer waiting", "customers wait", "wait days", "delayed", "delay", "逐个", "客户等待", "延迟"]
    delay_matches = [term for term in delay_terms if term in text]
    if delay_matches:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Delayed Customer Response",
            description="Customers or leads wait for acknowledgement or the next workflow action.",
            category="Customer Response",
            severity="High",
            terms=delay_terms,
            impact="May reduce customer trust, conversion rate, and service consistency.",
            suggested_fix="Use approved response templates, acknowledgements, and overdue alerts.",
            automation_pattern="Response template assistant",
            signal_count=len(delay_matches),
        )

    copy_terms = ["copy-paste", "copy paste", "copy and paste", "repeated", "repeatedly", "duplicate work", "duplicate entries", "复制粘贴", "重复"]
    copy_matches = [term for term in copy_terms if term in text]
    if copy_matches:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Repeated Copy-Paste Work",
            description="The same information is repeatedly copied between files, tools, or messages.",
            category="Quality Control",
            severity="Medium",
            terms=copy_terms,
            impact="May create duplicated work, inconsistent records, and avoidable mistakes.",
            suggested_fix="Standardize source fields and generate repeated outputs from approved templates.",
            automation_pattern="SOP checklist automation",
            signal_count=len(copy_matches),
        )

    error_terms = ["mistake", "error-prone", "human error", "wrong data", "missed order", "错误", "容易出错", "漏单"]
    error_matches = [term for term in error_terms if term in text]
    if error_matches:
        _add_bottleneck(
            results,
            parsed_workflow,
            name="Error-Prone Workflow",
            description="Manual handoffs and inconsistent records create avoidable quality failures.",
            category="Quality Control",
            severity="High",
            terms=error_terms,
            impact="May increase rework, customer complaints, and operational risk.",
            suggested_fix="Add validation, ownership, exception handling, and a documented checklist.",
            automation_pattern="SOP checklist automation",
            signal_count=len(error_matches),
        )

    return results
