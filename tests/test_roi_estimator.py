from next_ops.roi_estimator import estimate_roi


def test_estimate_roi_returns_monthly_hours():
    result = estimate_roi(
        [
            {"priority_level": "High Priority"},
            {"priority_level": "Medium Priority"},
        ]
    )
    assert "estimated_monthly_hours_saved_min" in result
    assert result["estimated_monthly_hours_saved_min"] == 12
    assert result["estimated_monthly_hours_saved_max"] == 23
    assert result["estimated_monthly_cost_saved_min"] == 360


def test_estimate_roi_supports_cost_size_and_frequency_inputs():
    result = estimate_roi(
        [{"priority_level": "High Priority"}],
        business_size="micro",
        hourly_cost_aud=42.0,
        workflow_frequency="daily",
    )
    assert result["hourly_cost_aud"] == 42.0
    assert result["business_size"] == "micro"
    assert result["workflow_frequency"] == "daily"
    assert result["estimated_monthly_hours_saved_min"] == 8.4
    assert result["roi_notes"]
