from next_ops.bottleneck_detector import detect_bottlenecks
from next_ops.workflow_parser import parse_workflow


def test_detect_bottlenecks_returns_list():
    parsed = parse_workflow(
        "Staff manually copy order details into Excel and prepare a weekly report."
    )
    results = detect_bottlenecks(parsed)
    assert isinstance(results, list)
    assert results
    assert all(item["severity"] in {"Low", "Medium", "High"} for item in results)
    assert any(item["bottleneck_name"] == "Manual Reporting" for item in results)
    assert all(item["automation_pattern"] for item in results)
    assert all(item["impact"] for item in results)
    assert all(item["confidence"] in {"Low", "Medium", "High"} for item in results)


def test_no_crm_is_treated_as_missing_structure():
    parsed = parse_workflow(
        "Leads arrive through WhatsApp and email. There is no CRM or structured lead tracking."
    )
    names = {item["bottleneck_name"] for item in detect_bottlenecks(parsed)}
    assert "Scattered Customer Information" in names
    assert "No Structured Lead Tracking" in names
