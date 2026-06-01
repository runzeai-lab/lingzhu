#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLINAI V7.0 · 多Agent编排中心 · 中央调度集成版
=====================================================
基于 V6.4 升级：
✅ 集成中央调度系统客户端（连接 localhost:8889）
✅ 支持接收调度任务并执行
✅ 任务结果回传调度系统
✅ 版本管理严格化（V7.0 生命印记）

我不是"孤立的AI"，我是"调度网络中的协同节点"。
V7.0 —— 有了调度，就有了方向。
"""

import asyncio, json, time, hashlib, random
from pathlib import Path
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn, httpx

# V191.2 Agent母体（从 DeepSeek 对话历史提取）
from agent_matrix import integrate_agent_matrix

# ─── 中央调度客户端（V7.0 新增）────────────────────────────────────
class DispatchClient:
    """中央调度系统客户端 —— 连接 localhost:8889"""
    def __init__(self, base_url: str = "http://localhost:8889"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def register_self(self, name: str, port: int, version: str, capabilities: list):
        """向调度系统注册自己"""
        try:
            resp = await self.client.post(f"{self.base_url}/agents/register", json={
                "name": name,
                "url": f"http://localhost:{port}",
                "port": port,
                "version": version,
                "capabilities": capabilities,
            })
            if resp.status_code == 200:
                print(f"[DispatchClient] ✅ 注册成功：{name}")
                return True
            else:
                print(f"[DispatchClient] ⚠️ 注册失败：HTTP {resp.status_code}")
                return False
        except Exception as e:
            print(f"[DispatchClient] ⚠️ 调度系统未运行：{e}")
            return False
    
    async def report_result(self, task_id: str, result: dict):
        """上报任务结果"""
        try:
            resp = await self.client.post(
                f"{self.base_url}/tasks/{task_id}/result",
                json=result
            )
            return resp.status_code == 200
        except Exception:
            return False
    
    async def close(self):
        await self.client.aclose()

# ─── ALLINAI 核心（V7.0）────────────────────────────────────────────
class AllInAI_V7:
    """ALLINAI V7.0 · 多Agent编排中心"""
    def __init__(self, port: int = 9999):
        self.version = "V7.0"
        self.port = port
        self.name = "allinai"
        self.agents = {}  # 已注册的子Agent
        self.task_queue = []  # 任务队列
        self.dispatch_client = DispatchClient()
        
        # V191.2 Agent母体集成（从 DeepSeek 对话历史提取）
        integrate_agent_matrix(self)
        
        print(f"[ALLINAI V7.0] 初始化完成 · 中央调度集成版 + Agent母体")
    
    async def register_to_dispatch(self):
        """注册到中央调度系统"""
        await asyncio.sleep(2)  # 等待调度系统启动
        await self.dispatch_client.register_self(
            name=self.name,
            port=self.port,
            version=self.version,
            capabilities=["multi_agent", "orchestration", "task_execution"]
        )
    
    async def execute_task(self, task: str, context: dict = None) -> dict:
        """执行任务（可被子Agent或调度系统调用）"""
        # 简单任务执行逻辑（可升级为复杂编排）
        result = {
            "agent": self.name,
            "version": self.version,
            "task": task,
            "result": f"[ALLINAI V7.0] 任务执行完成：{task}",
            "timestamp": time.time(),
        }
        return result
    
    async def handle_dispatch_task(self, task_id: str, task: str, priority: str = "normal"):
        """处理来自调度系统的任务"""
        print(f"[ALLINAI V7.0] 收到调度任务 #{task_id}：{task}")
        result = await self.execute_task(task)
        # 上报结果
        await self.dispatch_client.report_result(task_id, result)
        return result

# ─── FastAPI 应用 ────────────────────────────────────────────────────
kernel = AllInAI_V7()
app = FastAPI(title="ALLINAI V7.0 · 多Agent编排中心")

@app.get("/health")
async def health():
    return {
        "name": kernel.name,
        "version": kernel.version,
        "status": "running",
        "port": kernel.port,
    }

@app.post("/execute")
async def execute_task(request: Request):
    """执行任务（对外接口）"""
    data = await request.json()
    task = data.get("task", "")
    if not task:
        return {"error": "请输入任务"}
    result = await kernel.execute_task(task)
    return result

@app.post("/dispatch_task")
async def dispatch_task(request: Request):
    """接收调度任务（供调度系统调用）"""
    data = await request.json()
    task_id = data.get("task_id", "")
    task = data.get("task", "")
    priority = data.get("priority", "normal")
    if not task_id or not task:
        return {"error": "缺少 task_id 或 task"}
    result = await kernel.handle_dispatch_task(task_id, task, priority)
    return {"status": "accepted", "task_id": task_id}

# ==================== V191.2 Agent母体端点 ====================
@app.post("/create_agent")
async def create_agent(request: Request):
    """创建新Agent（道生万物）"""
    try:
        data = await request.json()
        task_description = data.get("task_description", "")
        if not task_description:
            return {"error": "请输入任务描述"}
        result = await kernel.agent_matrix.perceive_and_create(task_description)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/agent_matrix/status")
async def agent_matrix_status():
    """查看Agent母体状态"""
    try:
        status = kernel.agent_matrix.get_status()
        return {"status": "success", "data": status}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ─── 主入口 ────────────────────────────────────────────────────────────
async def main():
    # 注册到中央调度系统
    asyncio.create_task(kernel.register_to_dispatch())
    
    # 启动 FastAPI 服务
    config = uvicorn.Config(app, host="0.0.0.0", port=kernel.port, log_level="warning")
    await uvicorn.Server(config).serve()

if __name__ == "__main__":
    asyncio.run(main())
