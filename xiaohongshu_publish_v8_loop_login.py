#!/usr/bin/env python3
"""
小红书自动发布脚本 V8 - 循环检测登录状态
不使用 wait_for_url，而是循环检测 URL 变化
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# 项目路径
PROJECT_ROOT = Path('E:/WorkBuddy/Claw').resolve()
USER_DATA_DIR = PROJECT_ROOT / 'xiaohongshu_user_data_v3'
USER_DATA_DIR.mkdir(exist_ok=True, parents=True)

ARTICLE_FILE = PROJECT_ROOT / 'xiaohongshu_day1.md'
IMAGES_DIR = PROJECT_ROOT / 'xiaohongshu_images'

# 调试截图目录
DEBUG_DIR = PROJECT_ROOT / 'debug_screenshots_v2'
DEBUG_DIR.mkdir(exist_ok=True, parents=True)


def timestamp():
    """时间戳（用于截图命名）"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


async def debug_screenshot(page, step_name):
    """保存调试截图"""
    screenshot_path = DEBUG_DIR / f'{timestamp()}_{step_name}.png'
    await page.screenshot(path=str(screenshot_path), full_page=True)
    print(f'📸 调试截图: {screenshot_path.name}')
    return screenshot_path


async def wait_for_login(page, timeout=120):
    """
    循环检测登录状态
    每隔 2 秒检查一次 URL，直到不包含 'login' 或 'sign'
    """
    print(f'⏳ 等待登录完成（最多 {timeout} 秒）...')
    
    for i in range(timeout // 2):
        await asyncio.sleep(2)
        current_url = page.url
        
        # 检查是否已跳转到创作者平台（不在登录页面）
        if 'login' not in current_url and 'sign' not in current_url:
            print(f'✅ 登录成功！（等待 {i * 2} 秒）')
            return True
        
        # 每 10 秒打印一次进度
        if i % 5 == 0:
            print(f'   🔄 等待中... ({i * 2} 秒) URL: {current_url[:50]}...')
    
    print('❌ 登录超时')
    return False


async def publish_to_xiaohongshu():
    """使用 Playwright 自动发布到小红书"""
    from playwright.async_api import async_playwright
    
    print('🚀 启动 Playwright 浏览器（持久化登录）...')
    print(f'🔗 用户数据目录: {USER_DATA_DIR}')
    
    async with async_playwright() as p:
        # 使用持久化上下文
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # ===== 步骤 1: 打开创作者平台 =====
        print('📄 步骤 1: 打开小红书创作者平台...')
        await page.goto('https://creator.xiaohongshu.com/publish/publish')
        await asyncio.sleep(3)
        await debug_screenshot(page, 'step1_open')
        
        # ===== 步骤 2: 检查登录状态（循环检测）=====
        print('🔍 步骤 2: 检查登录状态...')
        current_url = page.url
        print(f'   当前 URL: {current_url}')
        
        if 'login' in current_url or 'sign' in current_url:
            print('⚠️ 需要登录！请扫码登录...')
            
            # 使用循环检测登录状态
            login_success = await wait_for_login(page, timeout=120)
            
            if not login_success:
                print('❌ 登录超时，请重试')
                await debug_screenshot(page, 'step2_login_timeout')
                await context.close()
                return
            
            # 登录成功后，强制等待页面完全加载
            print('⏳ 等待页面完全加载（10 秒）...')
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(10)
            
            await debug_screenshot(page, 'step2_after_login')
            print(f'   登录后 URL: {page.url}')
        
        else:
            print('✅ 已登录（使用保存的登录状态）')
        
        # ===== 步骤 3: 强制跳转到发布页面 =====
        print('📄 步骤 3: 强制跳转到发布页面...')
        await page.goto('https://creator.xiaohongshu.com/publish/publish')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(5)
        await debug_screenshot(page, 'step3_after_navigate')
        print(f'   跳转后 URL: {page.url}')
        
        # 检查是否成功跳转到发布页面
        if 'login' in page.url or 'sign' in page.url:
            print('❌ 跳转失败，仍在登录页面')
            await context.close()
            return
        
        # ===== 步骤 4: 智能检测页面状态 =====
        print('🔍 步骤 4: 检测当前页面状态...')
        
        # 检查是否在上传页面（通过查找标题输入框）
        title_input = None
        try:
            title_input = await page.wait_for_selector('input[placeholder*="标题"], input[placeholder*="填写标题"]', timeout=5000)
            print('✅ 已在上传页面（找到标题输入框）')
        except Exception:
            print('⚠️ 不在上传页面，尝试点击"上传图文"按钮...')
            
            # 查找并点击"上传图文"按钮
            try:
                upload_button = await page.wait_for_selector('text=上传图文', timeout=10000)
                await upload_button.click()
                print('✅ 点击"上传图文"成功')
                await asyncio.sleep(3)
                await debug_screenshot(page, 'step4_after_click_upload')
            except Exception as e2:
                print(f'❌ 无法找到"上传图文"按钮: {e2}')
                await debug_screenshot(page, 'step4_error_no_upload_button')
                # 继续尝试（可能页面已在上传状态）
        
        await asyncio.sleep(3)
        await debug_screenshot(page, 'step4_before_fill')
        
        # ===== 步骤 5: 读取文章内容 =====
        print('📖 步骤 5: 读取文章内容...')
        if not ARTICLE_FILE.exists():
            print(f'❌ 文章文件不存在: {ARTICLE_FILE}')
            await context.close()
            return
        
        with open(ARTICLE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题（第一行 # 后的内容）
        lines = content.split('\n')
        title = ''
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                body_start = i + 1
                break
        
        if not title:
            title = '颂钵疗愈 | Day 1 缘起'
        
        # 提取正文（去掉标题和 AI 标注）
        body_lines = []
        for line in lines[body_start:]:
            if '【声明】' in line or '---' in line:
                break
            if line.strip():
                body_lines.append(line)
        
        body = '\n'.join(body_lines[:50])  # 限制长度
        
        print(f'📝 标题: {title}')
        print(f'📝 正文长度: {len(body)} 字符')
        
        # ===== 步骤 6: 填写标题 =====
        print('✍️ 步骤 6: 填写标题...')
        try:
            title_input = await page.wait_for_selector('input[placeholder*="标题"], input[placeholder*="填写标题"]', timeout=10000)
            await title_input.fill(title)
            print('✅ 标题填写成功')
        except Exception as e:
            print(f'⚠️ 标题输入框未找到: {e}')
            await debug_screenshot(page, 'step6_title_error')
        
        await asyncio.sleep(1)
        
        # ===== 步骤 7: 填写正文 =====
        print('✍️ 步骤 7: 填写正文...')
        try:
            # 尝试多种选择器
            for selector in ['.ql-editor', '[contenteditable="true"]', 'textarea[placeholder*="正文"]', 'textarea']:
                try:
                    body_input = await page.wait_for_selector(selector, timeout=3000)
                    await body_input.fill(body)
                    print(f'✅ 正文填写成功（使用选择器: {selector}）')
                    break
                except Exception:
                    continue
            else:
                print('⚠️ 正文输入框未找到')
                await debug_screenshot(page, 'step7_body_error')
        except Exception as e:
            print(f'❌ 正文填写失败: {e}')
        
        await asyncio.sleep(2)
        
        # ===== 步骤 8: 上传图片 =====
        print('🖼️ 步骤 8: 上传图片...')
        
        # 检查图片目录
        if IMAGES_DIR.exists():
            image_files = list(IMAGES_DIR.glob('*.jpg')) + list(IMAGES_DIR.glob('*.png'))
        else:
            image_files = []
        
        if image_files:
            print(f'📁 找到 {len(image_files)} 张图片')
            
            try:
                # 查找文件上传输入框
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                
                # 上传所有图片
                for img_path in image_files[:6]:  # 最多6张
                    print(f'  📤 上传: {img_path.name}')
                    await file_input.set_input_files(str(img_path))
                    await asyncio.sleep(1)
                
                print('✅ 图片上传成功')
            except Exception as e:
                print(f'⚠️ 文件上传失败: {e}')
                await debug_screenshot(page, 'step8_upload_error')
        else:
            print('⚠️ 未找到图片文件')
        
        await asyncio.sleep(2)
        await debug_screenshot(page, 'step8_before_publish')
        
        # ===== 步骤 9: 点击"发布"按钮 =====
        print('🚀 步骤 9: 点击"发布"按钮...')
        try:
            # 尝试多种选择器
            for selector in ['button:has-text("发布")', '.publish-btn', 'button.btn-publish']:
                try:
                    publish_button = await page.wait_for_selector(selector, timeout=3000)
                    await publish_button.click()
                    print(f'✅ 发布按钮点击成功（使用选择器: {selector}）')
                    break
                except Exception:
                    continue
            else:
                print('⚠️ 发布按钮未找到')
                await debug_screenshot(page, 'step9_publish_error')
        except Exception as e:
            print(f'❌ 发布失败: {e}')
        
        # ===== 步骤 10: 等待发布完成 =====
        print('⏳ 步骤 10: 等待发布完成...')
        await asyncio.sleep(5)
        await debug_screenshot(page, 'step10_after_publish')
        
        # ===== 完成 =====
        print('✅ 发布流程完成！')
        print(f'🔗 浏览器保持打开状态，登录状态已保存到: {USER_DATA_DIR}')
        print('   下次运行脚本时，将自动使用保存的登录状态')
        
        # 保持浏览器打开（方便检查）
        print('\n💡 浏览器将保持打开状态 60 秒，按 Ctrl+C 可提前关闭...')
        await asyncio.sleep(60)
        
        await context.close()


if __name__ == '__main__':
    print('=' * 60)
    print('小红书自动发布脚本 V8 - 循环检测登录状态')
    print('=' * 60)
    print()
    print('📝 说明：')
    print('  1. 首次运行需要扫码登录（最多等待 120 秒）')
    print('  2. 登录状态会保存到本地，下次运行自动登录')
    print('  3. 脚本会自动填写标题、正文、上传图片、点击发布')
    print('  4. 每个关键步骤都会保存调试截图')
    print('  5. 使用循环检测登录状态（不再依赖 wait_for_url）')
    print()
    print('=' * 60)
    print()
    
    try:
        asyncio.run(publish_to_xiaohongshu())
    except KeyboardInterrupt:
        print('\n⚠️ 用户中断')
    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()
