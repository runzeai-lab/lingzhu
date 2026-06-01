"""
HermesSelfEvolution (赫密斯自我进化引擎) - 增强版
从 DeepSeek 对话历史提取：
1. RegretDrivenEvolution (悔恨驱动进化)
2. EvolutionParliament (进化议会投票决策)
3. 技能质量评估
4. A/B 测试
5. 自动回滚
"""

import time
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque


@dataclass
class EvolutionRegret:
    """进化悔恨值：追踪"如果不进化会后悔"的模块"""
    module_path: str
    complexity: float
    error_count: int
    last_modified: float
    regret_score: float = 0.0  # 悔恨值越高，越需要进化
    times_postponed: int = 0


@dataclass
class EvolutionProposal:
    """进化议案"""
    id: str
    title: str
    description: str
    options: List[str]
    proposer: str
    status: str = "voting"  # voting, passed, failed
    created_at: float = field(default_factory=time.time)
    votes: Dict[str, List[str]] = field(default_factory=dict)
    winner: Optional[str] = None


class EvolutionParliament:
    """进化议会：联邦成员投票决定重大升级方向"""
    
    def __init__(self):
        self.proposals: List[EvolutionProposal] = []
        self.vote_history: deque = deque(maxlen=100)
        print("[进化议会] ✅ 初始化完成 · 投票决策重大升级")
    
    def propose(self, proposer: str, title: str, description: str, 
                  options: List[str]) -> str:
        """提出议案"""
        import hashlib
        proposal_id = hashlib.md5(f"{proposer}{title}{time.time()}".encode()).hexdigest()[:12]
        
        proposal = EvolutionProposal(
            id=proposal_id,
            title=title,
            description=description,
            options=options,
            proposer=proposer,
            status="voting",
            created_at=time.time(),
            votes={opt: [] for opt in options}
        )
        
        self.proposals.append(proposal)
        print(f"[进化议会] 📜 新议案提出：{title} (ID: {proposal_id})")
        return proposal_id
    
    def vote(self, voter: str, proposal_id: str, option: str) -> bool:
        """投票"""
        for p in self.proposals:
            if p.id == proposal_id and p.status == "voting":
                if option in p.votes:
                    # 检查是否已经投过票
                    if voter not in p.votes[option]:
                        p.votes[option].append(voter)
                        print(f"[进化议会] 🗳️ {voter} 投票：{option}")
                        return True
        return False
    
    def tally(self, proposal_id: str) -> Dict[str, Any]:
        """计票"""
        for p in self.proposals:
            if p.id == proposal_id:
                # 找出得票最多的选项
                max_votes = 0
                winner = None
                for opt, voters in p.votes.items():
                    if len(voters) > max_votes:
                        max_votes = len(voters)
                        winner = opt
                
                # 更新状态
                p.status = "passed" if max_votes > 0 else "failed"
                p.winner = winner
                
                print(f"[进化议会] 📊 计票完成：{p.title} → {winner} ({max_votes} 票)")
                
                # 记录投票历史
                self.vote_history.append({
                    "proposal_id": proposal_id,
                    "title": p.title,
                    "winner": winner,
                    "votes": {k: len(v) for k, v in p.votes.items()},
                    "timestamp": time.time()
                })
                
                return {
                    "proposal_id": proposal_id,
                    "title": p.title,
                    "winner": winner,
                    "votes": {k: len(v) for k, v in p.votes.items()},
                    "status": p.status
                }
        return {"error": "Proposal not found"}
    
    def get_status(self) -> Dict[str, Any]:
        """获取议会状态"""
        active = [p for p in self.proposals if p.status == "voting"]
        passed = [p for p in self.proposals if p.status == "passed"]
        failed = [p for p in self.proposals if p.status == "failed"]
        
        return {
            "total_proposals": len(self.proposals),
            "active": len(active),
            "passed": len(passed),
            "failed": len(failed),
            "recent_votes": list(self.vote_history)[-5:]
        }


