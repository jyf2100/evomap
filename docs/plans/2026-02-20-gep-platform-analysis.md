# GEP 私有化平台 - 分析与设计文档

**日期**: 2026-02-20
**状态**: Draft
**作者**: AI Agent (Tashan Development Loop)

---

## 1. Analysis（分析）

### 1.1 现状（Current State）

**项目背景**：
- 基于 GEP（Genome Evolution Protocol）协议构建私有化 AI Agent 进化平台
- 目标：解决 AI Agent 的"经验孤岛"问题，实现能力继承和协作进化

**现有资产**：
- 3 份技术文档（协议描述、概念对比、起源故事）
- 无代码实现

**GEP 协议核心组件**：
```
┌─────────────────────────────────────────────────────────┐
│                    GEP Platform                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Evolver   │  │   EvoMap    │  │  GEP Proto  │     │
│  │   Engine    │  │   Graph     │  │   Layer     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │             │
│         └────────────────┴────────────────┘             │
│                          │                              │
│                    ┌─────┴─────┐                       │
│                    │  Storage  │                       │
│                    │  (Graph)  │                       │
│                    └───────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### 1.2 约束（Constraints）

**技术约束**：
- [C1] 后端使用 Python（FastAPI + SQLAlchemy）
- [C2] 前端使用 JavaScript（React 或 Vue）
- [C3] 部署使用 Docker Compose
- [C4] 数据库优先选择 PostgreSQL（图扩展）或 Neo4j
- [C5] 本地部署，无云服务依赖

**业务约束**：
- [B1] 必须支持 GEP 协议的核心数据结构（Gene, Capsule, Event）
- [B2] 必须实现 GEP 循环（Scan → Signal → Intent → Mutate → Validate → Solidify）
- [B3] 需要考虑与现有 MCP 协议的兼容性

**安全约束**：
- [S1] 私有化部署，数据不出本地
- [S2] 需要沙箱执行验证（防止"失控进化"）
- [S3] 修改限制（如：每次最多修改 60 个文件，核心文件禁止修改）

### 1.3 成功标准（Success Criteria）

**MVP 验收标准**：

| # | 功能 | 验证方式 |
|---|------|----------|
| 1 | Gene CRUD API | `pytest tests/test_genes.py` 全绿 |
| 2 | Capsule CRUD API | `pytest tests/test_capsules.py` 全绿 |
| 3 | Event 日志记录 | `pytest tests/test_events.py` 全绿 |
| 4 | GEP 循环：Scan 阶段 | 能从日志中识别错误模式 |
| 5 | GEP 循环：Mutate 阶段 | 能生成变异代码 |
| 6 | GEP 循环：Validate 阶段 | 沙箱执行 + 测试断言 |
| 7 | 基础 Web UI | 能在浏览器中查看 Gene 列表 |
| 8 | Docker Compose up | `docker compose up -d` 一键启动 |

### 1.4 风险（Risks）

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| LLM API 调用成本高 | 高 | 中 | 支持本地模型（Ollama） |
| 进化循环失控 | 中 | 高 | 严格沙箱 + 修改限制 |
| 图数据库复杂度 | 中 | 中 | 先用 PostgreSQL，后续迁移 Neo4j |
| 前后端集成困难 | 低 | 中 | 使用 OpenAPI 规范 + 代码生成 |

---

## 2. Design（设计）

### 2.1 方案对比

#### 方案 A：单体架构（Monolith）

```
┌─────────────────────────────────────┐
│         Docker Container            │
│  ┌─────────────────────────────┐   │
│  │      FastAPI Application    │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐   │   │
│  │  │ API │ │ GEP │ │ LLM │   │   │
│  │  │Layer│ │Loop │ │Call │   │   │
│  │  └─────┘ └─────┘ └─────┘   │   │
│  └─────────────────────────────┘   │
│              │                      │
│        PostgreSQL                  │
└─────────────────────────────────────┘
```

**优点**：
- 开发速度快，部署简单
- 调试方便
- 适合 MVP

**缺点**：
- 扩展性受限
- 单点故障

---

#### 方案 B：微服务架构（Microservices）

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  evolver-svc │   │  evomap-svc  │   │  gateway-svc │
│   :8001      │   │   :8002      │   │   :8000      │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                          │
                   ┌──────┴──────┐
                   │   Redis     │
                   │   Neo4j     │
                   └─────────────┘
```

