# Phase 01：全链路分析最小闭环

## 1. 阶段信息

| 项目 | 内容 |
| --- | --- |
| 阶段编号 | Phase 01 |
| 阶段名称 | 全链路分析最小闭环 |
| 状态 | IN_PROGRESS |
| 建议周期 | 6—8 周 |
| 默认技术栈 | Python 3.12、FastAPI、LangGraph、Pydantic |
| 默认数据底座 | PostgreSQL、pgvector、MinIO、Redis Streams |
| 主要使用者 | 产品、前端、后端、测试、项目管理 |
| 上位设计 | `docs/business-analysis-agent/technical-design.html` |

## 2. 阶段目标

第一阶段交付一个可以通过 Docker Compose 启动的 KnowItAll MVP，完成以下端到端闭环：

```text
数据接入
→ 知识解析与业务线标注
→ 结构化/全文/向量/关系索引
→ 用户提问与业务线作用域解析
→ LangGraph 检索编排
→ 证据归一与置信度计算
→ FastAPI 流式返回
→ 业务线隔离的会话记忆
```

第一阶段重点不是覆盖所有数据源，而是证明 KnowItAll 能基于少量真实数据，稳定完成可解释、可追溯、不会跨业务线污染的业务分析。

## 3. 成功标准

阶段结束时必须满足：

1. 可以接入本地文档、OpenAPI 和 Git 仓库三类数据源。
2. 可以按业务线、数据权限、版本和实体类型过滤检索结果。
3. 支持精确检索、PostgreSQL 全文检索、pgvector 语义检索及一至三跳关系查询。
4. 支持知识查询、变更影响分析、需求完整性审查三类 Agent 意图。
5. 所有事实型结论能够定位到文档段落、OpenAPI 节点或代码文件与行号。
6. 用户可以主动设置本轮业务线，Agent 也可以推断业务线并在不确定时请求确认。
7. 多轮对话只召回与本轮业务线作用域相关的历史记忆。
8. 能通过 SSE 展示分析进度，并通过 LangGraph checkpoint 暂停和恢复需要确认的任务。
9. 可以通过一条 Docker Compose 命令启动开发环境。
10. 核心验收数据集通过自动化回归，没有权限泄漏和跨业务线记忆污染。

## 4. 范围与非目标

### 4.1 本阶段范围

- 工程骨架与本地开发环境
- 核心领域模型、数据库迁移和 Repository/Port
- 业务线作用域模型与标签治理
- 本地文档、OpenAPI、Git 数据接入
- 知识解析、切片、实体抽取、关系生成和索引流水线
- 精确、全文、向量及关系查询
- LangGraph Agent 主状态图
- FastAPI REST、SSE 和人工确认接口
- 业务线隔离的会话记忆
- 最小 Web 交互界面
- 评测集、自动化测试、监控基础和部署文档

### 4.2 本阶段非目标

- 日志、指标、分布式 Trace 和生产告警接入
- 自动修改配置、代码或生产环境
- 自动发布和自动创建外部工单
- 完整的跨语言代码调用图
- ArangoDB、Neo4j 或 OpenSearch 强依赖
- 多 Agent 自主协作
- 企业级 SSO、复杂组织架构同步
- 大规模知识图谱可视化
- 面向海量数据的集群与高可用优化

## 5. 技术基线

### 5.1 应用层

- FastAPI：REST API、SSE、请求校验、身份与业务线作用域注入。
- LangGraph：状态图、条件路由、工具执行、checkpoint、`interrupt()` 人工确认。
- Pydantic：API DTO、Graph State、QueryPlan、EvidenceItem 和 Tool I/O Schema。
- Worker：连接器同步、文档解析、Embedding 和索引任务。

### 5.2 数据层

- PostgreSQL：业务实体、元数据、关系边、ACL、会话、记忆、任务和审计。
- PostgreSQL FTS：第一阶段全文索引，支持字段名、接口名、错误码和关键词搜索。
- pgvector：历史需求、技术文档、评审内容与代码注释的语义召回。
- MinIO：不可变源文件、附件、解析产物和大体积证据。
- Redis Streams：后台任务与索引事件；通过 Queue Port 保留未来迁移 Kafka 的能力。

