from next_ops.roadmap_builder import build_implementation_roadmap


def test_roadmap_builder_returns_structured_tasks():
    opportunities = [
        {
            "bottleneck_name": "Manual Follow-up",
            "priority_level": "High Priority",
            "total_score": 90,
            "recommended_solution_type": "Reminder Automation",
            "implementation_difficulty": "Easy",
        }
    ]
    roadmap = build_implementation_roadmap(opportunities)
    first_task = roadmap["seven_day_mvp"][0]
    assert isinstance(first_task, dict)
    assert set(first_task) == {
        "task",
        "why_it_matters",
        "related_bottleneck",
        "difficulty",
    }


def test_roadmap_builder_handles_no_opportunities():
    roadmap = build_implementation_roadmap([])
    assert roadmap["seven_day_mvp"][0]["task"]
