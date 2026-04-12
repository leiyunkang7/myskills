# Regex DateTime Bugfix Skill

## 问题描述

**症状：** `opportunity-scan.sh` 误报"48小时+陈旧任务"。实际上没有陈旧任务，但脚本反复生成告警。

**根因：** 正则表达式用 `[0-2][0-9]-` 匹配小时，但匹配到了日期中的数字。

```bash
# BUGGY: [0-2][0-9]- 匹配日期 "2026-03-26" 中的 "26"
# 任何在 26 号添加的任务都被误判为 48h+
grep -c '^- \[ \] \[.*\] .* | 添加:.*[0-2][0-9]-'
```

---

## 修复方案

**原则：** 时间计算用 Python/datetime，不用正则表达式。

```python
from datetime import datetime, timedelta

def is_stale(date_str, hours=48):
    """判断任务是否陈旧（超过指定小时数）"""
    try:
        # 解析 "2026-03-26 12:00" 格式
        task_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        age = datetime.now() - task_time
        return age.total_seconds() > hours * 3600
    except:
        return False
```

---

## 经验教训

### 何时容易引入此 Bug

- 用正则表达式处理日期/时间
- 期望用字符类匹配数字范围（如 `[0-9]` 配日期中的 `26`）
- 缺乏测试覆盖的时间相关逻辑

### 预防原则

1. **时间计算用专用库** - Python `datetime` / JavaScript `Date` / Shell `date`
2. **正则只用于模式匹配** - 不用于数值计算或日期解析
3. **测试边界条件** - 测试 01-09 点、月末、年末等特殊情况

### 检查清单

- [ ] 时间计算是否用了专用库而非正则？
- [ ] 是否测试了边界情况（00:00、月末、年末）？
- [ ] 错误处理是否处理了非法日期格式？

---

## 相关文件

- `scripts/opportunity-scan.sh` - 有问题的脚本
- `.task-pool.md` - 任务池文件

---

## 验证方法

```bash
# 测试正则是否误判
echo "2026-03-26 08:00" | grep -E '[0-2][0-9]-'
# 会匹配到 "26"，导致误判

# 用 Python 正确判断
python3 -c "
from datetime import datetime
task_time = datetime.strptime('2026-03-26 08:00', '%Y-%m-%d %H:%M')
age = (datetime.now() - task_time).total_seconds() / 3600
print(f'Age: {age:.1f} hours')
"
```
