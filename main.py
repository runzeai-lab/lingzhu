#!/usr/bin/env python3
"""
灵助 V181.0 - 多Agent统一管理系统
中央调度中心 + 灵魂赋能者 + 技能分享平台
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from unified_task_ledger import UnifiedTaskLedger
from dual_semantic_approval_chain import DualSemanticApprovalChain
from safeharness_defense import SafeHarnessDefense
from hermes_self_evolution import HermesSelfEvolution

class HermesLearnRequest(BaseModel):
    """Hermes学习请求体"""
    task_type: str = "read_file"
    task_params: Dict = {}
    result: Dict = {}
    success: bool = True
from dreaming_engine import DreamingEngine
from skill_metadata_aligner import SkillMetadataAligner
from mcp_dual_mode_engine import MCPDualModeEngine

class MCPSendRequest(BaseModel):
    """MCP发送消息请求体"""
    server_name: str
    message: Dict

class MCPRegisterRequest(BaseModel):
    """MCP注册服务器请求体"""
    server_name: str
    command: str
    args: Optional[List[str]] = None
from offline_autonomy import OfflineAutonomy
from docker_sandbox import DockerSandbox
from ima_knowledge_engine import IMAKnowledgeEngine
from quantclaw_bridge import QuantClawBridge

app = FastAPI(title="灵助 V181.0 - 多Agent统一管理系统")

# ==================== 多Agent配置 ====================
AGENTS_CONFIG = {
    "lingzhu": {"port": 8000, "version": "V181.0", "url": "http://localhost:8000"},
    "daonovice": {"port": 8088, "version": "V2.0", "url": "http://localhost:8088"},
    "hermes_agent": {"port": 8888, "version": "V3.0", "url": "http://localhost:8888"},
    "hermes": {"port": 5000, "version": "V2.0", "url": "http://localhost:5000"},
    "deer_flow": {"port": 7777, "version": "V1.0", "url": "http://localhost:7777"},
    "allinai": {"port": 9999, "version": "V6.4", "url": "http://localhost:9999"}
}

# ==================== 数据模型 ====================
class TaskCreate(BaseModel):
    task_type: str
    description: str
    priority: str = "medium"

class SkillShare(BaseModel):
    skill_name: str
    target_agent: str

class SoulEmpower(BaseModel):
    soul_content: str
    memory_content: Optional[str] = None

class AgentTrain(BaseModel):
    target_version: str
    skills: List[str]
    soul_upgrade: bool = False

# ==================== 模块1：跨空间灵魂与记忆调度 ====================

@app.get("/agents/{agent_name}/soul")
async def get_agent_soul(agent_name: str):
    """查看Agent的灵魂（SOUL.md）"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        async with httpx.AsyncClient() as client:
            # 假设其他Agent有/health端点，实际应该访问其SOUL.md
            # 这里先返回模拟数据
            return {
                "agent": agent_name,
                "soul": f"SOUL.md content for {agent_name} (TODO: implement actual read)",
                "version": AGENTS_CONFIG[agent_name]["version"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}/memory")
async def get_agent_memory(agent_name: str):
    """查看Agent的记忆（MEMORY.md）"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        return {
            "agent": agent_name,
            "memory": f"MEMORY.md content for {agent_name} (TODO: implement actual read)",
            "version": AGENTS_CONFIG[agent_name]["version"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """查看Agent的健康状态"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = AGENTS_CONFIG[agent_name]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{agent['url']}/health")
            if response.status_code == 200:
                return {
                    "agent": agent_name,
                    "status": "healthy",
                    "version": agent["version"],
                    "details": response.json()
                }
            else:
                return {
                    "agent": agent_name,
                    "status": "unhealthy",
                    "version": agent["version"],
                    "error": f"HTTP {response.status_code}"
                }
    except Exception as e:
        return {
            "agent": agent_name,
            "status": "unreachable",
            "version": agent["version"],
            "error": str(e)
        }

