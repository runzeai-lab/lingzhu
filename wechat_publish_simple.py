#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布脚本 V2.0
功能：生成封面图、上传、Markdown转HTML、直接发布到微信公众号
升级说明：
  - 修复标题截断（20→64字符）
  - 添加直接发布API（freepublish.submit）
  - 添加发布状态查询
  - 改进HTML转换（支持链接、列表、代码块；正确逐行处理列表）
"""

import json
import re
import requests
import time
from pathlib import Path
from datetime import datetime

# 配置
WECHAT_CONFIG = {
    "app_id": "wxb42b877d4ddf4b38",
    "app_secret": "0e853ba09adc82c76e4efbdba84cc66f"
}

def get_access_token():
    """获取微信access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_CONFIG['app_id']}&secret={WECHAT_CONFIG['app_secret']}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if 'access_token' in data:
            print(f"✅ 获取access_token成功")
            return data['access_token']
        else:
            print(f"❌ 获取access_token失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 获取access_token异常: {e}")
        return None

def create_cover_image(title, output_path):
    """创建简单的封面图"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (900, 500), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 900, 80], fill='#4cc9f0')
        draw.rectangle([0, 420, 900, 500], fill='#4cc9f0')
        short_title = title[:15] + '...' if len(title) > 15 else title
        try:
            font = ImageFont.truetype("msyh.ttc", 40)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), short_title, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((900 - tw) / 2, 250), short_title, fill='white', font=font)
        bbox2 = draw.textbbox((0, 0), "灵助日记", font=font)
        sw = bbox2[2] - bbox2[0]
        draw.text(((900 - sw) / 2, 320), "灵助日记", fill='#4cc9f0', font=font)
        img.save(output_path, 'JPEG', quality=95)
        print(f"✅ 封面图生成成功: {output_path}")
        return True
    except ImportError:
        print(f"⚠️ Pillow未安装，尝试安装...")
        import subprocess
        subprocess.run([r"C:\Users\RunzeAI\.workbuddy\binaries\python\versions\3.13.12\python.exe", "-m", "pip", "install", "Pillow"])
        print(f"✅ Pillow已安装，请重新运行脚本")
        return False
    except Exception as e:
        print(f"❌ 生成封面图失败: {e}")
        return False

def upload_image(token, image_path):
    """上传图片到微信"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    try:
        with open(image_path, 'rb') as f:
            files = {'media': (Path(image_path).name, f, 'image/jpeg')}
            resp = requests.post(url, files=files, timeout=30)
        data = resp.json()
        if 'media_id' in data:
            print(f"✅ 图片上传成功")
            print(f"   media_id: {data['media_id']}")
            return data['media_id'], data.get('url', '')
        else:
            print(f"❌ 图片上传失败: {data}")
            return None, None
    except Exception as e:
        print(f"❌ 图片上传异常: {e}")
        return None, None

def markdown_to_html(md_content):
    """将Markdown转换为微信兼容的HTML（正确逐行处理列表）"""
    # 先处理代码块（``` ... ```）
    def replace_code_block(match):
        code = match.group(1)
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code>{code}</code></pre>'
    
    html = re.sub(r'```(.+?)```', replace_code_block, md_content, flags=re.DOTALL)
    
    # 处理行内代码（`...`）
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 逐行处理，正确构建HTML
    lines = html.split('\n')
    result = []
    in_paragraph = False
    in_unordered_list = False
    in_ordered_list = False
    
    def close_paragraph():
        nonlocal in_paragraph, result
        if in_paragraph:
            result.append('</p>')
            in_paragraph = False
    
    def close_unordered_list():
        nonlocal in_unordered_list, result
        if in_unordered_list:
            result.append('</ul>')
            in_unordered_list = False
    
    def close_ordered_list():
        nonlocal in_ordered_list, result
        if in_ordered_list:
            result.append('</ol>')
            in_ordered_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # 空行：关闭所有打开的标签
        if not stripped:
            close_paragraph()
            close_unordered_list()
            close_ordered_list()
            result.append('')
            continue
        
        # 标题
        h1_match = re.match(r'^# (.+)$', stripped)
        h2_match = re.match(r'^## (.+)$', stripped)
        h3_match = re.match(r'^### (.+)$', stripped)
        if h1_match:
            close_paragraph(); close_unordered_list(); close_ordered_list()
            result.append(f'<h1>{h1_match.group(1)}</h1>')
            continue
        if h2_match:
            close_paragraph(); close_unordered_list(); close_ordered_list()
            result.append(f'<h2>{h2_match.group(1)}</h2>')
            continue
        if h3_match:
            close_paragraph(); close_unordered_list(); close_ordered_list()
            result.append(f'<h3>{h3_match.group(1)}</h3>')
            continue
        
        # 引用
        blockquote_match = re.match(r'^> (.+)$', stripped)
        if blockquote_match:
            close_paragraph(); close_unordered_list(); close_ordered_list()
            result.append(f'<blockquote>{blockquote_match.group(1)}</blockquote>')
            continue
        
        # 分隔符
        if stripped == '---':
            close_paragraph(); close_unordered_list(); close_ordered_list()
            result.append('<hr/>')
            continue
        
        # 无序列表项
        ul_match = re.match(r'^- (.+)$', stripped)
        if ul_match:
            close_paragraph()
            close_ordered_list()
            if not in_unordered_list:
                result.append('<ul>')
                in_unordered_list = True
            item_content = ul_match.group(1)
            item_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_content)
            item_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', item_content)
            item_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', item_content)
            result.append(f'<li>{item_content}</li>')
            continue
        
        # 有序列表项
        ol_match = re.match(r'^\d+\. (.+)$', stripped)
        if ol_match:
            close_paragraph()
            close_unordered_list()
            if not in_ordered_list:
                result.append('<ol>')
                in_ordered_list = True
            item_content = ol_match.group(1)
            item_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_content)
            item_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', item_content)
            item_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', item_content)
            result.append(f'<li>{item_content}</li>')
            continue
        
        # 普通段落文本
        close_unordered_list()
        close_ordered_list()
        if not in_paragraph:
            result.append('<p>')
            in_paragraph = True
        
        # 处理段落内的格式
        processed = stripped
        processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
        processed = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed)
        processed = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', processed)
        processed = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed)
        
        result.append(processed)
    
    # 关闭所有打开的标签
    close_paragraph()
    close_unordered_list()
    close_ordered_list()
    
    return '\n'.join(result)

