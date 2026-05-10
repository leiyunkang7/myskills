---
name: obsidian-archival
description: "归档经验到 Obsidian 笔记库。当用户要求将解决方案、经验、踩坑记录等内容保存到 Obsidian 时触发。处理：从问题分析到笔记创建的完整流程，包括诊断、解决方案、经验总结，并自动生成标签。When the user says: 归档, 保存到 Obsidian, 记到笔记, 写进 Obsidian or similar requests to save experience/knowledge to Obsidian."
---

# Obsidian Archival

将问题解决过程和经验归档到 Obsidian 笔记库。

## 工作流程

### Step 1: 诊断与理解

先用工具（terminal / read_file / search_files / web_search 等）弄清问题的根本原因，不能只记录表面现象。

### Step 2: 写笔记

笔记路径：`C:/code/note/<标题>.md`

**关键原则：直接写到 vault 目录，不用 bash 命令传递 content。** bash 会展开变量和反引号，导致内容被破坏。

写笔记正确方式：
```
write_file(path="C:/code/note/<标题>.md", content="# 标题\n\n正文...")
```

### Step 3: 内容结构

每个归档笔记应包含：

1. **问题描述** - 具体报错或症状
2. **根本原因** - 为什么出错，不是表面现象
3. **解决方法** - 具体的配置/命令/步骤
4. **未来怎么办** - 这个解决方案对后续有何影响
5. **诊断命令** - 帮助日后排查的相关命令
6. **标签** - `#标签1 #标签2` 格式

### Step 4: 验证

用 `obsidian vault=<vault> read file=<标题>` 验证内容正确。

### Step 5: 清理残留

如果之前 bash 方式创建了内容错误的笔记，删除它：
```
obsidian vault=<vault> delete file=<标题>
```

## 注意事项

- Windows MSYS/Git-Bash 环境：bash 会展开 `$VAR`、反引号、换行符等，直接用 `content=$(cat file)` 方式传 content 会导致内容被破坏
- 正确做法：用 `write_file` 写到 vault 目录下的目标路径
- vault 默认位置：`C:/code/note`
- 诊断性内容（`npm config get prefix`、`ls`、`echo $PATH` 等输出）可以帮助理解问题，应该包含在笔记中

## 参考

- 笔记模板结构参考：[references/note-template.md](references/note-template.md)
