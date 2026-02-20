# v1-phase-04: GEP Loop Core Logic

**Date**: 2026-02-21
**Status**: In Progress
**Parent**: 2026-02-20-gep-platform-analysis.md
**Depends On**: v1-phase-03-crud-api.md

---

## Overview

实现 GEP（Genome Evolution Protocol）循环的核心逻辑：Scan → Signal → Intent → Mutate → Validate → Solidify

## GEP Loop Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GEP Loop Engine                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌──────┐    ┌────────┐    ┌────────┐    ┌─────────┐        │
│    │ Scan │───►│ Signal │───►│ Intent │───►│ Mutate  │        │
│    └──────┘    └────────┘    └────────┘    └─────────┘        │
│         │                                      │               │
│         │          ┌───────────┐               │               │
│         └─────────►│  Validate │◄──────────────┘               │
│                    └─────┬─────┘                               │
│                          │                                      │
│                    ┌─────▼─────┐                               │
│                    │ Solidify  │                               │
│                    └───────────┘                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase Descriptions

1. **Scan**: 监控运行时日志，识别错误和停滞模式
2. **Signal**: 将非结构化日志转换为标准化进化信号
3. **Intent**: 根据信号规划进化方向（修复/优化/创新）
4. **Mutate**: 生成新代码或提示词策略
5. **Validate**: 在沙箱中执行并验证
6. **Solidify**: 验证通过后固化新能力

---

## Success Criteria

| # | Criteria | Verification |
|---|----------|--------------|
| 1 | Scanner can parse error logs | `pytest tests/test_gep_loop.py::test_scanner -v` |
| 2 | Signal generation works | `pytest tests/test_gep_loop.py::test_signal -v` |
| 3 | Intent classification | `pytest tests/test_gep_loop.py::test_intent -v` |
| 4 | Mutation generation | `pytest tests/test_gep_loop.py::test_mutate -v` |
| 5 | Validation in sandbox | `pytest tests/test_gep_loop.py::test_validate -v` |
| 6 | Solidify creates genes | `pytest tests/test_gep_loop.py::test_solidify -v` |
| 7 | Full loop integration | `pytest tests/test_gep_loop.py::test_full_loop -v` |

---

## Task 1: Scanner Service

### Files

```
backend/app/services/
├── __init__.py
├── scanner.py      # Log scanning and pattern detection
├── signal.py       # Signal generation
├── intent.py       # Intent classification
├── mutator.py      # Code/prompt mutation
├── validator.py    # Sandbox validation
├── solidifier.py   # Gene solidification
└── gep_loop.py     # Main loop orchestrator
```

---

## Verification Checklist

- [ ] All GEP loop tests pass
- [ ] Can process sample error logs end-to-end
- [ ] Creates validated genes from successful mutations

---

## Next Phase

After this phase is complete:
- **v1-phase-05**: Frontend UI
