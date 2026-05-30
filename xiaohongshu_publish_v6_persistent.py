#!/usr/bin/env python3
"""
小红书自动发布脚本 V6 - 持久化登录版
使用 Playwright + 持久化用户数据目录
用户只需首次扫码登录，之后自动保持登录状态
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 用户数据目录（保存登录状态）
USER_DATA_DIR = PROJECT_ROOT / "xiaohongshu_user_data"
USER_DATA_DIR.mkdir(exist_ok=True)

# 文章内容文件路径
ARTICLE_FILE = PROJECT_ROOT / "xiaohongshu_day1.md"

# 图片目录
IMAGES_DIR = PROJECT_ROOT / "xiaohongshu_images"


async def publish_to_xiaohongshu():
    """使用 Playwright 自动发布到小红书"""
    from playwright.async_api import async_playwright
    
    print("🚀 启动 Playwright 浏览器（持久化登录）...")
    
    async with async_playwright() as p:
        # 使用持久化上下文（保存登录状态）
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print(f"📄 打开小红书创作者平台...")
        await page.goto('https://creator.xiaohongshu.com/publish/publish')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        # 检查是否需要登录
        print("🔍 检查登录状态...")
        if 'login' in page.url or 'sign' in page.url:
            print("⚠️ 需要登录！请扫码登录...")
            print("⏳ 等待登录完成（最多 120 秒）...")
            
            try:
                # 等待登录完成（URL 变化）
                await page.wait_for_url('**/creator.xiaohongshu.com/**', timeout=120000)
                print("✅ 登录成功！")
                
                # 强制等待页面跳转
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(5)  # 增加等待时间
            except Exception as e:
                print(f"❌ 登录超时: {e}")
                await context.close()
                return
            
            # 重新导航到发布页面（强制）
            print("📄 强制跳转到发布页面...")
            await page.goto('https://creator.xiaohongshu.com/publish/publish')
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(5)  # 增加等待时间
        else:
            print("✅ 已登录（使用保存的登录状态）")
        
        # 智能检测：是否已在上传页面
        print("🔍 检测当前页面状态...")
        title_input = None
        try:
            title_input = await page.wait_for_selector('input[placeholder*="标题"], input[placeholder*="填写标题"]', timeout=5000)
            print("✅ 已在上传页面（找到标题输入框）")
        except Exception:
            print("⚠️ 不在上传页面，尝试点击'上传图文'按钮...")
            try:
                await page.wait_for_selector('text=上传图文', timeout=10000)
                await page.click('text=上传图文')
                print("✅ 点击'上传图文'成功")
                await asyncio.sleep(2)
            except Exception as e2:
                print(f"❌ 无法进入上传页面: {e2}")
        
        await asyncio.sleep(2)
        
        # 读取文章内容
        print("📖 读取文章内容...")
        if not ARTICLE_FILE.exists():
            print(f"❌ 文章文件不存在: {ARTICLE_FILE}")
            await context.close()
            return
        
        with open(ARTICLE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题（第一行 # 后的内容）
        lines = content.split('\n')
        title = ""
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                body_start = i + 1
            break
        
        # 如果没找到 # 标题，使用默认标题
        if not title:
            title = "颂钵疗愈 | Day 1 缘起"
        
        # 提取正文（去掉标题和 AI 标注）
        body_lines = []
        for line in lines[body_start:]:
            if '【声明】' in line or '---' in line:
                break
            if line.strip():
                body_lines.append(line)
        
        body = '\n'.join(body_lines[:50])  # 限制长度
        
        print(f"📝 标题: {title}")
        print(f"📝 正文长度: {len(body)} 字符")
        
        # 填写标题
        print("✍️ 填写标题...")
        try:
            title_input = await page.wait_for_selector('input[placeholder*="标题"], input[placeholder*="填写标题"]', timeout=10000)
            await title_input.fill(title)
            print("✅ 标题填写成功")
        except Exception as e:
            print(f"⚠️ 标题输入框未找到: {e}")
            # 尝试其他选择器
            try:
                await page.fill('input[type="text"]', title)
                print("✅ 标题填写成功（备用方法）")
            except Exception as e2:
                print(f"❌ 标题填写失败: {e2}")
        
        await asyncio.sleep(1)
        
        # 填写正文
        print("✍️ 填写正文...")
        try:
            body_input = await page.wait_for_selector('.ql-editor, [contenteditable="true"], textarea[placeholder*="正文"]', timeout=10000)
            await body_input.fill(body)
            print("✅ 正文填写成功")
        except Exception as e:
            print(f"⚠️ 正文输入框未找到: {e}")
            # 尝试其他选择器
            try:
                await page.fill('textarea', body)
                print("✅ 正文填写成功（备用方法）")
            except Exception as e2:
                print(f"❌ 正文填写失败: {e2}")
        
        await asyncio.sleep(2)
        
        # 上传图片
        print("🖼️ 上传图片...")
        image_files = list(IMAGES_DIR.glob('*.jpg')) + list(IMAGES_DIR.glob('*.png'))
        
        if image_files:
            print(f"📁 找到 {len(image_files)} 张图片")
            
            # 查找文件上传输入框
            try:
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                
                # 上传所有图片
                for img_path in image_files[:6]:  # 最多6张
                    print(f"  📤 上传: {img_path.name}")
                    await file_input.set_input_files(str(img_path))
                    await asyncio.sleep(1)
                
                print("✅ 图片上传成功")
            except Exception as e:
                print(f"⚠️ 文件上传输入框未找到: {e}")
        else:
            print("⚠️ 未找到图片文件")
        
        await asyncio.sleep(2)
        
        # 点击"发布"按钮
        print("🚀 点击'发布'按钮...")
        try:
            publish_button = await page.wait_for_selector('button:has-text("发布"), .publish-btn', timeout=10000)
            await publish_button.click()
            print("✅ 发布按钮点击成功")
        except Exception as e:
            print(f"⚠️ 发布按钮未找到: {e}")
            # 尝试其他选择器
            try:
                await page.click('button:has-text("发布")')
                print("✅ 发布按钮点击成功（备用方法）")
            except Exception as e2:
                print(f"❌ 发布失败: {e2}")
        
        # 等待发布完成
        print("⏳ 等待发布完成...")
        await asyncio.sleep(5)
        
        # 截图保存结果
        screenshot_path = PROJECT_ROOT / "xiaohongshu_publish_result.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"📸 结果截图已保存: {screenshot_path}")
        
        print("✅ 发布流程完成！")
        print(f"🔗 浏览器保持打开状态，登录状态已保存到: {USER_DATA_DIR}")
        print("   下次运行脚本时，将自动使用保存的登录状态")
        
        # 保持浏览器打开（方便检查）
        print("\n💡 浏览器将保持打开状态 60 秒，按 Ctrl+C 可提前关闭...")
        await asyncio.sleep(60)
        
        await context.close()


if __name__ == '__main__':
    print("=" * 60)
    print("小红书自动发布脚本 V6 - 持久化登录版")
    print("=" * 60)
    print()
    print("📝 说明：")
    print("  1. 首次运行需要扫码登录（最多等待 120 秒）")
    print("  2. 登录状态会保存到本地，下次运行自动登录")
    print("  3. 脚本会自动填写标题、正文、上传图片、点击发布")
    print()
    print("=" * 60)
    print()
    
    try:
        asyncio.run(publish_to_xiaohongshu())
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
