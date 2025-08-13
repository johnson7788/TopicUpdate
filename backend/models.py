from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Time, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    keywords = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Settings as individual columns for easier querying if needed
    frequency = Column(String, default="weekly")
    custom_date_range = Column(String, nullable=True)
    detection_time = Column(Time, nullable=True)
    notification_channels = Column(JSON, default=["email"])

    # PPT Settings
    template = Column(String, default="default")

    updates = relationship("UpdateRecord", back_populates="topic")

class UpdateRecord(Base):
    __tablename__ = "update_records"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    ppt_preview_link = Column(String, nullable=True)

    topic = relationship("Topic", back_populates="updates")

class Literature(Base):
    __tablename__ = "literature"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), index=True)
    title = Column(String)
    authors = Column(JSON)
    publication_date = Column(DateTime)
    journal_name = Column(String)
    keywords = Column(JSON)
    summary = Column(Text)
    literature_type = Column(String)

    topic = relationship("Topic")

class PPTPushRecord(Base):
    __tablename__ = "ppt_push_records"

    id = Column(Integer, primary_key=True, index=True)
    push_time = Column(DateTime)
    topic_name = Column(String)
    ppt_filename = Column(String)
    recipients = Column(JSON)
    channel = Column(String)
    status = Column(String)

    # Relationships for diffs
    diff_from = relationship("PPTDiff", foreign_keys="[PPTDiff.current_record_id]", back_populates="current_record", cascade="all, delete-orphan")
    diff_to = relationship("PPTDiff", foreign_keys="[PPTDiff.previous_record_id]", back_populates="previous_record", cascade="all, delete-orphan")


class PPTDiff(Base):
    __tablename__ = "ppt_diffs"

    id = Column(Integer, primary_key=True, index=True)
    current_record_id = Column(Integer, ForeignKey("ppt_push_records.id"), nullable=False)
    previous_record_id = Column(Integer, ForeignKey("ppt_push_records.id"), nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    current_record = relationship("PPTPushRecord", foreign_keys=[current_record_id], back_populates="diff_from")
    previous_record = relationship("PPTPushRecord", foreign_keys=[previous_record_id], back_populates="diff_to")
