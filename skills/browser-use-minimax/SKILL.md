---
name: browser-use-minimax
description: Configure browser-use with MiniMax API (OpenAI-compatible) for browser automation. Use this skill when user wants to set up browser-use with MiniMax LLM, or when configuring browser-use with custom OpenAI-compatible endpoints. Handles the MiniMax thinking content filtering, WebSocket compatibility, and Chrome CDP setup.
---

# browser-use + MiniMax 配置

本 skill 封装了 browser-use 与 MiniMax API 对接的完整配置流程。

## 核心问题

MiniMax API (OpenAI-compatible) 返回的 thinking 内容 (<think>...</think>) 会混入 JSON 输出，导致 browser-use 的 JSON schema 验证失败。需要创建 wrapper 过滤 thinking 内容。

## 完整配置步骤

### 1. 安装 browser-use

```bash
pipx install browser-use
```

### 2. 安装 playwright 到 browser-use venv

```bash
/root/.local/share/pipx/venvs/browser-use/bin/python -m pip install playwright
```

### 3. 降级 websockets (关键!)

WebSocket 兼容性问题，必须降级到 13.x:

```bash
/root/.local/share/pipx/venvs/browser-use/bin/python -m pip install "websockets<14"
```

### 4. 启动 Xvfb (无头浏览器环境)

```bash
# 检查是否已运行
pgrep -f "Xvfb :99" || Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99
```

### 5. 启动 Chrome (headless)

browser-use 的内置浏览器启动有问题，需手动启动:

```bash
CHROME_PATH=$(find ~/.cache/ms-playwright -name "chrome" -type f 2>/dev/null | grep "chromium-1217" | head -1)

nohup $CHROME_PATH \
  --headless=new \
  --no-sandbox \
  --disable-setuid-sandbox \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-test > /tmp/chrome.log 2>&1 &

sleep 3
```

验证 CDP 可用:
```bash
curl -s http://127.0.0.1:9222/json/version
```

## MiniMax LLM Wrapper

创建 `minimax_llm_wrapper.py`:

```python
"""
MiniMax LLM Wrapper for browser-use
过滤 thinking 内容: <think>...</think>
"""
import re
from typing import Any
from browser_use import ChatOpenAI
from browser_use.llm.base import BaseChatModel
from browser_use.llm.exceptions import ModelProviderError
from browser_use.llm.views import ChatInvokeCompletion


class MiniMaxLLM(BaseChatModel):
    """Wrapper that strips <think>...</think> tags from MiniMax responses"""

    def __init__(self, api_key: str, model: str = "MiniMax-M2.7-highspeed",
                 base_url: str = "https://api.minimaxi.com/v1"):
        self.llm = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key=api_key,
        )
        self.thinking_pattern = re.compile(r'<think>.*?</think>', re.DOTALL)

    @property
    def provider(self) -> str:
        return self.llm.provider

    @property
    def model(self) -> str:
        return self.llm.model

    async def ainvoke(self, messages: list, output_format: Any = None, **kwargs) -> ChatInvokeCompletion:
        if output_format is not None:
            kwargs_copy = dict(kwargs)
            kwargs_copy.pop('output_format', None)
            result = await self.llm.ainvoke(messages, output_format=None, **kwargs_copy)
            text = result.completion if isinstance(result.completion, str) else str(result.completion)
            text = self.thinking_pattern.sub('', text).strip()
            try:
                parsed = output_format.model_validate_json(text)
                return ChatInvokeCompletion(
                    completion=parsed,
                    usage=result.usage,
                    stop_reason=result.stop_reason,
                )
            except Exception as e:
                raise ModelProviderError(
                    message=f'JSON parse error: {e}\nText was: {text[:500]}',
                    status_code=500,
                    model=self.model
                )
        else:
            result = await self.llm.ainvoke(messages, output_format=None, **kwargs)
            text = result.completion if isinstance(result.completion, str) else str(result.completion)
            text = self.thinking_pattern.sub('', text).strip()
            return ChatInvokeCompletion(
                completion=text,
                usage=result.usage,
                stop_reason=result.stop_reason,
            )
```

