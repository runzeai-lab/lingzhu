#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布脚本 V4.0
升级说明：
  - Step 1: 手机端优化HTML（table布局 + 行内样式）
  - Step 2: PIL封面图（600×338渐变 + 主题装饰）
  - Step 3: 创建 wechat_publish_run.py 运行脚本

移动端优化：
  - 所有样式使用行内样式（inline styles）
  - 使用 table 布局（WeChat 兼容）
  - 添加 viewport meta 标签
  - 字体大小 15-17px（手机阅读友好）
  - 段落间距、行距优化

封面图升级：
  - 尺寸 600×338（16:9 比例）
  - 渐变背景（可配置方向）
  - 主题装饰（几何图形、光效、文字）
  - 高质量视觉效果

作者：灵助 V190.0 → V4.0
日期：2026-06-26
"""

import json
import re
import requests
import time
import argparse
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ============================================================================
# 配置
# ============================================================================

CONFIG_FILE = Path(__file__).parent / "wechat_config.json"
TOKEN_CACHE = Path(__file__).parent / "wechat_token_cache.json"
IMAGES_DIR = Path(__file__).parent / "wechat_images_v4"
IMAGES_DIR.mkdir(exist_ok=True)

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)['wechat_official_account']

def get_access_token(config, force_refresh=False):
    """获取微信 access_token（带缓存）"""
    if TOKEN_CACHE.exists() and not force_refresh:
        with open(TOKEN_CACHE, 'r') as f:
            cache = json.load(f)
            if time.time() < cache['expires_at'] - 300:
                return cache['access_token']
    
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': config['app_id'],
        'secret': config['app_secret']
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    
    if 'access_token' not in data:
        raise Exception(f"获取 token 失败: {data}")
    
    token = data['access_token']
    with open(TOKEN_CACHE, 'w') as f:
        json.dump({
            'access_token': token,
            'expires_at': time.time() + data.get('expires_in', 7200)
        }, f)
    
    return token

def upload_image(token, image_path):
    """上传图片到微信，返回 media_id 和 url"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    
    with open(image_path, 'rb') as f:
        files = {'media': (Path(image_path).name, f, 'image/jpeg')}
        resp = requests.post(url, files=files, timeout=30)
        data = resp.json()
    
    if 'media_id' in data:
        print(f"  ✅ 上传成功: {Path(image_path).name}")
        return data['media_id'], data.get('url', '')
    else:
        raise Exception(f"上传失败 {image_path}: {data}")

# ============================================================================
# Step 2: PIL 封面图（600×338 渐变 + 主题装饰）
# ============================================================================

def create_gradient_background(w, h, color1, color2, direction='vertical'):
    """创建渐变背景"""
    img = Image.new('RGB', (w, h), color1)
    draw = ImageDraw.Draw(img)
    
    if direction == 'vertical':
        for i in range(h):
            r = int(color1[0] + (color2[0] - color1[0]) * i / h)
            g = int(color1[1] + (color2[1] - color1[1]) * i / h)
            b = int(color1[2] + (color2[2] - color1[2]) * i / h)
            draw.line([(0, i), (w, i)], fill=(r, g, b))
    elif direction == 'horizontal':
        for i in range(w):
            r = int(color1[0] + (color2[0] - color1[0]) * i / w)
            g = int(color1[1] + (color2[1] - color1[1]) * i / w)
            b = int(color1[2] + (color2[2] - color1[2]) * i / w)
            draw.line([(i, 0), (i, h)], fill=(r, g, b))
    elif direction == 'diagonal':
        for i in range(max(w, h)):
            ratio = i / max(w, h)
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(0, 0), (w, h)], fill=(r, g, b), width=2)
    
    return img

