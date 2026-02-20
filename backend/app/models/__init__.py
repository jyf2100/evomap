"""SQLAlchemy models for GEP data structures."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, Integer, JSON, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


# Association table for Gene-Capsule M:N relationship
gene_capsule_association = Table(
    "gene_capsule",
    Base.metadata,
    Column("gene_id", String(36), ForeignKey("genes.id"), primary_key=True),
    Column("capsule_id", String(36), ForeignKey("capsules.id"), primary_key=True),
)


class Gene(Base):
    """Gene model - atomic capability unit.

    A Gene represents a reusable, verified code or prompt fragment
    that can be inherited and evolved across AI agents.
    """
    __tablename__ = "genes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    implementation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prompt_template: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
    )
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    context_tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    capsules: Mapped[list["Capsule"]] = relationship(
        secondary=gene_capsule_association,
        back_populates="genes",
    )


class Capsule(Base):
    """Capsule model - successful task execution path.

    A Capsule encapsulates a workflow of multiple Genes that together
    solve a specific problem or accomplish a task.
    """
    __tablename__ = "capsules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    input_schema: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    output_schema: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    execution_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    genes: Mapped[list["Gene"]] = relationship(
        secondary=gene_capsule_association,
        back_populates="capsules",
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="capsule",
        cascade="all, delete-orphan",
    )


class Event(Base):
    """Event model - immutable evolution log.

    An Event records mutations, repairs, validations, and other
    evolution-related activities for audit and lineage tracking.
    """
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    capsule_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("capsules.id"),
        nullable=True,
    )
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    capsule: Mapped[Optional["Capsule"]] = relationship(back_populates="events")
