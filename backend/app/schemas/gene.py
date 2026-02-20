"""Pydantic schemas for Gene model."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class GeneBase(BaseModel):
    """Base schema for Gene."""
    name: str = Field(..., min_length=1, max_length=100, description="Unique gene name")
    description: Optional[str] = Field(None, description="Gene description")
    implementation: Optional[str] = Field(None, description="Code implementation")
    prompt_template: Optional[str] = Field(None, description="Prompt template for LLM")
    status: str = Field(
        default="draft",
        pattern="^(draft|validated|deprecated)$",
        description="Gene lifecycle status",
    )
    success_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Success rate from 0.0 to 1.0",
    )
    context_tags: List[str] = Field(
        default_factory=list,
        description="Tags for context matching",
    )


class GeneCreate(GeneBase):
    """Schema for creating a Gene."""
    pass


class GeneUpdate(BaseModel):
    """Schema for updating a Gene."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    implementation: Optional[str] = None
    prompt_template: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|validated|deprecated)$")
    success_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    context_tags: Optional[List[str]] = None


class Gene(GeneBase):
    """Schema for reading a Gene."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique gene identifier")
    created_at: datetime
    updated_at: datetime
