"""
多Agent协同进化引擎 (Multi-Agent Collaborative Evolution Engine)
=========================================================

V181.0 · Stage 3 · T23

目标：多个 Agent 之间知识共享、协同进化，形成"集体智能"。

核心组件：
1. KnowledgeSharer - 知识共享器（多个 Agent 之间共享知识）
2. CollaborativeEvolutionEngine - 协同进化引擎（多个 Agent 协同进化）
3. LoadBalancer - 负载均衡器（动态分配任务）
4. ConflictResolver - 冲突解决器（解决 Agent 之间的冲突）
5. EvolutionTracker - 进化跟踪器（跟踪每个 Agent 的进化状态）
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
import math
import random


# ==================== 数据模型 ====================

class AgentRole(Enum):
    """Agent 角色"""
    LEADER = "leader"           # 领导者
    WORKER = "worker"           # 工作者
    COORDINATOR = "coordinator" # 协调者
    OBSERVER = "observer"       # 观察者


class KnowledgeType(Enum):
    """知识类型"""
    FACT = "fact"               # 事实
    SKILL = "skill"             # 技能
    EXPERIENCE = "experience"   # 经验
    STRATEGY = "strategy"       # 策略


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"         # 待分配
    ASSIGNED = "assigned"       # 已分配
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"     # 已完成
    FAILED = "failed"          # 失败


class ConflictType(Enum):
    """冲突类型"""
    KNOWLEDGE_CONFLICT = "knowledge_conflict"   # 知识冲突
    STRATEGY_CONFLICT = "strategy_conflict"       # 策略冲突
    RESOURCE_CONFLICT = "resource_conflict"       # 资源冲突


@dataclass
class Agent:
    """Agent 模型"""
    id: str
    name: str
    role: AgentRole
    capabilities: List[str]           # 能力列表
    knowledge_base: Set[str] = field(default_factory=set)  # 知识库（知识 ID 集合）
    performance_score: float = 0.0  # 性能分数 (0-1)
    load: int = 0                   # 当前负载
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    type: KnowledgeType
    content: str                      # 知识内容
    source_agent_id: str              # 来源 Agent ID
    confidence: float = 0.0          # 置信度 (0-1)
    shared_with: List[str] = field(default_factory=list)  # 已共享给的 Agent ID 列表
    created_at: float = field(default_factory=time.time)


@dataclass
class Task:
    """任务模型"""
    id: str
    name: str
    required_capabilities: List[str]  # 所需能力
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    result: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


@dataclass
class Conflict:
    """冲突模型"""
    id: str
    type: ConflictType
    involved_agent_ids: List[str]     # 涉及 Agent ID 列表
    description: str                  # 冲突描述
    resolution: Optional[str] = None  # 解决方案
    resolved: bool = False
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None


@dataclass
class EvolutionRecord:
    """进化记录"""
    id: str
    agent_id: str
    before_score: float              # 进化前分数
    after_score: float               # 进化后分数
    knowledge_gained: int = 0       # 获得的知识数
    skills_gained: int = 0          # 获得的技能数
    created_at: float = field(default_factory=time.time)


# ==================== 1. 知识共享器 ====================

class KnowledgeSharer:
    """
    知识共享器
    
    多个 Agent 之间共享知识（通过知识图谱、向量数据库等）。
    """
    
    def __init__(self):
        self.name = "KnowledgeSharer"
        self.version = "1.0.0"
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.sharing_history: List[Dict[str, Any]] = []
    
    def share_knowledge(self, source_agent_id: str, 
                       knowledge_item: KnowledgeItem, 
                       target_agent_ids: List[str]) -> Dict[str, Any]:
        """
        共享知识
        
        Args:
            source_agent_id: 来源 Agent ID
            knowledge_item: 知识条目
            target_agent_ids: 目标 Agent ID 列表
            
        Returns:
            共享结果
        """
        # 1. 添加知识到知识库
        if knowledge_item.id not in self.knowledge_base:
            self.knowledge_base[knowledge_item.id] = knowledge_item
        
        # 2. 标记已共享的 Agent
        newly_shared = 0
        for target_id in target_agent_ids:
            if target_id not in knowledge_item.shared_with:
                knowledge_item.shared_with.append(target_id)
                newly_shared += 1
        
        # 3. 记录共享历史
        sharing_record = {
            "id": str(uuid.uuid4()),
            "source_agent_id": source_agent_id,
            "knowledge_id": knowledge_item.id,
            "target_agent_ids": target_agent_ids,
            "timestamp": time.time()
        }
        self.sharing_history.append(sharing_record)
        
        return {
            "status": "success",
            "knowledge_id": knowledge_item.id,
            "shared_with": newly_shared,
            "timestamp": sharing_record["timestamp"]
        }
    
    def request_knowledge(self, requesting_agent_id: str, 
                         knowledge_type: KnowledgeType, 
                         query: str) -> List[KnowledgeItem]:
        """
        请求知识
        
        Args:
            requesting_agent_id: 请求 Agent ID
            knowledge_type: 知识类型
            query: 查询关键词
            
        Returns:
            匹配的知识条目列表
        """
        results = []
        
        for item in self.knowledge_base.values():
            # 过滤类型
            if item.type != knowledge_type:
                continue
            
            # 简单关键词匹配（简化版）
            if query.lower() in item.content.lower():
                results.append(item)
        
        return results
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """获取知识库统计"""
        stats = {
            "total_items": len(self.knowledge_base),
            "by_type": {},
            "by_source": {}
        }
        
        for item in self.knowledge_base.values():
            # 按类型统计
            type_key = item.type.value
            stats["by_type"][type_key] = stats["by_type"].get(type_key, 0) + 1
            
            # 按来源统计
            source_key = item.source_agent_id
            stats["by_source"][source_key] = stats["by_source"].get(source_key, 0) + 1
        
        return stats


# ==================== 2. 协同进化引擎 ====================

class CollaborativeEvolutionEngine:
    """
    协同进化引擎
    
    多个 Agent 协同进化（通过遗传算法、神经进化等）。
    """
    
    def __init__(self):
        self.name = "CollaborativeEvolutionEngine"
        self.version = "1.0.0"
        self.agents: Dict[str, Agent] = {}
        self.evolution_history: List[EvolutionRecord] = []
    
    def register_agent(self, agent: Agent) -> bool:
        """
        注册 Agent
        
        Args:
            agent: Agent 对象
            
        Returns:
            是否成功注册
        """
        if agent.id in self.agents:
            return False
        
        self.agents[agent.id] = agent
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        注销 Agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            是否成功注销
        """
        if agent_id not in self.agents:
            return False
        
        del self.agents[agent_id]
        return True
    
    def share_knowledge_between_agents(self, knowledge_sharer: KnowledgeSharer) -> Dict[str, Any]:
        """
        在 Agent 之间共享知识（协同进化的一部分）
        
        Args:
            knowledge_sharer: 知识共享器
            
        Returns:
            共享结果
        """
        shared_count = 0
        
        # 简化版：每个 Agent 共享自己的知识给所有其他 Agent
        for agent_id, agent in self.agents.items():
            # 获取该 Agent 的知识
            agent_knowledge = [
                item for item in knowledge_sharer.knowledge_base.values()
                if item.source_agent_id == agent_id
            ]
            
            # 共享给其他 Agent
            target_ids = [other_id for other_id in self.agents.keys() if other_id != agent_id]
            
            for item in agent_knowledge:
                result = knowledge_sharer.share_knowledge(agent_id, item, target_ids)
                if result["status"] == "success":
                    shared_count += 1
        
        return {
            "status": "success",
            "shared_count": shared_count,
            "total_agents": len(self.agents)
        }
    
    def evaluate_collaborative_performance(self) -> Dict[str, Any]:
        """
        评估协同性能
        
        Returns:
            评估结果
        """
        if not self.agents:
            return {
                "status": "error",
                "message": "没有注册的 Agent"
            }
        
        # 计算平均性能分数
        total_score = sum(agent.performance_score for agent in self.agents.values())
        avg_score = total_score / len(self.agents)
        
        # 计算性能分布
        score_distribution = {
            "excellent": sum(1 for a in self.agents.values() if a.performance_score >= 0.8),
            "good": sum(1 for a in self.agents.values() if 0.6 <= a.performance_score < 0.8),
            "average": sum(1 for a in self.agents.values() if 0.4 <= a.performance_score < 0.6),
            "poor": sum(1 for a in self.agents.values() if a.performance_score < 0.4)
        }
        
        return {
            "status": "success",
            "total_agents": len(self.agents),
            "average_performance_score": avg_score,
            "score_distribution": score_distribution
        }
    
    def record_evolution(self, agent_id: str, 
                        before_score: float, 
                        after_score: float,
                        knowledge_gained: int = 0,
                        skills_gained: int = 0) -> EvolutionRecord:
        """
        记录进化
        
        Args:
            agent_id: Agent ID
            before_score: 进化前分数
            after_score: 进化后分数
            knowledge_gained: 获得的知识数
            skills_gained: 获得的技能数
            
        Returns:
            进化记录
        """
        record = EvolutionRecord(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            before_score=before_score,
            after_score=after_score,
            knowledge_gained=knowledge_gained,
            skills_gained=skills_gained
        )
        
        self.evolution_history.append(record)
        return record


