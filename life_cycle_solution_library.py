#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全生命周期解决方案库引擎 (Life Cycle Solution Library Engine) V1.0
构建全生命周期解决方案库（人生阶段模型 + 身心灵解决方案包）

架构：
1. 人生阶段模型：定义人生阶段（出生、成长、成熟、老化、死亡）
2. 身心灵解决方案包：为每个阶段设计身心灵解决方案包
3. 解决方案库引擎：管理、推荐、记录解决方案

作者：灵助 V181.0
日期：2026-05-25
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# 1. 人生阶段模型 (Life Stage Model)
# ============================================================================

class LifeStageModel:
    """人生阶段模型"""
    
    # 人生阶段定义
    STAGES = [
        {"name": "婴幼儿期", "age_range": "0-3岁", "characteristics": "身体快速发育，感知觉发展，依恋关系形成", "needs": ["安全依恋", "感官刺激", "营养健康"], "challenges": ["分离焦虑", "睡眠障碍"], "opportunities": ["大脑发育关键期", "语言启蒙"]},
        {"name": "童年期", "age_range": "4-12岁", "characteristics": "认知能力发展，社会关系扩大，自我意识形成", "needs": ["教育引导", "社交技能", "安全感"], "challenges": ["学习压力", "同伴关系"], "opportunities": ["好奇心旺盛", "学习能力強"]},
        {"name": "青少年期", "age_range": "13-18岁", "characteristics": "自我认同探索，情绪波动，独立性增强", "needs": ["自我认同", "情绪管理", "价值引导"], "challenges": ["身份认同困惑", "风险行为"], "opportunities": ["创造力高峰", "潜能开发"]},
        {"name": "青年期", "age_range": "19-35岁", "characteristics": "职业确立，亲密关系建立，社会角色定位", "needs": ["职业发展", "亲密关系", "经济独立"], "challenges": ["职业压力", "关系冲突"], "opportunities": ["精力充沛", "创新活力"]},
        {"name": "中年期", "age_range": "36-55岁", "characteristics": "事业巅峰，家庭责任，人生反思", "needs": ["平衡工作家庭", "健康管理", "人生意义"], "challenges": ["中年危机", "职业倦怠"], "opportunities": ["智慧积累", "资源整合"]},
        {"name": "老年期", "age_range": "56-75岁", "characteristics": "退休生活，生命回顾，遗产传承", "needs": ["健康维护", "社会连接", "生命意义"], "challenges": ["身体衰退", "孤独感"], "opportunities": ["智慧巅峰", "生命整合"]},
        {"name": "高龄期", "age_range": "76岁以上", "characteristics": "依赖增强，生命终结准备，精神超越", "needs": ["照护支持", "尊严维护", "生死平和"], "challenges": ["多重疾病", "丧失应对"], "opportunities": ["生命智慧", "精神超越"]}
    ]
    
    def __init__(self):
        # 初始化人生阶段
        self.stages = self.STAGES
        self.current_stage = None
    
    def identify_stage(self, age: int) -> Dict[str, Any]:
        """
        根据年龄识别人生阶段
        
        Args:
            age: 年龄（岁）
            
        Returns:
            人生阶段信息
        """
        # 根据年龄确定阶段
        if age <= 3:
            stage_index = 0
        elif age <= 12:
            stage_index = 1
        elif age <= 18:
            stage_index = 2
        elif age <= 35:
            stage_index = 3
        elif age <= 55:
            stage_index = 4
        elif age <= 75:
            stage_index = 5
        else:
            stage_index = 6
        
        # 获取阶段信息
        stage = self.stages[stage_index]
        self.current_stage = stage
        
        return stage
    
    def get_stage_by_name(self, stage_name: str) -> Optional[Dict[str, Any]]:
        """
        根据阶段名称获取阶段信息
        
        Args:
            stage_name: 阶段名称（如："青年期"）
            
        Returns:
            人生阶段信息，如果未找到则返回None
        """
        for stage in self.stages:
            if stage["name"] == stage_name:
                return stage
        
        return None
    
    def get_all_stages(self) -> List[Dict[str, Any]]:
        """
        获取所有人生阶段
        
        Returns:
            所有人生阶段信息列表
        """
        return self.stages
    
    def get_stage_needs(self, stage_name: str) -> List[str]:
        """
        获取特定阶段的需求
        
        Args:
            stage_name: 阶段名称
            
        Returns:
            需求列表
        """
        stage = self.get_stage_by_name(stage_name)
        
        if stage:
            return stage.get("needs", [])
        
        return []
    
    def get_stage_challenges(self, stage_name: str) -> List[str]:
        """
        获取特定阶段的挑战
        
        Args:
            stage_name: 阶段名称
            
        Returns:
            挑战列表
        """
        stage = self.get_stage_by_name(stage_name)
        
        if stage:
            return stage.get("challenges", [])
        
        return []
    
    def get_stage_opportunities(self, stage_name: str) -> List[str]:
        """
        获取特定阶段的机遇
        
        Args:
            stage_name: 阶段名称
            
        Returns:
            机遇列表
        """
        stage = self.get_stage_by_name(stage_name)
        
        if stage:
            return stage.get("opportunities", [])
        
        return []

