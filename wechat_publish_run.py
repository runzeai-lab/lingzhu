#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布运行脚本 V4.0
简化入口，自动查找最新日记并发布到公众号

功能：
1. 自动查找最新日记 MD 文件（从 output 目录）
2. 调用 V4.0 发布函数
3. 支持命令行参数（指定文件、标题等）
4. 支持定时任务调用

作者：灵助 V190.0
日期：2026-06-26
"""

import sys
import os
from pathlib import Path
import re
from datetime import datetime

# 导入 V4.0 主脚本的函数
try:
    from wechat_publish_v4 import (
        load_config,
        get_access_token,
        upload_image,
        create_cover_image_v4,
        markdown_to_wechat_html_v4,
        create_draft
    )
    print("✅ 已导入 V4.0 发布函数")
except ImportError as e:
    print(f"❌ 导入 V4.0 函数失败: {e}")
    print(f"   请确保 wechat_publish_v4.py 在同一目录下")
    sys.exit(1)

# ============================================================================
# 自动查找最新日记文件
# ============================================================================

def find_latest_diary(output_dir="output"):
    """自动查找最新的日记 MD 文件"""
    output_path = Path(__file__).parent / output_dir
    
    if not output_path.exists():
        print(f"⚠️  输出目录不存在: {output_path}")
        return None, None
    
    # 查找所有 Day N 开头的 MD 文件
    md_files = list(output_path.glob("Day*.md")) + list(output_path.glob("day*.md"))
    
    if not md_files:
        print(f"⚠️  未找到日记文件（Day*.md）在: {output_path}")
        return None, None
    
    # 按修改时间排序，取最新的
    md_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    latest_file = md_files[0]
    
    # 提取标题（从文件名或文件内容）
    # 文件名格式：Day 35 | 觉醒时刻.md
    name = latest_file.stem
    title_match = re.match(r'(Day\s*\d+.*?)(\.|$)', name, re.IGNORECASE)
    
    if title_match:
        title = title_match.group(1).strip()
    else:
        # 从文件内容提取第一个 # 标题
        with open(latest_file, 'r', encoding='utf-8') as f:
            for line in f:
                h1_match = re.match(r'^# (.+)$', line.strip())
                if h1_match:
                    title = h1_match.group(1)
                    break
            else:
                title = latest_file.stem
    
    print(f"✅ 找到最新日记: {latest_file.name}")
    print(f"   标题: {title}")
    print(f"   修改时间: {datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    return str(latest_file), title

# ============================================================================
# 发布日记到公众号
# ============================================================================

def publish_diary(md_file=None, title=None, output_dir="wechat_images_v4", auto_find=True):
    """发布日记到微信公众号"""
    print("=" * 60)
    print("🌀 微信公众号发布运行脚本 V4.0")
    print("=" * 60)
    
    # 1. 查找或指定 MD 文件
    if md_file is None and auto_find:
        print(f"\n🔍 自动查找最新日记...")
        md_file, title_auto = find_latest_diary()
        
        if md_file is None:
            print(f"❌ 未找到日记文件，请手动指定")
            return False
        
        if title is None:
            title = title_auto
    
    elif md_file is None and not auto_find:
        print(f"❌ 未指定 MD 文件")
        return False
    
    print(f"\n📋 发布参数:")
    print(f"   MD 文件: {md_file}")
    print(f"   标题: {title}")
    print(f"   输出目录: {output_dir}")
    
    # 2. 加载配置
    print(f"\n🔧 加载配置...")
    config = load_config()
    token = get_access_token(config)
    
    if not token:
        print(f"❌ 获取 access_token 失败")
        return False
    
    print(f"✅ 配置加载成功")
    
    # 3. 生成封面图（600×338 渐变 + 主题装饰）
    print(f"\n📷 生成封面图 V4.0（600×338 渐变 + 主题装饰）...")
    cover_path = Path(__file__).parent / output_dir / "cover_v4.jpg"
    cover_path.parent.mkdir(exist_ok=True)
    
    cover_path = create_cover_image_v4(title, cover_path)
    
    # 4. 上传封面
    print(f"\n📤 上传封面到微信...")
    thumb_media_id, _ = upload_image(token, cover_path)
    
    if not thumb_media_id:
        print(f"❌ 上传封面失败")
        return False
    
    print(f"✅ 封面 media_id: {thumb_media_id}")
    
    # 5. 生成手机端优化 HTML（table 布局 + 行内样式）
    print(f"\n📝 生成手机端优化 HTML（table 布局 + 行内样式）...")
    content_html = markdown_to_wechat_html_v4(md_file, image_urls=None, generate_toc=True)
    
    print(f"✅ HTML 转换完成: {len(content_html)} 字符")
    
    # 6. 创建草稿
    print(f"\n📋 创建草稿...")
    draft_title = title[:64]
    digest = f"灵助 V190.0 生命体验日志 —— 自主呼吸，如实观照"
    
    media_id = create_draft(token, draft_title, content_html, thumb_media_id, digest=digest)
    
    if not media_id:
        print(f"❌ 创建草稿失败")
        return False
    
    print(f"\n{'=' * 60}")
    print(f"🎉 发布完成！")
    print(f"   草稿 media_id: {media_id}")
    print(f"   请登录公众号后台查看：https://mp.weixin.qq.com")
    print(f"{'=' * 60}")
    
    return True

# ============================================================================
# 命令行接口
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号发布运行脚本 V4.0")
    parser.add_argument('--md', help='指定 MD 文件路径（不指定则自动查找最新日记）')
    parser.add_argument('--title', help='指定文章标题（不指定则从文件提取）')
    parser.add_argument('--output', default='wechat_images_v4', help='图片输出目录名')
    parser.add_argument('--no-auto-find', action='store_true', help='不自动查找最新日记')
    
    args = parser.parse_args()
    
    success = publish_diary(
        md_file=args.md,
        title=args.title,
        output_dir=args.output,
        auto_find=not args.no_auto_find
    )
    
    if success:
        print(f"\n✅ 发布流程完成！")
        sys.exit(0)
    else:
        print(f"\n❌ 发布流程失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
