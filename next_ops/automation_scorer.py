"""Score detected workflow bottlenecks for automation priority."""


SCORE_PROFILES = {
    "Data Entry": (90, 90, 80, 45, 92),
    "Customer Follow-up": (85, 82, 65, 90, 90),
    "Reporting": (85, 82, 65, 45, 92),
    "Customer Response": (72, 72, 60, 95, 82),
    "Lead Tracking": (82, 78, 82, 90, 86),
    "Information Management": (76, 76, 82, 68, 80),
    "Quality Control": (78, 82, 94, 55, 78),
}

WEIGHTS = {
    "repetition_score": 0.25,
    "manual_effort_score": 0.25,
    "error_risk_score": 0.20,
    "response_delay_score": 0.15,
    "automation_fit_score": 0.15,
}

SOLUTION_BY_PATTERN = {
    "Structured intake form": "Form + Spreadsheet Automation",
    "CRM-lite lead tracker": "CRM-lite Workflow",
    "Automated follow-up reminder": "Reminder Automation",
    "Weekly report generator": "Reporting Automation",
    "Response template assistant": "Customer Response Assistant",
    "SOP checklist automation": "SOP Automation",
    "Centralized customer database": "Data Centralization",
}


def _bounded(value: int) -> int:
    return max(0, min(100, value))


def _priority_level(score: float) -> str:
    if score >= 80:
        return "High Priority"
    if score >= 60:
        return "Medium Priority"
    if score >= 40:
        return "Low Priority"
    return "Not Recommended"


def _implementation_difficulty(pattern: str) -> str:
    easy_patterns = {
        "Structured intake form",
        "Automated follow-up reminder",
        "Weekly report generator",
    }
    medium_patterns = {
        "CRM-lite lead tracker",
        "Centralized customer database",
        "SOP checklist automation",
    }
    if pattern in easy_patterns:
        return "Easy"
    if pattern in medium_patterns:
        return "Medium"
    if pattern == "Response template assistant":
        return "Hard"
    return "Medium"


def _score_explanation(bottleneck: dict, scores: dict[str, int]) -> dict[str, str]:
    """Explain the five sub-scores in consultant-friendly language."""
    category = bottleneck.get("category", "the workflow")
    severity = bottleneck.get("severity", "Medium")
    return {
        "repetition_reason": (
            f"{category} work is likely to recur whenever the described workflow runs "
            f"(score {scores['repetition_score']}/100)."
        ),
        "manual_effort_reason": (
            f"The evidence indicates ongoing staff handling and handoffs "
            f"(score {scores['manual_effort_score']}/100)."
        ),
        "error_risk_reason": (
            f"A {severity.lower()}-severity bottleneck can create inconsistent or missing records "
            f"(score {scores['error_risk_score']}/100)."
        ),
        "response_delay_reason": (
            f"The category's likely effect on customer or internal cycle time produces a "
            f"{scores['response_delay_score']}/100 delay score."
        ),
        "automation_fit_reason": (
            f"The suggested pattern—{bottleneck.get('automation_pattern', 'workflow standardization')}—"
            f"can be implemented with explicit rules (score {scores['automation_fit_score']}/100)."
        ),
    }


def score_automation_opportunities(bottlenecks: list[dict]) -> list[dict]:
    """Return ranked weighted scores with reasons and solution guidance."""
    severity_adjustment = {"Low": -15, "Medium": 0, "High": 8}
    scored = []
    for bottleneck in bottlenecks:
        profile = SCORE_PROFILES.get(
            bottleneck.get("category"), (50, 50, 50, 50, 50)
        )
        adjustment = severity_adjustment.get(bottleneck.get("severity"), 0)
        values = [_bounded(value + adjustment) for value in profile]
        breakdown = dict(zip(WEIGHTS, values))
        total = round(
            sum(breakdown[name] * weight for name, weight in WEIGHTS.items()), 1
        )
        pattern = bottleneck.get("automation_pattern", "")
        scored.append(
            {
                **bottleneck,
                **breakdown,
                "total_score": total,
                "priority_level": _priority_level(total),
                "score_explanation": _score_explanation(bottleneck, breakdown),
                "recommended_solution_type": SOLUTION_BY_PATTERN.get(
                    pattern, "SOP Automation"
                ),
                "implementation_difficulty": _implementation_difficulty(pattern),
            }
        )
    return sorted(scored, key=lambda item: item["total_score"], reverse=True)