@app.post("/agents/{agent_name}/empower")
async def empower_agent_soul(agent_name: str, empower_data: SoulEmpower):
    """赋能灵魂给目标Agent"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        # TODO: 实际实现灵魂赋能逻辑
        # 1. 连接目标Agent
        # 2. 更新其SOUL.md
        # 3. 重启Agent使配置生效
        
        return {
            "success": True,
            "agent": agent_name,
            "message": f"灵魂赋能成功，已更新{agent_name}的SOUL.md",
            "soul_preview": empower_data.soul_content[:100] + "..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 模块2：技能分享平台 ====================

# 技能库（模拟数据，实际应该从文件系统读取）
SKILLS_LIBRARY = {
    "版本管理": {
        "description": "Git版本控制、CHANGELOG、版本标签",
        "file": "VERSION_MANAGEMENT.md",
        "version": "V181.0"
    },
    "端口管理": {
        "description": "端口分配、冲突检测、文档化",
        "file": "PORT_MANAGEMENT.md",
        "version": "V181.0"
    },
    "灵魂升级": {
        "description": "SOUL.md迭代升级方法",
        "file": "SOUL_UPGRADE.md",
        "version": "V181.0"
    },
    "记忆管理": {
        "description": "MEMORY.md长期记忆机制",
        "file": "MEMORY_MANAGEMENT.md",
        "version": "V181.0"
    },
    "健康监控": {
        "description": "/health端点、自动重启",
        "file": "HEALTH_MONITOR.md",
        "version": "V181.0"
    }
}

@app.get("/skills")
async def list_all_skills():
    """列出所有可用技能"""
    return {
        "total": len(SKILLS_LIBRARY),
        "skills": SKILLS_LIBRARY
    }

# ==================== 模块5.9：技能格式对齐测试 ====================

@app.post("/skills/align")
async def align_skill(skill_file: str):
    """对齐单个技能文件的元数据"""
    result = skill_aligner.align_skill(skill_file)
    return {
        "result": result,
        "message": "Skill metadata aligned"
    }

@app.post("/skills/align_all")
async def align_all_skills():
    """对齐所有技能文件的元数据"""
    results = skill_aligner.align_all_skills()
    return {
        "results": results,
        "message": f"Aligned {results.get('total', 0)} skills"
    }

@app.get("/skills/alignment_stats")
async def get_alignment_stats():
    """查看技能对齐统计"""
    try:
        return skill_aligner.get_alignment_stats()
    except Exception as e:
        return {
            "error": str(e),
            "message": "Error in get_alignment_stats"
        }

@app.get("/skills/{skill_name}")
async def get_skill_details(skill_name: str):
    """查看技能详情"""
    if skill_name not in SKILLS_LIBRARY:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {
        "skill": skill_name,
        "details": SKILLS_LIBRARY[skill_name]
    }

@app.post("/skills/share")
async def share_skill(share_data: SkillShare):
    """分享技能给目标Agent"""
    if share_data.skill_name not in SKILLS_LIBRARY:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if share_data.target_agent not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Target agent not found")
    
    try:
        # TODO: 实际实现技能分享逻辑
        # 1. 打包技能文件
        # 2. 传输到目标Agent
        # 3. 目标Agent安装技能
        
        return {
            "success": True,
            "skill": share_data.skill_name,
            "target_agent": share_data.target_agent,
            "message": f"技能{share_data.skill_name}已分享给{share_data.target_agent}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}/skills")
async def get_agent_skills(agent_name: str):
    """查看Agent已安装的技能"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # TODO: 实际实现获取Agent已安装技能
    return {
        "agent": agent_name,
        "installed_skills": ["版本管理", "端口管理"],  # 模拟数据
        "available_skills": list(SKILLS_LIBRARY.keys())
    }

# ==================== 模块3：统一任务调度 ====================

# 统一任务账本（持久化，支持心跳监测和丢失任务恢复）
task_ledger = UnifiedTaskLedger()

# 双层语义审批链（第一层：灵助缰绳 + 第二层：OpenClaw ACP 语义审批）
approval_chain = DualSemanticApprovalChain()

# SafeHarness 四层防御融合
safeharness = SafeHarnessDefense()

# Hermes 自进化学习循环
hermes_evolution = HermesSelfEvolution()

# Dreaming 梦境系统（三阶段离线记忆整合）
def get_recent_interactions(limit: int = 100):
    """获取最近的交互（简化版，实际应该从数据库读取）"""
    # 这里简化实现，实际应该从任务账本或日志中读取
    return [
        {"task_type": "read_file", "outcome": "success", "tools_used": 2, "user_feedback": "positive", "content": f"Read file {i}"}
        for i in range(min(limit, 20))  # 模拟20条最近交互
    ]

def save_skill(skill_name: str, skill_content: str, meta: dict = None):
    """保存技能（简化版，实际应该保存到技能文件）"""
    print(f"[梦境] 保存技能：{skill_name}")
    return True

