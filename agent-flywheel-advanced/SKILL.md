# 🌀 Agent Flywheel Advanced - 永动机自动飞轮 v2.0

> 借鉴 AutoGPT/CrewAI/MetaGPT 成熟方案生产的 Agent Team 自动化系统

## 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    🌀 Agent Flywheel v2.0                       │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐ │
│  │ Task     │───▶│ Intent   │───▶│ Agent    │───▶│ Result  │ │
│  │ Pool     │    │ Gate     │    │ Select   │    │ Collect │ │
│  └──────────┘    └──────────┘    └──────────┘    └─────────┘ │
│       │                               │                │        │
│       ▼                               ▼                ▼        │
│  ┌──────────┐                  ┌──────────┐    ┌──────────┐ │
│  │ Priority │                  │ Agent    │    │ Output   │ │
│  │ Queue    │                  │ Registry │    │ Store    │ │
│  └──────────┘                  └──────────┘    └──────────┘ │
│                                    │                            │
│                                    ▼                            │
│                             ┌──────────┐                       │
│                             │ Session  │                       │
│                             │ Spawn    │                       │
│                             └──────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

## 成熟特性

### 0. 自我优化任务生成器 🌀 (永不空转)
- **当任务池为空时**：自动生成自优化任务
- **任务完成后**：30%概率再生成新自优化任务
- **每5-10个循环**：提升为更高优先级任务
- **15种自优化任务类型**：
  - 分析飞轮执行效率，提出3个改进点
  - 搜索行业最新AI工作流自动化案例
  - 检查系统健康状态，清理无用日志
  - 研究如何让飞轮更具创造性自我改进
  - ... 等

### 1. 任务依赖图 (Task Dependency Graph)
- 支持 `depends_on` 字段声明前置任务
- 自动拓扑排序确保执行顺序
- 并行分支任务可同时执行

### 2. 优先级队列 (Priority Queue)
- P0/P1/P2/P3 四级优先级
- 权重动态调整
- 任务老化机制（防止饥饿）

### 3. Agent 监管 (Agent Supervision)
- 心跳检测（60秒无响应 = Agent 失联）
- 超时控制（单个任务最大执行时间）
- 自动重试（指数退避：1s → 2s → 4s → 8s → 16s）

### 4. 结果聚合 (Result Aggregation)
- 所有子任务结果汇总到主任务
- 支持 `output_schema` 定义输出格式
- 结果持久化到 JSON 文件

### 5. 人类在环 (Human-in-the-Loop)
- P0 任务需人工审批
- 关键决策点暂停等待输入
- 紧急停止机制

## 任务格式

```markdown
## 任务ID: TASK-001
### 任务名称: 研究 Agent Team 最佳实践
### 优先级: P1
### 执行Agent: explore
### 状态: pending
### 截止时间: 2026-03-22
### 前置任务: TASK-000
### 输出格式: markdown
### 任务描述:
研究 AutoGPT、CrewAI、MetaGPT 的架构设计，
总结 10 个关键设计模式，并输出可复用的实现方案。
### 验收标准:
- [ ] 10 个设计模式已识别
- [ ] 每个模式有代码示例
- [ ] 可直接集成到当前系统
```

## 4 个专业化 Agent

| Agent | 角色 | 任务类型 | 超时 |
|-------|------|---------|------|
| **Explore** | 调研者 | 研究、搜索、分析 | 5min |
| **Hephaestus** | 执行者 | 代码、优化、修复 | 10min |
| **Prometheus** | 规划师 | 计划、设计、文档 | 3min |
| **Sisyphus** | 协调者 | 复杂任务分解 + 多Agent协调 | 15min |

## 使用方法

```bash
# 初始化飞轮
bash scripts/agent-flywheel-v2.sh init

# 添加任务
bash scripts/agent-flywheel-v2.sh add "任务描述" --agent explore --priority P1

# 启动飞轮
bash scripts/agent-flywheel-v2.sh start

# 查看状态
bash scripts/agent-flywheel-v2.sh status

# 单次循环
bash scripts/agent-flywheel-v2.sh cycle
```

## 任务池文件

位置: `.task-pool-v2.md`

## 状态文件

位置: `.flywheel-state-v2.json`

## 与 sessions_spawn 集成

`sessions_spawn` 是 OpenClaw LLM 会话工具，飞轮需要在 LLM 会话内运行。

### LLM 会话内调用方式

```javascript
// Hephaestus 执行
sessions_spawn({
  task: "任务描述",
  label: "flywheel-hephaestus",
  runtime: "subagent",
  mode: "run",
  runTimeoutSeconds: 600
})

// Sisyphus 协调（多 subagent）
sessions_spawn({
  task: "任务描述",
  label: "flywheel-sisyphus", 
  runtime: "subagent",
  mode: "run",
  runTimeoutSeconds: 900
})

// Explore 调研
sessions_spawn({
  task: "研究: ...",
  label: "flywheel-explore",
  runtime: "subagent",
  mode: "run",
  runTimeoutSeconds: 300
})
```

### CLI 模式

对于 CLI 脚本 (`agent-flywheel-v2.sh`)，它作为状态管理器和任务调度器使用，
实际的任务执行需要通过 OpenClaw 会话调用 `sessions_spawn`。

**工作流程:**
1. CLI 脚本管理任务池和状态
2. 在 LLM 会话中调用 `sessions_spawn` 执行实际任务
3. 子 Agent 完成后再调用 CLI 更新状态

## 成熟模式借鉴

### AutoGPT 启发
- 任务分解为子任务
- 递归执行直到完成
- 自我评估 + 迭代优化

### CrewAI 启发
- 多个 Agent 协同工作
- 任务分配给最适合的 Agent
- 最终汇总给 "Manager"

### MetaGPT 启发
- SOP 驱动的 Agent 协作
- 角色专业化
- 代码和文档自动生成

## 输出产物

1. `scripts/agent-flywheel-v2.sh` - 升级版飞轮主脚本
2. `.task-pool-v2.md` - 新任务池格式
3. `.flywheel-state-v2.json` - 增强状态文件
4. `logs/flywheel-v2.log` - 结构化日志
