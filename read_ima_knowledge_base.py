#!/usr/bin/env python3
"""
直接调用 IMA API 读取"经典V102"知识库的全部笔记内容
"""
import json
import urllib.request
import urllib.parse
import time
import sys

# IMA API 配置（从 mcp.json 中读取）
IMA_API_BASE = 'https://ima.qq.com'
IMA_CLIENT_ID = '910fce0cc27f5685b8f06c9d88a9ae1e'
IMA_API_KEY = 'BrqdfQbt50sKsme7VZX0xeTR4qwEYjS+vxUJP/2wiG5S57RGo7JB9uCh290CcXZuu6g88F4U8A=='

def ima_api_call(path: str, body: dict, module: str = 'wiki') -> dict:
    """
    调用 IMA OpenAPI
    """
    url = f"{IMA_API_BASE}/openapi/{module}/v1/{path}"
    
    headers = {
        'ima-openapi-clientid': IMA_CLIENT_ID,
        'ima-openapi-apikey': IMA_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    data = json.dumps(body, ensure_ascii=False).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode('utf-8')
            result = json.loads(resp_body)
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            "retcode": e.code,
            "errmsg": f"HTTP {e.code}: {error_body[:200]}"
        }
    except Exception as e:
        return {
            "retcode": -1,
            "errmsg": f"{type(e).__name__}: {str(e)[:200]}"
        }

def search_knowledge_base(query: str, limit: int = 20) -> list:
    """
    搜索知识库
    """
    print(f"🔍 搜索知识库: query='{query}', limit={limit}")
    
    body = {
        "query": query,
        "cursor": "",
        "limit": limit
    }
    
    response = ima_api_call('search_knowledge_base', body)
    
    if response.get('retcode', 0) == 0:
        data = response.get('data', {})
        results = data.get('infos', [])
        print(f"✅ 找到 {len(results)} 个知识库")
        return results
    else:
        print(f"❌ 搜索失败: {response.get('errmsg', 'Unknown error')}")
        return []

def get_knowledge_base(ids: list) -> dict:
    """
    获取知识库详情
    """
    print(f"📚 获取知识库详情: ids={ids}")
    
    body = {"ids": ids}
    
    response = ima_api_call('get_knowledge_base', body)
    
    if response.get('retcode', 0) == 0:
        data = response.get('data', {})
        infos = data.get('infos', {})
        print(f"✅ 获取到 {len(infos)} 个知识库详情")
        return infos
    else:
        print(f"❌ 获取详情失败: {response.get('errmsg', 'Unknown error')}")
        return {}

def list_knowledge(kb_id: str, folder_id: str = '', limit: int = 50) -> list:
    """
    浏览知识库内容列表
    """
    print(f"📂 浏览知识库内容: kb_id={kb_id[:20]}..., folder_id={folder_id}, limit={limit}")
    
    body = {
        "knowledge_base_id": kb_id,
        "cursor": "",
        "limit": limit
    }
    if folder_id:
        body["folder_id"] = folder_id
    
    response = ima_api_call('get_knowledge_list', body)
    
    if response.get('retcode', 0) == 0:
        data = response.get('data', {})
        knowledge_list = data.get('knowledge_list', [])
        print(f"✅ 找到 {len(knowledge_list)} 个内容")
        return knowledge_list
    else:
        print(f"❌ 浏览失败: {response.get('errmsg', 'Unknown error')}")
        return []

