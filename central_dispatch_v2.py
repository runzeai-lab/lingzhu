#!/usr/bin/env python3
"""
中央调度系统 V2.1（V191.1 升级）
端口：8889
功能：Agent注册、心跳保活、任务分配、状态监控

V191.1 升级内容：
✅ 心跳端点 POST /agents/heartbeat
✅ 单次查询 GET /agents/{name}
✅ 心跳超时检查（90秒）
✅ Agent 状态字段（online / offline）
✅ 启动时自动清理过期 Agent
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import time
import json
from datetime import datetime, timedelta

# ─── 内存数据存储 ─────────────────────────────────────────────────────────
agents = {}
tasks = {}
task_counter = 0

# ─── 配置 ─────────────────────────────────────────────────────────────────
HEARTBEAT_TIMEOUT = 90  # 心跳超时（秒），超过此时间未上报心跳视为离线


def _cleanup_offline_agents():
    """清理过期 Agent（心跳超时）"""
    now = datetime.now()
    offline_names = []
    for name, info in list(agents.items()):
        last_str = info.get("last_heartbeat", info.get("registered_at", ""))
        if not last_str:
            continue
        try:
            last_time = datetime.fromisoformat(last_str)
            if (now - last_time).total_seconds() > HEARTBEAT_TIMEOUT:
                offline_names.append(name)
        except Exception:
            pass
    for name in offline_names:
        print(f"[心跳检查] ⚠️  Agent {name} 心跳超时，标记为离线")
        agents[name]["status"] = "offline"
    return len(offline_names)


# ─── FastAPI 应用 ──────────────────────────────────────────────────────────
app = FastAPI(title="中央调度系统 V2.1", version="2.1.0")


@app.get("/health")
async def health():
    _cleanup_offline_agents()
    online_count = sum(1 for a in agents.values() if a.get("status") == "online")
    return {
        "status": "ok",
        "service": "central-dispatch",
        "version": "2.1.0",
        "agents_count": len(agents),
        "agents_online": online_count,
        "agents_offline": len(agents) - online_count,
        "tasks_count": len(tasks),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/agents/register")
async def register_agent(request: Request):
    """注册 Agent（如已存在则更新）"""
    try:
        body = await request.body()
        data = json.loads(body.decode("utf-8"))

        name = data.get("name", "unknown")
        url = data.get("url", "")
        port = data.get("port", 0)
        version = data.get("version", "unknown")
        capabilities = data.get("capabilities", [])

        now_iso = datetime.now().isoformat()
        if name in agents:
            # 已存在：更新信息，保持 online
            agents[name].update({
                "url": url,
                "port": port,
                "version": version,
                "capabilities": capabilities,
                "last_heartbeat": now_iso,
                "status": "online"
            })
            print(f"🔄 Agent 重新注册: {name} (端口 {port})")
        else:
            agents[name] = {
                "name": name,
                "url": url,
                "port": port,
                "version": version,
                "capabilities": capabilities,
                "registered_at": now_iso,
                "last_heartbeat": now_iso,
                "status": "online"
            }
            print(f"✅ Agent 注册成功: {name} (端口 {port})")

        return {
            "status": "ok",
            "message": f"Agent {name} 注册成功",
            "agent_id": name
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/agents/heartbeat")
async def heartbeat(request: Request):
    """Agent 心跳上报"""
    try:
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        name = data.get("name", "")
        if not name:
            return JSONResponse(status_code=400, content={"error": "缺少 name 字段"})

        if name not in agents:
            return JSONResponse(status_code=404, content={"error": f"Agent {name} 未注册"})

        now_iso = datetime.now().isoformat()
        agents[name]["last_heartbeat"] = now_iso
        agents[name]["status"] = "online"
        # 可选：更新额外信息（cpu/mem/version）
        if "version" in data:
            agents[name]["version"] = data["version"]

        return {"status": "ok", "message": f"Agent {name} 心跳收到"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/agents")
async def list_agents():
    """列出所有 Agent"""
    _cleanup_offline_agents()
    return {
        "agents": agents,
        "count": len(agents)
    }


@app.get("/agents/{name}")
async def get_agent(name: str):
    """查询单个 Agent 详情"""
    _cleanup_offline_agents()
    if name not in agents:
        return JSONResponse(status_code=404, content={"error": "Agent not found"})
    return agents[name]


@app.post("/tasks")
async def create_task(request: Request):
    """创建任务"""
    global task_counter
    try:
        body = await request.body()
        data = json.loads(body.decode("utf-8"))

        task_counter += 1
        task_id = f"task_{task_counter:04d}"

        task = {
            "task_id": task_id,
            "description": data.get("description", ""),
            "priority": data.get("priority", "medium"),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "assigned_to": data.get("assigned_to", [])
        }

        tasks[task_id] = task
        print(f"✅ 任务创建成功: {task_id} - {task['description'][:50]}")

        return {"status": "ok", "task_id": task_id, "task": task}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """查询任务状态"""
    if task_id in tasks:
        return tasks[task_id]
    else:
        return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.get("/tasks")
async def list_tasks():
    """列出所有任务"""
    return {
        "tasks": tasks,
        "count": len(tasks)
    }


@app.get("/status")
async def get_status():
    """系统状态"""
    _cleanup_offline_agents()
    online = [n for n, a in agents.items() if a.get("status") == "online"]
    return {
        "service": "central-dispatch",
        "version": "2.1.0",
        "agents": {
            "total": len(agents),
            "online": len(online),
            "offline": len(agents) - len(online),
            "list": list(agents.keys()),
            "online_list": online
        },
        "tasks": {
            "total": len(tasks),
            "pending": sum(1 for t in tasks.values() if t["status"] == "pending"),
            "running": sum(1 for t in tasks.values() if t["status"] == "running"),
            "completed": sum(1 for t in tasks.values() if t["status"] == "completed")
        },
        "uptime": time.time()
    }


# ─── 主入口 ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 中央调度系统 V2.1 启动中...")
    print("   监听端口：8889")
    print("   心跳超时：90 秒")
    print("   端点：")
    print("     - GET  http://localhost:8889/health")
    print("     - POST http://localhost:8889/agents/register")
    print("     - POST http://localhost:8889/agents/heartbeat")
    print("     - GET  http://localhost:8889/agents")
    print("     - GET  http://localhost:8889/agents/{name}")
    print("     - POST http://localhost:8889/tasks")
    print("     - GET  http://localhost:8889/tasks/{task_id}")
    print("     - GET  http://localhost:8889/status")

    uvicorn.run(app, host="0.0.0.0", port=8889, log_level="warning")