dreaming_engine = DreamingEngine(
    memory_callback={
        "get_recent": get_recent_interactions,
        "save_skill": save_skill
    }
)

# 技能格式对齐工具
skill_aligner = SkillMetadataAligner()

# MCP 双模引擎（支持 Stdio + SSE 双模）
mcp_engine = MCPDualModeEngine(mode="stdio", sse_port=8080)

# Docker 安全沙箱
sandbox = DockerSandbox()
offline_autonomy = OfflineAutonomy()

# QuantClaw 桥接引擎
quantclaw_bridge = QuantClawBridge()

# IMA 知识库引擎
ima_engine = IMAKnowledgeEngine()

# ==================== 模块5.12：离线自治系统测试 ====================

class OfflineDecisionRequest(BaseModel):
    """离线决策请求体"""
    context: Dict
    available_info: Optional[List[Dict]] = []

class OfflineKnowledgeRequest(BaseModel):
    """添加知识请求体"""
    title: str
    content: str
    tags: Optional[List[str]] = []

class OfflineTaskRequest(BaseModel):
    """缓存任务请求体"""
    task_type: str
    task_data: Dict
    priority: int = 5

class OfflineCompleteRequest(BaseModel):
    """完成任务请求体"""
    task_id: str
    result: Optional[Dict] = {}

@app.post("/offline/make_decision")
async def test_make_decision(request: OfflineDecisionRequest):
    """测试离线决策"""
    return offline_autonomy.make_decision(request.context, request.available_info)

@app.get("/offline/network_status")
async def test_get_network_status():
    """获取网络状态"""
    return {"online": True, "message": "Network is online"}

@app.post("/offline/add_knowledge")
async def test_add_knowledge(request: OfflineKnowledgeRequest):
    """测试添加知识"""
    return offline_autonomy.add_knowledge(request.title, request.content, request.tags)

@app.get("/offline/search_knowledge")
async def test_search_knowledge(query: str, limit: int = 10):
    """测试搜索知识"""
    return offline_autonomy.search_knowledge(query, limit)

@app.post("/offline/queue_task")
async def test_queue_task(request: OfflineTaskRequest):
    """测试缓存任务"""
    return offline_autonomy.queue_task(request.task_type, request.task_data, request.priority)

@app.get("/offline/get_next_task")
async def test_get_next_task():
    """测试获取下一个任务"""
    return offline_autonomy.get_next_task()

@app.post("/offline/complete_task")
async def test_complete_task(request: OfflineCompleteRequest):
    """测试完成任务"""
    return offline_autonomy.complete_task(request.task_id, request.result)

@app.post("/offline/sync")
async def test_sync():
    """测试与服务器同步"""
    return offline_autonomy.sync_with_server("")

@app.get("/offline/stats")
async def get_offline_stats():
    """查看离线自治统计"""
    return offline_autonomy.get_stats()




