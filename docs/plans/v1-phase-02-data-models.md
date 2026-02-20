# v1-phase-02: Gene/Capsule/Event Data Models

**Date**: 2026-02-20
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md
**Depends On**: v1-phase-01-scaffolding.md

---

## Overview

实现 GEP 协议的核心数据模型：Gene（基因）、Capsule（胶囊）、Event（事件）。

## GEP Data Model Reference

```
┌─────────────────────────────────────────────────────────────┐
│                     GEP Data Model                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐         ┌───────────┐         ┌───────────┐   │
│  │  Gene   │◄────────│  Capsule  │────────►│   Event   │   │
│  │         │  genes  │           │ events  │           │   │
│  └─────────┘  (M:N)  └───────────┘  (1:N)  └───────────┘   │
│       │                        │                           │
│       │   ┌────────────────────┼────────────────────┐      │
│       │   │                    │                    │      │
│       ▼   ▼                    ▼                    ▼      │
│  ┌─────────────┐         ┌───────────┐        ┌─────────┐ │
│  │ Capability  │         │  Workflow │        │   Log   │ │
│  │  (code +    │         │  (task    │        │ (audit  │ │
│  │   prompt)   │         │   path)   │        │  trail) │ │
│  └─────────────┘         └───────────┘        └─────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Gene（基因）
- 原子能力单元
- 包含：代码/提示词、成功率、上下文、版本历史
- 状态：draft → validated → deprecated

### Capsule（胶囊）
- 成功的任务执行路径
- 由多个 Gene 组成（M:N 关系）
- 包含：输入/输出、执行时间、资源消耗

### Event（事件）
- 不可变的进化日志
- 记录：变异（Innovation）、修复（Repair）、验证（Validation）
- 用于审计和追溯

---

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | Gene SQLAlchemy model created | `uv run pytest tests/test_models.py::test_gene_model -v` passes |
| 2 | Capsule SQLAlchemy model created | `uv run pytest tests/test_models.py::test_capsule_model -v` passes |
| 3 | Event SQLAlchemy model created | `uv run pytest tests/test_models.py::test_event_model -v` passes |
| 4 | Gene-Capsule M:N relationship | `uv run pytest tests/test_models.py::test_gene_capsule_relationship -v` passes |
| 5 | Capsule-Event 1:N relationship | `uv run pytest tests/test_models.py::test_capsule_event_relationship -v` passes |
| 6 | Pydantic schemas created | Import succeeds: `from app.schemas import Gene, Capsule, Event` |
| 7 | Alembic migration generated | `alembic revision --autogenerate -m "add gep models"` succeeds |

---

## Task 1: SQLAlchemy Models

### Step 1: Write Failing Tests (RED)

**File**: `backend/tests/test_models.py`

```python
"""Test SQLAlchemy models for GEP data structures."""
import pytest
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Gene, Capsule, Event, gene_capsule_association


@pytest.mark.asyncio
async def test_gene_model():
    """Test Gene model creation and attributes."""
    gene = Gene(
        id="gene-test-001",
        name="shell_exec",
        description="Execute shell commands safely",
        implementation="import subprocess\nsubprocess.run(cmd, shell=False)",
        prompt_template="Execute the following command: {cmd}",
        status="validated",
        success_rate=0.95,
        context_tags=["shell", "execution", "system"],
    )
    assert gene.id == "gene-test-001"
    assert gene.name == "shell_exec"
    assert gene.status == "validated"
    assert gene.success_rate == 0.95


@pytest.mark.asyncio
async def test_capsule_model():
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


@pytest.mark.asyncio
async def test_event_model():
    """Test Event model creation and attributes."""
    event = Event(
        id="event-test-001",
        event_type="mutation",
        description="Gene shell_exec mutated to support timeout",
        payload={"gene_id": "gene-001", "change": "added timeout param"},
    )
    assert event.id == "event-test-001"
    assert event.event_type == "mutation"


@pytest.mark.asyncio
async def test_gene_capsule_relationship(db_session: AsyncSession):
    """Test M:N relationship between Gene and Capsule."""
    gene = Gene(id="gene-001", name="gene_a", status="validated")
    gene2 = Gene(id="gene-002", name="gene_b", status="validated")
    capsule = Capsule(
        id="capsule-001",
        name="workflow_a",
        genes=[gene, gene2],
    )

    db_session.add_all([gene, gene2, capsule])
    await db_session.commit()

    # Query and verify relationship
    result = await db_session.execute(
        select(Capsule).where(Capsule.id == "capsule-001")
    )
    loaded_capsule = result.scalar_one()
    assert len(loaded_capsule.genes) == 2


@pytest.mark.asyncio
async def test_capsule_event_relationship(db_session: AsyncSession):
    """Test 1:N relationship between Capsule and Event."""
    capsule = Capsule(id="capsule-001", name="test_capsule")
    event1 = Event(
        id="event-001",
        capsule_id="capsule-001",
        event_type="creation",
        description="Capsule created",
    )
    event2 = Event(
        id="event-002",
        capsule_id="capsule-001",
        event_type="validation",
        description="Capsule validated",
    )

    db_session.add_all([capsule, event1, event2])
    await db_session.commit()

    # Query and verify relationship
    result = await db_session.execute(
        select(Capsule).where(Capsule.id == "capsule-001")
    )
    loaded_capsule = result.scalar_one()
    assert len(loaded_capsule.events) == 2
```

**Command**: `cd backend && uv run pytest tests/test_models.py -v`

**Expected**: FAIL - ModuleNotFoundError: No module named 'app.models'

---

## Task 2: Pydantic Schemas

### Files

```
backend/app/schemas/
├── __init__.py
├── gene.py
├── capsule.py
└── event.py
```

### Schema Definitions

**File**: `backend/app/schemas/gene.py`

```python
"""Pydantic schemas for Gene model."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GeneBase(BaseModel):
    """Base schema for Gene."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    implementation: Optional[str] = None
    prompt_template: Optional[str] = None
    status: str = Field(default="draft", pattern="^(draft|validated|deprecated)$")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    context_tags: list[str] = Field(default_factory=list)


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
    context_tags: Optional[list[str]] = None


class Gene(GeneBase):
    """Schema for reading a Gene."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## Task 3: Database Migration (Alembic)

### Setup

```bash
cd backend
uv add alembic
uv run alembic init alembic
```

### Configuration

**File**: `backend/alembic.ini`

```ini
[alembic]
script_location = alembic
sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

**File**: `backend/alembic/env.py` (modified)

```python
from app.config import settings
from app.database import Base
from app.models import Gene, Capsule, Event  # noqa: F401

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

### Generate Migration

```bash
uv run alembic revision --autogenerate -m "add gep models"
uv run alembic upgrade head
```

---

## Verification Checklist

- [ ] `uv run pytest tests/test_models.py -v` - All model tests pass
- [ ] `uv run python -c "from app.schemas import Gene, Capsule, Event"` - Schemas import
- [ ] `uv run alembic current` - Shows migration is applied
- [ ] `uv run pytest tests/ -v` - All tests still pass

---

## Next Phase

After this phase is complete:
- **v1-phase-03**: CRUD API Implementation