### 5.3 关键约束

- RAG 不是事实主库。
- LangGraph State 不是长期业务记忆库。
- 业务线标签不能替代 ACL，也不能扩大权限。
- Agent 不直接生成或执行未受控 SQL、AQL、Shell 或日志查询。
- 每条关系和事实必须具有来源、版本、有效时间与证据引用。

## 6. 任务拆解

### P01-T01：工程骨架与开发环境

**状态：** IN_PROGRESS

**目标：** 建立可扩展的 Python 单体模块化工程和本地一键启动环境。

**任务：**

- 建立 `apps/api`、`apps/worker` 和核心 Python package。
- 配置 FastAPI、LangGraph、Pydantic 和依赖管理。
- 提供 PostgreSQL、pgvector、MinIO、Redis 的 Docker Compose。
- 建立统一配置、Secret 加载、结构化日志和错误模型。
- 增加 lint、format、type check、unit test 和 migration 命令。
- 提供健康检查、readiness 和版本信息接口。

**交付物：** 工程目录、Compose 文件、开发命令、CI 基线和本地启动说明。

**验收：** 新环境按 README 操作可以启动 API、Worker 和所有依赖，健康检查全部通过。

### P01-T02：核心领域模型与数据库

**状态：** TODO

**目标：** 建立稳定、版本化、可追溯的知识模型。

**任务：**

- 定义 Tenant、User、Project、BusinessLine、DataSource。
- 定义 Requirement、Document、DocumentChunk、Repository、CodeSymbol、API、APIField、Page、Service。
- 定义 EntityRelation、Evidence、KnowledgeRevision、ACL。
- 定义 Conversation、ConversationTurn、Memory、AnalysisRun、IndexJob。
- 设计 Identity + Revision 模型及 `valid_from`/`valid_to`。
- 建立数据库迁移、唯一约束、必要索引和软删除策略。
- 定义 Domain Model、Persistence Model 与 API DTO 的转换边界。

**交付物：** Schema、迁移脚本、领域模型、Repository 接口和模型说明。

**验收：** 可以创建、更新和查询带版本的实体、关系与证据，并能查询指定时间点的数据视图。

### P01-T03：业务线作用域与标签治理

**状态：** TODO

**目标：** 让所有数据、提问、检索和记忆都处于明确业务线作用域内。

**任务：**

- 实现 BusinessLine 的稳定编码、名称、别名、层级和状态。
- 支持实体和记忆的主业务线、多业务线及 `shared` 标签。
- 保存标签来源：EXPLICIT、RULE、INHERITED、INFERRED。
- 建立项目、仓库和路径到业务线的映射规则。
- 实现业务线候选推断和置信度。
- 实现 Turn Scope，允许用户本轮覆盖会话默认标签。
- 所有 Search、Graph、Code、Memory 工具强制接收 `effective_scope`。
- 添加标签修正、版本记录和审计事件。

**交付物：** 业务线管理服务、推断服务、作用域中间件和治理接口。

**验收：** 显式标签优先；低置信推断要求确认；不同业务线的数据和记忆不会交叉返回。

### P01-T04：数据接入连接器

**状态：** TODO

**目标：** 接入构成第一条业务分析链路所需的最小数据源。

**任务：**

- 定义 Connector SDK：`discover`、`fetch`、`checkpoint`、`acl`、`health`。
- 实现本地 Markdown、HTML 和 TXT 文档连接器。
- 实现 OpenAPI 3.x JSON/YAML 连接器。
- 实现本地 Git 仓库连接器，支持 commit、diff、文件和符号元数据。
- 第一批代码语言选择项目最常用的两种，使用 Tree-sitter 抽取符号和引用。
- 所有原件保存内容哈希、源 URI、源版本和业务线标签。
- 实现全量同步、增量同步、幂等和失败重试。

**交付物：** Connector SDK、三个连接器、连接器配置与运行状态接口。

**验收：** 重复同步不会生成重复实体；源文件修改后只产生必要的新 Revision 和索引事件。

### P01-T05：知识加工与索引流水线

**状态：** TODO