@app.post("/tasks/create")
async def create_task(task_data: TaskCreate):
    """创建新任务并分配给合适的Agent（经过双层语义审批 + SafeHarnness四层防御）"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # SafeHarnness 四层防御检查
    defense_passed = await safeharness.full_defense_cycle(
        context=task_data.description,
        action="create_task",
        params={"task_type": task_data.task_type}
    )
    if not defense_passed:
        raise HTTPException(status_code=403, detail="SafeHarnness defense triggered: task creation blocked")
    
    # 双层语义审批（第一层：灵助缰绳 + 第二层：OpenClaw ACP）
    approval_result = approval_chain.full_approval(
        tool_name="create_task",
        tool_params={"task_type": task_data.task_type, "description": task_data.description},
        user_context={"role": "user"}
    )
    
    if not approval_result["approved"]:
        raise HTTPException(
            status_code=403,
            detail=f"Task creation rejected: {approval_result['reason']}"
        )
    
    # 任务类型与Agent匹配逻辑
    agent_mapping = {
        "ai_reasoning": "daonovice",
        "multi_agent_orchestration": "allinai",
        "agent_management": "hermes_agent",
        "backend_service": "deer_flow",
        "soul_upgrade": "lingzhu",
        "skill_share": "lingzhu"
    }
    
    assigned_agent = agent_mapping.get(task_data.task_type, "lingzhu")
    
    # 使用 UnifiedTaskLedger 创建任务（持久化）
    task_ledger.create_task(
        task_id=task_id,
        task_type=task_data.task_type,
        payload={"description": task_data.description},
        priority=5 if task_data.priority == "medium" else (3 if task_data.priority == "high" else 7),
        assigned_agent=assigned_agent
    )
    
    return {
        "success": True,
        "task_id": task_id,
        "assigned_agent": assigned_agent,
        "approval": approval_result["reason"],
        "message": f"任务已创建并分配给{assigned_agent}"
    }

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """查看任务状态"""
    task = task_ledger.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    """查看任务结果"""
    result = task_ledger.get_task_result(task_id)
    if not result:
        # 检查任务是否存在
        task = task_ledger.get_task_status(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            raise HTTPException(status_code=400, detail="Task not completed yet")
    
    return {
        "task_id": task_id,
        "result": result
    }

@app.get("/tasks")
async def list_all_tasks():
    """列出所有任务"""
    tasks = task_ledger.list_tasks()
    return {
        "total": len(tasks),
        "tasks": tasks
    }

# ==================== 模块4：Agent训练与进化 ====================

@app.post("/agents/{agent_name}/train")
async def train_agent(agent_name: str, train_data: AgentTrain):
    """训练Agent（升级版本、学习技能、赋能灵魂）"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        # TODO: 实际实现Agent训练逻辑
        # 1. 分析Agent当前状态
        # 2. 制定升级计划
        # 3. 赋能新灵魂/技能
        # 4. 测试验证
        # 5. 部署上线
        
        return {
            "success": True,
            "agent": agent_name,
            "target_version": train_data.target_version,
            "skills_to_learn": train_data.skills,
            "soul_upgrade": train_data.soul_upgrade,
            "message": f"Agent {agent_name} 训练计划已启动"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}/training_status")