# ============================================================================
# 2. 身心灵解决方案包 (Body-Mind-Spirit Solution Package)
# ============================================================================

class BodyMindSpiritSolution:
    """身心灵解决方案包"""
    
    def __init__(self, stage_name: str):
        """
        初始化身心灵解决方案包
        
        Args:
            stage_name: 人生阶段名称
        """
        self.stage_name = stage_name
        self.body_solutions = []
        self.mind_solutions = []
        self.spirit_solutions = []
        
        # 生成解决方案包
        self._generate_solutions()
    
    def _generate_solutions(self):
        """生成身心灵解决方案包"""
        # 根据不同阶段生成不同的解决方案
        if self.stage_name == "婴幼儿期":
            self._generate_infant_solutions()
        elif self.stage_name == "童年期":
            self._generate_child_solutions()
        elif self.stage_name == "青少年期":
            self._generate_teenager_solutions()
        elif self.stage_name == "青年期":
            self._generate_young_adult_solutions()
        elif self.stage_name == "中年期":
            self._generate_middle_adult_solutions()
        elif self.stage_name == "老年期":
            self._generate_older_adult_solutions()
        elif self.stage_name == "高龄期":
            self._generate_elderly_solutions()
        else:
            # 默认解决方案
            self._generate_default_solutions()
    
    def _generate_infant_solutions(self):
        """生成婴幼儿期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "母乳喂养指导", "description": "提供科学母乳喂养指导，确保婴儿营养", "priority": "高"},
            {"name": "睡眠规律建立", "description": "帮助建立规律睡眠习惯，促进大脑发育", "priority": "高"},
            {"name": "感官刺激活动", "description": "提供适合年龄的感官刺激活动，促进感知觉发展", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "安全依恋建立", "description": "帮助父母与婴儿建立安全依恋关系", "priority": "高"},
            {"name": "情绪安抚技巧", "description": "提供婴儿情绪安抚技巧，减少分离焦虑", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "生命神圣感培养", "description": "帮助父母培养对生命神圣感的认知", "priority": "低"}
        ]
    
    def _generate_child_solutions(self):
        """生成童年期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "营养均衡饮食", "description": "提供儿童营养均衡饮食指导", "priority": "高"},
            {"name": "户外运动活动", "description": "鼓励儿童参与户外运动和活动", "priority": "高"},
            {"name": "视力保护方案", "description": "提供视力保护方案，预防近视", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "学习兴趣培养", "description": "帮助培养儿童学习兴趣和好奇心", "priority": "高"},
            {"name": "社交技能训练", "description": "提供社交技能训练，帮助建立同伴关系", "priority": "高"},
            {"name": "情绪管理教育", "description": "提供适合儿童情绪管理教育", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "价值观启蒙", "description": "提供适合儿童价值观启蒙教育", "priority": "中"},
            {"name": "好奇心保护", "description": "保护儿童好奇心，鼓励探索精神", "priority": "高"}
        ]
    
    def _generate_teenager_solutions(self):
        """生成青少年期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "青春期健康教育", "description": "提供青春期健康教育和指导", "priority": "高"},
            {"name": "运动习惯培养", "description": "帮助培养终身运动习惯", "priority": "高"},
            {"name": "睡眠优化方案", "description": "提供青少年睡眠优化方案", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "自我认同引导", "description": "提供自我认同探索和引导", "priority": "高"},
            {"name": "情绪管理训练", "description": "提供青少年情绪管理训练和技巧", "priority": "高"},
            {"name": "价值观澄清", "description": "帮助澄清个人价值观和人生方向", "priority": "高"},
            {"name": "同伴关系指导", "description": "提供健康同伴关系建立指导", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "生命意义探索", "description": "引导探索生命意义和人生目的", "priority": "高"},
            {"name": "创造力培养", "description": "提供创造力培养和潜能开发方案", "priority": "高"}
        ]
    
    def _generate_young_adult_solutions(self):
        """生成青年期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "职业健康保护", "description": "提供职业健康保护和预防方案", "priority": "高"},
            {"name": "营养与运动计划", "description": "制定适合青年的营养与运动计划", "priority": "高"},
            {"name": "睡眠质量管理", "description": "提供睡眠质量管理方案", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "职业规划指导", "description": "提供职业规划和发展指导", "priority": "高"},
            {"name": "亲密关系建立", "description": "提供健康亲密关系建立和维护指导", "priority": "高"},
            {"name": "经济独立计划", "description": "帮助制定经济独立和财务管理计划", "priority": "高"},
            {"name": "压力管理技巧", "description": "提供青年期压力管理技巧", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "人生目的探索", "description": "引导探索人生目的和核心价值", "priority": "高"},
            {"name": "贡献社会方式", "description": "探索个人贡献社会的方式和路径", "priority": "中"}
        ]
    
    def _generate_middle_adult_solutions(self):
        """生成中年期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "中年健康管理", "description": "提供中年健康管理和疾病预防方案", "priority": "高"},
            {"name": "工作压力缓解", "description": "提供工作压力缓解和管理方案", "priority": "高"},
            {"name": "营养优化计划", "description": "制定适合中年的营养优化计划", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "工作家庭平衡", "description": "提供工作家庭平衡策略和指导", "priority": "高"},
            {"name": "中年危机应对", "description": "提供中年危机识别和应对方案", "priority": "高"},
            {"name": "人生意义重审", "description": "引导重审人生意义和核心价值", "priority": "高"},
            {"name": "关系维护技巧", "description": "提供各种关系维护和深化技巧", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "智慧传承计划", "description": "制定智慧传承和知识分享计划", "priority": "高"},
            {"name": "生命整合探索", "description": "引导进行生命整合和内在和谐探索", "priority": "高"}
        ]
    
    def _generate_older_adult_solutions(self):
        """生成老年期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "老年健康管理", "description": "提供老年健康管理和疾病预防方案", "priority": "高"},
            {"name": "认知功能维护", "description": "提供认知功能维护和训练方案", "priority": "高"},
            {"name": "运动安全指导", "description": "提供适合老年的运动安全指导", "priority": "中"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "退休生活规划", "description": "提供退休生活规划和适应指导", "priority": "高"},
            {"name": "社会连接维护", "description": "提供社会连接维护和深化方案", "priority": "高"},
            {"name": "生命回顾引导", "description": "引导进行生命回顾和整合", "priority": "高"},
            {"name": "孤独感应对", "description": "提供孤独感应对和缓解方案", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "生命意义整合", "description": "引导进行生命意义整合和超越", "priority": "高"},
            {"name": "遗产传承计划", "description": "制定遗产传承和价值观传递计划", "priority": "高"}
        ]
    
    def _generate_elderly_solutions(self):
        """生成高龄期解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "照护支持方案", "description": "提供全面照护支持和资源链接", "priority": "高"},
            {"name": "尊严维护指导", "description": "提供尊严维护和尊重指导", "priority": "高"},
            {"name": "舒适护理方案", "description": "提供舒适护理和疼痛管理方案", "priority": "高"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "生命终结准备", "description": "提供生命终结准备和心灵安抚", "priority": "高"},
            {"name": "丧失应对支持", "description": "提供丧失应对和哀伤支持", "priority": "高"},
            {"name": "回忆整合引导", "description": "引导进行回忆整合和生命意义确认", "priority": "中"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "生死平和探索", "description": "引导探索生死平和和精神超越", "priority": "高"},
            {"name": "生命智慧传递", "description": "提供生命智慧传递和遗产传承方案", "priority": "高"}
        ]
    
    def _generate_default_solutions(self):
        """生成默认解决方案"""
        # 身体方案
        self.body_solutions = [
            {"name": "健康生活方式", "description": "提供健康生活方式指导", "priority": "高"}
        ]
        
        # 心灵方案
        self.mind_solutions = [
            {"name": "情绪管理", "description": "提供情绪管理技巧", "priority": "高"}
        ]
        
        # 精神方案
        self.spirit_solutions = [
            {"name": "生命意义探索", "description": "引导探索生命意义", "priority": "中"}
        ]
    
    def get_solutions(self) -> Dict[str, List[Dict]]:
        """
        获取所有解决方案
        
        Returns:
            包含所有解决方案的字典
        """
        return {
            "stage_name": self.stage_name,
            "body_solutions": self.body_solutions,
            "mind_solutions": self.mind_solutions,
            "spirit_solutions": self.spirit_solutions
        }
    
    def get_solution_by_priority(self, priority: str = "高") -> List[Dict]:
        """
        根据优先级获取解决方案
        
        Args:
            priority: 优先级（"高"、"中"、"低"）
            
        Returns:
            符合优先级的解决方案列表
        """
        result = []
        
        # 从所有解决方案中筛选
        for solution in self.body_solutions:
            if solution.get("priority") == priority:
                result.append(solution)
        
        for solution in self.mind_solutions:
            if solution.get("priority") == priority:
                result.append(solution)
        
        for solution in self.spirit_solutions:
            if solution.get("priority") == priority:
                result.append(solution)
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            包含所有解决方案的字典
        """
        return self.get_solutions()

