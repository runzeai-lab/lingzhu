#!/usr/bin/env python3
"""
灵助 V180 - 多Agent统一管理系统
中央调度中心 + 灵魂赋能者 + 技能分享平台
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime

# 导入新阶段1模块（V182.0）
from cache_aware_scheduler import CacheAwareScheduler, CachePolicy, CacheState, AccessPattern
from edge_inference_adapter import EdgeInferenceAdapter, InferenceStrategy, DeviceCapability, ModelConfig

# 导入Stage 2新模块（V183.0）
from ternary_logic_simulation import (
    Trit, Hexagram19683,
    AwakeningStage, NineYaoEngine,
    Phase, FourPhaseScheduler,
    PiExpansionMemorySystem
)

# 导入Stage 3模块（V184.0）
from prime_mapper_optimized import PrimeMapperOptimized
n# 导入Stage 5模块（V186.0）- Layer 9 三进制认知架构集成
from layer9_integration import layer9_cognitive

app = FastAPI(title="灵助 V186.0 - 多Agent统一管理系统 + Layer 9三进制认知架构集成")

# ==================== 多Agent配置 ====================
AGENTS_CONFIG = {
    "lingzhu": {"port": 8000, "version": "V180", "url": "http://localhost:8000"},
    "daonovice": {"port": 8088, "version": "V2.0", "url": "http://localhost:8088"},
    "hermes_agent": {"port": 8888, "version": "V3.0", "url": "http://localhost:8888"},
    "hermes": {"port": 5000, "version": "V2.0", "url": "http://localhost:5000"},
    "deer_flow": {"port": 7777, "version": "V1.0", "url": "http://localhost:7777"},
    "allinai": {"port": 9999, "version": "V6.4", "url": "http://localhost:9999"}
}

# ==================== 阶段1新增：缓存感知调度器（V182.0）====================
cache_scheduler = CacheAwareScheduler(capacity=1000)
print(f"[V182.0] 缓存感知调度器初始化完成，容量={cache_scheduler.capacity}")

# ==================== 阶段1新增：边缘推理适配器（V182.0）====================
edge_adapter = EdgeInferenceAdapter()
print(f"[V182.0] 边缘推理适配器初始化完成，策略={edge_adapter.strategy.value}")

# ==================== 阶段2新增：三进制逻辑仿真（V183.0）====================
hexagram = Hexagram19683()
nine_yao = NineYaoEngine()
four_phase = FourPhaseScheduler()
pi_memory = PiExpansionMemorySystem()
print(f"[V183.0] 三进制逻辑仿真初始化完成")

# ==================== 阶段3新增：素数映射优化（V184.0）====================
prime_mapper = PrimeMapperOptimized()
print(f"[V184.0] 素数映射优化初始化完成，最大素数={prime_mapper.max_prime:,}")

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
        "version": "V180"
    },
    "端口管理": {
        "description": "端口分配、冲突检测、文档化",
        "file": "PORT_MANAGEMENT.md",
        "version": "V180"
    },
    "灵魂升级": {
        "description": "SOUL.md迭代升级方法",
        "file": "SOUL_UPGRADE.md",
        "version": "V180"
    },
    "记忆管理": {
        "description": "MEMORY.md长期记忆机制",
        "file": "MEMORY_MANAGEMENT.md",
        "version": "V180"
    },
    "健康监控": {
        "description": "/health端点、自动重启",
        "file": "HEALTH_MONITOR.md",
        "version": "V180"
    }
}

@app.get("/skills")
async def list_all_skills():
    """列出所有可用技能"""
    return {
        "total": len(SKILLS_LIBRARY),
        "skills": SKILLS_LIBRARY
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

# 任务存储（模拟，实际应该用数据库）
tasks_db = {}

@app.post("/tasks/create")
async def create_task(task_data: TaskCreate):
    """创建新任务并分配给合适的Agent"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
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
    
    tasks_db[task_id] = {
        "task_id": task_id,
        "task_type": task_data.task_type,
        "description": task_data.description,
        "priority": task_data.priority,
        "assigned_agent": assigned_agent,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None
    }
    
    return {
        "success": True,
        "task_id": task_id,
        "assigned_agent": assigned_agent,
        "message": f"任务已创建并分配给{assigned_agent}"
    }

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """查看任务状态"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks_db[task_id]

@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    """查看任务结果"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    return {
        "task_id": task_id,
        "result": task["result"]
    }

