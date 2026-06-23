"""Build a structured staged implementation roadmap for an SME."""


SEVEN_DAY_TASKS = {
    "Form + Spreadsheet Automation": "Create a structured intake form with required fields and one destination table.",
    "CRM-lite Workflow": "Create a CRM-lite lead tracker with status, owner, and next-action date.",
    "Reminder Automation": "Configure follow-up reminders and an overdue-task view.",
    "Reporting Automation": "Define a basic weekly report template and its source fields.",
    "Customer Response Assistant": "Approve five response templates for the most common enquiries.",
    "SOP Automation": "Turn the current handoff into a short checklist with exception notes.",
    "Data Centralization": "Define one shared customer record and migrate a small fictional pilot set.",
}


def _task(
    task: str,
    why_it_matters: str,
    related_bottleneck: str,
    difficulty: str,
) -> dict:
    """Return one consistently structured roadmap task."""
    return {
        "task": task,
        "why_it_matters": why_it_matters,
        "related_bottleneck": related_bottleneck,
        "difficulty": difficulty,
    }


def _ranked(opportunities: list[dict]) -> list[dict]:
    priority_order = {
        "High Priority": 0,
        "Medium Priority": 1,
        "Low Priority": 2,
        "Not Recommended": 3,
    }
    return sorted(
        opportunities,
        key=lambda item: (
            priority_order.get(item.get("priority_level"), 4),
            -float(item.get("total_score", 0)),
        ),
    )


def _generic_roadmap() -> dict:
    return {
        "seven_day_mvp": [
            _task(
                "Document one repeated workflow and measure its current cycle time.",
                "A baseline is required before choosing a useful automation target.",
                "No detected bottleneck",
                "Easy",
            )
        ],
        "thirty_day_optimization": [
            _task(
                "Standardize the workflow, owner, inputs, outputs, and exception path.",
                "Automation should follow a stable process rather than hide unclear work.",
                "No detected bottleneck",
                "Medium",
            )
        ],
        "ninety_day_systemization": [
            _task(
                "Review workflow evidence again and select a measurable pilot.",
                "More operational detail can improve diagnosis confidence.",
                "No detected bottleneck",
                "Medium",
            )
        ],
    }


def build_implementation_roadmap(scored_opportunities: list[dict]) -> dict:
    """Return prioritized 7-, 30-, and 90-day roadmap task dictionaries."""
    ranked = [
        item
        for item in _ranked(scored_opportunities)
        if item.get("priority_level") != "Not Recommended"
    ]
    if not ranked:
        return _generic_roadmap()

    seven_day = []
    for opportunity in ranked[:4]:
        solution = opportunity.get("recommended_solution_type", "SOP Automation")
        seven_day.append(
            _task(
                SEVEN_DAY_TASKS.get(
                    solution,
                    "Standardize the highest-priority workflow and define a small pilot.",
                ),
                "A small visible improvement creates evidence before broader investment.",
                opportunity.get("bottleneck_name", "Top opportunity"),
                opportunity.get("implementation_difficulty", "Medium"),
            )
        )

    primary = ranked[0].get("bottleneck_name", "Top opportunity")
    thirty_day = [
        _task(
            "Build a lightweight dashboard for volume, owner, status, and overdue work.",
            "Shared visibility reduces manual status chasing and supports measurement.",
            primary,
            "Medium",
        ),
        _task(
            "Create approved response templates and a human-review rule for exceptions.",
            "Templates improve response consistency without removing human judgment.",
            primary,
            "Medium",
        ),
        _task(
            "Document the SOP and automate the weekly summary from structured fields.",
            "A documented process and recurring report make the pilot repeatable.",
            primary,
            "Medium",
        ),
    ]
    ninety_day = [
        _task(
            "Connect successful pilot steps into a CRM-lite workflow and knowledge base.",
            "Systemization preserves customer context and reusable operating knowledge.",
            primary,
            "Hard",
        ),
        _task(
            "Define role ownership, access, exception handling, and fallback procedures.",
            "Clear accountability keeps automation safe when unusual cases occur.",
            "Cross-workflow governance",
            "Medium",
        ),
        _task(
            "Monitor response time, manual hours, error rate, and lead conversion KPIs.",
            "KPI monitoring shows whether automation is creating real operational value.",
            "Cross-workflow measurement",
            "Medium",
        ),
    ]
    return {
        "seven_day_mvp": seven_day,
        "thirty_day_optimization": thirty_day,
        "ninety_day_systemization": ninety_day,
    }