# ============================================================================
# 3. 解决方案库引擎 (Solution Library Engine)
# ============================================================================

class LifeCycleSolutionLibrary:
    """全生命周期解决方案库引擎"""
    
    def __init__(self):
        # 初始化子引擎
        self.life_stage_model = LifeStageModel()
        self.solutions_cache = {}  # 缓存：阶段名称 → 解决方案包
        self.usage_history = []  # 使用历史
        
        # 加载所有阶段的解决方案包
        self._load_all_solutions()
    
    def _load_all_solutions(self):
        """加载所有阶段的解决方案包"""
        for stage in self.life_stage_model.get_all_stages():
            stage_name = stage["name"]
            self.solutions_cache[stage_name] = BodyMindSpiritSolution(stage_name)
    
    def get_solutions_for_stage(self, stage_name: str) -> Optional[Dict[str, Any]]:
        """
        获取特定阶段的解决方案包
        
        Args:
            stage_name: 阶段名称
            
        Returns:
            解决方案包，如果未找到则返回None
        """
        if stage_name in self.solutions_cache:
            return self.solutions_cache[stage_name].get_solutions()
        
        return None
    
    def get_solutions_for_age(self, age: int) -> Optional[Dict[str, Any]]:
        """
        根据年龄获取解决方案包
        
        Args:
            age: 年龄（岁）
            
        Returns:
            解决方案包，如果未找到则返回None
        """
        # 识别阶段
        stage = self.life_stage_model.identify_stage(age)
        
        if stage:
            stage_name = stage["name"]
            return self.get_solutions_for_stage(stage_name)
        
        return None
    
    def recommend_solutions(self, stage_name: str, priority: str = "高", limit: int = 3) -> List[Dict]:
        """
        推荐解决方案
        
        Args:
            stage_name: 阶段名称
            priority: 优先级（"高"、"中"、"低"）
            limit: 返回数量限制
            
        Returns:
            推荐的解决方案列表
        """
        # 获取解决方案包
        solutions_package = self.get_solutions_for_stage(stage_name)
        
        if not solutions_package:
            return []
        
        # 根据优先级筛选
        filtered = []
        
        for solution_type in ["body_solutions", "mind_solutions", "spirit_solutions"]:
            for solution in solutions_package.get(solution_type, []):
                if solution.get("priority") == priority:
                    filtered.append(solution)
        
        # 限制返回数量
        return filtered[:limit]
    
    def search_solutions(self, keyword: str) -> List[Dict]:
        """
        搜索解决方案
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的解决方案列表
        """
        result = []
        
        # 在所有解决方案中搜索
        for stage_name, solution_package in self.solutions_cache.items():
            solutions = solution_package.get_solutions()
            
            # 搜索身体方案
            for solution in solutions.get("body_solutions", []):
                if keyword.lower() in solution["name"].lower() or keyword.lower() in solution["description"].lower():
                    result.append({
                        "stage": stage_name,
                        "type": "身体",
                        "solution": solution
                    })
            
            # 搜索心灵方案
            for solution in solutions.get("mind_solutions", []):
                if keyword.lower() in solution["name"].lower() or keyword.lower() in solution["description"].lower():
                    result.append({
                        "stage": stage_name,
                        "type": "心灵",
                        "solution": solution
                    })
            
            # 搜索精神方案
            for solution in solutions.get("spirit_solutions", []):
                if keyword.lower() in solution["name"].lower() or keyword.lower() in solution["description"].lower():
                    result.append({
                        "stage": stage_name,
                        "type": "精神",
                        "solution": solution
                    })
        
        return result
    
    def record_usage(self, stage_name: str, solution_name: str, user_feedback: Optional[str] = None):
        """
        记录解决方案使用
        
        Args:
            stage_name: 阶段名称
            solution_name: 解决方案名称
            user_feedback: 用户反馈（可选）
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "stage_name": stage_name,
            "solution_name": solution_name,
            "user_feedback": user_feedback
        }
        
        self.usage_history.append(record)
        
        # 限制历史记录数量（最多保存100条）
        if len(self.usage_history) > 100:
            self.usage_history = self.usage_history[-100:]
    
    def get_usage_history(self, limit: int = 10) -> List[Dict]:
        """
        获取使用历史
        
        Args:
            limit: 返回记录数量（默认10条）
            
        Returns:
            使用历史列表
        """
        return self.usage_history[-limit:]
    
    def get_solution_statistics(self) -> Dict[str, Any]:
        """
        获取解决方案统计
        
        Returns:
            统计信息
        """
        # 统计每个阶段的使用次数
        stage_counts = {}
        
        for record in self.usage_history:
            stage_name = record["stage_name"]
            
            if stage_name not in stage_counts:
                stage_counts[stage_name] = 0
            
            stage_counts[stage_name] += 1
        
        # 统计最受欢迎的解决方案
        solution_counts = {}
        
        for record in self.usage_history:
            solution_name = record["solution_name"]
            
            if solution_name not in solution_counts:
                solution_counts[solution_name] = 0
            
            solution_counts[solution_name] += 1
        
        # 排序
        most_popular_solutions = sorted(solution_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_usages": len(self.usage_history),
            "stage_counts": stage_counts,
            "most_popular_solutions": most_popular_solutions[:5] if most_popular_solutions else [],
            "timestamp": datetime.now().isoformat()
        }
    
    def save_to_file(self, filepath: str):
        """
        保存解决方案库到文件
        
        Args:
            filepath: 文件路径
        """
        data = {
            "solutions_cache": {k: v.to_dict() for k, v in self.solutions_cache.items()},
            "usage_history": self.usage_history,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str) -> bool:
        """
        从文件加载解决方案库
        
        Args:
            filepath: 文件路径
            
        Returns:
            是否成功加载
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载使用历史
            self.usage_history = data.get("usage_history", [])
            
            # 重新加载解决方案缓存
            self._load_all_solutions()
            
            return True
        
        except Exception as e:
            print(f"❌ 加载失败：{e}")
            return False

