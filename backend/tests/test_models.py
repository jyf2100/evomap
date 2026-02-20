"""Test SQLAlchemy models for GEP data structures."""
import pytest
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Gene, Capsule, Event


class TestGeneModel:
    """Test Gene model."""

    def test_gene_creation(self):
        """Test Gene model creation and attributes."""
        gene = Gene(
            id="gene-test-001",
            name="shell_exec",
            description="Execute shell commands safely",
            implementation="import subprocess\nsubprocess.run(cmd, shell=False)",
            prompt_template="Execute the following command: {cmd}",
            status="validated",
            success_rate=0.95,
        )
        assert gene.id == "gene-test-001"
        assert gene.name == "shell_exec"
        assert gene.status == "validated"
        assert gene.success_rate == 0.95

    def test_gene_default_status(self):
        """Test Gene status field has database-level default.

        Note: SQLAlchemy's `default` is applied at INSERT time, not at
        object creation. This test verifies the column definition is correct.
        """
        gene = Gene(id="gene-002", name="test_gene", status="draft")
        assert gene.status == "draft"
        # Verify the column has a default defined
        from sqlalchemy import inspect
        mapper = inspect(Gene)
        status_col = mapper.columns.status
        assert status_col.default is not None
        assert status_col.default.arg == "draft"

    def test_gene_context_tags(self):
        """Test Gene context tags."""
        gene = Gene(
            id="gene-003",
            name="test",
            context_tags=["shell", "execution", "system"],
        )
        assert "shell" in gene.context_tags
        assert len(gene.context_tags) == 3


class TestCapsuleModel:
    """Test Capsule model."""

    def test_capsule_creation(self):
        """Test Capsule model creation and attributes."""
        capsule = Capsule(
            id="capsule-test-001",
            name="disk_cleanup",
            description="Clean up disk space by removing temp files",
            input_schema={"path": "string", "max_age_days": "integer"},
            output_schema={"freed_bytes": "integer", "files_removed": "integer"},
            execution_time_ms=1500,
        )
        assert capsule.id == "capsule-test-001"
        assert capsule.name == "disk_cleanup"
        assert capsule.execution_time_ms == 1500

    def test_capsule_schemas(self):
        """Test Capsule input/output schemas."""
        capsule = Capsule(
            id="capsule-002",
            name="test",
            input_schema={"input_field": "type"},
            output_schema={"output_field": "type"},
        )
        assert capsule.input_schema == {"input_field": "type"}
        assert capsule.output_schema == {"output_field": "type"}


class TestEventModel:
    """Test Event model."""

    def test_event_creation(self):
        """Test Event model creation and attributes."""
        event = Event(
            id="event-test-001",
            event_type="mutation",
            description="Gene shell_exec mutated to support timeout",
            payload={"gene_id": "gene-001", "change": "added timeout param"},
        )
        assert event.id == "event-test-001"
        assert event.event_type == "mutation"
        assert event.payload["gene_id"] == "gene-001"

    def test_event_types(self):
        """Test different event types."""
        valid_types = ["mutation", "repair", "validation", "creation", "deprecation"]
        for event_type in valid_types:
            event = Event(id=f"event-{event_type}", event_type=event_type)
            assert event.event_type == event_type


class TestRelationships:
    """Test relationships between models."""

    def test_gene_capsule_relationship(self):
        """Test M:N relationship between Gene and Capsule."""
        gene1 = Gene(id="gene-rel-001", name="gene_a", status="validated")
        gene2 = Gene(id="gene-rel-002", name="gene_b", status="validated")
        capsule = Capsule(
            id="capsule-rel-001",
            name="workflow_a",
        )
        # Set relationship
        capsule.genes = [gene1, gene2]

        assert len(capsule.genes) == 2
        assert gene1 in capsule.genes
        assert gene2 in capsule.genes

    def test_capsule_event_relationship(self):
        """Test 1:N relationship between Capsule and Event."""
        capsule = Capsule(id="capsule-event-001", name="test_capsule")
        event1 = Event(
            id="event-rel-001",
            event_type="creation",
            description="Capsule created",
        )
        event2 = Event(
            id="event-rel-002",
            event_type="validation",
            description="Capsule validated",
        )
        # Set relationship
        capsule.events = [event1, event2]

        assert len(capsule.events) == 2
        assert event1 in capsule.events
        assert event2 in capsule.events