**目标：** 将源数据加工为可查询的实体、关系、文本切片和向量。

**任务：**

- 实现原件入 MinIO、解析、标准化和切片。
- 实现确定性实体抽取和强标识对齐。
- 实现基础关系：DESCRIBES、HAS_FIELD、IMPLEMENTS、CALLS、REFERENCES、AFFECTS。
- 建立 Evidence Envelope，保存段落、JSON Pointer、文件与行号定位。
- 实现 Embedding、模型版本和批量写入。
- 使用 PostgreSQL outbox 驱动全文、向量和关系索引更新。
- 实现索引 revision、重试、死信和全量重建。
- 对模型推断关系标记 PROPOSED，不自动升级为 VERIFIED。

**交付物：** Pipeline Worker、Outbox Consumer、索引状态接口和重建命令。

**验收：** 任一派生索引可以从原件和事实库重建；索引结果均能回溯到源内容。

### P01-T06：混合检索与关系查询

**状态：** TODO

**目标：** 根据问题类型组合确定性查询、全文、向量和关系检索。

**任务：**

- 实现 Entity Resolver，支持接口名、字段名、错误码和符号精确绑定。
- 实现 PostgreSQL FTS 及字段权重。
- 实现 pgvector 检索及业务线、类型、版本和 ACL metadata filter。
- 实现一至三跳关系遍历、方向、关系类型和时间过滤。
- 实现 Hybrid Search 的合并、去重和重排。
- 统一输出 `EvidenceItem[]`，禁止工具只返回无来源自由文本。
- 定义检索预算、超时、最大结果数和降级策略。

**交付物：** Search Port、Graph Port、PostgreSQL Adapter 和检索测试集。

**验收：** 精确实体问题优先命中确定性结果；语义问题能够召回相似历史文档；所有结果遵守业务线和 ACL。

### P01-T07：LangGraph Agent 编排

**状态：** TODO

**目标：** 建立受约束、可恢复、有证据的主分析工作流。

**任务：**

- 定义 AnalysisState、AnalysisIntent、QueryPlan 和 AnalysisAnswer。
- 实现 `resolve_scope`、`classify_intent`、`resolve_entities`、`build_plan`。
- 实现 `execute_tools`、`normalize_evidence`、`detect_conflicts`。
- 实现 `score_confidence`、`human_gate`、`compose_answer`。
- 支持 KNOWLEDGE_SEARCH、CHANGE_IMPACT、REQUIREMENT_REVIEW。
- 使用模板化查询计划限制自主规划范围。
- 配置节点重试、超时、预算、checkpoint 和幂等键。
- 使用 `interrupt()` 处理业务线、实体歧义和高风险确认。
- 保存工具版本、模型版本、Prompt 版本和证据引用。

**交付物：** LangGraph 工作流、节点单元测试、状态恢复测试和三类意图端到端测试。

**验收：** Agent 可以暂停、恢复和重试；证据不足或冲突时不会生成确定性结论。

### P01-T08：业务线隔离的会话记忆

**状态：** TODO

**目标：** 支持多轮对话，同时防止不同业务线的历史上下文互相污染。

**任务：**

- 区分 LangGraph checkpoint 与可召回长期记忆。
- 每条记忆保存业务线、作用域来源、置信度和来源 Turn ID。
- 实现按 `effective_scope ∩ user_allowed_scope` 检索记忆。
- 实现按业务线分区的对话摘要。
- 跨业务线问题按域分桶召回并平衡配额。
- 无标签业务记忆默认不参与召回。
- 全局记忆仅允许保存语言和展示格式等白名单偏好。
- 返回选中记忆数量和按作用域排除数量，供审计而非泄露隐藏内容。

**交付物：** Memory Service、摘要任务、作用域过滤器和污染测试。

**验收：** 订单与会员业务线交替对话时，任一轮上下文中不出现另一业务线的业务记忆。

### P01-T09：FastAPI 服务接口

**状态：** TODO

**目标：** 对外提供稳定、可观测、可恢复的分析和数据管理接口。

**任务：**

