"""Capsule CRUD API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import Capsule, Gene
from app.schemas import Capsule as CapsuleSchema
from app.schemas import CapsuleCreate, CapsuleUpdate

router = APIRouter()

# Type alias for database session dependency
DBSession = Annotated[AsyncSession, Depends(get_session)]


def _capsule_to_schema(capsule: Capsule) -> CapsuleSchema:
    """Convert Capsule model to schema with gene_ids."""
    return CapsuleSchema(
        id=capsule.id,
        name=capsule.name,
        description=capsule.description,
        input_schema=capsule.input_schema,
        output_schema=capsule.output_schema,
        execution_time_ms=capsule.execution_time_ms,
        created_at=capsule.created_at,
        updated_at=capsule.updated_at,
        gene_ids=[g.id for g in capsule.genes],
    )


@router.get("", response_model=list[CapsuleSchema])
async def list_capsules(
    db: DBSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """List all capsules with pagination."""
    query = (
        select(Capsule)
        .options(selectinload(Capsule.genes))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    capsules = list(result.scalars().all())
    return [_capsule_to_schema(c) for c in capsules]


@router.post("", response_model=CapsuleSchema, status_code=201)
async def create_capsule(
    db: DBSession,
    capsule: CapsuleCreate,
):
    """Create a new capsule."""
    # Check for duplicate name
    existing = await db.execute(
        select(Capsule).where(Capsule.name == capsule.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Capsule with this name already exists")

    # Get genes if provided
    genes = []
    if capsule.gene_ids:
        result = await db.execute(
            select(Gene).where(Gene.id.in_(capsule.gene_ids))
        )
        genes = list(result.scalars().all())

    # Store gene IDs before committing (to avoid lazy load issues)
    gene_ids = [g.id for g in genes]

    # Create capsule
    db_capsule = Capsule(
        id=str(uuid.uuid4()),
        name=capsule.name,
        description=capsule.description,
        input_schema=capsule.input_schema,
        output_schema=capsule.output_schema,
        execution_time_ms=capsule.execution_time_ms,
        genes=genes,
    )
    db.add(db_capsule)
    await db.commit()
    await db.refresh(db_capsule)

    # Return using stored gene_ids
    return CapsuleSchema(
        id=db_capsule.id,
        name=db_capsule.name,
        description=db_capsule.description,
        input_schema=db_capsule.input_schema,
        output_schema=db_capsule.output_schema,
        execution_time_ms=db_capsule.execution_time_ms,
        created_at=db_capsule.created_at,
        updated_at=db_capsule.updated_at,
        gene_ids=gene_ids,
    )


@router.get("/{capsule_id}", response_model=CapsuleSchema)
async def get_capsule(
    db: DBSession,
    capsule_id: str,
):
    """Get a capsule by ID."""
    result = await db.execute(
        select(Capsule)
        .options(selectinload(Capsule.genes))
        .where(Capsule.id == capsule_id)
    )
    capsule = result.scalar_one_or_none()

    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")

    return _capsule_to_schema(capsule)


@router.put("/{capsule_id}", response_model=CapsuleSchema)
async def update_capsule(
    db: DBSession,
    capsule_id: str,
    capsule_update: CapsuleUpdate,
):
    """Update a capsule."""
    result = await db.execute(
        select(Capsule)
        .options(selectinload(Capsule.genes))
        .where(Capsule.id == capsule_id)
    )
    capsule = result.scalar_one_or_none()

    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")

    # Update provided fields
    update_data = capsule_update.model_dump(exclude_unset=True)

    # Handle gene_ids separately
    gene_ids = update_data.pop("gene_ids", None)
    for field, value in update_data.items():
        setattr(capsule, field, value)

    # Update genes if provided
    if gene_ids is not None:
        result = await db.execute(
            select(Gene).where(Gene.id.in_(gene_ids))
        )
        capsule.genes = list(result.scalars().all())

    await db.commit()
    await db.refresh(capsule)

    return _capsule_to_schema(capsule)


@router.delete("/{capsule_id}", status_code=204)
async def delete_capsule(
    db: DBSession,
    capsule_id: str,
):
    """Delete a capsule."""
    result = await db.execute(
        select(Capsule).where(Capsule.id == capsule_id)
    )
    capsule = result.scalar_one_or_none()

    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")

    await db.delete(capsule)
    await db.commit()
    return None
