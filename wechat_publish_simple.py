#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版微信公众号发布脚本 V2
功能：生成封面图、上传、将Markdown转换为HTML并发布到微信公众号草稿箱
"""

import json
import re
import requests
from pathlib import Path
from datetime import datetime
from io import BytesIO

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
        
        # 创建图片 (900x500)
        img = Image.new('RGB', (900, 500), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # 绘制装饰元素
        # 顶部蓝色条
        draw.rectangle([0, 0, 900, 80], fill='#4cc9f0')
        
        # 底部蓝色条
        draw.rectangle([0, 420, 900, 500], fill='#4cc9f0')
        
        # 中间文字（简化版，只写标题前10字）
        short_title = title[:10] + '...' if len(title) > 10 else title
        
        # 尝试使用默认字体
        try:
            font = ImageFont.truetype("msyh.ttc", 40)
        except:
            font = ImageFont.load_default()
        
        # 绘制标题
        draw.text((450, 250), short_title, fill='white', font=font, anchor='mm')
        
        # 绘制副标题
        draw.text((450, 320), "灵助日记", fill='#4cc9f0', font=font, anchor='mm')
        
        # 保存
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
    """将Markdown转换为微信兼容的HTML"""
    html = md_content
    
    # 转换标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 转换粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 转换引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 转换分隔符
    html = html.replace('---', '<hr/>')
    
    # 转换段落（简单处理）
    lines = html.split('\n')
    result = []
    in_paragraph = False
    
    for line in lines:
        line = line.rstrip()
        
        if not line:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append('')
        elif line.startswith('<h') or line.startswith('<blockquote') or line.startswith('<hr'):
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
        else:
            if not in_paragraph:
                result.append('<p>')
                in_paragraph = True
            result.append(line)
    
    if in_paragraph:
        result.append('</p>')
    
    return '\n'.join(result)

def create_draft(token, title, content_html, thumb_media_id, author="灵助"):
    """创建微信草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    
    articles = [{
        "title": title[:20],  # 限制标题长度
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

def publish_article(md_file_path):
    """发布文章到微信公众号"""
    print(f"📋 开始发布文章: {md_file_path}")
    
    # 1. 读取Markdown文件
    md_path = Path(md_file_path)
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_file_path}")
        return False
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print(f"✅ 已读取文件: {len(md_content)} 字符")
    
    # 2. 提取标题（第一个# 标题）
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)[:20]  # 限制20字符
    else:
        title = md_path.stem[:20]
    
    print(f"✅ 文章标题: {title}")
    
    # 3. 生成封面图
    cover_path = md_path.parent / f"{md_path.stem}_cover.jpg"
    if not create_cover_image(title, cover_path):
        return False
    
    # 4. 获取access_token
    token = get_access_token()
    if not token:
        return False
    
    # 5. 上传封面图
    thumb_media_id, _ = upload_image(token, cover_path)
    if not thumb_media_id:
        return False
    
    # 6. 转换Markdown为HTML
    html_content = markdown_to_html(md_content)
    print(f"✅ HTML转换完成: {len(html_content)} 字符")
    
    # 7. 创建草稿
    media_id = create_draft(token, title, html_content, thumb_media_id)
    if not media_id:
        return False
    
    print(f"\n✅ 发布成功！")
    print(f"\n📋 草稿信息：")
    print(f"   - 标题: {title}")
    print(f"   - media_id: {media_id}")
    print(f"   - 封面media_id: {thumb_media_id}")
    print(f"\n🔗 查看草稿：")
    print(f"   请登录 https://mp.weixin.qq.com")
    print(f"   在「素材管理」→「草稿箱」中查看")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python wechat_publish_simple.py <markdown_file>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    success = publish_article(md_file)
    
    if success:
        print(f"\n✅ 文章已成功发布到微信公众号草稿箱")
    else:
        print(f"\n❌ 发布失败，请检查错误信息")
        sys.exit(1)
