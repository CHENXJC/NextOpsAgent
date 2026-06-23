from next_ops.automation_scorer import score_automation_opportunities


def test_score_automation_opportunities_returns_total_score():
    bottlenecks = [
        {
            "bottleneck_name": "Manual follow-up",
            "category": "Customer Follow-up",
            "severity": "High",
            "description": "Follow-up is manual.",
            "evidence": "Staff manually follow up.",
            "suggested_fix": "Add reminders.",
            "automation_pattern": "Automated follow-up reminder",
            "impact": "May delay conversion.",
            "confidence": "High",
        }
    ]
    results = score_automation_opportunities(bottlenecks)
    assert "total_score" in results[0]
    assert 0 <= results[0]["total_score"] <= 100
    assert results[0]["priority_level"] in {
        "High Priority",
        "Medium Priority",
        "Low Priority",
        "Not Recommended",
    }
    assert results[0]["score_explanation"]["repetition_reason"]
    assert results[0]["implementation_difficulty"] == "Easy"
    assert results[0]["recommended_solution_type"] == "Reminder Automation"