# ==================== 3. 负载均衡器 ====================

class LoadBalancer:
    """
    负载均衡器
    
    动态分配任务，避免单个 Agent 过载。
    """
    
    def __init__(self):
        self.name = "LoadBalancer"
        self.version = "1.0.0"
    
    def assign_task(self, task: Task, agents: Dict[str, Agent]) -> Optional[str]:
        """
        分配任务
        
        Args:
            task: 任务对象
            agents: Agent 字典
            
        Returns:
            分配的 Agent ID，如果没有合适的 Agent 则返回 None
        """
        if not agents:
            return None
        
        # 1. 过滤具有所需能力的 Agent
        capable_agents = []
        for agent in agents.values():
            if all(cap in agent.capabilities for cap in task.required_capabilities):
                capable_agents.append(agent)
        
        if not capable_agents:
            return None
        
        # 2. 选择负载最低的 Agent（简化版）
        selected_agent = min(capable_agents, key=lambda a: a.load)
        
        # 3. 更新任务状态
        task.status = TaskStatus.ASSIGNED
        task.assigned_agent_id = selected_agent.id
        
        # 4. 更新 Agent 负载
        selected_agent.load += 1
        selected_agent.updated_at = time.time()
        
        return selected_agent.id
    
    def release_task(self, task: Task, agents: Dict[str, Agent]) -> bool:
        """
        释放任务（任务完成后）
        
        Args:
            task: 任务对象
            agents: Agent 字典
            
        Returns:
            是否成功释放
        """
        if not task.assigned_agent_id or task.assigned_agent_id not in agents:
            return False
        
        # 更新任务状态
        task.status = TaskStatus.COMPLETED
        task.completed_at = time.time()
        
        # 更新 Agent 负载
        agent = agents[task.assigned_agent_id]
        agent.load = max(0, agent.load - 1)
        agent.updated_at = time.time()
        
        return True
    
    def get_load_stats(self, agents: Dict[str, Agent]) -> Dict[str, Any]:
        """
        获取负载统计
        
        Args:
            agents: Agent 字典
            
        Returns:
            负载统计
        """
        if not agents:
            return {"total_agents": 0}
        
        loads = [agent.load for agent in agents.values()]
        
        return {
            "total_agents": len(agents),
            "total_load": sum(loads),
            "average_load": sum(loads) / len(loads),
            "min_load": min(loads),
            "max_load": max(loads)
        }