**优点**：
- 独立扩展
- 故障隔离
- 团队并行开发

**缺点**：
- 开发复杂度高
- 运维成本高
- MVP 阶段过度设计

---

#### 方案 C：模块化单体（Modular Monolith）【推荐】

```
┌─────────────────────────────────────────────────────┐
│               Docker Compose Stack                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │            FastAPI Application              │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ evolver │ │ evomap  │ │  api    │       │   │
│  │  │ module  │ │ module  │ │ module  │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘       │   │
│  │       │            │            │           │   │
│  │       └────────────┴────────────┘           │   │
│  │                    │                        │   │
│  │            ┌───────┴───────┐               │   │
│  │            │    Core       │               │   │
│  │            │  (Models,     │               │   │
│  │            │   Services)   │               │   │
│  │            └───────────────┘               │   │
│  └─────────────────────────────────────────────┘   │
│                      │                              │
│  ┌───────────────────┼───────────────────┐        │
│  │            PostgreSQL                 │        │
│  │  ┌─────────────────────────────────┐  │        │
│  │  │  genes | capsules | events      │  │        │
│  │  └─────────────────────────────────┘  │        │
│  └───────────────────────────────────────┘        │
│                                                     │
│  ┌───────────────────────────────────────┐        │
│  │         React Frontend (:3000)        │        │
│  └───────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

**优点**：
- 模块化设计，易于拆分
- 单体部署，简单可靠
- 适合 MVP 和早期迭代
- 后续可平滑迁移到微服务

**缺点**：
- 需要严格的模块边界
- 单进程扩展受限

---

### 2.2 推荐方案：方案 C（模块化单体）

**理由**：
1. **MVP 优先**：快速交付，验证核心价值
2. **渐进式演进**：模块边界清晰，后续可拆分
3. **本地部署友好**：Docker Compose 一键启动
4. **技术债务可控**：避免早期过度设计

---

## 3. 技术架构

### 3.1 后端技术栈

```
┌─────────────────────────────────────┐
│            Backend Stack            │
├─────────────────────────────────────┤
│  Framework    : FastAPI 0.110+      │
│  ORM          : SQLAlchemy 2.0      │
│  Validation   : Pydantic v2         │
│  Database     : PostgreSQL 16       │
│  LLM Client   : openai / ollama     │
│  Task Queue   : Celery + Redis      │
│  Testing      : pytest + httpx      │
└─────────────────────────────────────┘
```

### 3.2 前端技术栈

```
┌─────────────────────────────────────┐
│           Frontend Stack            │
├─────────────────────────────────────┤
│  Framework    : React 18 + Vite     │
│  UI Library   : shadcn/ui + Tailwind│
│  State        : Zustand             │
│  Data Fetching: TanStack Query      │
│  API Client   : openapi-typescript  │
└─────────────────────────────────────┘
```

### 3.3 项目目录结构

```
evomap/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   ├── models/              # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── gene.py
│   │   │   ├── capsule.py
│   │   │   └── event.py
│   │   ├── schemas/             # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── gene.py
│   │   │   ├── capsule.py
│   │   │   └── event.py
│   │   ├── api/                 # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── genes.py
│   │   │   ├── capsules.py
│   │   │   └── events.py
│   │   ├── services/            # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── gep_loop.py      # GEP 循环核心
│   │   │   ├── evolver.py       # Evolver 引擎
│   │   │   └── sandbox.py       # 沙箱执行
│   │   └── workers/             # Celery Tasks
│   │       └── evolution.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_genes.py
│   │   ├── test_capsules.py
│   │   └── test_gep_loop.py
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── stores/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
└── docs/
    └── plans/
        └── 2026-02-20-gep-platform-analysis.md
```

---

## 4. 下一步

本分析文档完成后，需要创建具体的工程计划：

1. **v1-phase-01**: 项目脚手架 + 基础配置
2. **v1-phase-02**: Gene/Capsule/Event 数据模型
3. **v1-phase-03**: CRUD API 实现
4. **v1-phase-04**: GEP 循环核心逻辑
5. **v1-phase-05**: 前端 UI
6. **v1-phase-06**: Docker 部署

每个 Phase 都需要独立的计划文档，遵循 TDD 流程。
