from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String

from database import Base

class Task(Base):
    """Databse model for storing FocusForge tasks."""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    due_date = Column(String, nullable=True)
    due_date_resolved = Column(String, nullable=True)
    urgency = Column(String, nullable=False, default="normal")
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))