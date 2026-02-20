# v1-phase-03: CRUD API Implementation

**Date**: 2026-02-20
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md
**Depends On**: v1-phase-02-data-models.md

---

## Overview

实现 Gene、Capsule、Event 的 RESTful CRUD API 端点。

## API Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        RESTful API                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Genes                                                          │
│  ├── GET    /api/v1/genes          List all genes               │
│  ├── POST   /api/v1/genes          Create a gene                │
│  ├── GET    /api/v1/genes/{id}     Get gene by ID               │
│  ├── PUT    /api/v1/genes/{id}     Update gene                  │
│  └── DELETE /api/v1/genes/{id}     Delete gene                  │
│                                                                 │
│  Capsules                                                       │
│  ├── GET    /api/v1/capsules       List all capsules            │
│  ├── POST   /api/v1/capsules       Create a capsule             │
│  ├── GET    /api/v1/capsules/{id}  Get capsule by ID            │
│  ├── PUT    /api/v1/capsules/{id}  Update capsule               │
│  └── DELETE /api/v1/capsules/{id}  Delete capsule               │
│                                                                 │
│  Events                                                         │
│  ├── GET    /api/v1/events         List all events              │
│  ├── POST   /api/v1/events         Create an event              │
│  └── GET    /api/v1/events/{id}    Get event by ID              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | Gene CRUD API | `pytest tests/test_api_genes.py -v` passes |
| 2 | Capsule CRUD API | `pytest tests/test_api_capsules.py -v` passes |
| 3 | Event API | `pytest tests/test_api_events.py -v` passes |
| 4 | Database integration | Tests use test database |
| 5 | Pagination support | List endpoints support `skip` and `limit` |
| 6 | Error handling | 404 for not found, 422 for validation errors |

---

## Task 1: Database Test Configuration

### Step 1: Write Test Fixtures (RED → GREEN)

**File**: `backend/tests/conftest.py`

```python
"""Pytest configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.database import Base, get_session
from app.config import settings

# Use SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.fixture
def client(db_session: AsyncSession) -> TestClient:
    """Create test client with database override."""
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
```

---

## Task 2: Gene CRUD API

### Files

```
backend/app/api/
├── __init__.py
├── router.py        # Main API router
└── genes.py         # Gene endpoints
```

### Step 1: Write Failing Tests (RED)

**File**: `backend/tests/test_api_genes.py`

```python
"""Test Gene API endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_list_genes_empty(client: TestClient):
    """Test listing genes when empty."""
    response = client.get("/api/v1/genes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_gene(client: TestClient):
    """Test creating a gene."""
    response = client.post(
        "/api/v1/genes",
        json={
            "name": "shell_exec",
            "description": "Execute shell commands",
            "implementation": "subprocess.run(cmd)",
            "status": "draft",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "shell_exec"
    assert "id" in data


def test_get_gene(client: TestClient):
    """Test getting a gene by ID."""
    # Create first
    create_response = client.post(
        "/api/v1/genes",
        json={"name": "test_gene"},
    )
    gene_id = create_response.json()["id"]

    # Get by ID
    response = client.get(f"/api/v1/genes/{gene_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "test_gene"


def test_get_gene_not_found(client: TestClient):
    """Test getting a non-existent gene."""
    response = client.get("/api/v1/genes/nonexistent")
    assert response.status_code == 404


def test_update_gene(client: TestClient):
    """Test updating a gene."""
    # Create first
    create_response = client.post(
        "/api/v1/genes",
        json={"name": "gene_to_update"},
    )
    gene_id = create_response.json()["id"]

    # Update
    response = client.put(
        f"/api/v1/genes/{gene_id}",
        json={"status": "validated", "success_rate": 0.95},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "validated"
    assert response.json()["success_rate"] == 0.95


def test_delete_gene(client: TestClient):
    """Test deleting a gene."""
    # Create first
    create_response = client.post(
        "/api/v1/genes",
        json={"name": "gene_to_delete"},
    )
    gene_id = create_response.json()["id"]

    # Delete
    response = client.delete(f"/api/v1/genes/{gene_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/api/v1/genes/{gene_id}")
    assert get_response.status_code == 404
```

**Command**: `cd backend && uv run pytest tests/test_api_genes.py -v`

**Expected**: FAIL - 404 errors for all endpoints

---

## Task 3: Capsule CRUD API

Similar structure to Gene API.

## Task 4: Event API

Events are immutable - no update/delete endpoints.

---

## Verification Checklist

- [ ] `uv run pytest tests/test_api_genes.py -v` - All Gene API tests pass
- [ ] `uv run pytest tests/test_api_capsules.py -v` - All Capsule API tests pass
- [ ] `uv run pytest tests/test_api_events.py -v` - All Event API tests pass
- [ ] `uv run pytest tests/ -v` - All tests pass
- [ ] `curl http://localhost:8000/api/v1/genes` - Returns empty list

---

## Next Phase

After this phase is complete:
- **v1-phase-04**: GEP Loop Core Logic
