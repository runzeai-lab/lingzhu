#!/usr/bin/env python3
"""
小红书自动发布脚本 V3.0
- 使用原生 Playwright，不依赖 agent-browser 技能
- 完全自动化（除了扫码登录）
- 符合小红书用户阅读习惯
"""

import asyncio
import json
import time
from pathlib import Path

async def publish_to_xiaohongshu():
    """自动发布笔记到小红书"""
    
    print("🚀 小红书自动发布脚本 V3.0")
    print("=" * 50)
    
    # 1. 启动 Playwright
    print("\n📂 步骤1：启动浏览器...")
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        # 启动浏览器（显示界面，方便扫码）
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器界面
            args=['--start-maximized']  # 最大化窗口
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # 2. 打开小红书创作者平台
        print("📂 步骤2：打开小红书创作者平台...")
        await page.goto('https://creator.xiaohongshu.com/publish/publish')
        await page.wait_for_load_state('networkidle')
        
        # 3. 检查登录状态
        print("📂 步骤3：检查登录状态...")
        
        # 等待页面加载
        await asyncio.sleep(3)
        
        # 检查是否需要登录
        if 'login' in page.url or await page.locator('text=扫码登录').count() > 0:
            print("⚠️  需要登录！请使用小红书APP扫描二维码...")
            print("⏳ 等待扫码登录（最多120秒）...")
            
            # 等待登录成功（检测 URL 变化）
            try:
                await page.wait_for_url('**/publish**', timeout=120000)
                print("✅ 登录成功！")
            except:
                print("❌ 登录超时！请手动扫码后继续...")
                await asyncio.sleep(60)  # 再等60秒
        
        # 4. 点击"上传图文"
        print("\n📝 步骤4：点击'上传图文'...")
        await asyncio.sleep(2)
        
        # 尝试多种选择器
        upload_buttons = [
            'text=上传图文',
            'button:has-text("上传图文")',
            '[class*="upload"][class*="image"]',
        ]
        
        clicked = False
        for selector in upload_buttons:
            try:
                await page.click(selector, timeout=3000)
                clicked = True
                print(f"✅ 成功点击：{selector}")
                break
            except:
                continue
        
        if not clicked:
            print("⚠️  未找到'上传图文'按钮，截图调试...")
            await page.screenshot(path='E:/WorkBuddy/Claw/debug_click.png')
            print("📸 截图已保存：debug_click.png")
        
        # 等待页面跳转
        await asyncio.sleep(3)
        await page.wait_for_load_state('networkidle')
        
        # 5. 填写标题
        print("\n📝 步骤5：填写标题...")
        title = "颂钵疗愈 |  Day 1 遇见颂钵的奇妙旅程 ✨"
        
        title_selectors = [
            'input[placeholder*="标题"]',
            'input[class*="title"]',
            '#title',
        ]
        
        for selector in title_selectors:
            try:
                await page.fill(selector, title, timeout=3000)
                print(f"✅ 标题已填写：{title}")
                break
            except:
                continue
        
        # 6. 填写正文
        print("\n📝 步骤6：填写正文...")
        
        content = """今天想和大家分享一个特别的故事 —— 我是如何遇见颂钵，以及它如何改变了我的生活。

🪷 初遇颂钵

那是一个疲惫的傍晚，我被朋友拉去了一场颂钵音疗会。说实话，一开始我是拒绝的。"不就是敲个碗吗？能有什么特别的？"

但当声音响起的瞬间，我感受到了一种从未有过的震动 —— 不是耳朵听到的，而是整个身体感受到的。

✨ 颂钵是什么？

颂钵（Singing Bowl），源于喜马拉雅山区，原本是日常生活用的食器，后来被发现具有极佳的音频疗愈功能。

它的声音频率可以：
• 快速进入放松状态 🧘‍♀️
• 平衡左右脑，提升专注力 🧠
• 释放积压的情绪和压力 💆‍♀️
• 改善睡眠质量 🌙

🙏 我的变化

坚持颂钵冥想 30 天后：
✅ 焦虑感明显减少
✅ 睡眠质量提升（深睡时间增加）
✅ 专注力更强（工作效率和创造力都提升了）

💡 给新手的建议

如果你也想尝试颂钵疗愈：
1️⃣ 找个安静的空间（不需要完全静音）
2️⃣ 选择固定时间（建议睡前 30 分钟）
3️⃣ 保持开放心态（不要带着"要见效"的期待）

🌟 写在最后

颂钵不是魔法，但它确实为我打开了一扇门 —— 通往内在平静的门。

如果你也想尝试，欢迎在评论区告诉我，我可以分享我的入门经验～

#颂钵疗愈 #音疗 #冥想 #放松 #身心健康 #瑜伽生活 #内在探索

（本内容由 AI 辅助创作）

📸 配图说明：6张竖版图片，展示颂钵、冥想场景、疗愈空间等。"""

        content_selectors = [
            'div[contenteditable="true"]',
            'textarea[placeholder*="正文"]',
            '.ql-editor',
        ]
        
        for selector in content_selectors:
            try:
                await page.fill(selector, content, timeout=3000)
                print(f"✅ 正文已填写（{len(content)} 字符）")
                break
            except:
                continue
        
        # 7. 上传图片
        print("\n📝 步骤7：上传图片...")
        
        image_dir = Path('E:/WorkBuddy/Claw/xiaohongshu_images')
        image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))
        
        if image_files:
            print(f"📂 找到 {len(image_files)} 张图片")
            
            # 查找文件上传输入框
            file_input_selectors = [
                'input[type="file"]',
                'input[accept*="image"]',
            ]
            
            for selector in file_input_selectors:
                try:
                    # 设置文件
                    await page.set_input_files(selector, [str(f) for f in image_files[:6]])
                    print(f"✅ 已上传 {min(6, len(image_files))} 张图片")
                    break
                except:
                    continue
        else:
            print("⚠️  未找到图片文件，跳过上传")
        
        # 8. 添加标签
        print("\n📝 步骤8：添加标签...")
        tags = ["#颂钵疗愈", "#音疗", "#冥想", "#放松", "#身心健康", "#瑜伽生活"]
        
        # 小红书的标签通常在正文中用 # 表示，不需要单独添加
        print(f"✅ 标签已包含在正文中：{', '.join(tags)}")
        
        # 9. 截图预览
        print("\n📸 步骤9：截图预览...")
        await page.screenshot(path='E:/WorkBuddy/Claw/debug_preview.png', full_page=True)
        print("📸 预览截图已保存：debug_preview.png")
        
        # 10. 点击发布（暂停，等待用户确认）
        print("\n⚠️  步骤10：准备发布...")
        print("⏸️  已暂停！请手动检查内容，确认无误后按 Enter 继续...")
        input("按 Enter 继续发布...")
        
        publish_selectors = [
            'button:has-text("发布")',
            'button:has-text("立即发布")',
            '.publish-btn',
        ]
        
        for selector in publish_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ 已点击发布按钮")
                break
            except:
                continue
        
        # 等待发布完成
        await asyncio.sleep(5)
        
        # 11. 验证发布成功
        print("\n✅ 步骤11：验证发布结果...")
        await page.screenshot(path='E:/WorkBuddy/Claw/debug_result.png')
        print("📸 结果截图已保存：debug_result.png")
        
        # 检查是否跳转到笔记管理页面
        if 'note' in page.url or 'manage' in page.url:
            print("🎉 发布成功！已跳转到笔记管理页面")
        else:
            print("⚠️  未检测到成功提示，请手动确认")
        
        print("\n" + "=" * 50)
        print("🎉 发布流程完成！")
        print("=" * 50)
        
        # 保持浏览器打开（方便查看结果）
        print("\n💡 浏览器保持打开状态，按 Ctrl+C 退出...")
        await asyncio.sleep(300)

if __name__ == '__main__':
    asyncio.run(publish_to_xiaohongshu())
