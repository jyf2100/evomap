"""Pydantic schemas for Event model."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# Valid event types based on GEP protocol
EVENT_TYPES = ["mutation", "repair", "validation", "creation", "deprecation", "execution"]


class EventBase(BaseModel):
    """Base schema for Event."""
    event_type: str = Field(
        ...,
        description="Type of event (mutation, repair, validation, etc.)",
    )
    description: Optional[str] = Field(None, description="Event description")
    payload: Optional[Dict[str, Any]] = Field(
        None,
        description="Event-specific data payload",
    )


class EventCreate(EventBase):
    """Schema for creating an Event."""
    capsule_id: Optional[str] = Field(None, description="Associated capsule ID")


class Event(EventBase):
    """Schema for reading an Event."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique event identifier")
    capsule_id: Optional[str] = Field(None, description="Associated capsule ID")
    created_at: datetime