## 使用方法

```python
import asyncio
import json
from browser_use import Agent
from browser_use.browser import BrowserSession
from minimax_llm_wrapper import MiniMaxLLM

# 从 Claude Code 配置读取 MiniMax API Key
with open("/root/.claude/settings.json") as f:
    config = json.load(f)
    api_key = config["env"]["ANTHROPIC_AUTH_TOKEN"]

llm = MiniMaxLLM(api_key=api_key)

session = BrowserSession(
    cdp_url="http://127.0.0.1:9222",
    is_local=True,
)

agent = Agent(
    task="访问百度首页,告诉我页面上显示的Logo文字是什么",
    llm=llm,
    browser_session=session,
)

async def run():
    await session.start()
    result = await agent.run()
    await session.stop()
    return result

asyncio.run(run())
```

## MiniMax API 配置

| 配置项 | 值 |
|--------|-----|
| API 端点 | `https://api.minimaxi.com/v1` (中国版) |
| | `https://api.minimax.io/v1` (国际版) |
| 模型 | `MiniMax-M2.7-highspeed` |
| API Key 来源 | `~/.claude/settings.json` → `env.ANTHROPIC_AUTH_TOKEN` |

## 已知限制

1. **JSON Schema 不匹配** - MiniMax 输出的 JSON 格式与 browser-use 期望的 AgentOutput schema 有细微差异，某些复杂任务可能失败
2. **需要预启动 Chrome** - browser-use 的内置浏览器启动有问题，必须手动启动 Chrome 并通过 CDP 连接
3. **每次运行前检查 Chrome** - 如果 Chrome 崩溃退出，需要重新启动

## 快速验证脚本

```bash
# 验证 API 连接
curl -s http://127.0.0.1:9222/json/version && echo "CDP OK"

# 测试 MiniMax API
/root/.local/share/pipx/venvs/browser-use/bin/python -c "
from browser_use import ChatOpenAI
from browser_use.llm.messages import UserMessage
import asyncio
async def test():
    llm = ChatOpenAI(
        model='MiniMax-M2.7-highspeed',
        base_url='https://api.minimaxi.com/v1',
        api_key='YOUR_API_KEY',
    )
    result = await llm.ainvoke([UserMessage(content='Say hello in Chinese')])
    print(result.completion[:100])
asyncio.run(test())
"
```

## 一键配置脚本

保存为 `setup_browser_use_minimax.sh`:

```bash
#!/bin/bash
set -e

# 安装 browser-use
pipx install browser-use 2>/dev/null || true

# 安装 playwright
VENV_PATH=$(find ~/.local/share/pipx/venvs -name "browser-use" -type d 2>/dev/null | head -1)
"$VENV_PATH/bin/python" -m pip install playwright --quiet 2>/dev/null || true

# 降级 websockets
"$VENV_PATH/bin/python" -m pip install "websockets<14" --quiet 2>/dev/null || true

# 启动 Xvfb
pgrep -f "Xvfb :99" || Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99

# 启动 Chrome
pgrep -f "chrome-linux64/chrome" || \
  nohup ~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome \
    --headless=new --no-sandbox --disable-setuid-sandbox \
    --disable-dev-shm-usage --remote-debugging-port=9222 \
    --user-data-dir=/tmp/chrome-test > /tmp/chrome.log 2>&1 &

sleep 3
curl -s http://127.0.0.1:9222/json/version && echo " ✅ 配置完成"
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| `InvalidMessage: did not receive a valid HTTP response` | 降级 websockets 到 <14 |
| Chrome 启动失败 `libGLESv2.so Permission denied` | 使用 `--disable-dev-shm-usage` 和 `xvfb-run` |
| CDP 连接失败 | 检查 `curl http://127.0.0.1:9222/json/version` 是否返回 JSON |
| JSON 解析错误 `invalid json at position 0` | MiniMax thinking 内容未过滤，检查 wrapper 是否正确工作 |