import json
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime, time

# --- Base Models ---

class TopicSettings(BaseModel):
    frequency: Literal["weekly", "monthly", "quarterly", "custom_range"] = "weekly"
    custom_date_range: Optional[str] = Field(None, description="e.g., '2025-08-11 to 2025-09-11'")
    detection_time: Optional[time] = Field(None, description="Time of day for updates, used for specific frequencies if ever needed")
    notification_channels: List[Literal["email", "app_push"]] = ["email"]

class PPTGenerationSettings(BaseModel):
    template: str = "default"

# --- Topic ---

class TopicBase(BaseModel):
    name: str
    keywords: List[str]

class TopicCreate(TopicBase):
    settings: Optional[TopicSettings] = Field(default_factory=TopicSettings)
    ppt_settings: Optional[PPTGenerationSettings] = Field(default_factory=PPTGenerationSettings)

class Topic(TopicBase):
    id: int
    created_at: datetime
    last_updated: datetime
    frequency: str
    custom_date_range: Optional[str]
    detection_time: Optional[time]
    notification_channels: List[str]
    template: str

    class Config:
        from_attributes = True


# --- Topic History ---

class UpdateRecord(BaseModel):
    timestamp: datetime
    status: Literal["success", "failed"]
    ppt_preview_link: Optional[str] = None

    class Config:
        from_attributes = True

class TopicHistory(BaseModel):
    topic_id: int
    updates: List[UpdateRecord] = []


# --- Literature ---

class Literature(BaseModel):
    id: int
    title: str
    authors: List[str]
    publication_date: datetime
    journal_name: str
    keywords: List[str]
    summary: str
    literature_type: str

    class Config:
        from_attributes = True


# --- PPT Push History ---

class PPTPushRecord(BaseModel):
    id: int
    push_time: datetime
    topic_name: str
    ppt_filename: str
    recipients: List[str]

    @validator('recipients', pre=True)
    def parse_recipients_from_json_string(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    channel: str
    status: Literal["success", "failed", "pending"]
    diff_summary: Optional[str] = None

    class Config:
        from_attributes = True

# --- Literature Analysis ---

class LiteratureAnalysisStats(BaseModel):
    total_count: int
    high_citation_count: int
    clinical_trial_count: int
    meta_analysis_count: int

class TrendDataPoint(BaseModel):
    date: str
    count: int

class DistributionDataPoint(BaseModel):
    type: str
    count: int

class LiteratureAnalysis(BaseModel):
    stats: LiteratureAnalysisStats
    trend_data: List[TrendDataPoint]
    distribution_data: List[DistributionDataPoint]
    literature: List[Literature]
