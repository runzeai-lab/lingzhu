"""
梦境引擎强化版 - 增加灵感连接功能
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class DreamingEngine:
    """梦境引擎 - 强化版（增加灵感连接功能）"""
    
    def __init__(self, memory_callback=None):
        self.dream_log = []
        self.inspiration_connections = []
        self.concept_library = [
            "AI", "梦境", "创造力", "潜意识", "灵感", "连接", "创新",
            "技术", "艺术", "哲学", "科学", "自然", "宇宙", "人类",
            "数字", "生命", "智慧", "进化", "共生"
        ]
        self.memory_callback = memory_callback or {}
        print("梦境引擎强化版初始化完成")
    
    def start_dreaming(self, topic: str = "") -> Dict:
        """开始梦境"""
        dream_entry = {
            "topic": topic if topic else "自由梦境",
            "start_time": str(datetime.now()),
            "status": "dreaming"
        }
        self.dream_log.append(dream_entry)
        
        # 生成梦境内容
        dream_content = self._generate_dream_content(topic)
        dream_entry["content"] = dream_content
        dream_entry["status"] = "completed"
        dream_entry["end_time"] = str(datetime.now())
        
        return {
            "status": "success",
            "dream": dream_entry,
            "message": "梦境生成完成"
        }
    
    async def run(self, topic: str = ""):
        """运行梦境引擎（异步版本，调用 start_dreaming）"""
        return self.start_dreaming(topic)
    
    def get_dream_log(self) -> List[Dict]:
        """获取梦境日志"""
        return self.dream_log
    
    def analyze_dream(self, dream_id: int = -1) -> Dict:
        """分析梦境"""
        if not self.dream_log:
            return {"error": "没有梦境记录"}
        
        if dream_id == -1:
            dream = self.dream_log[-1]  # 最新梦境
        elif 0 <= dream_id < len(self.dream_log):
            dream = self.dream_log[dream_id]
        else:
            return {"error": f"无效的梦境ID: {dream_id}"}
        
        analysis = {
            "dream_id": dream_id,
            "topic": dream["topic"],
            "key_themes": self._extract_themes(dream.get("content", "")),
            "inspiration_level": random.uniform(0.6, 0.95),
            "analysis": "梦境分析完成"
        }
        
        return analysis
    
    def inspiration_connection(self, concept1: str, concept2: str) -> Dict:
        """灵感连接 - 将两个不相关的概念进行连接，产生创新想法（新增功能）"""
        # 1. 检查概念是否在概念库中
        if concept1 not in self.concept_library:
            self.concept_library.append(concept1)
        if concept2 not in self.concept_library:
            self.concept_library.append(concept2)
        
        # 2. 生成连接（创新想法）
        connection = self._generate_connection(concept1, concept2)
        
        # 3. 记录连接
        connection_record = {
            "concept1": concept1,
            "concept2": concept2,
            "connection": connection,
            "timestamp": str(datetime.now()),
            "inspiration_score": random.uniform(0.7, 0.95)
        }
        self.inspiration_connections.append(connection_record)
        
        return {
            "concept1": concept1,
            "concept2": concept2,
            "connection": connection,
            "inspiration_score": connection_record["inspiration_score"],
            "message": "灵感连接生成完成"
        }
    
    def batch_inspiration_connections(self, concept_pairs: List[List[str]]) -> List[Dict]:
        """批量灵感连接"""
        results = []
        for pair in concept_pairs:
            if len(pair) >= 2:
                result = self.inspiration_connection(pair[0], pair[1])
                results.append(result)
        return results
    
    def get_inspiration_connections(self) -> List[Dict]:
        """获取所有灵感连接记录"""
        return self.inspiration_connections
    
    def _generate_dream_content(self, topic: str) -> str:
        """生成梦境内容（简化版）"""
        if not topic:
            # 自由梦境：随机组合概念
            concepts = random.sample(self.concept_library, min(3, len(self.concept_library)))
            return f"梦境中出现了 {', '.join(concepts)} 等概念，它们交织成奇妙的画面..."
        else:
            # 主题梦境：围绕主题生成
            return f"围绕主题「{topic}」，梦境中展现出多种可能性和创新想法..."
    
    def _extract_themes(self, content: str) -> List[str]:
        """提取主题（简化版）"""
        # 简单实现：从概念库中查找出现在内容中的概念
        themese = [c for c in self.concept_library if c in content]
        return themese if themese else ["未知主题"]
    
    def _generate_connection(self, concept1: str, concept2: str) -> str:
        """生成两个概念的连接（创新想法）"""
        # 预定义的连接模板
        templates = [
            f"将 {concept1} 的核心理念应用到 {concept2} 中，可能会产生...",
            f"如果 {concept1} 和 {concept2} 结合，会创造出全新的...",
            f"从 {concept1} 的视角重新审视 {concept2}，会发现...",
            f"{concept1} 与 {concept2} 的交叉点可能隐藏着...",
        ]
        
        # 随机选择一个模板，并添加具体描述
        connection = random.choice(templates)
        connection += f"\n具体想法：{self._generate_specific_idea(concept1, concept2)}"
        
        return connection
    
    def _generate_specific_idea(self, concept1: str, concept2: str) -> str:
        """生成具体的创新想法（简化版）"""
        ideas = [
            f"一种新型的 {concept1}-{concept2} 混合系统",
            f"基于 {concept1} 原理的 {concept2} 优化方案",
            f"将 {concept1} 的灵活性引入 {concept2} 的设计中",
            f"利用 {concept2} 的资源增强 {concept1} 的能力",
        ]
        return random.choice(ideas)