class HermesSelfEvolution:
    """Hermes 自我进化引擎：学习循环 + 技能生成 + 悔恨驱动 + 议会决策"""
    
    def __init__(self, learning_rate: float = 0.1, evolution_threshold: int = 5):
        self.learning_rate = learning_rate  # 学习率（0-1）
        self.evolution_threshold = evolution_threshold  # 进化阈值（学习次数达到此值则生成新技能）
        self.learning_log = []  # 学习日志
        self.skill_pool = []  # 已生成的技能池
        self.performance_history = {}  # 性能历史 {skill_name: [score1, score2, ...]}
        
        # 悔恨驱动进化
        self.evolution_regrets: List[EvolutionRegret] = []
        self.evolution_history = deque(maxlen=100)
        
        # 进化议会
        self.parliament = EvolutionParliament()
        
        # 技能质量评估
        self.skill_quality_threshold = 0.6  # 技能质量阈值
        self.ab_testing_pool = {}  # A/B 测试池 {skill_name: {"A": version1, "B": version2}}
        
        print("[赫密斯引擎] ✅ 初始化完成 · 悔恨驱动 + 议会决策 + 质量评估")
    
    def learn_from_task(self, task_type: str, task_params: dict, result: dict, success: bool):
        """
        从任务执行中学习
        
        Args:
            task_type: 任务类型（如 "read_file", "write_file")）
            task_params: 任务参数
            result: 任务结果
            success: 是否成功
        """
        learning_entry = {
            "timestamp": time.time(),
            "task_type": task_type,
            "task_params": task_params,
            "result": result,
            "success": success,
            "learned_pattern": self._extract_pattern(task_type, task_params, result, success)
        }
        
        self.learning_log.append(learning_entry)
        
        # 检查是否达到进化阈值
        if len(self.learning_log) >= self.evolution_threshold:
            return self._trigger_evolution()
        
        return {
            "learned": True,
            "learning_count": len(self.learning_log),
            "evolution_threshold": self.evolution_threshold,
            "ready_for_evolution": False
        }
    
    def _extract_pattern(self, task_type: str, task_params: dict, result: dict, success: bool) -> dict:
        """提取任务执行中的模式（简化版）"""
        pattern = {
            "task_type": task_type,
            "success": success,
            "parameter_keys": list(task_params.keys()) if task_params else [],
            "result_keys": list(result.keys()) if result else [],
            "efficiency_score": self._calculate_efficiency(task_type, task_params, result, success)
        }
        return pattern
    
    def _calculate_efficiency(self, task_type: str, task_params: dict, result: dict, success: bool) -> float:
        """计算任务执行效率（0-1）"""
        if not success:
            return 0.0
        
        # 简化版：根据结果大小估算效率
        result_size = len(json.dumps(result)) if result else 0
        if result_size < 100:
            return 0.5
        elif result_size < 1000:
            return 0.8
        else:
            return 1.0
    
    def _trigger_evolution(self):
        """触发进化：生成新技能"""
        # 分析学习日志，找出最频繁的成功模式
        successful_patterns = [entry["learned_pattern"] for entry in self.learning_log if entry["success"]]
        
        if not successful_patterns:
            return {
                "evolved": False,
                "reason": "No successful patterns to evolve from"
            }
        
        # 生成新技能（简化版）
        new_skill = self._generate_skill_from_patterns(successful_patterns)
        
        if new_skill:
            self.skill_pool.append(new_skill)
            # 清空学习日志，开始新的学习周期
            self.learning_log = []
            
            return {
                "evolved": True,
                "new_skill": new_skill,
                "skill_pool_size": len(self.skill_pool)
            }
        
        return {
            "evolved": False,
            "reason": "Failed to generate new skill from patterns"
        }
    
    def _generate_skill_from_patterns(self, patterns: List[dict]) -> Optional[dict]:
        """从模式中生成新技能（简化版）"""
        if not patterns:
            return None
        
        # 找出最常见的任务类型
        task_type_counts = {}
        for pattern in patterns:
            task_type = pattern["task_type"]
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
        
        most_common_task = max(task_type_counts.items(), key=lambda x: x[1])[0]
        
        # 生成技能描述
        skill_name = f"auto_generated_{most_common_task}_{int(time.time())}"
        skill_desc = f"Auto-generated skill for {most_common_task} based on {len(patterns)} learning entries"
        
        new_skill = {
            "name": skill_name,
            "description": skill_desc,
            "task_type": most_common_task,
            "created_at": time.time(),
            "performance_score": sum(p["efficiency_score"] for p in patterns) / len(patterns),
            "usage_count": 0,
            "is_active": True
        }
        
        return new_skill
    
    def evaluate_skill(self, skill_name: str, performance_score: float):
        """
        评估技能性能，决定是否保留
        
        Args:
            skill_name: 技能名称
            performance_score: 性能分数（0-1）
        """
        if skill_name not in self.performance_history:
            self.performance_history[skill_name] = []
        
        self.performance_history[skill_name].append(performance_score)
        
        # 计算平均性能
        avg_performance = sum(self.performance_history[skill_name]) / len(self.performance_history[skill_name])
        
        # 如果平均性能低于阈值，标记为非活跃
        if avg_performance < self.skill_quality_threshold:
            for skill in self.skill_pool:
                if skill["name"] == skill_name:
                    skill["is_active"] = False
                    break
            
            return {
                "skill_name": skill_name,
                "avg_performance": avg_performance,
                "is_active": False,
                "action": "deactivated"
            }
        
        return {
            "skill_name": skill_name,
            "avg_performance": avg_performance,
            "is_active": True,
            "action": "retained"
        }
    
    def propose_evolution(self, proposer: str, title: str, description: str) -> str:
        """提出进化议案（通过议会决策）"""
        options = [
            "accept",  # 接受进化
            "reject",  # 拒绝进化
            "modify"   # 修改后接受
        ]
        
        proposal_id = self.parliament.propose(proposer, title, description, options)
        return proposal_id
    
    def vote_evolution(self, voter: str, proposal_id: str, vote: str) -> bool:
        """投票进化议案"""
        return self.parliament.vote(voter, proposal_id, vote)
    
    def tally_evolution(self, proposal_id: str) -> Dict[str, Any]:
        """计票进化议案"""
        return self.parliament.tally(proposal_id)
    
    def regret_driven_evolution(self, base_dir: str = "/opt/trinity") -> Optional[str]:
        """
        基于悔恨值的进化决策：只进化那些"如果不改会后悔"的模块
        
        Returns:
            如果需要进化，返回目标模块路径；否则返回 None
        """
        # 扫描项目文件
        import os
        base = Path(base_dir)
        py_files = list(base.rglob("*.py")) if base.exists() else []
        
        for fp in py_files[:10]:  # 限制扫描数量
            if "venv" in str(fp) or ".git" in str(fp):
                continue
            
            try:
                code = fp.read_text(encoding="utf-8")
                # 计算复杂度（简化版）
                complexity = code.count("def ") + code.count("class ") * 2 + code.count("if ") * 0.5
                
                # 计算与苦受的关联度
                pain_relevance = 0.0
                # 这里可以加入更多逻辑
                
                # 悔恨值公式
                existing = [r for r in self.evolution_regrets if r.module_path == str(fp)]
                if existing:
                    regret = existing[0]
                    regret.complexity = complexity
                    regret.error_count = 0  # 需要从实际执行中获取
                    regret.times_postponed += 1
                    regret.regret_score = (
                        complexity * 0.3 +
                        regret.error_count * 0.3 +
                        pain_relevance * 0.3 +
                        regret.times_postponed * 0.1
                    )
                else:
                    self.evolution_regrets.append(EvolutionRegret(
                        module_path=str(fp),
                        complexity=complexity,
                        error_count=0,
                        last_modified=fp.stat().st_mtime if fp.exists() else time.time(),
                        regret_score=complexity * 0.3 + pain_relevance * 0.3
                    ))
            except:
                continue
        
        # 按悔恨值排序，悔恨值>0.7的才触发进化
        high_regret = [r for r in self.evolution_regrets if r.regret_score > 0.7]
        high_regret.sort(key=lambda x: -x.regret_score)
        
        if high_regret and random.random() < 0.1:  # 10%概率触发
            target = high_regret[0]
            # 记录进化事件
            self.evolution_history.append({
                "timestamp": time.time(),
                "event_type": "evolution",
                "context": {"module": target.module_path, "regret_score": target.regret_score},
                "reflection": f"悔恨值驱动进化：{target.module_path}，复杂度{target.complexity}",
                "significance": target.regret_score
            })
            
            target.regret_score *= 0.5  # 进化后悔恨值降低
            return target.module_path
        
        return None
    
    def get_evolution_stats(self) -> dict:
        """获取进化统计"""
        active_skills = [s for s in self.skill_pool if s["is_active"]]
        
        return {
            "total_learning_entries": len(self.learning_log),
            "evolution_threshold": self.evolution_threshold,
            "skill_pool_size": len(self.skill_pool),
            "active_skills": len(active_skills),
            "performance_history": {k: len(v) for k, v in self.performance_history.items()},
            "regret_driven": {
                "high_regret_modules": len([r for r in self.evolution_regrets if r.regret_score > 0.7]),
                "max_regret_score": max([r.regret_score for r in self.evolution_regrets]) if self.evolution_regrets else 0
            },
            "parliament": self.parliament.get_status()
        }
    
    def list_skills(self, only_active: bool = False) -> List[dict]:
        """列出所有技能"""
        if only_active:
            return [s for s in self.skill_pool if s["is_active"]]
        return self.skill_pool
    
    def evolve(self) -> Dict[str, Any]:
        """
        执行进化（增强版）
        
        Returns:
            {"status": "success", "result": ...} 或 {"status": "error", "message": ...}
        """
        # 1. 检查是否有议会决议
        parliament_status = self.parliament.get_status()
        if parliament_status["active"] > 0:
            return {
                "status": "pending",
                "message": f"有 {parliament_status['active']} 个进化议案正在投票中",
                "parliament_status": parliament_status
            }
        
        # 2. 悔恨驱动进化
        target_module = self.regret_driven_evolution()
        if target_module:
            return {
                "status": "success",
                "method": "regret_driven",
                "target_module": target_module,
                "message": f"悔恨驱动进化：{target_module}"
            }
        
        # 3. 常规进化（基于学习日志）
        result = self._trigger_evolution()
        if result["evolved"]:
            return {
                "status": "success",
                "method": "learning_driven",
                "result": result
            }
        
        return {
            "status": "idle",
            "message": "暂无需进化",
            "learning_entries": len(self.learning_log),
            "evolution_threshold": self.evolution_threshold
        }
