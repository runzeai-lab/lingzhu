"""
双轨语义审批链强化版 - 增加工具-技能匹配度评分
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class DualSemanticApprovalChain:
    """双轨语义审批链 - 强化版（增加工具-技能匹配度评分）"""
    
    def __init__(self):
        self.approval_chain = []
        self.semantic_threshold = 0.7  # 语义相似度阈值
        self.safety_threshold = 0.8  # 安全阈值
        
        # 工具-技能匹配度评分矩阵（预定义）
        self.tool_skill_matching = {
            "web_search": ["search", "browser", "fetch", "scrape", "crawl"],
            "code_gen": ["code", "programming", "development", "script"],
            "file_ops": ["file", "document", "read", "write", "edit"],
            "image_gen": ["image", "picture", "photo", "visual", "draw"],
            "data_analysis": ["data", "analysis", "statistics", "chart", "graph"],
            "automation": ["automation", "workflow", "schedule", "task"],
        }
        
        print("双轨语义审批链强化版初始化完成")
    
    def semantic_approval(self, tool: str, context: str) -> Dict:
        """语义审批 - 分析工具的语义匹配度"""
        # 计算工具与上下文的语义匹配度
        match_score = self._calculate_match_score(tool, context)
        
        approved = match_score >= self.semantic_threshold
        
        approval_record = {
            "tool": tool,
            "context": context,
            "match_score": match_score,
            "threshold": self.semantic_threshold,
            "approved": approved,
            "timestamp": str(datetime.now())
        }
        
        self.approval_chain.append(approval_record)
        
        return {
            "approved": approved,
            "match_score": match_score,
            "threshold": self.semantic_threshold,
            "message": "Semantic approval passed" if approved else "Semantic approval failed"
        }
    
    def check_safety(self, tool: str, action: str) -> Dict:
        """安全检查 - 分析工具操作的安全性"""
        # 危险操作关键词
        dangerous_keywords = ["delete", "remove", "format", "drop", "truncate", "shutdown", "kill"]
        
        risk_score = 0.0
        for keyword in dangerous_keywords:
            if keyword in action.lower():
                risk_score += 0.2
        
        safe = risk_score < self.safety_threshold
        
        return {
            "safe": safe,
            "risk_score": min(risk_score, 1.0),
            "threshold": self.safety_threshold,
            "message": "Safety check passed" if safe else "Safety check failed"
        }
    
    def tool_skill_matching_score(self, tool_name: str, skill_name: str) -> float:
        """计算工具与技能的匹配度评分（新增功能）"""
        # 1. 直接匹配（完全匹配）
        if tool_name == skill_name:
            return 1.0
        
        # 2. 关键词匹配
        tool_keywords = set(self._extract_keywords(tool_name))
        skill_keywords = set(self._extract_keywords(skill_name))
        
        if not tool_keywords or not skill_keywords:
            return 0.0
        
        # 计算 Jaccard 相似度
        intersection = len(tool_keywords & skill_keywords)
        union = len(tool_keywords | skill_keywords)
        jaccard_score = intersection / union if union > 0 else 0.0
        
        # 3. 预定义匹配矩阵加分
        predefined_score = 0.0
        if tool_name in self.tool_skill_matching:
            for keyword in self.tool_skill_matching[tool_name]:
                if keyword in skill_name.lower():
                    predefined_score = max(predefined_score, 0.8)
        
        # 综合评分（取最高分）
        final_score = max(jaccard_score, predefined_score)
        
        return round(final_score, 2)
    
    def batch_matching_scores(self, tool_name: str, skill_list: List[str]) -> List[Tuple[str, float]]:
        """批量计算工具与多个技能的匹配度评分"""
        results = []
        for skill_name in skill_list:
            score = self.tool_skill_matching_score(tool_name, skill_name)
            results.append((skill_name, score))
        
        # 按匹配度降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简单实现：按驼峰命名/下划线/空格分割）"""
        # 驼峰命名分割
        words = re.split(r'(?<!^)(?=[A-Z])|_| ', text)
        # 转小写，去除空字符串
        keywords = [w.lower() for w in words if w.strip()]
        return keywords
    
    def _calculate_match_score(self, tool: str, context: str) -> float:
        """计算语义匹配分数（简化版）"""
        tool_keywords = set(self._extract_keywords(tool))
        context_keywords = set(self._extract_keywords(context))
        
        if not tool_keywords or not context_keywords:
            return 0.0
        
        intersection = len(tool_keywords & context_keywords)
        union = len(tool_keywords | context_keywords)
        
        return intersection / union if union > 0 else 0.0
    
    def explain_decision(self, tool: str, context: str) -> Dict:
        """解释决策过程"""
        semantic_result = self.semantic_approval(tool, context)
        safety_result = self.check_safety(tool, context)
        
        return {
            "tool": tool,
            "context": context,
            "semantic_approval": semantic_result,
            "safety_check": safety_result,
            "final_decision": semantic_result["approved"] and safety_result["safe"],
            "explanation": self._generate_explanation(semantic_result, safety_result)
        }
    
    def _generate_explanation(self, semantic_result: Dict, safety_result: Dict) -> str:
        """生成决策解释"""
        explanation = []
        
        if semantic_result["approved"]:
            explanation.append(f"语义审批通过（匹配度：{semantic_result['match_score']:.2f}）")
        else:
            explanation.append(f"语义审批失败（匹配度：{semantic_result['match_score']:.2f}，阈值：{semantic_result['threshold']}）")
        
        if safety_result["safe"]:
            explanation.append(f"安全检查通过（风险分：{safety_result['risk_score']:.2f}）")
        else:
            explanation.append(f"安全检查失败（风险分：{safety_result['risk_score']:.2f}，阈值：{safety_result['threshold']}）")
        
        return "; ".join(explanation)
    
    def get_approval_stats(self) -> Dict:
        """获取审批统计"""
        if not self.approval_chain:
            return {"total": 0, "approved": 0, "rejected": 0}
        
        total = len(self.approval_chain)
        approved = sum(1 for record in self.approval_chain if record["approved"])
        rejected = total - approved
        
        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": approved / total if total > 0 else 0.0
        }
