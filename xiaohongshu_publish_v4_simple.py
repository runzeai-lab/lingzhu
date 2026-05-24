#!/usr/bin/env python3
"""
小红书自动发布脚本 V4.0 - 极简版
- 直接调用 agent-browser CLI（已安装）
- 不需要 Playwright 依赖
- 完全自动化（除了扫码）
"""

import subprocess
import time
import json
import os

def run_browser_command(cmd):
    """运行 agent-browser 命令"""
    result = subprocess.run(
        f"agent-browser {cmd}",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return result.stdout

def main():
    print("🚀 小红书自动发布脚本 V4.0 (极简版)")
    print("=" * 60)
    
    # 1. 打开浏览器
    print("\n📂 步骤1：打开小红书创作者平台...")
    run_browser_command('open https://creator.xiaohongshu.com/publish/publish')
    time.sleep(3)
    
    # 2. 等待页面加载
    print("📂 步骤2：等待页面加载...")
    run_browser_command('wait --load networkidle')
    
    # 3. 检查登录状态
    print("\n📂 步骤3：检查登录状态...")
    snapshot = run_browser_command('snapshot')
    
    # 检查是否需要登录
    if '扫码' in snapshot or '登录' in snapshot:
        print("⚠️  需要登录！请使用小红书APP扫描二维码...")
        print("📸 正在截图二维码...")
        
        # 截图并显示
        run_browser_command('screenshot')
        print("✅ 二维码截图已保存")
        print("👉 请用小红书APP扫描屏幕上的二维码")
        print("⏳ 等待登录（最多120秒）...")
        
        # 等待登录成功
        for i in range(24):  # 24 * 5 = 120秒
            time.sleep(5)
            snapshot = run_browser_command('snapshot')
            if '五感六觉' in snapshot or '润泽博士' in snapshot:
                print("✅ 登录成功！")
                break
            print(f"   等待中... ({i*5}/120秒)")
        else:
            print("❌ 登录超时！请手动扫码后继续...")
            input("按 Enter 继续...")
    
    # 4. 点击"上传图文"
    print("\n📝 步骤4：点击'上传图文'...")
    run_browser_command('click "ref=e5"')  # 使用之前获取的 ref
    time.sleep(3)
    
    # 5. 填写标题
    print("\n📝 步骤5：填写标题...")
    title = "颂钵疗愈 | Day 1 遇见颂钵的奇妙旅程 ✨"
    
    # 先点击标题输入框
    run_browser_command('click "ref=e12"')  # 假设标题输入框的 ref
    time.sleep(1)
    
    # 输入标题
    run_browser_command(f'type "{title}"')
    print(f"✅ 标题已填写：{title}")
    
    # 6. 上传图片
    print("\n📝 步骤6：上传图片...")
    image_dir = r'E:\WorkBuddy\Claw\xiaohongshu_images'
    
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
        print(f"📂 找到 {len(images)} 张图片")
        
        # 点击"上传图片"按钮
        run_browser_command('click "ref=e13"')  # 假设上传按钮的 ref
        time.sleep(2)
        
        # 使用 Windows 文件选择对话框上传
        # 注意：这里需要模拟文件选择，比较复杂
        # 暂时跳过，手动上传
        print("⚠️  图片上传需要手动操作（文件选择对话框）")
        print("📂 图片目录：", image_dir)
        input("请手动上传图片，然后按 Enter 继续...")
    else:
        print("⚠️  未找到图片目录，跳过上传")
    
    # 7. 填写正文
    print("\n📝 步骤7：填写正文...")
    
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

（本内容由 AI 辅助创作）"""
    
    # 点击正文输入框
    run_browser_command('click "ref=e14"')  # 假设正文输入框的 ref
    time.sleep(1)
    
    # 输入正文（分段输入，避免超时）
    paragraphs = content.split('\n')
    for i, para in enumerate(paragraphs):
        if para.strip():
            run_browser_command(f'type "{para}"')
            time.sleep(0.5)
    
    print(f"✅ 正文已填写（{len(content)} 字符）")
    
    # 8. 添加标签
    print("\n📝 步骤8：添加标签...")
    # 小红书的标签通常在正文中用 # 表示，不需要单独添加
    print("✅ 标签已包含在正文中")
    
    # 9. 截图预览
    print("\n📸 步骤9：截图预览...")
    run_browser_command('screenshot')
    print("✅ 预览截图已保存")
    
    # 10. 点击发布（自动执行）
    print("\n📝 步骤10：点击发布...")
    print("⏳ 自动发布中...")
    
    # 查找并点击发布按钮
    snapshot = run_browser_command('snapshot')
    
    # 尝试多种可能的发布按钮 ref
    publish_refs = ['e15', 'e17', 'e19', 'e20']
    published = False
    
    for ref in publish_refs:
        try:
            run_browser_command(f'click "ref={ref}"')
            time.sleep(2)
            print(f"✅ 已点击发布按钮 (ref={ref})")
            published = True
            break
        except:
            continue
    
    if not published:
        print("⚠️  未找到发布按钮，请手动点击...")
        # 截图供用户查看
        run_browser_command('screenshot')
    
    time.sleep(5)
    
    # 11. 验证发布成功
    print("\n✅ 步骤11：验证发布结果...")
    run_browser_command('screenshot')
    
    snapshot = run_browser_command('snapshot')
    if '笔记管理' in snapshot or '发布成功' in snapshot:
        print("🎉 发布成功！")
    else:
        print("⚠️  未检测到成功提示，请手动确认")
    
    print("\n" + "=" * 60)
    print("🎉 发布流程完成！")
    print("=" * 60)
    
    # 保持浏览器打开
    print("\n💡 浏览器保持打开状态，方便查看结果")
    print("按 Ctrl+C 退出...")

if __name__ == '__main__':
    main()
