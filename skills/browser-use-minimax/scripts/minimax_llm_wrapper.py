"""
MiniMax LLM Wrapper for browser-use
过滤 thinking 内容: <think>...</think>

用法:
    from minimax_llm_wrapper import MiniMaxLLM

    llm = MiniMaxLLM(api_key="your-api-key")
    agent = Agent(task="...", llm=llm, browser_session=session)
"""

import re
import os
import json
from typing import Any
from browser_use import ChatOpenAI
from browser_use.llm.base import BaseChatModel
from browser_use.llm.exceptions import ModelProviderError
from browser_use.llm.views import ChatInvokeCompletion


class MiniMaxLLM(BaseChatModel):
    """Wrapper that strips <think>...</think> tags from MiniMax responses

    MiniMax API 返回的 thinking 内容会混入 JSON 输出，导致 schema 验证失败。
    此 wrapper 在 JSON 解析前过滤掉所有 thinking 标签。
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "MiniMax-M2.7-highspeed",
        base_url: str = "https://api.minimaxi.com/v1",
        config_path: str = "~/.claude/settings.json",
    ):
        """
        初始化 MiniMax LLM wrapper

        Args:
            api_key: MiniMax API key。如果不提供，从 config_path 读取。
            model: 模型名称，默认 MiniMax-M2.7-highspeed
            base_url: API 端点。
                - 中国版: https://api.minimaxi.com/v1
                - 国际版: https://api.minimax.io/v1
            config_path: Claude Code 配置路径，从中读取 api_key
        """
        if api_key is None:
            config_path = os.path.expanduser(config_path)
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config["env"]["ANTHROPIC_AUTH_TOKEN"]

        if api_key is None:
            raise ValueError("api_key is required")

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
        """调用 LLM 并过滤 thinking 内容"""
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
                    message=f'JSON parse error after filtering thinking: {e}\nFiltered text was: {text[:500]}',
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


def get_default_llm() -> MiniMaxLLM:
    """从 Claude Code 配置创建默认 LLM 实例"""
    return MiniMaxLLM()


if __name__ == "__main__":
    import asyncio
    from browser_use.llm.messages import UserMessage

    async def test():
        print("测试 MiniMax LLM Wrapper...")
        llm = get_default_llm()
        print(f"  Provider: {llm.provider}")
        print(f"  Model: {llm.model}")

        messages = [UserMessage(content='请用中文回复: 你好')]
        result = await llm.ainvoke(messages)
        print(f"  响应: {result.completion[:100]}...")
        print("✅ 测试通过!")

    asyncio.run(test())