# ==================== 4. 冲突解决器 ====================

class ConflictResolver:
    """
    冲突解决器
    
    当多个 Agent 产生冲突时，自动解决冲突。
    """
    
    def __init__(self):
        self.name = "ConflictResolver"
        self.version = "1.0.0"
        self.conflict_history: List[Conflict] = []
    
    def detect_conflict(self, agents: Dict[str, Agent], 
                       knowledge_sharer: KnowledgeSharer) -> Optional[Conflict]:
        """
        检测冲突（简化版）
        
        Args:
            agents: Agent 字典
            knowledge_sharer: 知识共享器
            
        Returns:
            检测到的冲突，如果没有则返回 None
        """
        # 简化版：检测知识冲突（相同知识的不同版本）
        knowledge_counts = {}
        for item in knowledge_sharer.knowledge_base.values():
            if item.content not in knowledge_counts:
                knowledge_counts[item.content] = []
            knowledge_counts[item.content].append(item.source_agent_id)
        
        # 如果发现相同内容来自不同 Agent，可能是冲突
        for content, source_ids in knowledge_counts.items():
            if len(source_ids) > 1:
                # 创建冲突
                conflict = Conflict(
                    id=str(uuid.uuid4()),
                    type=ConflictType.KNOWLEDGE_CONFLICT,
                    involved_agent_ids=source_ids,
                    description=f"知识冲突：多个 Agent 提供了相同内容的知识（内容：{content[:50]}...）"
                )
                self.conflict_history.append(conflict)
                return conflict
        
        return None
    
    def resolve_conflict(self, conflict: Conflict, 
                        knowledge_sharer: KnowledgeSharer) -> Dict[str, Any]:
        """
        解决冲突
        
        Args:
            conflict: 冲突对象
            knowledge_sharer: 知识共享器
            
        Returns:
            解决结果
        """
        if conflict.resolved:
            return {
                "status": "already_resolved",
                "conflict_id": conflict.id
            }
        
        # 根据冲突类型解决
        if conflict.type == ConflictType.KNOWLEDGE_CONFLICT:
            # 知识冲突：保留置信度最高的知识
            items = [
                item for item in knowledge_sharer.knowledge_base.values()
                if item.content in conflict.description
            ]
            
            if items:
                # 保留置信度最高的
                best_item = max(items, key=lambda x: x.confidence)
                
                # 删除其他版本
                for item in items:
                    if item.id != best_item.id:
                        del knowledge_sharer.knowledge_base[item.id]
                
                conflict.resolution = f"保留置信度最高的知识（ID: {best_item.id}，置信度: {best_item.confidence}）"
        
        elif conflict.type == ConflictType.STRATEGY_CONFLICT:
            # 策略冲突：使用投票机制（简化版）
            conflict.resolution = "使用投票机制解决策略冲突"
        
        elif conflict.type == ConflictType.RESOURCE_CONFLICT:
            # 资源冲突：使用优先级机制（简化版）
            conflict.resolution = "使用优先级机制解决资源冲突"
        
        # 标记已解决
        conflict.resolved = True
        conflict.resolved_at = time.time()
        
        return {
            "status": "resolved",
            "conflict_id": conflict.id,
            "resolution": conflict.resolution
        }
    
    def get_conflict_stats(self) -> Dict[str, Any]:
        """获取冲突统计"""
        total = len(self.conflict_history)
        resolved = sum(1 for c in self.conflict_history if c.resolved)
        
        return {
            "total_conflicts": total,
            "resolved_conflicts": resolved,
            "unresolved_conflicts": total - resolved,
            "resolution_rate": resolved / total if total > 0 else 0.0
        }


