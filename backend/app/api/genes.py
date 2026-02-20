"""Gene CRUD API endpoints."""
import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Gene
from app.schemas import Gene as GeneSchema
from app.schemas import GeneCreate, GeneUpdate

router = APIRouter()

# Type alias for database session dependency
DBSession = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[GeneSchema])
async def list_genes(
    db: DBSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    status: Optional[str] = None,
):
    """List all genes with optional filtering and pagination."""
    query = select(Gene).offset(skip).limit(limit)

    if status:
        query = query.where(Gene.status == status)

    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=GeneSchema, status_code=201)
async def create_gene(
    db: DBSession,
    gene: GeneCreate,
):
    """Create a new gene."""
    # Check for duplicate name
    existing = await db.execute(
        select(Gene).where(Gene.name == gene.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Gene with this name already exists")

    # Create gene with UUID
    db_gene = Gene(
        id=str(uuid.uuid4()),
        **gene.model_dump(),
    )
    db.add(db_gene)
    await db.commit()
    await db.refresh(db_gene)
    return db_gene


@router.get("/{gene_id}", response_model=GeneSchema)
async def get_gene(
    db: DBSession,
    gene_id: str,
):
    """Get a gene by ID."""
    result = await db.execute(
        select(Gene).where(Gene.id == gene_id)
    )
    gene = result.scalar_one_or_none()

    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")

    return gene


@router.put("/{gene_id}", response_model=GeneSchema)
async def update_gene(
    db: DBSession,
    gene_id: str,
    gene_update: GeneUpdate,
):
    """Update a gene."""
    result = await db.execute(
        select(Gene).where(Gene.id == gene_id)
    )
    gene = result.scalar_one_or_none()

    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")

    # Update only provided fields
    update_data = gene_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(gene, field, value)

    await db.commit()
    await db.refresh(gene)
    return gene


@router.delete("/{gene_id}", status_code=204)
async def delete_gene(
    db: DBSession,
    gene_id: str,
):
    """Delete a gene."""
    result = await db.execute(
        select(Gene).where(Gene.id == gene_id)
    )
    gene = result.scalar_one_or_none()

    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")

    await db.delete(gene)
    await db.commit()
    return None
