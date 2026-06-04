#!/usr/bin/env python3
"""
IMA 知识库引擎 - 灵助 V180.3
集成腾讯IMA知识库的搜索、读取、查询功能
性能优化版：异步HTTP、连接池、内存缓存、并发批处理
"""
import json
import time
import asyncio
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime

# IMA API 配置
IMA_API_BASE = 'https://ima.qq.com'
IMA_CLIENT_ID = '910fce0cc27f5685b8f06c9d88a9ae1e'
IMA_API_KEY = 'BrqdfQbt50sKsme7VZX0xeTR4qwEYjS+vxUJP/2wiG5S57RGo7JB9uCh290CcXZuu6g88F4U8A=='

# 缓存配置
CACHE_TTL = 60  # 缓存有效期（秒）
MAX_CONCURRENT = 5  # 最大并发数
MAX_RETRIES = 2  # 最大重试次数


class MemoryCache:
    """简单的内存缓存，支持TTL过期"""

    def __init__(self, ttl: int = CACHE_TTL):
        self._cache: Dict[str, tuple] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expire_at = self._cache[key]
            if time.time() < expire_at:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expire_at = time.time() + (ttl or self._ttl)
        self._cache[key] = (value, expire_at)

    def invalidate(self, key: str):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()


class IMAKnowledgeEngine:
    """IMA 知识库引擎 - 封装所有 IMA API 调用（异步高性能版）"""

    def __init__(self):
        self.api_base = IMA_API_BASE
        self.client_id = IMA_CLIENT_ID
        self.api_key = IMA_API_KEY
        self._call_count = 0
        self._last_reset = datetime.now()
        self._client: Optional[httpx.AsyncClient] = None
        self._cache = MemoryCache(ttl=CACHE_TTL)
        self._semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建HTTP客户端（连接池复用）"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                limits=httpx.Limits(
                    max_keepalive_connections=10,
                    max_connections=20,
                    keepalive_expiry=30.0
                )
            )
        return self._client

    async def _api_call(self, path: str, body: dict, module: str = 'wiki') -> dict:
        """调用 IMA OpenAPI（异步+重试+限流）"""
        url = f"{self.api_base}/openapi/{module}/v1/{path}"

        headers = {
            'ima-openapi-clientid': self.client_id,
            'ima-openapi-apikey': self.api_key,
            'Content-Type': 'application/json; charset=utf-8'
        }

        data = json.dumps(body, ensure_ascii=False).encode('utf-8')

        async with self._semaphore:
            for attempt in range(MAX_RETRIES + 1):
                try:
                    client = await self._get_client()
                    resp = await client.post(url, content=data, headers=headers)
                    self._call_count += 1

                    result = resp.json()
                    # 统一响应格式：将 code 映射为 retcode
                    if 'code' in result and 'retcode' not in result:
                        result['retcode'] = result['code']
                    return result

                except (httpx.TimeoutException, httpx.ConnectError) as e:
                    if attempt < MAX_RETRIES:
                        wait = (attempt + 1) * 1.0
                        await asyncio.sleep(wait)
                        continue
                    return {
                        "retcode": -1,
                        "errmsg": f"Request failed after {MAX_RETRIES + 1} attempts: {type(e).__name__}: {str(e)[:200]}"
                    }
                except httpx.HTTPStatusError as e:
                    self._call_count += 1
                    try:
                        error_body = e.response.json()
                    except Exception:
                        error_body = e.response.text[:200]
                    return {
                        "retcode": e.response.status_code,
                        "errmsg": f"HTTP {e.response.status_code}: {error_body}"
                    }
                except Exception as e:
                    self._call_count += 1
                    # 尝试获取响应文本用于调试
                    try:
                        resp_text = resp.text[:500] if 'resp' in dir() else 'no response'
                    except Exception:
                        resp_text = 'cannot read response'
                    return {
                        "retcode": -1,
                        "errmsg": f"{type(e).__name__}: {str(e)[:200]}",
                        "_debug_response": resp_text
                    }

    def get_stats(self) -> dict:
        """获取引擎统计信息"""
        return {
            "status": "active",
            "api_call_count": self._call_count,
            "last_reset": self._last_reset.isoformat(),
            "api_base": self.api_base,
            "cache_size": len(self._cache._cache),
            "cache_ttl": CACHE_TTL
        }

    async def search_knowledge_base(self, query: str, limit: int = 20) -> dict:
        """搜索知识库"""
        cache_key = f"search_kb:{query}:{limit}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        body = {
            "query": query,
            "cursor": "",
            "limit": limit
        }

        response = await self._api_call('search_knowledge_base', body)

        if response.get('retcode', 0) == 0:
            data = response.get('data', {})
            results = data.get('infos', data.get('info_list', []))
            result = {
                "status": "success",
                "count": len(results),
                "results": results
            }
            self._cache.set(cache_key, result, ttl=30)
            return result
        else:
            return {
                "status": "error",
                "message": response.get('errmsg', response.get('msg', 'Unknown error')),
                "results": []
            }

    async def get_knowledge_base_info(self, ids: List[str]) -> dict:
        """获取知识库详情"""
        cache_key = f"kb_info:{','.join(sorted(ids))}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        body = {
            "ids": ids
        }

        response = await self._api_call('get_knowledge_base', body)

        if response.get('retcode', 0) == 0:
            data = response.get('data', {})
            infos = data.get('infos', data.get('info_list', {}))
            # infos 可能是字典（key=kb_id）或列表
            if isinstance(infos, dict):
                info_list = list(infos.values())
            else:
                info_list = infos
            result = {
                "status": "success",
                "count": len(info_list),
                "knowledge_bases": info_list
            }
            self._cache.set(cache_key, result)
            return result
        else:
            return {
                "status": "error",
                "message": response.get('errmsg', response.get('msg', 'Unknown error')),
                "knowledge_bases": []
            }

    async def list_knowledge(self, kb_id: str, folder_id: str = "", limit: int = 50, cursor: str = "") -> dict:
        """浏览知识库内容列表"""
        cache_key = f"list_knowledge:{kb_id}:{folder_id}:{limit}:{cursor}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        body = {
            "knowledge_base_id": kb_id,
            "folder_id": folder_id,
            "cursor": cursor,
            "limit": limit
        }

        response = await self._api_call('get_knowledge_list', body)

        if response.get('retcode', 0) == 0:
            data = response.get('data', {})
            items = data.get('knowledge_list', data.get('infos', data.get('info_list', [])))
            next_cursor = data.get('next_cursor', '')
            has_more = not data.get('is_end', True)
            result = {
                "status": "success",
                "count": len(items),
                "items": items,
                "next_cursor": next_cursor,
                "has_more": has_more
            }
            self._cache.set(cache_key, result, ttl=30)
            return result
        else:
            return {
                "status": "error",
                "message": response.get('errmsg', response.get('msg', 'Unknown error')),
                "items": []
            }

    @staticmethod
    def _extract_doc_id(doc_id: str) -> str:
        """从 media_id 中提取真实的 doc_id
        
        media_id 格式: note_<hash>_<数字ID>
        真实 doc_id 是数字ID的前16位
        """
        if '_' in doc_id:
            parts = doc_id.split('_')
            last_part = parts[-1]
            if last_part.isdigit() and len(last_part) >= 16:
                return last_part[:16]
        return doc_id

    async def get_note_content(self, kb_id: str, doc_id: str, format: str = 'text') -> dict:
        """获取笔记内容"""
        # 从 media_id 中提取真实 doc_id
        real_doc_id = self._extract_doc_id(doc_id)
        
        cache_key = f"note_content:{kb_id}:{real_doc_id}:{format}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        # 调用 note/v1/get_doc_content 获取笔记内容
        doc_content_response = await self._api_call('get_doc_content', {
            "doc_id": real_doc_id,
            "target_content_format": 0  # 0=text, 1=markdown
        }, 'note')

        code = doc_content_response.get('code', -1)
        if code != 0:
            return {
                "status": "error",
                "message": f"Failed to get doc content: {doc_content_response.get('msg', doc_content_response.get('errmsg', 'Unknown error'))}"
            }

        content_data = doc_content_response.get('data', {})
        result = {
            "status": "success",
            "doc_id": doc_id,
            "real_doc_id": real_doc_id,
            "content": content_data.get('content', ''),
            "title": content_data.get('title', '')
        }
        self._cache.set(cache_key, result, ttl=120)
        return result

    async def search_notes(self, kb_id: str, query: str, limit: int = 20) -> dict:
        """搜索知识库中的笔记"""
        cache_key = f"search_notes:{kb_id}:{query}:{limit}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        body = {
            "knowledge_base_id": kb_id,
            "query": query,
            "cursor": "",
            "limit": limit
        }

        response = await self._api_call('search_knowledge', body)

        if response.get('retcode', 0) == 0:
            data = response.get('data', {})
            results = data.get('infos', data.get('info_list', []))
            result = {
                "status": "success",
                "count": len(results),
                "results": results
            }
            self._cache.set(cache_key, result, ttl=30)
            return result
        else:
            return {
                "status": "error",
                "message": response.get('errmsg', response.get('msg', 'Unknown error')),
                "results": []
            }

    async def batch_get_notes(self, kb_id: str, doc_ids: List[str], format: str = 'text') -> dict:
        """批量获取笔记内容（并发执行）"""
        if not doc_ids:
            return {"status": "error", "message": "doc_ids is empty", "notes": []}

        # 并发获取所有笔记
        tasks = [self.get_note_content(kb_id, doc_id, format) for doc_id in doc_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        notes = []
        errors = []
        for doc_id, result in zip(doc_ids, results):
            if isinstance(result, Exception):
                errors.append({"doc_id": doc_id, "error": f"{type(result).__name__}: {str(result)[:200]}"})
            elif result.get('status') == 'success':
                notes.append(result)
            else:
                errors.append({"doc_id": doc_id, "error": result.get('message', '')})

        return {
            "status": "success",
            "total": len(doc_ids),
            "success_count": len(notes),
            "error_count": len(errors),
            "notes": notes,
            "errors": errors
        }

    async def close(self):
        """关闭HTTP客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
