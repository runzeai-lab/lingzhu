import json
import html
import re

# 1. 读取JSON文件（处理HTML实体编码）
with open(r'E:\WorkBuddy\Claw\deepseek_share_vxdt6wlq2gdk82hau2.json', 'r', encoding='utf-8') as f:
    raw = f.read()
    data = json.loads(html.unescape(raw))

# 2. 提取对话
biz_data = data.get('data', {}).get('biz_data', {})
conversations = biz_data.get('messages', [])
title = biz_data.get('title', 'DeepSeek 分享对话')

# 3. 转换为Markdown
markdown_lines = []
markdown_lines.append(f'# {title}\n\n')
markdown_lines.append(f'**分享ID**: vxdt6wlq2gdk82hau2\n')
markdown_lines.append(f'**对话轮数**: {len(conversations)} 轮\n')
markdown_lines.append(f'**导出时间**: 2026-05-29\n\n')
markdown_lines.append('---\n\n')

for i, conv in enumerate(conversations, 1):
    role = conv.get('role', 'unknown')
    content = conv.get('content', '')
    
    # 角色中文映射
    role_cn = '用户' if role == 'user' else 'DeepSeek'
    
    # 添加轮次标题
    markdown_lines.append(f'## 第 {i} 轮 - {role_cn}\n\n')
    
    # 处理内容中的代码块
    content = content.replace('```', '\n```\n')
    
    # 添加内容
    markdown_lines.append(f'{content}\n\n')
    markdown_lines.append('---\n\n')

# 4. 保存为Markdown
output_path = r'E:\WorkBuddy\Claw\deepseek_share_vxdt6wlq2gdk82hau2_full.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(markdown_lines)

print(f'✅ 完成！共解析 {len(conversations)} 轮对话')
print(f'✅ 输出文件: {output_path}')
