#!/usr/bin/env python3
"""
browser-use + MiniMax 使用示例

运行前确保:
1. 已运行 ./setup.sh 完成配置
2. Chrome 已启动并监听 9222 端口

用法:
    python example.py "访问百度首页，告诉我Logo文字"
"""

import asyncio
import sys
import os

# 添加脚本目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minimax_llm_wrapper import MiniMaxLLM
from browser_use import Agent
from browser_use.browser import BrowserSession


async def main(task: str):
    """执行浏览器任务"""
    print(f"任务: {task}")
    print("-" * 50)

    # 创建 LLM
    llm = MiniMaxLLM()
    print(f"  模型: {llm.model}")
    print(f"  提供商: {llm.provider}")

    # 连接 Chrome CDP
    session = BrowserSession(
        cdp_url="http://127.0.0.1:9222",
        is_local=True,
    )

    # 创建 Agent
    agent = Agent(
        task=task,
        llm=llm,
        browser_session=session,
    )

    # 执行
    print("\n开始执行...")
    await session.start()
    result = await agent.run()
    await session.stop()

    print("\n" + "=" * 50)
    print("结果:")
    print(result)
    return result


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "访问百度首页，告诉我Logo文字是什么"
    asyncio.run(main(task))