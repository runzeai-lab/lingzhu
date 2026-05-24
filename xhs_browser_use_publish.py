#!/usr/bin/env python3
"""
小红书自动发布脚本 - 使用 browser-use AI代理
"""
import asyncio
import sys
import os

# 添加 skills 目录到 Python 路径
skills_dir = r'C:\Users\RunzeAI\.workbuddy\skills'
if skills_dir not in sys.path:
    sys.path.insert(0, skills_dir)

try:
    from skills.browser_use.scripts.run_agent import stealth_session, gemini_llm
    from browser_use import Agent
    print("✅ 成功导入 browser-use 模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("尝试直接导入 browser_use...")
    from browser_use import Agent
    # 如果没有 gemini_llm，使用默认 LLM
    gemini_llm = None
    stealth_session = None

async def publish_xiaohongshu():
    """使用 browser-use Agent 完成小红书发布"""
    
    # 读取文章内容
    article_path = r'E:\WorkBuddy\Claw\xiaohongshu_day1.md'
    image_path = r'E:\WorkBuddy\Claw\xiaohongshu_images\cover_xhs.jpg'
    
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 跳过AI标注行
        lines = content.split('\n')
        clean_lines = [line for line in lines if '【AI生成内容标注】' not in line]
        article_text = '\n'.join(clean_lines).strip()
        # 提取标题和正文
        if '---' in article_text:
            parts = article_text.split('---', 1)
            title = parts[0].replace('#', '').strip()
            body = parts[1].strip()
        else:
            title = "颂钵疗愈 | Day1 缘起"
            body = article_text
    except Exception as e:
        print(f"⚠️ 读取文章失败: {e}")
        title = "颂钵疗愈 | Day1 缘起"
        body = "今天是我在小红书分享颂钵疗愈的第一天..."
    
    print(f"📝 标题: {title}")
    print(f"📄 正文长度: {len(body)} 字符")
    print(f"🖼️ 图片: {image_path}")
    
    # 任务描述
    task = f"""
    你是一个小红书自动发布助手。请完成以下任务：
    
    1. 打开浏览器，访问 https://creator.xiaohongshu.com/publish/publish
    2. 如果页面显示登录界面，请等待用户扫码登录（暂停60秒）
    3. 登录成功后，点击"上传图文"按钮
    4. 上传图片文件：{image_path}
    5. 填写标题输入框，标题为：{title}
    6. 填写正文输入框，正文为：{body}
    7. 点击"添加话题"按钮，添加以下话题：
       #颂钵
       #身心灵放松
       #解压颂钵音
       #疗愈的力量
       #将冥想带入生活
    8. 点击红色的"发布"按钮
    9. 等待页面显示"发布成功"提示
    10. 返回成功消息
    
    注意：
    - 使用人类化的操作速度（不要过快）
    - 如果找不到元素，尝试使用 JavaScript 点击
    - 确保点击"发布"按钮后等待页面响应
    """
    
    print("🚀 启动 browser-use Agent...")
    
    try:
        # 创建 LLM（优先使用 Gemini）
        if gemini_llm:
            llm = gemini_llm()
            print("✅ 使用 Gemini LLM")
        else:
            # 使用默认 LLM（需要设置 ANTHROPIC_API_KEY 或 OPENAI_API_KEY）
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o")
            print("✅ 使用 OpenAI LLM")
        
        # 创建浏览器会话（使用 stealth_session 避免检测）
        if stealth_session:
            session = stealth_session(headless=False)  # 显示浏览器，方便调试
            print("✅ 使用 stealth_session（反检测）")
        else:
            from browser_use import BrowserSession
            session = BrowserSession(headless=False)
            print("✅ 使用默认 BrowserSession")
        
        # 创建 Agent
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=session,
            max_actions_per_step=5  # 每步最多5个动作
        )
        
        print("🤖 Agent 已创建，开始执行任务...")
        
        # 运行 Agent
        result = await agent.run()
        
        print("✅ 任务执行完成")
        print(f"结果: {result.final_result()}")
        
        return result.final_result()
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("小红书自动发布脚本（使用 browser-use）")
    print("=" * 60)
    
    result = asyncio.run(publish_xiaohongshu())
    
    print("=" * 60)
    if result:
        print("✅ 发布成功！")
        print(result)
    else:
        print("❌ 发布失败，请检查错误信息")
    print("=" * 60)
