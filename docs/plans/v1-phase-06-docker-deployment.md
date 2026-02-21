# v1-phase-06: Docker Deployment

**Date**: 2026-02-21
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md
**Depends On**: v1-phase-05-frontend-ui.md

---

## Overview

配置 Docker Compose 实现一键部署。

## Services

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Frontend   │  │   Backend   │  │  PostgreSQL │             │
│  │   :3000     │  │   :8000     │  │   :5432     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                      │
│         └────────────────┴────────────────┘                      │
│                          │                                       │
│                   ┌──────┴──────┐                               │
│                   │   Network   │                               │
│                   └─────────────┘                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | `docker compose build` succeeds | No errors |
| 2 | `docker compose up -d` starts all services | All containers healthy |
| 3 | Backend API accessible | `curl http://localhost:8000/health` |
| 4 | Frontend accessible | Browser shows UI |
| 5 | Database migrations run | Tables created |

---

## Files

```
docker-compose.yml
docker-compose.prod.yml
backend/Dockerfile
frontend/Dockerfile
.env.example
```

---

## Verification

```bash
# Start all services
docker compose up -d

# Check health
docker compose ps
curl http://localhost:8000/health
curl http://localhost:3000

# View logs
docker compose logs -f
```
