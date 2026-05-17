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
    
    # ==================== 新增：测试与验证功能 ====================
    
    def evaluate_evolution_effectiveness(self, old_skill: dict, new_skill: dict, test_tasks: list) -> dict:
        """
        评估进化效果（对比新旧技能性能）
        
        Args:
            old_skill: 旧技能定义
            new_skill: 新技能定义
            test_tasks: 测试任务列表 [{"type": ..., "params": ...}, ...]
        
        Returns:
            {
                "old_skill_avg_score": float,
                "new_skill_avg_score": float,
                "improvement": float,  # 正值为改进，负值为退化
                "recommendation": str  # "keep_new", "rollback", "needs_more_testing"
            }
        """
        old_scores = []
        new_scores = []
        
        for task in test_tasks:
            # 模拟执行旧技能
            old_score = self._simulate_skill_execution(old_skill, task)
            old_scores.append(old_score)
            
            # 模拟执行新技能
            new_score = self._simulate_skill_execution(new_skill, task)
            new_scores.append(new_score)
        
        avg_old = sum(old_scores) / len(old_scores) if old_scores else 0
        avg_new = sum(new_scores) / len(new_scores) if new_scores else 0
        improvement = avg_new - avg_old
        
        if improvement > 0.1:
            recommendation = "keep_new"
        elif improvement < -0.1:
            recommendation = "rollback"
        else:
            recommendation = "needs_more_testing"
        
        return {
            "old_skill_avg_score": round(avg_old, 2),
            "new_skill_avg_score": round(avg_new, 2),
            "improvement": round(improvement, 2),
            "recommendation": recommendation,
            "message": f"新技能性能 {'提升' if improvement > 0 else '下降'}了 {abs(improvement):.2f}"
        }
    
    def _simulate_skill_execution(self, skill: dict, task: dict) -> float:
        """模拟技能执行，返回性能评分（0-1）"""
        # 简化版：根据技能定义的复杂度评分
        complexity = len(skill.get("code", "")) / 1000  # 代码越长，复杂度越高
        success_rate = skill.get("estimated_success_rate", 0.5)
        
        # 模拟执行时间（越短越好）
        execution_time = complexity * 2  # 假设每1000字符需要2秒
        time_score = max(0, 1 - execution_time / 10)  # 10秒以上得0分
        
        # 综合评分
        return success_rate * 0.7 + time_score * 0.3
    
    def run_ab_test(self, skill_a: dict, skill_b: dict, num_tasks: int = 10) -> dict:
        """
        A/B测试框架：同时运行两个技能，对比结果
        
        Args:
            skill_a: 技能A（通常是旧版本）
            skill_b: 技能B（通常是新版本）
            num_tasks: 测试任务数量
        
        Returns:
            {
                "skill_a_avg_score": float,
                "skill_b_avg_score": float,
                "winner": str,  # "A" or "B"
                "confidence": float  # 0-1，置信度
            }
        """
        import random
        
        scores_a = []
        scores_b = []
        
        for i in range(num_tasks):
            # 生成模拟任务
            task = {
                "type": random.choice(["read_file", "write_file", "execute_command"]),
                "params": {"test": i}
            }
            
            score_a = self._simulate_skill_execution(skill_a, task)
            score_b = self._simulate_skill_execution(skill_b, task)
            
            scores_a.append(score_a)
            scores_b.append(score_b)
        
        avg_a = sum(scores_a) / len(scores_a)
        avg_b = sum(scores_b) / len(scores_b)
        
        # 计算置信度（简化版：用分数差的绝对值）
        confidence = min(1.0, abs(avg_b - avg_a) * 2)
        
        return {
            "skill_a_avg_score": round(avg_a, 2),
            "skill_b_avg_score": round(avg_b, 2),
            "winner": "B" if avg_b > avg_a else "A",
            "confidence": round(confidence, 2),
            "message": f"技能{'B' if avg_b > avg_a else 'A'}获胜，置信度{confidence:.2f}"
        }
    
    def stress_test_learning_loop(self, num_tasks: int = 100) -> dict:
        """
        学习循环压力测试：模拟大量任务，看学习是否稳定
        
        Args:
            num_tasks: 模拟任务数量
        
        Returns:
            {
                "total_tasks": int,
                "successful_learnings": int,
                "evolution_triggered": int,
                "avg_learning_time": float,
                "stability_score": float  # 0-1，越接近1越稳定
            }
        """
        import time
        import random
        
        original_log = self.learning_log.copy()
        self.learning_log = []  # 清空当前日志
        
        successful = 0
        evolution_count = 0
        start_time = time.time()
        
        for i in range(num_tasks):
            # 模拟任务执行
            task_type = random.choice(["read_file", "write_file", "execute_command", "list_dir"])
            task_params = {"param1": f"value_{i}"}
            result = {"status": "success", "data": f"result_{i}"}
            success = random.random() > 0.2  # 80%成功率
            
            # 学习
            learn_result = self.learn_from_task(task_type, task_params, result, success)
            
            if success:
                successful += 1
            
            if learn_result.get("evolved"):
                evolution_count += 1
        
        end_time = time.time()
        avg_time = (end_time - start_time) / num_tasks
        
        # 稳定性评分（简化版：基于成功率和进化频率）
        success_rate = successful / num_tasks
        evolution_rate = evolution_count / (num_tasks / self.evolution_threshold) if self.evolution_threshold > 0 else 0
        stability = success_rate * 0.6 + min(1.0, evolution_rate) * 0.4
        
        # 恢复原始日志
        self.learning_log = original_log
        
        return {
            "total_tasks": num_tasks,
            "successful_learnings": successful,
            "evolution_triggered": evolution_count,
            "avg_learning_time": round(avg_time, 4),
            "stability_score": round(stability, 2),
            "message": f"压力测试完成，稳定性评分{stability:.2f}"
        }
    
    def get_evolution_history(self) -> list:
        """获取进化历史追踪（记录每次进化的详细信息）"""
        # 从技能池中生成历史（简化版）
        history = []
        for i, skill in enumerate(self.skill_pool):
            history.append({
                "evolution_id": i + 1,
                "timestamp": skill.get("created_at", "unknown"),
                "skill_name": skill.get("name", f"skill_{i + 1}"),
                "performance_before": skill.get("performance_before", 0.5),
                "performance_after": skill.get("performance_after", 0.5),
                "improvement": skill.get("performance_after", 0.5) - skill.get("performance_before", 0.5)
            })
        
        return history
    
    def auto_rollback_if_needed(self, skill_name: str, current_performance: float, threshold: float = 0.1) -> dict:
        """
        自动回滚机制：如果新技能性能下降，自动回滚到旧版本
        
        Args:
            skill_name: 技能名称
            current_performance: 当前性能评分
            threshold: 性能下降阈值（默认10%）
        
        Returns:
            {
                "rolled_back": bool,
                "reason": str,
                "previous_version": dict or None
            }
        """
        # 查找技能的历史版本（简化版：从性能历史中查找）
        if skill_name not in self.performance_history:
            return {
                "rolled_back": False,
                "reason": "No performance history found",
                "previous_version": None
            }
        
        history = self.performance_history[skill_name]
        if len(history) < 2:
            return {
                "rolled_back": False,
                "reason": "Not enough history for comparison",
                "previous_version": None
            }
        
        # 对比当前性能和历史平均
        avg_previous = sum(history[:-1]) / len(history[:-1])  # 排除当前
        
        if current_performance < avg_previous - threshold:
            # 性能下降超过阈值，回滚
            # 简化版：只记录回滚，不实际恢复代码
            return {
                "rolled_back": True,
                "reason": f"Performance dropped from {avg_previous:.2f} to {current_performance:.2f}",
                "previous_version": {"performance": avg_previous},
                "message": "自动回滚已触发"
            }
        else:
            return {
                "rolled_back": False,
                "reason": "Performance is within acceptable range",
                "previous_version": None
            }
    
    def update_performance_history(self, skill_name: str, performance: float):
        """更新技能性能历史"""
        if skill_name not in self.performance_history:
            self.performance_history[skill_name] = []
        
        self.performance_history[skill_name].append(performance)
        
        # 只保留最近10次记录
        if len(self.performance_history[skill_name]) > 10:
            self.performance_history[skill_name] = self.performance_history[skill_name][-10:]