- 实现分析创建、状态查询、取消和 SSE 事件接口。
- 实现人工确认与 LangGraph Run 恢复接口。
- 实现业务线列表、作用域推断与 Turn Scope 修正接口。
- 实现数据源注册、同步、索引任务和状态查询接口。
- 实现 Search、Entity、Graph Path 和 Feedback 接口。
- 定义统一错误模型、请求 ID、幂等键和分页。
- SSE 使用稳定事件类型，不透传 LangGraph 内部对象。
- 添加 API 权限、限流、超时和审计日志。

**交付物：** FastAPI 应用、OpenAPI 文档、API 测试和调用示例。

**验收：** 可通过 API 完成数据导入、提问、流式读取、用户确认和最终结果获取。

### P01-T10：最小 Web 交互界面

**状态：** TODO

**目标：** 让目标用户能够验证核心交互，而不仅依赖 Swagger。

**任务：**

- 实现对话输入与流式回答。
- 实现业务线标签选择、自动推断提示和一键修正。
- 实现跨业务线模式的明确提示。
- 展示执行阶段、结论、影响对象、置信度和不确定项。
- 实现证据列表、来源类型、版本和原文展开。
- 实现确认、反馈和错误恢复交互。

**交付物：** 可运行的最小 Web 页面和交互测试。

**验收：** 非研发用户能够独立完成一次提问、确认作用域、查看证据和提交反馈。

### P01-T11：质量、评测与可观测性

**状态：** TODO

**目标：** 建立可持续回归的质量门禁。

**任务：**

- 建立第一批 Gold Set：知识检索、接口字段影响、需求完整性和业务线隔离。
- 实现 Evidence Precision、Unsupported Claim Rate、Scope Accuracy 等评测。
- 添加领域模型、连接器、检索、Agent、权限和 API 测试。
- 添加跨租户、跨业务线和提示注入安全测试。
- 输出索引延迟、工具耗时、模型耗时、Token、错误率和检索命中指标。
- 对关键链路增加 Trace ID，并贯穿 FastAPI、LangGraph 和 Worker。

**交付物：** 自动化评测、测试报告、基础 Dashboard 和回归命令。

**验收：** CI 自动执行关键测试；权限泄漏为 0；事实型回答的 Evidence Precision 达到 95%。

### P01-T12：一键部署与开发者文档

**状态：** TODO

**目标：** 形成可被外部开发者运行和理解的开源 MVP。

**任务：**

- 完善 Dockerfile 和 Docker Compose Profile。
- 提供数据库迁移、初始化、示例数据和健康检查。
- 提供环境变量模板，不提交任何真实密钥。
- 编写 Quick Start、架构说明、连接器开发和故障排查文档。
- 提供备份、恢复和索引重建基础操作说明。
- 增加开源许可证、贡献指南和安全报告入口。

**交付物：** 可发布的部署包、示例项目和开发者文档。

**验收：** 全新环境能够按照 Quick Start 在 30 分钟内完成启动、导入示例数据并获得第一条带证据回答。

## 7. 里程碑与依赖

| 里程碑 | 建议时间 | 包含任务 | 出口条件 |
| --- | --- | --- | --- |
| M1：基础可运行 | 第 1—2 周 | T01、T02、T03 | 服务可启动，模型可迁移，作用域可计算 |
| M2：知识可检索 | 第 3—4 周 | T04、T05、T06 | 三类数据可导入，能够返回带证据检索结果 |
| M3：Agent 闭环 | 第 5—6 周 | T07、T08、T09 | 三类意图可运行，支持流式、确认和隔离记忆 |
| M4：可交付 MVP | 第 7—8 周 | T10、T11、T12 | UI、评测、部署和文档达到验收标准 |

主要依赖关系：

```text
T01 → T02 → T03
T01 → T04 → T05 → T06 → T07
T03 ─────────────────→ T07 → T08 → T09
T09 → T10
T02～T10 → T11 → T12
```

## 8. 阶段交付物

- FastAPI API 服务
- LangGraph Agent Runtime
- 索引 Worker
- PostgreSQL/pgvector 数据模型与迁移
- MinIO 原件存储适配器
- Redis Streams 任务适配器
- 文档、OpenAPI、Git 连接器
- 混合检索与关系查询服务
- 业务线作用域和记忆隔离服务
- 最小 Web 交互界面
- Docker Compose 部署配置
- Gold Set、自动化评测与测试报告
- Quick Start、API 和运维文档

