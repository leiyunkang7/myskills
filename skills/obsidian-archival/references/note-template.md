# Obsidian 笔记模板

## 标准结构

```markdown
# <标题>

## 问题

<具体报错或症状>

## 根本原因

<为什么出错，不是表面现象>

## 解决方法

<具体的配置/命令/步骤>

## 未来怎么办

<这个解决方案对后续有何影响>

## 诊断命令

```bash
# <命令1>
<输出>

# <命令2>
<输出>
```

## 标签

#标签1 #标签2
```

## 示例

```markdown
# nushell 配置：npm 全局路径

## 问题

使用 `npm i -g bun` 安装 bun 后，在 nushell 中运行 `bun -v` 报错：
```
Command `bun` not found
```

但 bun 确实已经安装了。

## 根本原因

npm 全局安装路径 `C:\Users\leiyu\AppData\Roaming\npm` 没有被加入 nushell 的 PATH。

Windows 上 npm 装全局工具时不会自动更新系统 PATH，而 nushell 读不到 Windows 系统 PATH 的变化。

## 解决方法

编辑 nushell 配置文件：

路径：`C:\Users\leiyu\AppData\Roaming\nushell\config.nu`

在 PATH 列表中加入 npm 目录：

```nushell
$env.PATH = [
    "C:/Users/leiyu/hermes-venv/Scripts"
    "C:/Users/leiyu/.local/bin"
    "C:/Users/leiyu/AppData/Roaming/npm"
    ...$env.PATH
]
```

重启 nushell 或执行 `config nu` 重新加载配置。

## 未来怎么办

不需要额外操作。所有全局安装的包都会放到 `AppData\Roaming\npm` 目录，只要这个目录在 PATH 中，所有全局包都能直接用。

## 诊断命令

```bash
# 查看 npm 全局路径
npm config get prefix

# 查看 bun 是否存在于该目录
ls "$HOME/AppData/Roaming/npm/" | grep bun
```

## 标签

#nushell #windows #npm #环境配置
```

## 注意事项

- Windows MSYS/Git-Bash 环境：bash 会展开 `$VAR`、反引号等，直接用 bash 传 content 会导致内容被破坏
- 用 `write_file` 直接写到 vault 目录下的目标路径
- vault 默认位置：`C:/code/note`
- 代码块用三个反引号包裹，注明语言类型（nushell、bash、json 等）
- 标题用 `H1`（`#`），章节用 `H2`（`##`）
