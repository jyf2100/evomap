"""Event API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Event
from app.schemas import Event as EventSchema
from app.schemas import EventCreate

router = APIRouter()

# Type alias for database session dependency
DBSession = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[EventSchema])
async def list_events(
    db: DBSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    event_type: str | None = None,
    capsule_id: str | None = None,
):
    """List all events with optional filtering and pagination."""
    query = select(Event).offset(skip).limit(limit)

    if event_type:
        query = query.where(Event.event_type == event_type)
    if capsule_id:
        query = query.where(Event.capsule_id == capsule_id)

    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=EventSchema, status_code=201)
async def create_event(
    db: DBSession,
    event: EventCreate,
):
    """Create a new event.

    Events are immutable - once created, they cannot be modified.
    """
    db_event = Event(
        id=str(uuid.uuid4()),
        **event.model_dump(),
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.get("/{event_id}", response_model=EventSchema)
async def get_event(
    db: DBSession,
    event_id: str,
):
    """Get an event by ID."""
    result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
