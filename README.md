# KnowItAll

KnowItAll 是一个面向产品、前端、后端、测试和项目管理角色的全链路业务分析 Agent。项目使用 Hybrid Knowledge Architecture，将结构化事实、关系图、全文检索、向量召回、代码索引和证据链分别建模。

当前处于 [Phase 01：全链路分析最小闭环](./task_summary/phase-01-foundation-mvp.md)。

## 当前开发基线

- Python 3.12
- FastAPI
- LangGraph
- Pydantic
- PostgreSQL + pgvector
- MinIO
- Redis Streams

## 本地启动

当前版本提供 FastAPI API、LangGraph 最小工作流和本地基础设施配置。需要：

- Python 3.12
- GNU Make
- Docker Desktop，或兼容的 Docker Runtime
- `docker-compose` v1 或 `docker compose` v2

### 1. 首次初始化

```bash
cd /path/to/KnowItAll
cp .env.example .env
make install
```

`make install` 会在项目根目录创建 `.venv`，并将项目以 editable 模式安装到该虚拟环境。无需手动激活虚拟环境即可使用后续 Make 命令。

### 2. 启动本地基础设施

确保 Docker Desktop 已启动，然后执行：

```bash
make infra-up
```

该命令默认使用本机的 `docker-compose`，启动 PostgreSQL/pgvector、Redis 和 MinIO。使用 Docker Compose v2 时执行：

```bash
make infra-up COMPOSE="docker compose -f compose.yaml"
```

查看容器状态：

```bash
docker-compose -f compose.yaml ps
```

### 3. 启动 FastAPI

```bash
make dev
```

API 默认监听 `127.0.0.1:8000`，支持代码热更新。启动后访问：

- 健康检查：[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- 就绪检查：[http://127.0.0.1:8000/ready](http://127.0.0.1:8000/ready)
- OpenAPI：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- MinIO 控制台：[http://127.0.0.1:9001](http://127.0.0.1:9001)

MinIO 本地开发账号来自 `.env.example`：

```text
用户名：knowitall
密码：change-me
```

### 4. 验证分析接口

可以在 OpenAPI 页面调用 `POST /api/v1/analyses`，或执行：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyses \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "修改订单字段会影响哪些页面？",
    "business_line_ids": ["commerce-order"]
  }'
```

当前接口会返回意图识别和有效业务线作用域。数据库持久化、知识接入和真实证据检索将在 Phase 01 后续任务中接入。

### 5. 日常开发检查

```bash
make check
```

该命令依次运行 Ruff、Mypy 和 Pytest。也可以单独执行：

```bash
make lint
make typecheck
make test
```

### 6. 停止服务

在运行 FastAPI 的终端按 `Ctrl+C`，然后停止本地基础设施：

```bash
make infra-down
```

### 仅启动 API

当前 API 骨架尚未实际连接数据库。如果暂时不需要 PostgreSQL、Redis 和 MinIO，可以跳过 `make infra-up`，直接执行：

```bash
make dev
```

### 常见问题

- `docker-compose: command not found`：使用 `make infra-up COMPOSE="docker compose -f compose.yaml"`。
- `Cannot connect to the Docker daemon`：先启动 Docker Desktop。
- `Address already in use`：检查本机的 8000、5432、6379、9000、9001 端口。
- PyCharm 显示依赖无法导入：按下一节将解释器切换到项目 `.venv/bin/python`。

## PyCharm 配置

项目采用 `src layout`，依赖安装在仓库根目录的 `.venv`。PyCharm 必须使用以下项目解释器：

```text
<项目根目录>/.venv/bin/python
```

配置步骤：

1. 打开 `Settings / Preferences → Project: KnowItAll → Python Interpreter`。
2. 选择 `Add Interpreter → Add Local Interpreter → Existing`。
3. 选择项目中的 `.venv/bin/python`，不要选择 Anaconda 的 Python 3.11 或系统 Python 3.12。
4. 如果 `knowitall` 仍显示红线，右键 `src`，选择 `Mark Directory as → Sources Root`。
5. 重新打开 PyCharm Terminal，执行以下命令确认：

```bash
which python
python -c "import fastapi, knowitall; print(fastapi.__file__); print(knowitall.__file__)"
```

第一行应指向当前项目的 `.venv/bin/python`。

## 文档

- [Agent 技术设计](./docs/business-analysis-agent/technical-design.html)
- [阶段任务档案](./task_summary/README.md)