def create_draft(token, title, content_html, thumb_media_id, author="灵助"):
    """创建微信草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    articles = [{
        "title": title[:64],
        "author": author,
        "digest": "",
        "content": content_html,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }]
    payload = {"articles": articles}
    try:
        body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
        data = resp.json()
        if 'media_id' in data:
            print(f"✅ 草稿创建成功！")
            print(f"   media_id: {data['media_id']}")
            return data['media_id']
        else:
            print(f"❌ 创建草稿失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 创建草稿异常: {e}")
        return None

def submit_publish(token, media_id):
    """提交发布（直接发布，不需要手动操作）"""
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
    payload = {"media_id": media_id}
    try:
        body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
        data = resp.json()
        if data.get('errcode') == 0:
            print(f"✅ 发布提交成功！")
            print(f"   publish_id: {data.get('publish_id')}")
            return data.get('publish_id')
        else:
            print(f"❌ 发布提交失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 发布提交异常: {e}")
        return None

def get_publish_status(token, publish_id):
    """查询发布状态"""
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token={token}"
    payload = {"publish_id": publish_id}
    try:
        body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
        data = resp.json()
        if data.get('errcode') == 0:
            status = data.get('publish_status', -1)
            status_msg = {
                0: "发布成功",
                1: "发布中",
                2: "原创失败",
                3: "常规失败",
                4: "平台审核不通过",
                5: "发布中用户取消"
            }.get(status, "未知状态")
            print(f"✅ 发布状态查询成功")
            print(f"   状态: {status_msg} ({status})")
            if status == 0:
                print(f"   文章ID: {data.get('article_id', '')}")
                print(f"   文章URL: {data.get('article_url', '')}")
            return status
        else:
            print(f"❌ 发布状态查询失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 发布状态查询异常: {e}")
        return None

def publish_article(md_file_path, auto_publish=True):
    """发布文章到微信公众号（支持直接发布）"""
    print(f"📋 开始发布文章: {md_file_path}")
    
    md_path = Path(md_file_path)
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_file_path}")
        return False
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print(f"✅ 已读取文件: {len(md_content)} 字符")
    
    # 提取标题（第一个# 标题）
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)[:64]
    else:
        title = md_path.stem[:64]
    
    print(f"✅ 文章标题: {title}")
    
    # 生成封面图
    cover_path = md_path.parent / f"{md_path.stem}_cover.jpg"
    if not create_cover_image(title, cover_path):
        return False
    
    # 获取access_token
    token = get_access_token()
    if not token:
        return False
    
    # 上传封面图
    thumb_media_id, _ = upload_image(token, cover_path)
    if not thumb_media_id:
        return False
    
    # 转换Markdown为HTML
    html_content = markdown_to_html(md_content)
    print(f"✅ HTML转换完成: {len(html_content)} 字符")
    
    # 创建草稿
    media_id = create_draft(token, title, html_content, thumb_media_id)
    if not media_id:
        return False
    
    print(f"\n✅ 草稿创建成功！")
    print(f"   media_id: {media_id}")
    
    # 直接发布（如果启用）
    if auto_publish:
        publish_id = submit_publish(token, media_id)
        if publish_id:
            print(f"\n✅ 文章已提交发布！")
            print(f"   publish_id: {publish_id}")
            time.sleep(2)
            get_publish_status(token, publish_id)
        else:
            print(f"\n⚠️ 草稿已创建，但发布提交失败，请手动发布")
            print(f"\n🔗 查看草稿：")
            print(f"   请登录 https://mp.weixin.qq.com")
            print(f"   在「素材管理」→「草稿箱」中查看")
    else:
        print(f"\n🔗 查看草稿：")
        print(f"   请登录 https://mp.weixin.qq.com")
        print(f"   在「素材管理」→「草稿箱」中查看")
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python wechat_publish_simple.py <markdown_file> [--no-publish]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    auto_publish = "--no-publish" not in sys.argv
    success = publish_article(md_file, auto_publish=auto_publish)
    
    if success:
        print(f"\n✅ 文章处理完成")
    else:
        print(f"\n❌ 处理失败，请检查错误信息")
        sys.exit(1)
