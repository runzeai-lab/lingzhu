"""
Hermes 自进化学习循环
从任务执行中学习，生成新技能，实现自我进化
"""

import json
import time
import os
from typing import Dict, List, Optional
from datetime import datetime


class HermesSelfEvolution:
    """Hermes 自进化引擎：学习循环 + 技能生成"""
    
    def __init__(self, learning_rate: float = 0.1, evolution_threshold: int = 5):
        self.learning_rate = learning_rate  # 学习率（0-1）
        self.evolution_threshold = evolution_threshold  # 进化阈值（学习次数达到此值则生成新技能）
        self.learning_log = []  # 学习日志
        self.skill_pool = []  # 已生成的技能池
        self.performance_history = {}  # 性能历史 {skill_name: [score1, score2, ...]}
        
    def learn_from_task(self, task_type: str, task_params: dict, result: dict, success: bool):
        """
        从任务执行中学习
        
        Args:
            task_type: 任务类型（如 "read_file", "write_file"）
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
            "created_at": datetime.now().isoformat(),
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
        if avg_performance < 0.3:  # 阈值：0.3
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
    
    def get_evolution_stats(self) -> dict:
        """获取进化统计"""
        active_skills = [s for s in self.skill_pool if s["is_active"]]
        
        return {
            "total_learning_entries": len(self.learning_log),
            "evolution_threshold": self.evolution_threshold,
            "skill_pool_size": len(self.skill_pool),
            "active_skills": len(active_skills),
            "performance_history": {k: len(v) for k, v in self.performance_history.items()}
        }
    
    def list_skills(self, only_active: bool = False) -> List[dict]:
        """列出所有技能"""
        if only_active:
            return [s for s in self.skill_pool if s["is_active"]]
        return self.skill_pool
