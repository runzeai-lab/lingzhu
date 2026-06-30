#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布主脚本 V4.0
创建时间: 2026-06-26
功能: V4.0 移动端优化版本（table布局 + 行内样式 + PIL封面图）

此脚本是 V4.0 的生产入口，调用 wechat_publish_v4.py 中的核心函数
"""

import sys
import os

# 导入 V4.0 核心函数
try:
    from wechat_publish_v4 import (
        create_cover_image_v4,
        markdown_to_wechat_html_v4,
        upload_image,
        get_access_token,
        create_draft
    )
    # publish_diary 函数在 wechat_publish_run.py 中
    from wechat_publish_run import publish_diary
    print("✅ 已导入 V4.0 发布函数")
except ImportError as e:
    print(f"❌ 导入 V4.0 函数失败: {e}")
    sys.exit(1)

# 为了兼容性，保留原有的函数接口
def create_cover_image(title="Day N | 颂钵疗愈", output_path=None):
    """创建封面图（V4.0 接口）"""
    return create_cover_image_v4(title, output_path)

def markdown_to_wechat_html(md_file, image_urls=None, generate_toc=True):
    """转换 MD 为微信 HTML（V4.0 接口）"""
    return markdown_to_wechat_html_v4(md_file, image_urls, generate_toc)

def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信公众号发布脚本 V4.0')
    parser.add_argument('--md', type=str, help='指定 MD 文件路径')
    parser.add_argument('--title', type=str, help='指定文章标题')
    parser.add_argument('--output', type=str, default='wechat_images_v4', help='图片输出目录名')
    parser.add_argument('--no-auto-find', action='store_true', help='不自动查找最新日记')
    
    args = parser.parse_args()
    
    # 调用发布函数
    publish_diary(
        md_file=args.md,
        title=args.title,
        output_dir=args.output,
        auto_find=not args.no_auto_find
    )

if __name__ == "__main__":
    main()
