"""Pydantic schemas for Capsule model."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CapsuleBase(BaseModel):
    """Base schema for Capsule."""
    name: str = Field(..., min_length=1, max_length=100, description="Unique capsule name")
    description: Optional[str] = Field(None, description="Capsule description")
    input_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON schema for input parameters",
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON schema for output data",
    )
    execution_time_ms: Optional[int] = Field(
        None,
        ge=0,
        description="Average execution time in milliseconds",
    )


class CapsuleCreate(CapsuleBase):
    """Schema for creating a Capsule."""
    gene_ids: Optional[List[str]] = Field(
        default_factory=list,
        description="List of gene IDs to associate",
    )


class CapsuleUpdate(BaseModel):
    """Schema for updating a Capsule."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[int] = Field(None, ge=0)
    gene_ids: Optional[List[str]] = None


class Capsule(CapsuleBase):
    """Schema for reading a Capsule."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique capsule identifier")
    created_at: datetime
    updated_at: datetime
    gene_ids: List[str] = Field(default_factory=list, description="Associated gene IDs")
