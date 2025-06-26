import pytest
from kaizen_talent_analytics.goal_tracker import GoalTracker, Goal

def test_add_and_get_goal():
    tracker = GoalTracker()
    goal = Goal(id="test1", description="Test goal", status="pending")
    tracker.add_goal(goal)
    retrieved = tracker.get_goal("test1")
    assert retrieved == goal

def test_resolve_goal():
    tracker = GoalTracker()
    goal = Goal(id="test2", description="Another goal", status="pending")
    tracker.add_goal(goal)
    tracker.resolve_goal("test2")
    resolved_goal = tracker.get_goal("test2")
    assert resolved_goal.status == "resolved"

def test_get_nonexistent_goal():
    tracker = GoalTracker()
    assert tracker.get_goal("nonexistent") is None