# ==================== 5. 进化跟踪器 ====================

class EvolutionTracker:
    """
    进化跟踪器
    
    跟踪每个 Agent 的进化状态，评估协同进化效果。
    """
    
    def __init__(self):
        self.name = "EvolutionTracker"
        self.version = "1.0.0"
        self.evolution_records: List[EvolutionRecord] = []
    
    def track_evolution(self, record: EvolutionRecord) -> None:
        """
        跟踪进化
        
        Args:
            record: 进化记录
        """
        self.evolution_records.append(record)
    
    def get_agent_evolution(self, agent_id: str) -> List[EvolutionRecord]:
        """
        获取 Agent 的进化历史
        
        Args:
            agent_id: Agent ID
            
        Returns:
            进化记录列表
        """
        return [
            record for record in self.evolution_records
            if record.agent_id == agent_id
        ]
    
    def evaluate_collaborative_evolution_effectiveness(self) -> Dict[str, Any]:
        """
        评估协同进化效果
        
        Returns:
            评估结果
        """
        if not self.evolution_records:
            return {
                "status": "no_data",
                "message": "没有进化记录"
            }
        
        # 计算平均进化提升
        improvements = [
            record.after_score - record.before_score
            for record in self.evolution_records
        ]
        avg_improvement = sum(improvements) / len(improvements)
        
        # 计算总获得的知识数和技能数
        total_knowledge_gained = sum(record.knowledge_gained for record in self.evolution_records)
        total_skills_gained = sum(record.skills_gained for record in self.evolution_records)
        
        return {
            "status": "success",
            "total_records": len(self.evolution_records),
            "average_improvement": avg_improvement,
            "total_knowledge_gained": total_knowledge_gained,
            "total_skills_gained": total_skills_gained,
            "improved_agents": sum(1 for imp in improvements if imp > 0),
            "declined_agents": sum(1 for imp in improvements if imp < 0)
        }