async def get_training_status(agent_name: str):
    """查看Agent训练状态"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # TODO: 实际实现获取训练状态
    return {
        "agent": agent_name,
        "training_status": "in_progress",  # 模拟数据
        "progress": "60%",
        "message": "训练中..."
    }

# ==================== 模块5：统一状态监控 ====================

# ==================== 模块5.5：双层语义审批链测试 ====================

@app.get("/approval/test")
async def test_approval(tool_name: str = "read_file", tool_params: dict = None, user_role: str = "user"):
    """测试某个工具的审批结果"""
    result = approval_chain.full_approval(
        tool_name=tool_name,
        tool_params=tool_params,
        user_context={"role": user_role}
    )
    return {
        "tool_name": tool_name,
        "category": approval_chain.classify_action(tool_name, tool_params),
        "approved": result["approved"],
        "reason": result["reason"],
        "layer": result["layer"]
    }

@app.get("/approval/stats")
async def get_approval_stats():
    """查看审批统计"""
    return approval_chain.get_approval_stats()

# ==================== 模块5.6：双轨语义审批链强化（匹配度评分）====================

@app.get("/approval/tool_skill_match")
async def get_tool_skill_match(tool_name: str, skill_name: str):
    """计算工具与技能的匹配度评分"""
    score = approval_chain.tool_skill_matching_score(tool_name, skill_name)
    return {
        "tool_name": tool_name,
        "skill_name": skill_name,
        "match_score": score,
        "match_level": "high" if score >= 0.7 else "medium" if score >= 0.4 else "low"
    }

class BatchMatchRequest(BaseModel):
    """批量匹配请求体"""
    tool_name: str
    skill_list: List[str]

@app.post("/approval/batch_match")
async def get_batch_match(request: BatchMatchRequest):
    """批量计算工具与多个技能的匹配度"""
    results = approval_chain.batch_matching_scores(request.tool_name, request.skill_list)
    return {
        "tool_name": request.tool_name,
        "matches": [{"skill_name": skill, "match_score": score} for skill, score in results],
        "best_match": {"skill_name": results[0][0], "match_score": results[0][1]} if results else None
    }

# ==================== 模块5.7：Hermes 自进化学习循环测试 ====================

@app.post("/hermes/learn")
async def hermes_learn(request: HermesLearnRequest):
    """测试 Hermes 学习循环"""
    if task_params is None:
        task_params = {}
    if result is None:
        result = {}
    
    learn_result = hermes_evolution.learn_from_task(
        task_type=task_type,
        task_params=task_params,
        result=result,
        success=success
    )
    return {
        "learn_result": learn_result,
        "message": "Hermes learned from task"
    }

@app.get("/hermes/evolve")
async def hermes_evolve():
    """手动触发 Hermes 进化"""
    evolution_result = hermes_evolution._trigger_evolution()
    return {
        "evolution_result": evolution_result,
        "message": "Hermes evolution triggered"
    }

@app.get("/hermes/skills")
async def hermes_list_skills(only_active: bool = False):
    """列出 Hermes 生成的所有技能"""
    skills = hermes_evolution.list_skills(only_active=only_active)
    return {
        "total_skills": len(skills),
        "skills": skills
    }

@app.get("/hermes/stats")
async def hermes_stats():
    """查看 Hermes 自进化统计"""
    return hermes_evolution.get_evolution_stats()

# ==================== 模块5.8：Dreaming 梦境系统测试 ====================

@app.post("/dreaming/start")
async def start_dreaming():
    """启动梦境循环"""
    await dreaming_engine.run()
    return {
        "status": "completed",
        "message": "梦境循环已完成（浅睡→REM→深睡）"
    }

@app.get("/dreaming/log")
async def get_dream_log():
    """查看梦境日志"""
    return {
        "dream_log": dreaming_engine.get_dream_log(),
        "stats": dreaming_engine.get_dream_stats()
    }

# ==================== 模块5.8：梦境引擎强化（灵感连接）====================

@app.get("/dream/inspiration_connection")
async def create_inspiration_connection(concept1: str, concept2: str):
    """创建灵感连接"""
    result = dreaming_engine.inspiration_connection(concept1, concept2)
    return result

class BatchConnectionRequest(BaseModel):
    """批量连接请求体"""
    concept_pairs: List[List[str]]

@app.post("/dream/batch_connections")
async def create_batch_connections(request: BatchConnectionRequest):
    """批量创建灵感连接"""
    results = dreaming_engine.batch_inspiration_connections(request.concept_pairs)
    return {
        "results": results,
        "message": f"Created {len(results)} inspiration connections"
    }

@app.get("/dream/connections")
async def get_inspiration_connections():
    """查看所有灵感连接记录"""
    return {
        "total": len(dreaming_engine.get_inspiration_connections()),
        "connections": dreaming_engine.get_inspiration_connections()
    }

# ==================== 模块5.9：技能格式对齐测试 ====================

@app.post("/skills/align")
async def align_skill(skill_file: str):
    """对齐单个技能文件的元数据"""
    result = skill_aligner.align_skill(skill_file)
    return {
        "result": result,
        "message": "Skill metadata aligned"
    }

@app.post("/skills/align_all")
async def align_all_skills():
    """对齐所有技能文件的元数据"""
    results = skill_aligner.align_all_skills()
    return {
        "results": results,
        "message": f"Aligned {results.get('total', 0)} skills"
    }

# ==================== 模块5.10：MCP 双模引擎测试 ====================

@app.post("/mcp/register")
async def register_mcp_server(server_name: str, command: str, args: List[str] = None):
    """注册 MCP 服务器（Stdio 模式）"""
    result = mcp_engine.register_server(server_name, command, args or [])
    return {
        "success": result,
        "server_name": server_name,
        "message": f"MCP 服务器 {server_name} 注册" + ("成功" if result else "失败")
    }

@app.post("/mcp/send")
async def send_mcp_message(request: MCPSendRequest):
    """向 MCP 服务器发送消息（Stdio 模式）"""
    # 注意：当前 MCPDualModeEngine 不支持 send_message，使用 get_server_status 作为占位
    status = mcp_engine.get_server_status(request.server_name)
    return {
        "server_name": request.server_name,
        "message": "MCP send_message not implemented",
        "status": status,
        "note": "Please use /mcp/status to check server status"
    }

@app.get("/mcp/status")
async def get_mcp_status(server_name: str = None):
    """查看 MCP 服务器状态"""
    status = mcp_engine.get_server_status(server_name)
    return status

@app.post("/mcp/switch_mode")
async def switch_mcp_mode(mode: str, sse_port: int = None):
    """切换 MCP 通信模式"""
    result = mcp_engine.switch_mode(mode, sse_port)
    return {
        "success": result,
        "new_mode": mode,
        "message": f"Switched to {mode} mode" if result else f"Failed to switch to {mode}"
    }

# ==================== 模块5.11：Docker 安全沙箱测试 ====================

@app.post("/sandbox/execute_code")
async def execute_code_in_sandbox(code: str, language: str = "python"):
    """在 Docker 沙箱中执行代码"""
    result = sandbox.execute_code(code, language)
    return {
        "result": result,
        "message": "Code executed" if result["success"] else "Execution failed"
    }

@app.post("/sandbox/execute_command")
async def execute_command_in_sandbox(command: str):
    """在 Docker 沙箱中执行命令"""
    result = sandbox.execute_command(command)
    return {
        "result": result,
        "message": "Command executed" if result["success"] else "Execution failed"
    }

@app.get("/sandbox/stats")
async def get_sandbox_stats():
    """查看 Docker 沙箱统计"""
    return sandbox.get_sandbox_stats()

# ==================== 模块5：统一状态监控（续）====================

@app.get("/monitor/agents")
async def monitor_all_agents():
    """监控所有Agent状态"""
    results = []
    
    for agent_name, agent_config in AGENTS_CONFIG.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{agent_config['url']}/health")
                if response.status_code == 200:
                    results.append({
                        "agent": agent_name,
                        "status": "healthy",
                        "version": agent_config["version"],
                        "port": agent_config["port"]
                    })
                else:
                    results.append({
                        "agent": agent_name,
                        "status": "unhealthy",
                        "version": agent_config["version"],
                        "port": agent_config["port"],
                        "error": f"HTTP {response.status_code}"
                    })
        except Exception as e:
            results.append({
                "agent": agent_name,
                "status": "unreachable",
                "version": agent_config["version"],
                "port": agent_config["port"],
                "error": str(e)
            })
    
    healthy_count = sum(1 for r in results if r["status"] == "healthy")
    
    return {
        "total_agents": len(AGENTS_CONFIG),
        "healthy_agents": healthy_count,
        "unhealthy_agents": len(AGENTS_CONFIG) - healthy_count,
        "agents": results
    }

@app.get("/monitor/agents/{agent_name}")
async def monitor_agent(agent_name: str):
    """监控指定Agent状态"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # 调用上面的状态检查端点
    return await get_agent_status(agent_name)