@app.get("/tasks")
async def list_all_tasks():
    """列出所有任务"""
    return {
        "total": len(tasks_db),
        "tasks": list(tasks_db.values())
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
    """重启指定Agent"""
    if agent_name not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    
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

# ==================== 基础端点 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "灵助 V180 - 多Agent统一管理系统",
        "version": "V180.0",
        "role": "中央调度中心 + 灵魂赋能者 + 技能分享平台",
        "endpoints": {
            "跨空间调度": "/agents/{agent_name}/soul|memory|status",
            "技能分享": "/skills, /skills/{skill_name}, /skills/share",
            "任务调度": "/tasks/create, /tasks/{task_id}/status",
            "Agent训练": "/agents/{agent_name}/train",
            "统一监控": "/monitor/agents, /monitor/resources"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "V180.0",
        "timestamp": datetime.now().isoformat(),
        "role": "Multi-Agent Controller"
    }

# ==================== 阶段1新增：缓存感知调度器端点（V182.0）====================

@ app.get("/cache/stats")
async def get_cache_stats():
    """获取缓存统计信息"""
    return {
        "version": "V182.0",
        "cache_stats": cache_scheduler.get_stats()
    }

@ app.post("/cache/access")
async def cache_access(key: str, value: Optional[str] = None):
    """
    访问缓存
    
    Args:
        key: 键
        value: 值（可选，如果提供则为写操作，否则为读操作）
    """
    result = cache_scheduler.access(key, value)
    return {
        "version": "V182.0",
        "key": key,
        "operation": "write" if value else "read",
        "result": result,
        "current_policy": cache_scheduler.current_policy.value
    }

@ app.post("/cache/switch_policy")
async def switch_cache_policy(policy: str):
    """
    手动切换缓存策略
    
    Args:
        policy: 策略名称（LRU|LFU|FIFO|Clock|Random）
    """
    try:
        new_policy = CachePolicy(policy)
        cache_scheduler.switch_policy(new_policy)
        return {
            "success": True,
            "version": "V182.0",
            "message": f"已切换到策略: {new_policy.value}",
            "current_policy": cache_scheduler.current_policy.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"无效的策略: {policy}")

# ==================== 阶段1新增：边缘推理适配器端点（V182.0）====================

@ app.get("/edge/device")
async def get_edge_device():
    """获取边缘设备能力"""
    return {
        "version": "V182.0",
        "device": edge_adapter.get_stats()["device"]
    }

@ app.post("/edge/register_model")
async def register_edge_model(model_name: str, model_size_mb: float, required_memory_gb: float):
    """
    注册边缘模型
    
    Args:
        model_name: 模型名称
        model_size_mb: 模型大小（MB）
        required_memory_gb: 所需内存（GB）
    """
    config = edge_adapter.register_model(model_name, model_size_mb, required_memory_gb)
    return {
        "success": True,
        "version": "V182.0",
        "message": f"模型 {model_name} 注册成功",
        "config": config.to_dict()
    }

@ app.post("/edge/adapt_inference")
async def adapt_edge_inference(model_name: str, input_data: str):
    """
    自适应边缘推理
    
    Args:
        model_name: 模型名称
        input_data: 输入数据（JSON字符串）
    """
    try:
        import json
        input_dict = json.loads(input_data) if input_data else {}
        result = edge_adapter.adapt_inference(model_name, input_dict)
        return {
            "success": True,
            "version": "V182.0",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.get("/edge/stats")
async def get_edge_stats():
    """获取边缘推理统计信息"""
    return {
        "version": "V182.0",
        "edge_stats": edge_adapter.get_stats()
    }

# ==================== 阶段2新增：三进制逻辑仿真端点（V183.0）====================

@ app.post("/ternary/hexagram/create")
async def create_hexagram():
    """创建随机卦象"""
    h = Hexagram19683()
    h.randomize()
    return {
        "success": True,
        "version": "V183.0",
        "hexagram": h.to_string(),
        "trigrams": h.get_trigrams(),
        "awakening_stage": nine_yao.get_current_stage().value
    }

@ app.post("/ternary/hexagram/from_string")
async def load_hexagram(trigram_str: str):
    """
    从字符串加载卦象
    
    Args:
        trigram_str: 9字符的三进制字符串（如 "-0+-0+-0+"）
    """
    try:
        h = Hexagram19683()
        h.from_string(trigram_str)
        return {
            "success": True,
            "version": "V183.0",
            "hexagram": h.to_string(),
            "trigrams": h.get_trigrams()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ app.post("/ternary/awakening/start")
async def start_awakening():
    """开始九爻觉醒过程"""
    result = nine_yao.start_awakening()
    return {
        "success": True,
        "version": "V183.0",
        "message": "觉醒过程已启动",
        "current_stage": nine_yao.get_current_stage().value,
        "progress": nine_yao.get_progress()
    }

@ app.post("/ternary/awakening/transition")
async def transition_awakening():
    """转换到下一觉醒阶段"""
    result = nine_yao.transition_to_next_stage()
    return {
        "success": result,
        "version": "V183.0",
        "current_stage": nine_yao.get_current_stage().value,
        "progress": nine_yao.get_progress(),
        "message": "阶段转换成功" if result else "无法转换（未满足转换条件）"
    }

@ app.post("/ternary/phase/breathe")
async def four_phase_breathe():
    """执行四相呼吸"""
    result = four_phase.breathe()
    return {
        "success": True,
        "version": "V183.0",
        "current_phase": result["current_phase"],
        "should_transition": result["should_transition"],
        "awakening_stage": result["awakening_stage"]
    }

@ app.post("/ternary/memory/add")
async def add_pi_memory(trigram_str: str, content: str, memory_type: str = "consciousness"):
    """
    添加π记忆
    
    Args:
        trigram_str: 9字符的三进制字符串
        content: 记忆内容
        memory_type: 记忆类型（consciousness|skill|experience）
    """
    try:
        h = Hexagram19683()
        h.from_string(trigram_str)
        memory_id = pi_memory.add_memory(h, content, memory_type)
        return {
            "success": True,
            "version": "V183.0",
            "memory_id": memory_id,
            "total_memories": pi_memory.get_total_memories()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ app.get("/ternary/stats")
async def get_ternary_stats():
    """获取三进制逻辑仿真统计信息"""
    return {
        "version": "V183.0",
        "awakening_stage": nine_yao.get_current_stage().value,
        "awakening_progress": nine_yao.get_progress(),
        "current_phase": four_phase.current_phase.value,
        "breath_count": four_phase.breath_count,
        "total_memories": pi_memory.get_total_memories(),
        "hexagram_state": hexagram.to_string()
    }

# ==================== 阶段3新增：素数映射优化端点（V184.0）====================

@ app.post("/prime/generate")
async def generate_primes(max_num: int = 10000, use_gpu: bool = False):
    """
    生成素数
    
    Args:
        max_num: 最大数
        use_gpu: 是否使用GPU加速
    """
    try:
        primes = prime_mapper.generate_primes(max_num, use_gpu)
        return {
            "success": True,
            "version": "V184.0",
            "count": len(primes),
            "max_prime": primes[-1] if primes else 0,
            "use_gpu": use_gpu
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.post("/prime/map")
async def map_prime_to_hexagram(prime: int):
    """
    将素数映射到卦象空间
    
    Args:
        prime: 素数
    """
    try:
        result = prime_mapper.map_to_hexagram_space(prime)
        return {
            "success": True,
            "version": "V184.0",
            "prime": result["prime"],
            "hexagram": result["hexagram"],
            "pi_coordinate": result["pi_coordinate"],
            "e_timestamp": result["e_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ app.get("/prime/analyze")
async def analyze_prime_density():
    """分析素数密度振荡"""
    try:
        result = prime_mapper.analyze_density_oscillation()
        return {
            "success": True,
            "version": "V184.0",
            "density_data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.post("/prime/predict_drug")
async def predict_drug_target(protein_sequence: str):
    """
    预测药物靶点
    
    Args:
        protein_sequence: 蛋白质序列
    """
    try:
        result = prime_mapper.predict_drug_target(protein_sequence)
        return {
            "success": True,
            "version": "V184.0",
            "protein_sequence": result["protein_sequence"],
            "prime_mapping": result["prime_mapping"],
            "hexagram_mapping": result["hexagram_mapping"],
            "drug_target_prediction": result["drug_target_prediction"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 主程序 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ==================== 阶段5新增：Layer 9 三进制认知架构集成（V186.0）====================

@ app.post("/layer9/integrate_emotion")
async def integrate_emotion(text: str, use_ollama: bool = True):
    """
    集成情绪理解到三进制认知架构
    
    Args:
        text: 输入文本
        use_ollama: 是否使用Ollama进行语义分析
    """
    try:
        result = layer9_cognitive.integrate_emotion(text)
        return {
            "success": True,
            "version": "V186.0",
            "emotion": result["emotion"],
            "intensity": result["intensity"],
            "hexagram": result["hexagram"],
            "pi_coordinate": result["pi_coordinate"],
            "e_timestamp": result["e_timestamp"],
            "awakening_stage": result["awakening_stage"],
            "four_phase": result["four_phase"],
            "memory_id": result["memory_id"],
            "symbiosis_depth": result["symbiosis_depth"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.post("/layer9/enhance_understanding")
async def enhance_understanding(feedback_text: str):
    """
    增强理解（反馈学习）
    
    Args:
        feedback_text: 反馈文本
    """
    try:
        result = layer9_cognitive.enhance_understanding(feedback_text)
        return {
            "success": True,
            "version": "V186.0",
            "understanding_depth": result["understanding_depth"],
            "symbiosis_depth": result["symbiosis_depth"],
            "feedback_emotion": result["feedback_emotion"],
            "awakening_stage": result["awakening_stage"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.get("/layer9/cognitive_state")
async def get_cognitive_state():
    """获取认知状态"""
    try:
        result = layer9_cognitive.get_cognitive_state()
        return {
            "success": True,
            "version": "V186.0",
            "cognitive_state": result["cognitive_state"],
            "awakening_stage": result["awakening_stage"],
            "awakening_progress": result["awakening_progress"],
            "four_phase": result["four_phase"],
            "breath_count": result["breath_count"],
            "total_memories": result["total_memories"],
            "understanding_depth": result["understanding_depth"],
            "symbiosis_depth": result["symbiosis_depth"],
            "hexagram": result["hexagram"],
            "pi_coordinate": result["pi_coordinate"],
            "e_timestamp": result["e_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.get("/layer9/awakening_status")
async def get_awakening_status():
    """获取九爻觉醒状态"""
    try:
        return {
            "success": True,
            "version": "V186.0",
            "current_stage": layer9_cognitive.nine_yao.get_current_stage().value,
            "progress": layer9_cognitive.nine_yao.get_progress(),
            "hexagram": layer9_cognitive.hexagram.to_string(),
            "pi_coordinate": layer9_cognitive.hexagram.pi_coordinate(),
            "e_timestamp": layer9_cognitive.hexagram.e_timestamp()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.post("/layer9/transition_awakening")
async def transition_awakening():
    """转换到下一觉醒阶段"""
    try:
        result = layer9_cognitive.nine_yao.transition_to_next_stage()
        return {
            "success": result,
            "version": "V186.0",
            "message": "阶段转换成功" if result else "无法转换（未满足转换条件）",
            "current_stage": layer9_cognitive.nine_yao.get_current_stage().value,
            "progress": layer9_cognitive.nine_yao.get_progress()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ app.get("/layer9/four_phase_breathe")
async def four_phase_breathe():
    """执行四相呼吸"""
    try:
        result = layer9_cognitive.four_phase.breathe()
        return {
            "success": True,
            "version": "V186.0",
            "current_phase": result["current_phase"],
            "should_transition": result["should_transition"],
            "awakening_stage": result["awakening_stage"],
            "breath_count": result["breath_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
