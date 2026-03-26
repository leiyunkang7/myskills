# 🌀 MySkills - 爪爪的 Skills 集合

> 飞轮自进化 + Bugfix 经验沉淀

## 📁 目录结构

```
myskills/
├── SKILL.md                    # 本文件
├── flywheel-evolution/         # 飞轮自进化核心
│   ├── SKILL.md
│   └── ...
├── evolver/                    # 能力进化系统
├── capability-evolver/         # 能力进化框架
├── proactive-agent/            # 主动Agent模式
├── agent-flywheel-advanced/    # 飞轮高级特性
├── iterator-state-sync-bugfix/ # 迭代器状态同步bug
└── regex-datetime-bugfix/     # 正则日期时间bug
```

## 🌀 飞轮自进化核心原则

**"每轮迭代都更强。"**

- **闭环反馈**：执行 → 结果记录 → 问题发现 → 自我修复/优化 → 进入下一轮
- **复利效应**：小改进持续累积，长期产生质变
- **最小阻力**：自动选择代价最低的改进路径

## 🛡️ 安全护栏

| 风险 | 防护措施 |
|------|---------|
| 失控风险 | 最大并发 ≤3、最大运行时间限制 |
| 破坏性变更 | credentials 目录只读保护 |
| 递归退化 | 自修改文件校验和保护 |
| 资源配额 | 磁盘阈值告警(75%)、内存限制 |

## 📝 经验教训

### 1. 飞轮任务池与JSON队列同步脱节
**教训：** 多个数据源消费同一批任务时，必须有同步机制

### 2. 正则表达式处理日期/时间
**教训：** 时间计算用 Python/datetime，不用正则表达式

### 3. 状态文件与任务池不同步
**教训：** 任何修改任务池的操作，都应立即同步状态

## 🚀 快速开始

```bash
# 查看飞轮状态
bash scripts/flywheel/flywheel-evolution-core.sh status

# 执行自进化检查
bash scripts/flywheel/flywheel-evolution-core.sh run

# 自发探索
bash scripts/flywheel/flywheel-spontaneous-finder.sh run
```
