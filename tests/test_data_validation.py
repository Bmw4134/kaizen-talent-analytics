import pytest
from pydantic import ValidationError
from kaizen_talent_analytics.data.schema import ATSEvent, Goal, PredictionOutput, SessionRecord
from datetime import datetime

def test_ats_event_valid():
    event = {
        "candidate_id": "C00001",
        "source": "LinkedIn",
        "stage": "Interview",
        "outcome": "Passed",
        "timestamp": "2024-06-26T12:00:00"
    }
    ats_event = ATSEvent(**event)
    assert ats_event.candidate_id == "C00001"

def test_ats_event_invalid_timestamp():
    event = {
        "candidate_id": "C00002",
        "source": "Referral",
        "stage": "Screened",
        "outcome": "Failed",
        "timestamp": "invalid-date"
    }
    with pytest.raises(ValidationError):
        ATSEvent(**event)

def test_goal_model():
    goal = Goal(id="G1", description="Test goal", status="pending")
    assert goal.status == "pending"

def test_prediction_output():
    pred = PredictionOutput(model_name="RetentionModel", prediction={"score": 0.8}, confidence=0.9)
    assert pred.model_name == "RetentionModel"

def test_session_record():
    session = SessionRecord(
        start_time=datetime.now(),
        duration=3600,
        files_touched=["file1.py", "file2.py"],
        active_modules=["ModuleA", "ModuleB"]
    )
    assert session.duration == 3600
