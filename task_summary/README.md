# KnowItAll 阶段开发任务档案

本目录用于保存 KnowItAll 每个开发阶段的目标、任务拆解、交付物和验收标准，作为阶段启动、执行跟踪和验收复盘的共同基线。

## 命名约定

每个阶段使用一个独立的 Markdown 文件：

```text
phase-<阶段编号>-<简短英文主题>.md
```

例如：

- `phase-01-foundation-mvp.md`
- `phase-02-runtime-observability.md`

## 固定章节

后续每个阶段的任务文档应至少包含：

1. 阶段信息
2. 阶段目标
3. 成功标准
4. 范围与非目标
5. 技术基线
6. 任务拆解
7. 里程碑与依赖
8. 交付物
9. 验收场景
10. 质量门禁
11. 风险与应对
12. 完成定义
13. 阶段结束记录

## 状态约定

- `DRAFT`：讨论中，尚未承诺执行范围
- `READY`：范围和验收标准已经确认，可以启动
- `IN_PROGRESS`：正在开发
- `BLOCKED`：存在需要外部决策或资源解决的阻塞
- `DONE`：满足完成定义并通过阶段验收

任务状态使用：`TODO`、`IN_PROGRESS`、`BLOCKED`、`DONE`。

## 当前阶段

- [Phase 01：全链路分析最小闭环](./phase-01-foundation-mvp.md)
