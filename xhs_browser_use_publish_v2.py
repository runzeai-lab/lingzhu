#!/usr/bin/env python3
"""
小红书自动发布脚本 v2 - 使用 browser-use AI代理（不依赖 skills 模块）
"""
import asyncio
import os
import sys

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
    
    # 任务描述（给 AI Agent 的指令）
    task = f"""
    你是一个小红书自动发布助手。请完成以下任务：
    
    1. 打开浏览器，访问 https://creator.xiaohongshu.com/publish/publish
    2. 如果页面显示登录界面，请等待60秒让用户扫码登录
    3. 登录成功后，找到并点击"上传图文"按钮
    4. 上传图片文件：{image_path}
       - 可能需要点击"选择文件"按钮，然后输入文件路径
       - 或者使用拖拽方式上传
    5. 填写标题输入框，标题为：{title}
    6. 填写正文输入框，正文为：{body}
    7. 点击"添加话题"按钮（或话题图标），添加以下话题：
       #颂钵
       #身心灵放松
       #解压颂钵音
       #疗愈的力量
       #将冥想带入生活
    8. 找到并点击红色的"发布"按钮
       - 如果普通点击不生效，尝试使用 JavaScript 点击：document.querySelector('button.el-button--primary').click()
       - 或者尝试按 Ctrl+Enter 快捷键
    9. 等待页面显示"发布成功"提示或跳转到笔记管理页面
    10. 返回成功消息
    
    注意：
    - 使用人类化的操作速度（不要过快）
    - 每个动作之间等待1-2秒
    - 如果找不到元素，尝试使用不同的选择器
    - 确保点击"发布"按钮后等待页面响应（最多30秒）
    - 如果遇到验证码，暂停并提示用户手动完成
    """
    
    print("🚀 启动 browser-use Agent...")
    
    try:
        # 导入 browser-use
        from browser_use import Agent, BrowserSession
        from langchain_openai import ChatOpenAI
        
        print("✅ 成功导入 browser-use 模块")
        
        # 创建 LLM（需要 OPENAI_API_KEY 环境变量）
        # 如果没有 OpenAI API key，可以使用其他 LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1
        )
        print("✅ 使用 OpenAI LLM")
        
        # 创建浏览器会话（不使用 stealth_session，避免依赖 skills 模块）
        session = BrowserSession(
            headless=False,  # 显示浏览器，方便调试
            browser_type='chromium'
        )
        print("✅ 创建浏览器会话（非 headless 模式）")
        
        # 创建 Agent
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=session,
            max_actions_per_step=10  # 每步最多10个动作
        )
        
        print("🤖 Agent 已创建，开始执行任务...")
        print("=" * 60)
        
        # 运行 Agent
        result = await agent.run()
        
        print("=" * 60)
        print("✅ 任务执行完成")
        final_result = result.final_result()
        print(f"结果: {final_result}")
        
        return final_result
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装必要的包：")
        print("  pip install browser-use langchain-openai")
        return None
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("小红书自动发布脚本 v2（使用 browser-use）")
    print("=" * 60)
    print()
    
    # 检查环境变量
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("⚠️ 未设置 OPENAI_API_KEY 环境变量")
        print("将尝试使用其他 LLM...")
        print()
    
    # 运行异步函数
    result = asyncio.run(publish_xiaohongshu())
    
    print()
    print("=" * 60)
    if result:
        print("✅ 发布成功！")
        print(result)
    else:
        print("❌ 发布失败，请检查错误信息")
        print("可能的原因：")
        print("  1. 未设置 OPENAI_API_KEY 环境变量")
        print("  2. 浏览器驱动问题")
        print("  3. 小红书页面结构变化")
        print("  4. 网络问题")
    print("=" * 60)