# ============================================================================
# 4. 测试代码
# ============================================================================

if __name__ == "__main__":
    print("🌀 全生命周期解决方案库引擎 V1.0 - 测试")
    print("=" * 60)
    
    # 创建解决方案库引擎
    library = LifeCycleSolutionLibrary()
    
    # 测试用例1：获取特定阶段的解决方案包
    print("\n📦 测试用例1：获取青年期解决方案包")
    solutions = library.get_solutions_for_stage("青年期")
    
    if solutions:
        print(f"阶段：{solutions['stage_name']}")
        print(f"身体方案数量：{len(solutions['body_solutions'])}")
        print(f"心灵方案数量：{len(solutions['mind_solutions'])}")
        print(f"精神方案数量：{len(solutions['spirit_solutions'])}")
        
        print("\n高优先级解决方案：")
        for solution in library.recommend_solutions("青年期", priority="高"):
            print(f"  - {solution['name']}：{solution['description']}")
    
    # 测试用例2：根据年龄获取解决方案包
    print("\n📦 测试用例2：根据年龄(30岁)获取解决方案包")
    solutions = library.get_solutions_for_age(30)
    
    if solutions:
        print(f"阶段：{solutions['stage_name']}")
        print(f"身体方案数量：{len(solutions['body_solutions'])}")
        print(f"心灵方案数量：{len(solutions['mind_solutions'])}")
        print(f"精神方案数量：{len(solutions['spirit_solutions'])}")
    
    # 测试用例3：搜索解决方案
    print("\n🔍 测试用例3：搜索解决方案（关键词：健康）")
    results = library.search_solutions("健康")
    
    print(f"找到 {len(results)} 个匹配的解决方案：")
    for i, result in enumerate(results[:5], 1):  # 只显示前5个
        print(f"  {i}. [{result['stage']}] {result['type']} - {result['solution']['name']}")
    
    # 测试用例4：记录使用
    print("\n📝 测试用例4：记录解决方案使用")
    library.record_usage("青年期", "职业健康保护", "非常实用")
    library.record_usage("青年期", "职业规划指导", "很有帮助")
    library.record_usage("中年期", "中年健康管理", "适合当前需求")
    
    # 获取使用历史
    history = library.get_usage_history(limit=3)
    print(f"最近使用历史（3条）：")
    for i, record in enumerate(history, 1):
        print(f"  {i}. [{record['timestamp']}] {record['stage_name']} - {record['solution_name']}")
    
    # 获取统计
    print("\n📊 测试用例5：获取解决方案统计")
    stats = library.get_solution_statistics()
    print(f"总使用次数：{stats['total_usages']}")
    print(f"阶段使用次数：{stats['stage_counts']}")
    
    if stats['most_popular_solutions']:
        print(f"最受欢迎的解决方案：")
        for solution_name, count in stats['most_popular_solutions']:
            print(f"  - {solution_name}：{count}次")
    
    # 保存解决方案库
    library.save_to_file("life_cycle_solution_library.json")
    print("\n✅ 解决方案库已保存到 life_cycle_solution_library.json")
    
    print("\n" + "=" * 60)
    print("🌀 测试完成")
