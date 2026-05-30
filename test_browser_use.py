"""测试 browser-use 技能 - 打开小红书创作者平台"""

import asyncio
from skills.browser_use.scripts.run_agent import stealth_session, gemini_llm
from browser_use import Agent


async def test_xiaohongshu():
    """测试打开小红书"""
    print("🚀 启动 browser-use (AI 驱动浏览器)...")
    
    # 使用 Gemini LLM（免费，通过 Google Cloud Code Assist）
    llm = gemini_llm()
    
    # 使用 stealth_session（反检测）
    session = stealth_session(headless=False)
    
    # 创建 Agent，给它任务
    agent = Agent(
        task="打开 https://creator.xiaohongshu.com/publish/publish 并等待页面加载完成",
        llm=llm,
        browser_session=session
    )
    
    # 运行 Agent
    result = await agent.run()
    
    print(f"✅ 任务完成: {result}")
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("测试 browser-use 技能")
    print("=" * 60)
    print()
    
    try:
        result = asyncio.run(test_xiaohongshu())
        print(f"\n📝 结果: {result}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
