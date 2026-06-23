from next_ops.workflow_parser import parse_workflow


def test_parse_workflow_returns_expected_structure():
    result = parse_workflow(
        "A tutoring business receives leads by WeChat and email. Staff copy details into Excel."
    )
    assert isinstance(result, dict)
    assert result["detected_steps"]
    assert "WeChat" in result["detected_channels"]
    assert "Excel" in result["detected_tools"]
    assert result["detected_business_type"] == "Tutoring"
    assert result["evidence_snippets"]
    assert result["workflow_complexity_level"] in {"Simple", "Moderate", "Complex"}
    assert result["cleaned_text"]


def test_parse_workflow_uses_safe_fallbacks():
    result = parse_workflow("A team completes a general internal task.")
    assert result["detected_business_type"] == "General SME"
    assert result["detected_channels"] == []


def test_parse_workflow_extracts_evidence_frequency_and_complexity():
    text = (
        "Daily staff manually copy every inquiry into Excel. Then they send email. "
        "Then they follow up one by one. Then customers wait. Then the owner prepares "
        "a weekly report. Then duplicate work is checked monthly."
    )
    result = parse_workflow(text)
    assert "daily" in result["detected_frequency_terms"]
    assert "weekly" in result["detected_frequency_terms"]
    assert "one by one" in result["detected_pain_keywords"]
    assert all(len(snippet) <= 160 for snippet in result["evidence_snippets"])
    assert result["workflow_complexity_level"] == "Complex"