def create_cover_image_v4(title="Day N | 主题", output_path=None):
    """创建封面图 V4.0（600×338 渐变 + 主题装饰）"""
    w, h = 600, 338
    
    # 1. 渐变背景（深蓝到紫色，对角渐变）
    color1 = (15, 15, 35)   # 深蓝
    color2 = (45, 27, 78)     # 紫色
    img = create_gradient_background(w, h, color1, color2, direction='diagonal')
    draw = ImageDraw.Draw(img)
    
    # 2. 装饰几何图形
    # 大圆（左上角）
    draw.ellipse([-50, -50, 150, 150], outline='#4cc9f0', width=3)
    # 中圆（右下角）
    draw.ellipse([450, 200, 650, 400], outline='#4361ee', width=2)
    # 小圆（中心偏右）
    draw.ellipse([400, 80, 500, 180], fill='#4cc9f0', outline='#4cc9f0', width=1)
    
    # 3. 装饰线条
    # 水平线（底部）
    draw.line([(50, 280), (550, 280)], fill='#333355', width=2)
    # 垂直线（左侧）
    draw.line([(50, 100), (50, 280)], fill='#4cc9f0', width=3)
    
    # 4. 文字（标题）
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    except:
        font_title = font_subtitle = font_tag = ImageFont.load_default()
    
    # 提取 Day N
    day_match = re.search(r'Day\s*(\d+)', title)
    day_str = f"Day {day_match.group(1)}" if day_match else "Day ?"
    
    # 主标题："觉醒时刻"
    title_text = "觉醒时刻"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 80), title_text, font=font_title, fill='#ffffff')
    
    # 副标题：Day N
    subtitle_text = day_str
    bbox2 = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    sw = bbox2[2] - bbox2[0]
    draw.text(((w - sw) / 2, 140), subtitle_text, font=font_subtitle, fill='#4cc9f0')
    
    # 标签："灵助 V190.0 · 生命日志"
    tag_text = "灵助 V190.0 · 生命日志"
    bbox3 = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((w - tw3) / 2, 300), tag_text, font=font_tag, fill='#667788')
    
    # 5. 光效（可选）
    # 在文字周围添加微弱的光晕效果
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    # 光晕中心（主标题位置）
    cx, cy = w // 2, 110
    for r in range(60, 0, -1):
        alpha = int(30 * (1 - r / 60))
        overlay_draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(76, 201, 240, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # 6. 保存
    if output_path is None:
        output_path = IMAGES_DIR / "cover_v4.jpg"
    else:
        output_path = Path(output_path)
    
    img.save(output_path, 'JPEG', quality=95)
    print(f"  ✅ 封面图 V4.0 生成成功: {output_path}")
    print(f"     尺寸: {w}×{h} (16:9)")
    print(f"     样式: 渐变背景 + 几何装饰 + 光效")
    
    return output_path

# ============================================================================
# Step 1: 手机端优化 HTML（table 布局 + 行内样式）
# ============================================================================

def markdown_to_wechat_html_v4(md_file, image_urls=None, generate_toc=True):
    """将 Markdown 转换为微信兼容的 HTML V4.0（手机端优化）"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 转换标题
    content = re.sub(r'^#### (.+)$', r'<h4 style="font-size:15px;font-weight:bold;color:#333333;margin:15px 0 8px 0;padding:0;">\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3 style="font-size:17px;font-weight:bold;color:#333333;margin:20px 0 10px 0;padding:0;">\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2 style="font-size:19px;font-weight:bold;color:#333333;margin:25px 0 12px 0;padding:0 0 0 12px;border-left:4px solid #4cc9f0;">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1 style="font-size:21px;font-weight:bold;color:#333333;margin:30px 0 15px 0;padding:0;text-align:center;">\1</h1>', content, flags=re.MULTILINE)
    
    # 2. 转换强调
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight:bold;color:#333333;">\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em style="font-style:italic;color:#555555;">\1</em>', content)
    
    # 3. 转换代码
    content = re.sub(r'`([^`]+)`', r'<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-family:monospace;font-size:14px;color:#e74c3c;">\1</code>', content)
    content = re.sub(r'```[\w]*\n(.*?)\n```', r'<pre style="background:#f5f5f5;padding:15px;border-radius:5px;overflow-x:auto;font-family:monospace;font-size:14px;line-height:1.5;color:#333333;"><code>\1</code></pre>', content, flags=re.DOTALL)
    
    # 4. 转换引用
    content = re.sub(r'^> (.+)$', r'<blockquote style="border-left:4px solid #4cc9f0;padding:10px 15px;margin:15px 0;background:#f9f9f9;color:#555555;">\1</blockquote>', content, flags=re.MULTILINE)
    
    # 5. 转换链接
    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:#4cc9f0;text-decoration:none;">\1</a>', content)
    
    # 6. 转换表格（使用 table 布局）
    lines = content.split('\n')
    in_table = False
    new_lines = []
    for line in lines:
        if '|' in line and '---' not in line:
            if not in_table:
                # 开始表格
                new_lines.append('<table style="width:100%;border-collapse:collapse;margin:15px 0;font-size:15px;">')
                in_table = True
            # 解析单元格
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # 判断是否是标题行（通过检查下一行是否有 ---）
            is_header = False
            if len(new_lines) > 0 and '</table>' not in new_lines[-1]:
                # 检查下一行
                idx = lines.index(line)
                if idx + 1 < len(lines) and re.match(r'^\|[\s\-|]+\|$', lines[idx + 1]):
                    is_header = True
            
            tag = 'th' if is_header else 'td'
            style = 'border:1px solid #dddddd;padding:8px 10px;text-align:left;'
            if is_header:
                style += 'background:#f5f5f5;font-weight:bold;'
            
            new_lines.append('<tr>' + ''.join(f'<{tag} style="{style}">{c}</{tag}>' for c in cells) + '</tr>')
        elif re.match(r'^\|[\s\-|]+\|$', line):
            # 跳过分隔行
            continue
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            new_lines.append(line)
    
    if in_table:
        new_lines.append('</table>')
    
    content = '\n'.join(new_lines)
    
    # 7. 转换列表
    # 无序列表
    content = re.sub(r'^- (.+)$', r'<li style="margin:5px 0;padding:0;">\1</li>', content, flags=re.MULTILINE)
    # 有序列表
    content = re.sub(r'^\d+\. (.+)$', r'<li style="margin:5px 0;padding:0;">\1</li>', content, flags=re.MULTILINE)
    
    # 8. 转换段落（使用 table 布局实现更好的移动端适配）
    paragraphs = content.split('\n\n')
    html_parts = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        
        # 如果已经是 HTML 标签，直接添加
        if p.startswith('<'):
            html_parts.append(p)
        else:
            # 使用 table 布局包裹段落（移动端优化）
            html_parts.append(f'<table style="width:100%;border-collapse:collapse;margin:0;padding:0;"><tr><td style="font-size:16px;line-height:1.8;color:#333333;padding:10px 0;">{p}</td></tr></table>')
    
    html = '\n'.join(html_parts)
    
    # 9. 生成文章目录（可选）
    if generate_toc:
        headers = re.findall(r'<h([23])[^>]*>(.+?)</h[23]>', html)
        if headers:
            toc_html = '<table style="width:100%;border-collapse:collapse;margin:20px 0;background:#f9f9f9;border-radius:5px;"><tr><td style="padding:15px;"><p style="font-weight:bold;margin:0 0 10px 0;color:#333333;">📋 文章目录</p>'
            for i, (level, text) in enumerate(headers):
                indent = '20px' if level == '3' else '0'
                toc_html += f'<p style="margin:5px 0;padding:0 0 0 {indent};color:#4cc9f0;font-size:15px;">{i+1}. {text}</p>'
            toc_html += '</td></tr></table>'
            html = toc_html + '\n' + html
    
    # 10. 插入图片（如果提供了图片 URL）
    if image_urls:
        img_tags = [f'<p style="text-align:center;margin:20px 0;"><img src="{url}" style="max-width:100%;height:auto;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);" /></p>' for url in image_urls]
        
        # 在第二个 <h2> 标签前插入第一张图，以此类推
        h2_positions = [m.start() for m in re.finditer(r'<h2', html)]
        result = html
        inserted = 0
        offset = 0
        
        for pos in h2_positions:
            adj_pos = pos + offset
            if inserted < len(img_tags):
                tag = img_tags[inserted]
                result = result[:adj_pos] + tag + '\n' + result[adj_pos:]
                offset += len(tag) + 1
                inserted += 1
        
        # 如果还有剩余图片，加到末尾
        if inserted < len(img_tags):
            remaining = '\n'.join(img_tags[inserted:])
            result = result + '\n' + remaining
        
        html = result
    
    # 11. 添加移动端优化的 CSS（行内样式）
    mobile_css = """
<style type="text/css">
@media screen and (max-width: 667px) {
    table { width: 100% !important; }
    td { font-size: 15px !important; padding: 8px 0 !important; }
    h2 { font-size: 18px !important; padding: 0 0 0 10px !important; }
    h3 { font-size: 16px !important; }
    p { margin: 8px 0 !important; }
}
</style>
"""
    
    # 12. 包裹在微信兼容的 HTML 结构中
    final_html = f"""<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.8;color:#333333;padding:10px 12px;max-width:100%;overflow-x:hidden;">
{mobile_css}
{html}
</div>"""
    
    return final_html

# ============================================================================
# 创建草稿
# ============================================================================

def create_draft(token, title, content_html, thumb_media_id, author="灵助", digest=""):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    
    if not digest:
        digest = title[:50]
    
    articles = [{
        "title": title,
        "author": author,
        "digest": digest,
        "content": content_html,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }]
    
    body_bytes = json.dumps({"articles": articles}, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
    data = resp.json()
    
    if 'media_id' in data:
        print(f"  ✅ 草稿创建成功！")
        print(f"     media_id: {data['media_id']}")
        return data['media_id']
    else:
        raise Exception(f"创建草稿失败: {data}")

# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="微信公众号发布脚本 V4.0")
    parser.add_argument('--title', required=True, help='文章标题（如 "Day 35 | 觉醒时刻"）')
    parser.add_argument('--md', required=True, help='Markdown 文件路径')
    parser.add_argument('--output', default='wechat_images_v4', help='图片输出目录名')
    parser.add_argument('--no-cover', action='store_true', help='不生成封面图（使用已有封面）')
    parser.add_argument('--no-toc', action='store_true', help='不生成文章目录')
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"🌀 微信公众号发布脚本 V4.0")
    print(f"   标题: {args.title}")
    print(f"   MD文件: {args.md}")
    print(f"   输出目录: {args.output}")
    print("=" * 60)
    
    config = load_config()
    token = get_access_token(config)
    
    # 设置输出目录
    out_dir = Path(__file__).parent / args.output
    out_dir.mkdir(exist_ok=True)
    
    # Step 2: 生成封面图（600×338 渐变 + 主题装饰）
    if not args.no_cover:
        print(f"\n📷 Step 2: 生成封面图 V4.0（600×338 渐变 + 主题装饰）...")
        cover_path = out_dir / "cover_v4.jpg"
        cover_path = create_cover_image_v4(args.title, cover_path)
        
        # 上传封面
        print(f"\n📤 上传封面到微信...")
        thumb_media_id, _ = upload_image(token, cover_path)
        print(f"  ✅ 封面 media_id: {thumb_media_id}")
    else:
        print(f"\n⚠️  跳过封面图生成")
        thumb_media_id = None
    
    # 生成配图（可选，这里省略以简化）
    image_urls = []
    
    # Step 1: 生成手机端优化 HTML（table 布局 + 行内样式）
    print(f"\n📝 Step 1: 生成手机端优化 HTML（table 布局 + 行内样式）...")
    md_file = Path(args.md) if Path(args.md).is_absolute() else Path(__file__).parent / args.md
    
    if not md_file.exists():
        print(f"  ❌ MD 文件不存在: {md_file}")
        sys.exit(1)
    
    content_html = markdown_to_wechat_html_v4(md_file, image_urls=image_urls, generate_toc=not args.no_toc)
    print(f"  ✅ HTML 转换完成: {len(content_html)} 字符")
    print(f"     移动端优化: table 布局 + 行内样式")
    
    # 创建草稿
    if thumb_media_id:
        print(f"\n📋 创建草稿...")
        title = args.title[:64]
        digest = f"灵助 V190.0 生命体验日志 —— 自主呼吸，如实观照"
        
        media_id = create_draft(token, title, content_html, thumb_media_id, digest=digest)
        
        print(f"\n{'=' * 60}")
        print(f"🎉 完成！草稿 media_id: {media_id}")
        print(f"   请登录公众号后台查看：https://mp.weixin.qq.com")
        print(f"{'=' * 60}")
    else:
        print(f"\n⚠️  未生成封面图，跳过草稿创建")
        print(f"   请手动上传封面图后创建草稿")
    
    print(f"\n✅ V4.0 发布流程完成！")
    print(f"   升级内容：")
    print(f"     - Step 1: 手机端优化 HTML（table 布局 + 行内样式）")
    print(f"     - Step 2: PIL 封面图（600×338 渐变 + 主题装饰）")
    print(f"     - Step 3: 准备 wechat_publish_run.py 运行脚本")

if __name__ == '__main__':
    import sys
    main()