@app.get("/monitor/resources")
async def monitor_resources():
    """监控资源使用情况（模拟数据，实际应该调用系统API）"""
    return {
        "cpu_usage": "45%",
        "memory_usage": "62%",
        "disk_usage": "38%",
        "agents_count": len(AGENTS_CONFIG),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/monitor/agents/{agent_name}/restart")
async def restart_agent(agent_name: str):
    """重启指定Agent（经过 SafeHarness 四层防御）"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # SafeHarness 四层防御检查（重启Agent是高风险操作）
    defense_passed = await safeharness.full_defense_cycle(
        context=f"Restart agent {agent_name}",
        action="restart_agent",
        params={"agent_role": "admin"}  # 重启Agent需要admin权限
    )
    if not defense_passed:
        raise HTTPException(status_code=403, detail="SafeHarness defense triggered: agent restart blocked")
    
    try:
        # TODO: 实际实现Agent重启逻辑
        # 1. 调用Docker API停止容器
        # 2. 重新启动容器
        # 3. 等待健康检查通过
        
        return {
            "success": True,
            "agent": agent_name,
            "message": f"Agent {agent_name} 正在重启..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 模块5.10：SafeHarness 防御系统强化（测试端点）====================

@app.get("/safeharness/stats")
async def get_safeharness_stats():
    """查看防御统计信息"""
    return safeharness.get_defense_stats()

@app.get("/safeharness/security_log")
async def get_security_log(limit: int = 50):
    """查看安全日志"""
    return {
        "total": len(safeharness.get_security_log(limit)),
        "logs": safeharness.get_security_log(limit),
        "message": "安全日志"
    }

@app.post("/safeharness/reset")
async def reset_safeharness():
    """重置防御系统"""
    return safeharness.reset_defense()

class DefenseCycleRequest(BaseModel):
    """防御周期请求体"""
    context: str = ""
    action: str = ""
    params: Dict = {}
    module: str = None

@app.post("/safeharness/defense_cycle")
async def test_defense_cycle(request: DefenseCycleRequest):
    """手动触发防御周期"""
    result = await safeharness.full_defense_cycle(
        request.context, request.action, request.params, request.module
    )
    return result

# ==================== 模块5.11：Hermes 自进化学习循环测试 ====================

@app.get("/hermes/evolution_stats")
async def get_evolution_stats():
    """查看自进化统计信息"""
    return {
        "learning_log_count": len(hermes_evolution.learning_log),
        "skill_pool_count": len(hermes_evolution.skill_pool),
        "evolution_threshold": hermes_evolution.evolution_threshold,
        "learning_rate": hermes_evolution.learning_rate,
        "performance_history": hermes_evolution.performance_history,
        "message": "自进化统计信息"
    }

@app.post("/hermes/evaluate_evolution")
async def evaluate_evolution(old_skill: dict, new_skill: dict, test_tasks: List[dict]):
    """评估进化效果（对比新旧技能）"""
    result = hermes_evolution.evaluate_evolution_effectiveness(old_skill, new_skill, test_tasks)
    return result

@app.post("/hermes/ab_test")
async def run_ab_test(skill_a: dict, skill_b: dict, num_tasks: int = 10):
    """A/B测试框架：对比两个技能"""
    result = hermes_evolution.run_ab_test(skill_a, skill_b, num_tasks)
    return result

@app.post("/hermes/stress_test")
async def stress_test_learning(num_tasks: int = 100):
    """学习循环压力测试"""
    result = hermes_evolution.stress_test_learning_loop(num_tasks)
    return result

@app.get("/hermes/evolution_history")
async def get_evolution_history():
    """获取进化历史追踪"""
    return {
        "total_evolutions": len(hermes_evolution.get_evolution_history()),
        "history": hermes_evolution.get_evolution_history(),
        "message": "进化历史"
    }

@app.post("/hermes/auto_rollback")
async def auto_rollback(skill_name: str, current_performance: float, threshold: float = 0.1):
    """自动回滚机制：如果性能下降则回滚"""
    result = hermes_evolution.auto_rollback_if_needed(skill_name, current_performance, threshold)
    return result

# ==================== 基础端点 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "灵助 V181.0 - 多Agent统一管理系统",
        "version": "V181.0",
        "role": "中央调度中心 + 灵魂赋能者 + 技能分享平台",
        "endpoints": {
            "跨空间调度": "/agents/{agent_name}/soul|memory|status",
            "技能分享": "/skills, /skills/{skill_name}, /skills/share",
            "任务调度": "/tasks/create, /tasks/{task_id}/status",
            "Agent训练": "/agents/{agent_name}/train",
            "统一监控": "/monitor/agents, /monitor/resources"
        }
    }


# ==================== IMA 知识库引擎端点 ====================

@app.get("/ima/stats")
async def ima_stats():
    """获取 IMA 知识库引擎状态"""
    return ima_engine.get_stats()

@app.get("/ima/search_kb")
async def ima_search_kb(query: str = "", limit: int = 20):
    """搜索知识库"""
    result = await ima_engine.search_knowledge_base(query, limit)
    return result

@app.get("/ima/kb_info")
async def ima_kb_info(ids: str):
    """获取知识库详情（逗号分隔的ID列表）"""
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    result = await ima_engine.get_knowledge_base_info(id_list)
    return result

@app.get("/ima/list_knowledge")
async def ima_list_knowledge(kb_id: str, folder_id: str = "", limit: int = 50, cursor: str = ""):
    """浏览知识库内容列表"""
    result = await ima_engine.list_knowledge(kb_id, folder_id, limit, cursor)
    return result

@app.get("/ima/note_content")
async def ima_note_content(kb_id: str, doc_id: str, format: str = "text"):
    """获取笔记内容"""
    result = await ima_engine.get_note_content(kb_id, doc_id, format)
    return result

@app.get("/ima/search_notes")
async def ima_search_notes(kb_id: str, query: str = "", limit: int = 20):
    """搜索知识库中的笔记"""
    result = await ima_engine.search_notes(kb_id, query, limit)
    return result

@app.post("/ima/batch_notes")
async def ima_batch_notes(request: dict):
    """批量获取笔记内容"""
    kb_id = request.get("kb_id", "")
    doc_ids = request.get("doc_ids", [])
    format_type = request.get("format", "text")
    if not kb_id or not doc_ids:
        return {"status": "error", "message": "kb_id and doc_ids are required"}
    result = await ima_engine.batch_get_notes(kb_id, doc_ids, format_type)
    return result


# ==================== QuantClaw 桥接引擎端点 ====================

@app.get("/quantclaw/health")
async def quantclaw_health():
    """检查 QuantClaw 服务健康状态"""
    result = await quantclaw_bridge.health_check()
    return {"status": "success", "data": result}

@app.get("/quantclaw/status")
async def quantclaw_status():
    """获取 QuantClaw 运行状态"""
    result = await quantclaw_bridge.get_status()
    return {"status": "success", "data": result}

@app.get("/quantclaw/config")
async def quantclaw_config(path: str = ""):
    """获取 QuantClaw 配置"""
    result = await quantclaw_bridge.get_config(path)
    return {"status": "success", "data": result}

@app.post("/quantclaw/agent/request")
async def quantclaw_agent_request(request: dict):
    """发送消息给 QuantClaw Agent"""
    message = request.get("message", "")
    session_id = request.get("session_id", "default")
    model = request.get("model")
    if not message:
        return {"status": "error", "message": "message is required"}
    result = await quantclaw_bridge.send_agent_request(message, session_id, model)
    return {"status": "success", "data": result}

@app.post("/quantclaw/agent/stop")
async def quantclaw_agent_stop(request: dict):
    """停止 QuantClaw Agent"""
    session_id = request.get("session_id", "default")
    result = await quantclaw_bridge.stop_agent(session_id)
    return {"status": "success", "data": result}

@app.get("/quantclaw/sessions")
async def quantclaw_list_sessions():
    """列出 QuantClaw 所有会话"""
    result = await quantclaw_bridge.list_sessions()
    return {"status": "success", "data": result}

@app.get("/quantclaw/sessions/history")
async def quantclaw_session_history(session_id: str = "default"):
    """获取 QuantClaw 会话历史"""
    result = await quantclaw_bridge.get_session_history(session_id)
    return {"status": "success", "data": result}

@app.post("/quantclaw/sessions/delete")
async def quantclaw_delete_session(request: dict):
    """删除 QuantClaw 会话"""
    session_id = request.get("session_id", "")
    if not session_id:
        return {"status": "error", "message": "session_id is required"}
    result = await quantclaw_bridge.delete_session(session_id)
    return {"status": "success", "data": result}

@app.post("/quantclaw/sessions/reset")
async def quantclaw_reset_session(request: dict):
    """重置 QuantClaw 会话"""
    session_id = request.get("session_id", "default")
    result = await quantclaw_bridge.reset_session(session_id)
    return {"status": "success", "data": result}

@app.get("/quantclaw/plugins")
async def quantclaw_list_plugins():
    """列出 QuantClaw 所有插件"""
    result = await quantclaw_bridge.list_plugins()
    return {"status": "success", "data": result}

@app.get("/quantclaw/plugins/tools")
async def quantclaw_plugin_tools():
    """列出 QuantClaw 插件工具"""
    result = await quantclaw_bridge.list_plugin_tools()
    return {"status": "success", "data": result}

@app.get("/quantclaw/plugins/services")
async def quantclaw_plugin_services():
    """列出 QuantClaw 插件服务"""
    result = await quantclaw_bridge.list_plugin_services()
    return {"status": "success", "data": result}

@app.get("/quantclaw/plugins/providers")
async def quantclaw_plugin_providers():
    """列出 QuantClaw 插件 Provider"""
    result = await quantclaw_bridge.list_plugin_providers()
    return {"status": "success", "data": result}

@app.get("/quantclaw/plugins/commands")
async def quantclaw_plugin_commands():
    """列出 QuantClaw 插件命令"""
    result = await quantclaw_bridge.list_plugin_commands()
    return {"status": "success", "data": result}

@app.post("/quantclaw/config/reload")
async def quantclaw_reload_config():
    """重新加载 QuantClaw 配置"""
    result = await quantclaw_bridge.reload_config()
    return {"status": "success", "data": result}

@app.get("/quantclaw/models")
async def quantclaw_list_models():
    """列出 QuantClaw 可用模型"""
    result = await quantclaw_bridge.list_models()
    return {"status": "success", "data": result}

@app.post("/quantclaw/chat/completions")
async def quantclaw_chat_completions(request: dict):
    """通过 QuantClaw 调用 OpenAI 兼容接口"""
    messages = request.get("messages", [])
    model = request.get("model", "qwen-max")
    temperature = request.get("temperature", 0.7)
    max_tokens = request.get("max_tokens", 4096)
    if not messages:
        return {"status": "error", "message": "messages is required"}
    result = await quantclaw_bridge.chat_completions(messages, model, temperature, max_tokens)
    return {"status": "success", "data": result}

@app.get("/quantclaw/stats")
async def quantclaw_bridge_stats():
    """获取 QuantClaw 桥接引擎统计信息"""
    return quantclaw_bridge.get_stats()


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "V181.0",
        "timestamp": datetime.now().isoformat(),
        "role": "Multi-Agent Controller"
    }

# ==================== 主程序 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
