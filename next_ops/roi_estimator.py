"""Estimate directional time and labour savings for automation candidates."""


HOURS_BY_PRIORITY = {
    "High Priority": (8, 15),
    "Medium Priority": (4, 8),
    "Low Priority": (1, 4),
    "Not Recommended": (0, 1),
}

BUSINESS_SIZE_MULTIPLIERS = {
    "micro": 0.7,
    "small": 1.0,
    "medium": 1.5,
}

FREQUENCY_MULTIPLIERS = {
    "daily": 1.5,
    "weekly": 1.0,
    "monthly": 0.5,
    "ad_hoc": 0.3,
}


def estimate_roi(
    scored_opportunities: list[dict],
    business_size: str = "small",
    hourly_cost_aud: float = 30.0,
    workflow_frequency: str = "weekly",
) -> dict:
    """Return a configurable monthly time and labour-cost savings estimate."""
    normalized_size = business_size.lower()
    if normalized_size not in BUSINESS_SIZE_MULTIPLIERS:
        normalized_size = "small"
    normalized_frequency = workflow_frequency.lower()
    if normalized_frequency not in FREQUENCY_MULTIPLIERS:
        normalized_frequency = "weekly"
    hourly_cost = max(0.0, float(hourly_cost_aud))

    base_min = 0
    base_max = 0
    for opportunity in scored_opportunities:
        low, high = HOURS_BY_PRIORITY.get(
            opportunity.get("priority_level"), (0, 1)
        )
        base_min += low
        base_max += high

    multiplier = (
        BUSINESS_SIZE_MULTIPLIERS[normalized_size]
        * FREQUENCY_MULTIPLIERS[normalized_frequency]
    )
    hours_min = round(base_min * multiplier, 1)
    hours_max = round(base_max * multiplier, 1)
    cost_min = round(hours_min * hourly_cost, 2)
    cost_max = round(hours_max * hourly_cost, 2)
    confidence = "Medium" if len(scored_opportunities) >= 2 else "Low"

    return {
        "estimated_monthly_hours_saved_min": hours_min,
        "estimated_monthly_hours_saved_max": hours_max,
        "estimated_monthly_cost_saved_min": cost_min,
        "estimated_monthly_cost_saved_max": cost_max,
        "hourly_cost_aud": hourly_cost,
        "business_size": normalized_size,
        "workflow_frequency": normalized_frequency,
        "assumption": (
            f"Directional estimate using AUD {hourly_cost:,.2f}/hour, a "
            f"{normalized_size} business multiplier, and {normalized_frequency} workflow frequency."
        ),
        "confidence_level": confidence,
        "roi_notes": [
            "This estimate supports workflow planning and is not a financial promise.",
            "Actual savings depend on team adoption, implementation quality, and tool selection.",
            "Validate the estimate against measured baseline hours and a stable pilot workflow.",
        ],
    }
