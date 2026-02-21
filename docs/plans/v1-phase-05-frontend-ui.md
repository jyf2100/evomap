# v1-phase-05: Frontend UI

**Date**: 2026-02-21
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md
**Depends On**: v1-phase-03-crud-api.md

---

## Overview

构建前端 UI，展示 Gene 列表、Capsule 详情和 Event 日志。

## Tech Stack

- React 18 + TypeScript
- Vite
- TanStack Query (数据获取)
- Tailwind CSS (样式)

## Pages

```
/               - Dashboard (概览)
/genes          - Gene 列表
/genes/:id      - Gene 详情
/capsules       - Capsule 列表
/capsules/:id   - Capsule 详情
/events         - Event 日志
```

---

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | Dashboard shows stats | Visual check |
| 2 | Gene list renders | Fetch from API |
| 3 | Gene detail page works | Route navigation |
| 4 | Capsule pages work | Create/View |
| 5 | Event log displays | Real-time feel |
| 6 | `npm run build` succeeds | Production build |

---

## Files

```
frontend/src/
├── api/
│   └── client.ts       # API client
├── components/
│   ├── Layout.tsx
│   ├── GeneCard.tsx
│   └── EventRow.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── Genes.tsx
│   ├── GeneDetail.tsx
│   ├── Capsules.tsx
│   ├── CapsuleDetail.tsx
│   └── Events.tsx
├── App.tsx
└── main.tsx
```

---

## Next Phase

After this phase is complete:
- **v1-phase-06**: Docker Deployment
