from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ATSEvent(BaseModel):
    """
    Pydantic model representing an ATS event.
    """
    candidate_id: str
    source: str
    stage: str
    outcome: str
    timestamp: datetime

class Goal(BaseModel):
    """
    Pydantic model representing a Goal.
    """
    id: str
    description: str
    status: str  # e.g., "pending", "in_progress", "resolved"
    last_updated: Optional[datetime] = None

class PredictionOutput(BaseModel):
    """
    Pydantic model representing prediction output from models.
    """
    model_name: str
    prediction: dict
    confidence: Optional[float] = None

class SessionRecord(BaseModel):
    """
    Pydantic model representing a session record.
    """
    start_time: datetime
    duration: int
    files_touched: List[str]
    active_modules: List[str]