## 9. 核心验收场景

1. 查询“订单接口的 `discountAmount` 字段在哪里使用”，返回接口定义、相关代码文件与行号。
2. 查询“修改创建订单接口会影响哪些代码和文档”，返回一至三跳影响路径和证据。
3. 查询“找出与会员自动续费相关的历史需求”，通过混合检索返回相似文档并解释相似点。
4. 上传一份需求并询问是否缺少权限、异常态、埋点和灰度策略，输出已覆盖、缺失、含糊和冲突项。
5. 用户不设置标签时，系统根据强实体推断业务线，并展示来源与置信度。
6. 推断存在两个相近候选时，系统暂停并要求用户确认，而不是静默选择。
7. 用户在订单和会员业务线之间切换，本轮上下文只包含当前业务线相关记忆。
8. 跨业务线问题明确显示多标签作用域，结果按业务线标注来源。
9. 用户无权访问某业务线时，主动选择该标签也不能获取相关数据或推断候选信息。
10. 数据或证据不足时，Agent 明确输出不确定项和建议补充信息，不虚构依赖关系。

## 10. 质量门禁

| 指标 | 阶段门槛 |
| --- | --- |
| Evidence Precision | ≥ 95% |
| Unsupported Claim Rate | < 2% |
| 业务线作用域推断准确率 | 强实体场景 ≥ 95% |
| 跨业务线记忆污染 | 0 |
| 跨租户/越权数据泄漏 | 0 |
| 核心 API 集成测试 | 100% 通过 |
| 索引任务幂等测试 | 100% 通过 |
| MVP 关键查询 p95 | 目标值在基准测试后冻结，首期建议 < 8 秒 |

若权限泄漏、跨业务线污染或无法追溯事实来源，阶段不得标记为 DONE。

## 11. 风险与应对

| 风险 | 影响 | 应对 |
| --- | --- | --- |
| 数据源范围过大 | 阶段延期 | 固定三类连接器，不临时新增生产系统 |
| 实体对齐质量不足 | 关系图失真 | 强标识优先；模型结果保持 PROPOSED；人工修正可追溯 |
| 业务线标签错误 | 记忆污染或漏召回 | 显式标签优先、低置信确认、服务端强制作用域 |
| LangGraph State 膨胀 | checkpoint 性能下降 | State 保存引用，大结果写证据库或对象存储 |
| 模型输出不稳定 | 结论不可验收 | 模板化 QueryPlan、结构化输出、证据绑定和离线评测 |
| PostgreSQL 图查询不足 | 影响分析变慢 | 第一阶段限制三跳；保留 Graph Port，后续评估专用图数据库 |
| 开发环境过重 | 开源体验差 | Lite Profile 减少依赖，提供示例数据和健康检查 |

## 12. 完成定义（Definition of Done）

Phase 01 只有同时满足以下条件才能完成：

- 所有阶段范围内任务完成或经过明确批准移出范围。
- 核心验收场景全部通过并保留测试结果。
- 权限泄漏和跨业务线记忆污染测试为 0。
- 数据导入、索引、检索、Agent 和 API 有自动化测试覆盖。
- Docker Compose 可以在全新环境启动。
- 示例数据可以产生至少三类带证据回答。
- 所有事实型结论能够打开原始证据。
- 数据库迁移、备份恢复和索引重建经过验证。
- API、架构、部署和已知限制文档完整。
- 阶段结束记录已经填写。

## 13. 阶段结束记录

> 本章节在 Phase 01 验收时填写。

| 项目 | 记录 |
| --- | --- |
| 实际开始日期 | 待填写 |
| 实际完成日期 | 待填写 |
| 最终状态 | 待填写 |
| 完成任务 | 待填写 |
| 延后任务 | 待填写 |
| 关键技术决策 | 待填写 |
| 质量指标结果 | 待填写 |
| 已知问题 | 待填写 |
| 下一阶段输入 | 待填写 |
