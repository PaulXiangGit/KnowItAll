# KnowItAll Business Analysis Agent

本目录集中管理 KnowItAll 全链路业务分析 Agent 的产品与技术设计资料。

## 当前文档

- [`technical-design.html`](./technical-design.html)：总体技术设计，包含 Hybrid Knowledge Architecture、五层架构、数据底座选型、知识加工与索引流水线、Agent 编排、核心链路、API、证据机制、安全治理及开源部署方案。

## 后续建议结构

```text
business-analysis-agent/
├── README.md
├── technical-design.html
├── adr/                 # 架构决策记录
├── domain-model/        # 实体、关系、版本与证据 Schema
├── api/                 # OpenAPI 与工具协议
├── connectors/          # 数据源接入规范
├── deployment/          # Compose、Helm 与运维设计
└── evals/               # 评测集、指标与回归标准
```

子目录在产生实际文档时再创建，避免保留无内容的目录。
