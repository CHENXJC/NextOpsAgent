"""Parse an SME workflow description using transparent local rules."""

import re


CHANNEL_KEYWORDS = {
    "WeChat": ["wechat", "微信"],
    "WhatsApp": ["whatsapp"],
    "Email": ["email", "e-mail", "邮箱", "邮件"],
    "Phone": ["phone", "call", "telephone", "电话", "来电"],
}

TOOL_KEYWORDS = {
    "Excel": ["excel"],
    "Spreadsheet": ["spreadsheet", "spreadsheets", "电子表格"],
    "Google Sheets": ["google sheets", "google sheet"],
    "CRM": ["crm", "customer relationship management"],
    "Manual follow-up": ["manual follow-up", "manual follow up", "manually follow", "人工跟进", "手动跟进"],
    "Weekly report": ["weekly report", "weekly summary", "周报", "每周报告"],
}

BUSINESS_TYPE_KEYWORDS = {
    "Tutoring": ["tutoring", "tutor", "student lessons", "辅导", "家教"],
    "E-commerce": ["ecommerce", "e-commerce", "online store", "webshop", "电商", "网店"],
    "Real Estate": ["real estate", "property agency", "property agent", "房产", "房地产"],
    "Clinic": ["clinic", "patient appointment", "medical practice", "诊所", "患者"],
    "Restaurant": ["restaurant", "takeaway", "food delivery", "餐厅", "外卖"],
    "Consulting": ["consulting", "consultant", "advisory", "咨询公司", "顾问"],
    "Agency": ["agency", "client campaign", "marketing agency", "代理公司", "营销机构"],
}

PAIN_KEYWORDS = {
    "manually": ["manually"],
    "manual": ["manual", "手动", "人工"],
    "copy": ["copy", "复制"],
    "paste": ["paste", "粘贴"],
    "Excel": ["excel"],
    "spreadsheet": ["spreadsheet", "spreadsheets", "表格"],
    "delayed": ["delayed", "delay", "late reply", "延迟"],
    "follow up": ["follow up", "follow-up", "跟进"],
    "no tracking": ["no tracking", "no crm", "no structured lead tracking", "not tracked", "without tracking", "没有跟踪", "没有记录"],
    "scattered": ["scattered", "fragmented", "分散"],
    "repeated": ["repeated", "repeatedly", "重复"],
    "weekly report": ["weekly report", "weekly summary", "每周报告", "周报"],
    "customer waiting": ["customer waiting", "customers wait", "wait days", "客户等待"],
    "missed leads": ["missed leads", "lost leads", "forget leads", "漏掉线索"],
    "duplicate work": ["duplicate work", "duplicate entries", "duplicated work", "重复工作"],
    "chat records": ["chat records", "group chat", "聊天记录", "群聊"],
    "one by one": ["one by one", "逐个", "一个个"],
}

FREQUENCY_TERMS = {
    "daily": ["daily"],
    "weekly": ["weekly"],
    "monthly": ["monthly"],
    "every day": ["every day", "每天"],
    "every week": ["every week", "每周"],
    "after 3 days": ["after 3 days", "三天后"],
    "every inquiry": ["every inquiry", "每个咨询"],
    "each customer": ["each customer", "每位客户", "每个客户"],
    "one by one": ["one by one", "逐个", "一个个"],
}


def clean_workflow_text(text: str) -> str:
    """Remove repeated whitespace while preserving the original wording."""
    normalized_lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    return "\n".join(line for line in normalized_lines if line)


def _contains_keyword(text: str, keyword: str) -> bool:
    keyword_lower = keyword.lower()
    if re.search(r"[\u3400-\u9fff]", keyword_lower):
        return keyword_lower in text
    return bool(re.search(rf"\b{re.escape(keyword_lower)}\b", text))


def _detect_labels(text: str, rules: dict[str, list[str]]) -> list[str]:
    return [
        label
        for label, keywords in rules.items()
        if any(_contains_keyword(text, keyword) for keyword in keywords)
    ]


def _split_steps(text: str) -> list[str]:
    """Split sentences, commas, and common workflow connectors into steps."""
    if not text:
        return []
    split_pattern = (
        r"(?<=[.!?。！？；;])\s*|\n+|,\s*|，\s*|"
        r"\s+\b(?:and then|then|after that)\b\s+|"
        r"\s+\band\b\s+|(?=\b(?:daily|weekly)\b)"
    )
    parts = re.split(split_pattern, text, flags=re.IGNORECASE)
    steps = [part.strip(" -•\t.;；") for part in parts if part.strip(" -•\t.;；")]
    return steps or [text]


def _sentence_chunks(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?。！？;；])\s*|\n+", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _evidence_snippets(
    text: str,
    pain_keywords: list[str],
    detected_tools: list[str],
    detected_channels: list[str],
) -> list[str]:
    """Return short source snippets that support the detected workflow signals."""
    search_terms = [
        *(term.lower() for term in pain_keywords),
        *(term.lower() for term in detected_tools),
        *(term.lower() for term in detected_channels),
    ]
    snippets = []
    for chunk in _sentence_chunks(text):
        if any(term in chunk.lower() for term in search_terms):
            snippet = chunk[:160]
            if snippet not in snippets:
                snippets.append(snippet)
    if not snippets:
        snippets.append(text[:160] if text else "No workflow text provided.")
    return snippets


def _complexity_level(step_count: int) -> str:
    if step_count <= 2:
        return "Simple"
    if step_count <= 5:
        return "Moderate"
    return "Complex"


def parse_workflow(text: str) -> dict:
    """Return an evidence-rich local parse of an SME workflow description."""
    original_text = str(text or "").strip()
    cleaned_text = clean_workflow_text(original_text)
    normalized = cleaned_text.lower()
    steps = _split_steps(cleaned_text)
    channels = _detect_labels(normalized, CHANNEL_KEYWORDS)
    tools = _detect_labels(normalized, TOOL_KEYWORDS)
    business_types = _detect_labels(normalized, BUSINESS_TYPE_KEYWORDS)
    pain_keywords = _detect_labels(normalized, PAIN_KEYWORDS)
    frequency_terms = _detect_labels(normalized, FREQUENCY_TERMS)
    return {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "detected_steps": steps,
        "detected_channels": channels,
        "detected_tools": tools,
        "detected_business_type": business_types[0] if business_types else "General SME",
        "detected_pain_keywords": pain_keywords,
        "detected_frequency_terms": frequency_terms,
        "evidence_snippets": _evidence_snippets(
            cleaned_text, pain_keywords, tools, channels
        ),
        "workflow_complexity_level": _complexity_level(len(steps)),
    }
