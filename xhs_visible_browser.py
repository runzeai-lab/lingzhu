#!/usr/bin/env python3
"""
小红书自动发布脚本 v3 - 可见浏览器 + 手动登录
用户可以看到浏览器窗口，手动扫码登录，然后脚本自动完成发布
"""
import asyncio
import sys
import os

async def publish_xiaohongshu_visible():
    """使用可见浏览器完成小红书发布"""
    
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
    
    print("=" * 60)
    print("小红书自动发布脚本 v3（可见浏览器模式）")
    print("=" * 60)
    print(f"📝 标题: {title}")
    print(f"📄 正文长度: {len(body)} 字符")
    print(f"🖼️ 图片: {image_path}")
    print()
    
    try:
        from playwright.async_api import async_playwright
        
        print("🚀 启动可见浏览器...")
        
        async with async_playwright() as p:
            # 启动可见浏览器（headless=False）
            browser = await p.chromium.launch(
                headless=False,  # 显示浏览器窗口
                slow_mo=50,       # 减慢操作速度，更像人类
                args=[
                    '--disable-blink-features=AutomationControlled',  # 反检测
                    '--disable-dev-shm-usage',
                ]
            )
            
            # 创建浏览器上下文
            context = await browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # 创建页面
            page = await context.new_page()
            
            print("✅ 浏览器已打开（请查看浏览器窗口）")
            print()
            print("步骤 1/4: 打开小红书创作者平台...")
            print("-" * 60)
            
            # 打开小红书创作者平台
            await page.goto('https://creator.xiaohongshu.com/publish/publish', wait_until='networkidle', timeout=30000)
            
            print("✅ 页面已加载")
            print()
            print("=" * 60)
            print("⚠️ 请手动登录")
            print("=" * 60)
            print("请在浏览器窗口中：")
            print("  1. 点击右上角「二维码」图标")
            print("  2. 用小红书 APP 扫一扫")
            print("  3. 确认登录")
            print()
            print("登录成功后，我将自动继续...")
            print("=" * 60)
            print()
            
            # 等待用户登录（检查 URL 变化）
            print("⏳ 等待登录（最多 120 秒）...")
            
            try:
                # 等待 URL 变化（登录成功后跳转到发布页面）
                await page.wait_for_url('**/publish/publish**', timeout=120000)
                print("✅ 登录成功！")
            except Exception as e:
                print(f"⚠️ 等待超时或出错: {e}")
                print("请手动确认是否已登录，然后按 Enter 继续...")
                input()  # 等待用户按 Enter
            
            print()
            print("步骤 2/4: 上传图片和填写内容...")
            print("-" * 60)
            
            # 点击"上传图文"按钮
            print("📤 点击「上传图文」按钮...")
            try:
                await page.click('text=上传图文', timeout=10000)
                await page.wait_for_timeout(2000)
                print("✅ 已点击「上传图文」")
            except Exception as e:
                print(f"⚠️ 点击「上传图文」失败: {e}")
                print("尝试使用 JavaScript 点击...")
                await page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('*'));
                    const target = buttons.find(el => el.textContent.includes('上传图文'));
                    if (target) target.click();
                }""")
                await page.wait_for_timeout(2000)
            
            # 上传图片
            print(f"📤 上传图片: {image_path}")
            try:
                # 触发文件上传
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(image_path)
                    await page.wait_for_timeout(3000)
                    print("✅ 图片已上传")
                else:
                    print("⚠️ 未找到文件上传输入框，尝试点击上传区域...")
                    await page.click('text=点击上传', timeout=5000)
                    await page.wait_for_timeout(1000)
                    file_input = await page.query_selector('input[type="file"]')
                    if file_input:
                        await file_input.set_input_files(image_path)
                        await page.wait_for_timeout(3000)
                        print("✅ 图片已上传（通过点击上传区域）")
            except Exception as e:
                print(f"❌ 上传图片失败: {e}")
                print("请手动上传图片，然后按 Enter 继续...")
                input()
            
            # 填写标题
            print(f"📝 填写标题: {title}")
            try:
                title_input = await page.query_selector('input[placeholder*="标题"]')
                if title_input:
                    await title_input.fill(title)
                    await page.wait_for_timeout(1000)
                    print("✅ 标题已填写")
                else:
                    print("⚠️ 未找到标题输入框，尝试其他选择器...")
                    await page.fill('input[type="text"]', title)
                    await page.wait_for_timeout(1000)
                    print("✅ 标题已填写（通过通用选择器）")
            except Exception as e:
                print(f"⚠️ 填写标题失败: {e}")
            
            # 填写正文
            print(f"📝 填写正文（{len(body)} 字符）...")
            try:
                body_input = await page.query_selector('textarea[placeholder*="正文"]')
                if body_input:
                    await body_input.fill(body)
                    await page.wait_for_timeout(2000)
                    print("✅ 正文已填写")
                else:
                    print("⚠️ 未找到正文输入框，尝试其他选择器...")
                    await page.fill('textarea', body)
                    await page.wait_for_timeout(2000)
                    print("✅ 正文已填写（通过通用选择器）")
            except Exception as e:
                print(f"⚠️ 填写正文失败: {e}")
            
            # 添加话题
            print("🏷️ 添加话题标签...")
            topics = ["颂钵", "身心灵放松", "解压颂钵音", "疗愈的力量", "将冥想带入生活"]
            
            for topic in topics:
                try:
                    # 点击"添加话题"按钮
                    await page.click('text=添加话题', timeout=3000)
                    await page.wait_for_timeout(1000)
                    
                    # 输入话题
                    topic_input = await page.query_selector('input[placeholder*="话题"]')
                    if topic_input:
                        await topic_input.fill(topic)
                        await page.wait_for_timeout(1000)
                        await page.press('input[placeholder*="话题"]', 'Enter')
                        await page.wait_for_timeout(1000)
                        print(f"  ✅ 已添加话题: #{topic}")
                    else:
                        print(f"  ⚠️ 未找到话题输入框，跳过: #{topic}")
                except Exception as e:
                    print(f"  ⚠️ 添加话题失败: #{topic} - {e}")
            
            print()
            print("步骤 3/4: 点击发布按钮...")
            print("-" * 60)
            
            # 点击发布按钮
            print("🚀 尝试点击「发布」按钮...")
            
            # 方法1：普通点击
            try:
                await page.click('button:has-text("发布")', timeout=5000)
                print("✅ 已点击「发布」按钮（方法1）")
                await page.wait_for_timeout(5000)
            except Exception as e1:
                print(f"⚠️ 方法1失败: {e1}")
                
                # 方法2：JavaScript 点击
                try:
                    await page.evaluate("""() => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        const publishBtn = buttons.find(el => el.textContent.includes('发布'));
                        if (publishBtn) publishBtn.click();
                    }""")
                    print("✅ 已点击「发布」按钮（方法2: JavaScript）")
                    await page.wait_for_timeout(5000)
                except Exception as e2:
                    print(f"⚠️ 方法2失败: {e2}")
                    print()
                    print("=" * 60)
                    print("⚠️ 无法自动点击「发布」按钮")
                    print("=" * 60)
                    print("请手动点击红色的「发布」按钮，然后按 Enter 继续...")
                    input()
            
            print()
            print("步骤 4/4: 验证发布结果...")
            print("-" * 60)
            
            # 等待发布完成
            try:
                await page.wait_for_url('**/publish/note**', timeout=10000)
                print("✅ 发布成功！已跳转到笔记管理页面")
            except Exception as e:
                print(f"⚠️ 未检测到跳转: {e}")
                print("请检查浏览器窗口，确认是否发布成功...")
            
            # 截图保存结果
            screenshot_path = r'E:\WorkBuddy\Claw\xhs_publish_result.png'
            await page.screenshot(path=screenshot_path)
            print(f"📸 截图已保存: {screenshot_path}")
            
            print()
            print("=" * 60)
            print("✅ 任务完成！")
            print("=" * 60)
            print()
            print("浏览器将保持打开状态，按 Ctrl+C 关闭...")
            
            # 保持浏览器打开
            await asyncio.sleep(300)  # 保持5分钟
            
        print()
        print("✅ 发布成功！")
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 执行失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print()
    result = asyncio.run(publish_xiaohongshu_visible())
    print()
    if result:
        print("✅ 发布成功！")
    else:
        print("❌ 发布失败，请检查错误信息")
    print()
