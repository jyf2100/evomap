# v1-phase-01: Project Scaffolding + Base Configuration

**Date**: 2026-02-20
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md

---

## Overview

搭建项目脚手架，配置开发环境，确保最小可运行状态。

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | Backend project structure created | `ls backend/app/` shows all directories |
| 2 | Backend dependencies installed | `cd backend && uv sync` succeeds |
| 3 | FastAPI app starts | `cd backend && uv run uvicorn app.main:app --reload` returns 200 |
| 4 | Database connection works | `uv run python -c "from app.database import engine; engine.connect()"` succeeds |
| 5 | Frontend project structure created | `ls frontend/src/` shows all directories |
| 6 | Frontend dependencies installed | `cd frontend && npm install` succeeds |
| 7 | Frontend dev server starts | `npm run dev` shows Vite welcome page |
| 8 | Docker Compose up | `docker compose up -d` starts all services |

---

## Task 1: Backend Scaffolding

### Files

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration (pydantic-settings)
│   └── database.py          # SQLAlchemy async engine
├── tests/
│   └── conftest.py          # pytest fixtures
├── pyproject.toml           # uv project file
└── Dockerfile
```

### Step 1: Write Failing Test (RED)

**File**: `backend/tests/test_main.py`

```python
"""Test main application entry point."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Command**: `cd backend && uv run pytest tests/test_main.py -v`

**Expected**: FAIL - ModuleNotFoundError: No module named 'app'

### Step 2: Create Minimal Implementation (GREEN)

**File**: `backend/pyproject.toml`

```toml
[project]
name = "evomap-backend"
version = "0.1.0"
description = "GEP Platform Backend"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.29.0",
    "pydantic-settings>=2.0.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**File**: `backend/app/__init__.py`

```python
"""EvoMap Backend Application."""
```

**File**: `backend/app/config.py`

```python
"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "EvoMap GEP Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/evomap"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"


settings = Settings()
```

**File**: `backend/app/main.py`

```python
"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
```

**File**: `backend/app/database.py`

```python
"""Database configuration and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Initialize database connection."""
    async with engine.begin() as conn:
        # Test connection
        await conn.execute("SELECT 1")


async def get_session() -> AsyncSession:
    """Get database session dependency."""
    async with async_session() as session:
        yield session
```

**File**: `backend/tests/conftest.py`

```python
"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)
```

**Command**: `cd backend && uv sync && uv run pytest tests/test_main.py -v`

**Expected**: PASS - test_health_check returns 200

### Step 3: Refactor (if needed)

No refactor needed for minimal setup.

---

## Task 2: Frontend Scaffolding

### Files

```
frontend/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

### Step 1: Initialize Vite Project (GREEN)

**File**: `frontend/package.json`

```json
{
  "name": "evomap-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.1.0"
  }
}
```

**File**: `frontend/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**File**: `frontend/tsconfig.node.json`

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

**File**: `frontend/vite.config.ts`

```import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**File**: `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EvoMap GEP Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**File**: `frontend/src/main.tsx`

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**File**: `frontend/src/App.tsx`

```tsx
function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>EvoMap GEP Platform</h1>
      <p>AI Self-Evolution Infrastructure</p>
    </div>
  )
}

export default App
```

**File**: `frontend/src/vite-env.d.ts`

```typescript
/// <reference types="vite/client" />
```

**Command**: `cd frontend && npm install && npm run dev`

**Expected**: Vite dev server starts on http://localhost:3000

---

## Task 3: Docker Compose Setup

### Files

```
docker-compose.yml
docker-compose.dev.yml
backend/Dockerfile
frontend/Dockerfile
```

### Step 1: Create Docker Compose Files (GREEN)

**File**: `docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: evomap
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@postgres:5432/evomap
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

**File**: `docker-compose.dev.yml`

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - ./backend:/app
    command: uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      DEBUG: "true"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    volumes:
      - ./frontend/src:/app/src
    command: npm run dev -- --host
```

**File**: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY app ./app

# Install dependencies
RUN uv sync --no-dev

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File**: `frontend/Dockerfile`

```dockerfile
FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

**File**: `frontend/Dockerfile.dev`

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
```

**File**: `frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Command**: `docker compose up -d`

**Expected**: All services start successfully

---

## Verification Checklist

- [ ] `cd backend && uv run pytest tests/ -v` - All tests pass
- [ ] `cd backend && uv run uvicorn app.main:app --reload` - Server starts
- [ ] `curl http://localhost:8000/health` - Returns `{"status": "ok"}`
- [ ] `cd frontend && npm run dev` - Vite server starts
- [ ] `docker compose up -d` - All containers healthy
- [ ] `docker compose ps` - Shows 3 running services

---

## Next Phase

After this phase is complete:
- **v1-phase-02**: Gene/Capsule/Event data models
