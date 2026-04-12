# Iterator State Sync Bugfix Skill

## 问题描述

**症状：** 迭代器状态文件 (`.recipe-iterator-state.json`) 显示 `pending_tasks: 0`，但任务池文件 (`.recipe-iteration-tasks.md`) 实际有多个待处理任务。

**影响：** 迭代器读取状态文件发现 0 个待处理任务，判定"任务池空"并跳过执行，导致迭代器停转。

---

## 根因

状态文件只在**迭代结束时**更新，但任务可能在**迭代之间**被添加（如 task seeder、requirements analyst）。如果状态文件在某次迭代结束时写入 0，然后 seeder 添加了新任务，状态文件不会同步更新。

```
时序：
1. T1: 迭代结束，pending=0，写入状态文件
2. T2: Seeder 添加 5 个任务（状态文件未更新！）
3. T3: 迭代器启动，读到 pending=0，跳过执行 ← BUG
```

---

## 修复方案

### 方案：状态文件实时同步

**原则：** 每次任务池发生变化时，立即更新状态文件。

**修改点：**

1. **`add_task()`** - 添加任务后调用 `sync_state_from_pool()`

2. **`complete_task()`** - 完成任务后调用 `sync_state_from_pool()`

3. **`fail_task()`** - 任务失败后调用 `sync_state_from_pool()`

4. **`save_state()`** - 重用 `sync_state_from_pool()` 确保一致性

### 新增函数

```bash
sync_state_from_pool() {
    # 使用 Python 可靠计算pending/completed/failed数量
    pending=$(python3 -c "print(len([l for l in open('$TASK_POOL').read().splitlines() if l.startswith('- [ ]')]))")
    completed=$(python3 -c "print(len([l for l in open('$TASK_POOL').read().splitlines() if l.startswith('- [x]')]))")
    failed=$(python3 -c "print(len([l for l in open('$TASK_POOL').read().splitlines() if l.startswith('! ')]))")
    
    # 写入状态文件
    cat > "$STATE_FILE" << EOF
{
    "pending_tasks": $pending,
    "completed_tasks": $completed,
    ...
}
EOF
}
```

---

## 经验教训

### 何时容易引入此 Bug

- 状态文件只在单一入口更新（迭代结束时）
- 多个数据源可以修改任务池（seeder、analyst、手动）
- 状态文件被用作"快速判断"而非每次从源头计算

### 预防原则

1. **写入时同步** - 任何修改任务池的操作，都应立即更新状态
2. **单一数据源** - 如果可以，每次读取都从任务池重新计算
3. **状态验证** - 迭代开始前，验证状态文件与实际任务池是否一致

### 检查清单

- [ ] 添加任务后是否更新状态文件？
- [ ] 完成/失败任务后是否更新状态文件？
- [ ] Seeder/Analyst 添加任务后是否更新状态文件？
- [ ] 状态文件的 pending_tasks 是否与任务池实际一致？

---

## 相关文件

- `scripts/recipe-app-iterator/iterator-state.sh` - 状态管理模块
- `scripts/recipe-app-iterator/modules/07-analyst.sh` - 需求分析师
- `.recipe-iterator-state.json` - 状态文件
- `.recipe-iteration-tasks.md` - 任务池文件

---

## 验证方法

```bash
# 检查状态文件
cat .recipe-iterator-state.json | jq '.pending_tasks'

# 检查任务池实际数量
grep -c "^- \[ \]" .recipe-iteration-tasks.md

# 应该一致！
```