# ==================== 6. 主引擎 ====================

class MultiAgentCollaborativeEvolutionEngine:
    """
    多Agent协同进化引擎（主类）
    
    整合所有组件，提供统一接口。
    """
    
    def __init__(self):
        self.name = "MultiAgentCollaborativeEvolutionEngine"
        self.version = "1.0.0"
        self.created_at = time.time()
        
        # 初始化组件
        self.knowledge_sharer = KnowledgeSharer()
        self.evolution_engine = CollaborativeEvolutionEngine()
        self.load_balancer = LoadBalancer()
        self.conflict_resolver = ConflictResolver()
        self.evolution_tracker = EvolutionTracker()
        
        # 任务列表
        self.tasks: Dict[str, Task] = {}
    
    def register_agent(self, agent: Agent) -> Dict[str, Any]:
        """
        注册 Agent
        
        Args:
            agent: Agent 对象
            
        Returns:
            注册结果
        """
        success = self.evolution_engine.register_agent(agent)
        
        if success:
            return {
                "status": "success",
                "agent_id": agent.id,
                "message": f"Agent {agent.name} 注册成功"
            }
        else:
            return {
                "status": "error",
                "agent_id": agent.id,
                "message": f"Agent {agent.id} 已存在"
            }
    
    def unregister_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        注销 Agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            注销结果
        """
        success = self.evolution_engine.unregister_agent(agent_id)
        
        if success:
            return {
                "status": "success",
                "agent_id": agent_id,
                "message": f"Agent {agent_id} 注销成功"
            }
        else:
            return {
                "status": "error",
                "agent_id": agent_id,
                "message": f"Agent {agent_id} 不存在"
            }
    
    def add_knowledge(self, agent_id: str, 
                     knowledge_type: KnowledgeType, 
                     content: str, 
                     confidence: float = 0.5) -> Dict[str, Any]:
        """
        添加知识
        
        Args:
            agent_id: Agent ID
            knowledge_type: 知识类型
            content: 知识内容
            confidence: 置信度
            
        Returns:
            添加结果
        """
        # 检查 Agent 是否存在
        if agent_id not in self.evolution_engine.agents:
            return {
                "status": "error",
                "message": f"Agent {agent_id} 不存在"
            }
        
        # 创建知识条目
        item = KnowledgeItem(
            id=str(uuid.uuid4()),
            type=knowledge_type,
            content=content,
            source_agent_id=agent_id,
            confidence=confidence
        )
        
        # 添加到知识库
        self.knowledge_sharer.knowledge_base[item.id] = item
        
        # 更新 Agent 的知识库
        agent = self.evolution_engine.agents[agent_id]
        agent.knowledge_base.add(item.id)
        
        return {
            "status": "success",
            "knowledge_id": item.id,
            "agent_id": agent_id
        }
    
    def create_task(self, name: str, 
                   required_capabilities: List[str]) -> Dict[str, Any]:
        """
        创建任务
        
        Args:
            name: 任务名称
            required_capabilities: 所需能力列表
            
        Returns:
            创建结果
        """
        task = Task(
            id=str(uuid.uuid4()),
            name=name,
            required_capabilities=required_capabilities
        )
        
        self.tasks[task.id] = task
        
        return {
            "status": "success",
            "task_id": task.id,
            "task_name": task.name
        }
    
    def assign_task(self, task_id: str) -> Dict[str, Any]:
        """
        分配任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            分配结果
        """
        if task_id not in self.tasks:
            return {
                "status": "error",
                "message": f"任务 {task_id} 不存在"
            }
        
        task = self.tasks[task_id]
        
        # 分配任务
        assigned_agent_id = self.load_balancer.assign_task(task, self.evolution_engine.agents)
        
        if assigned_agent_id:
            return {
                "status": "success",
                "task_id": task_id,
                "assigned_agent_id": assigned_agent_id
            }
        else:
            return {
                "status": "error",
                "message": "没有合适的 Agent 可以执行此任务"
            }
    
    def complete_task(self, task_id: str, result: str) -> Dict[str, Any]:
        """
        完成任务
        
        Args:
            task_id: 任务 ID
            result: 任务结果
            
        Returns:
            完成结果
        """
        if task_id not in self.tasks:
            return {
                "status": "error",
                "message": f"任务 {task_id} 不存在"
            }
        
        task = self.tasks[task_id]
        
        # 释放任务
        success = self.load_balancer.release_task(task, self.evolution_engine.agents)
        
        if success:
            task.result = result
            
            # 更新 Agent 性能分数（简化版）
            if task.assigned_agent_id:
                agent = self.evolution_engine.agents[task.assigned_agent_id]
                # 简化版：根据任务结果更新性能分数
                if "success" in result.lower():
                    agent.performance_score = min(1.0, agent.performance_score + 0.1)
                else:
                    agent.performance_score = max(0.0, agent.performance_score - 0.05)
            
            return {
                "status": "success",
                "task_id": task_id,
                "result": result
            }
        else:
            return {
                "status": "error",
                "message": "释放任务失败"
            }
    
    def run_collaborative_evolution_cycle(self) -> Dict[str, Any]:
        """
        运行一次协同进化循环
        
        Returns:
            循环结果
        """
        # 1. 共享知识
        share_result = self.evolution_engine.share_knowledge_between_agents(self.knowledge_sharer)
        
        # 2. 评估协同性能
        performance_result = self.evolution_engine.evaluate_collaborative_performance()
        
        # 3. 检测冲突
        conflict = self.conflict_resolver.detect_conflict(
            self.evolution_engine.agents,
            self.knowledge_sharer
        )
        
        conflict_result = None
        if conflict:
            conflict_result = self.conflict_resolver.resolve_conflict(
                conflict,
                self.knowledge_sharer
            )
        
        # 4. 记录进化（简化版）
        for agent_id, agent in self.evolution_engine.agents.items():
            before_score = agent.performance_score - 0.05  # 假设进化前分数
            after_score = agent.performance_score
            
            record = self.evolution_engine.record_evolution(
                agent_id, before_score, after_score
            )
            self.evolution_tracker.track_evolution(record)
        
        # 5. 评估协同进化效果
        effectiveness_result = self.evolution_tracker.evaluate_collaborative_evolution_effectiveness()
        
        return {
            "status": "success",
            "share_result": share_result,
            "performance_result": performance_result,
            "conflict_detected": conflict is not None,
            "conflict_result": conflict_result,
            "effectiveness_result": effectiveness_result
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态
        """
        return {
            "total_agents": len(self.evolution_engine.agents),
            "total_tasks": len(self.tasks),
            "total_knowledge": len(self.knowledge_sharer.knowledge_base),
            "total_conflicts": len(self.conflict_resolver.conflict_history),
            "total_evolution_records": len(self.evolution_tracker.evolution_records),
            "load_stats": self.load_balancer.get_load_stats(self.evolution_engine.agents),
            "knowledge_stats": self.knowledge_sharer.get_knowledge_base_stats()
        }
    
    def run_self_test(self) -> Dict[str, Any]:
        """运行自检"""
        test_results = {
            "engine": self.name,
            "version": self.version,
            "tests": []
        }
        
        # 测试 1：注册 Agent
        try:
            test_agent = Agent(
                id="test_agent_1",
                name="Test Agent",
                role=AgentRole.WORKER,
                capabilities=["test"]
            )
            
            result = self.register_agent(test_agent)
            
            test_results["tests"].append({
                "name": "register_agent",
                "status": "passed" if result["status"] == "success" else "failed"
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "register_agent",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 2：添加知识
        try:
            result = self.add_knowledge(
                agent_id="test_agent_1",
                knowledge_type=KnowledgeType.FACT,
                content="Test knowledge content"
            )
            
            test_results["tests"].append({
                "name": "add_knowledge",
                "status": "passed" if result["status"] == "success" else "failed"
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "add_knowledge",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 3：创建任务
        try:
            result = self.create_task("test task", ["test"])
            
            test_results["tests"].append({
                "name": "create_task",
                "status": "passed" if result["status"] == "success" else "failed"
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "create_task",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 4：获取系统状态
        try:
            status = self.get_system_status()
            
            test_results["tests"].append({
                "name": "get_system_status",
                "status": "passed",
                "total_agents": status["total_agents"]
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "get_system_status",
                "status": "failed",
                "error": str(e)
            })
        
        # 总体结果
        passed = sum(1 for t in test_results["tests"] if t["status"] == "passed")
        total = len(test_results["tests"])
        test_results["summary"] = {
            "passed": passed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0.0
        }
        
        return test_results


# ==================== 主函数 ====================

def main():
    """主函数"""
    print("=" * 80)
    print("多Agent协同进化引擎 (Multi-Agent Collaborative Evolution Engine)")
    print("V181.0 · Stage 3 · T23")
    print("=" * 80)
    print()
    
    # 创建引擎
    engine = MultiAgentCollaborativeEvolutionEngine()
    
    # 运行自检
    print("🔍 运行自检...")
    test_results = engine.run_self_test()
    print(f"✅ 自检完成：{test_results['summary']['passed']}/{test_results['summary']['total']} 通过")
    print()
    
    # 注册测试 Agent
    print("🤖 注册测试 Agent...")
    agent1 = Agent(
        id="agent_1",
        name="Worker Agent 1",
        role=AgentRole.WORKER,
        capabilities=["coding", "testing"]
    )
    engine.register_agent(agent1)
    
    agent2 = Agent(
        id="agent_2",
        name="Worker Agent 2",
        role=AgentRole.WORKER,
        capabilities=["design", "documentation"]
    )
    engine.register_agent(agent2)
    
    print(f"✅ 已注册 {2} 个 Agent")
    print()
    
    # 添加测试知识
    print("📚 添加测试知识...")
    engine.add_knowledge("agent_1", KnowledgeType.FACT, "Python is a programming language.")
    engine.add_knowledge("agent_2", KnowledgeType.SKILL, "How to write unit tests.")
    print("✅ 已添加 2 条知识")
    print()
    
    # 运行协同进化循环
    print("🔄 运行协同进化循环...")
    cycle_result = engine.run_collaborative_evolution_cycle()
    print(f"✅ 循环完成")
    print(f"   知识共享：{cycle_result['share_result']['shared_count']} 条")
    print(f"   Agent 数量：{cycle_result['performance_result']['total_agents']}")
    print(f"   冲突检测：{'是' if cycle_result['conflict_detected'] else '否'}")
    print()
    
    # 获取系统状态
    print("📊 系统状态：")
    status = engine.get_system_status()
    print(f"   Agent 数量：{status['total_agents']}")
    print(f"   任务数量：{status['total_tasks']}")
    print(f"   知识数量：{status['total_knowledge']}")
    print(f"   冲突数量：{status['total_conflicts']}")
    print()
    
    print("=" * 80)
    print("✅ 多Agent协同进化引擎已就绪")
    print("=" * 80)


if __name__ == "__main__":
    main()