def get_note_content(kb_id: str, doc_id: str, format: str = 'text') -> dict:
    """
    获取笔记内容（完整流程）
    """
    # 步骤1: 调用 get_media_info 获取笔记的 notebook_id
    media_id = doc_id
    
    media_info_response = ima_api_call('get_media_info', {
        "knowledge_base_id": kb_id,
        "media_id": media_id
    })
    
    if media_info_response.get('retcode', -1) != 0 and media_info_response.get('code', -1) != 0:
        return {
            "status": "error",
            "message": f"Failed to get media info: {media_info_response.get('errmsg', media_info_response.get('msg', 'Unknown error'))}"
        }
    
    # 提取 notebook_id
    data = media_info_response.get('data', {})
    notebook_ext_info = data.get('note_book_ext_info', {})
    notebook_id = notebook_ext_info.get('note_book_id', '')
    
    if not notebook_id:
        notebook_id = data.get('note_book_id', '') or data.get('note_id', '')
    
    if not notebook_id:
        return {
            "status": "error",
            "message": "This document does not appear to be a note (no notebook_id found)"
        }
    
    # 步骤2: 调用 note/v1/get_doc_content 获取笔记内容
    url = f"{IMA_API_BASE}/openapi/note/v1/get_doc_content"
    
    headers = {
        'ima-openapi-clientid': IMA_CLIENT_ID,
        'ima-openapi-apikey': IMA_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    body = {
        "note_id": notebook_id,
        "format": format
    }
    
    data = json.dumps(body, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode('utf-8')
            doc_content_response = json.loads(resp_body)
            
            if doc_content_response.get('retcode', -1) != 0 and doc_content_response.get('code', -1) != 0:
                return {
                    "status": "error",
                    "message": f"Failed to get doc content: {doc_content_response.get('errmsg', doc_content_response.get('msg', 'Unknown error'))}"
                }
            
            content_data = doc_content_response.get('data', {})
            return {
                "status": "success",
                "doc_id": doc_id,
                "notebook_id": notebook_id,
                "content": content_data.get('content', ''),
                "title": content_data.get('title', '')
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"{type(e).__name__}: {str(e)[:200]}"
        }

def main():
    print("=" * 60)
    print("IMA 知识库读取工具 - 经典V102")
    print("=" * 60)
    
    # 步骤1: 搜索"经典V102"知识库
    kb_list = search_knowledge_base('经典V102', limit=20)
    
    if not kb_list:
        print("\n❌ 未找到'经典V102'知识库，尝试列出所有知识库...")
        kb_list = search_knowledge_base('', limit=50)
        
        if not kb_list:
            print("❌ 未找到任何知识库")
            return
    
    # 找到"经典V102"知识库
    target_kb = None
    for kb in kb_list:
        kb_name = kb.get('name', '')
        print(f"  知识库: {kb_name} (ID: {kb.get('id', '')})")
        if '经典V102' in kb_name or 'V102' in kb_name:
            target_kb = kb
            break
    
    if not target_kb:
        print(f"\n⚠️ 未找到名称完全匹配的'经典V102'知识库，使用第一个: {kb_list[0].get('name', '')}")
        target_kb = kb_list[0]
    
    kb_id = target_kb.get('id', '')
    kb_name = target_kb.get('name', '')
    print(f"\n✅ 目标知识库: {kb_name} (ID: {kb_id})")
    
    # 步骤2: 获取知识库详情
    kb_details = get_knowledge_base([kb_id])
    if kb_id in kb_details:
        kb_detail = kb_details[kb_id]
        print(f"  名称: {kb_detail.get('name', '')}")
        print(f"  描述: {kb_detail.get('description', '')}")
    
    # 步骤3: 浏览知识库内容
    print(f"\n📂 浏览知识库内容...")
    knowledge_list = list_knowledge(kb_id, folder_id='', limit=50)
    
    if not knowledge_list:
        print("❌ 知识库为空或读取失败")
        return
    
    # 步骤4: 提取所有笔记
    notes = []
    folders = []
    
    for item in knowledge_list:
        item_type = item.get('type', '')
        if item_type == 11:  # 笔记类型
            notes.append(item)
        elif item_type == 1:  # 文件夹类型
            folders.append(item)
        
        item_name = item.get('title', item.get('name', ''))
        item_id = item.get('id', '')
        print(f"  {'📄' if item_type == 11 else '📁'} {item_name} (ID: {item_id[:30]}...)")
    
    print(f"\n📊 统计: {len(notes)} 篇笔记, {len(folders)} 个文件夹")
    
    # 步骤5: 读取所有笔记内容
    print(f"\n📖 读取所有笔记内容...")
    notes_content = []
    
    for i, note in enumerate(notes, 1):
        doc_id = note.get('id', '')
        title = note.get('title', '')
        
        print(f"  [{i}/{len(notes)}] 读取: {title}...", end=' ')
        
        content_result = get_note_content(kb_id, doc_id, format='text')
        
        if content_result.get('status') == 'success':
            print(f"✅ (内容长度: {len(content_result.get('content', ''))})")
            notes_content.append({
                "title": title,
                "doc_id": doc_id,
                "content": content_result.get('content', ''),
                "notebook_id": content_result.get('notebook_id', '')
            })
        else:
            print(f"❌ {content_result.get('message', 'Unknown error')}")
        
        # 避免 API 限流
        time.sleep(0.5)
    
    # 步骤6: 保存结果
    print(f"\n💾 保存结果...")
    
    output_file = 'ima_classic_v102_notes.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "knowledge_base": {
                "id": kb_id,
                "name": kb_name
            },
            "notes_count": len(notes_content),
            "notes": notes_content
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 结果已保存到: {output_file}")
    print(f"   共 {len(notes_content)} 篇笔记")
    
    #  also 保存纯文本版本（方便阅读）
    txt_file = 'ima_classic_v102_notes.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"# IMA 知识库: {kb_name}\n\n")
        f.write(f"知识库 ID: {kb_id}\n")
        f.write(f"笔记数量: {len(notes_content)}\n")
        f.write(f"导出时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("=" * 60 + "\n\n")
        
        for i, note in enumerate(notes_content, 1):
            f.write(f"## {i}. {note['title']}\n\n")
            f.write(note['content'])
            f.write("\n\n" + "=" * 60 + "\n\n")
    
    print(f"✅ 纯文本版本已保存到: {txt_file}")
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
