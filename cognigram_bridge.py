import re
import json
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict

class CognigramBridge:
    """
    CogniGram 语义理解桥梁 - 增强版
    功能：
    1. 语义理解引擎（轻量级，基于规则和向量化）
    2. Multi-modal 理解（文本 + 代码 + 结构化数据）
    3. 上下文记忆（短期 + 长期）
    4. 语义推理（因果关系、类比推理）
    5. 知识图谱接口（连接到外部知识库）
    """
    
    def __init__(self, memory_callback=None, knowledge_base=None):
        self.memory_callback = memory_callback or {}
        self.knowledge_base = knowledge_base or {}
        
        # 语义理解：停用词表（中文 + 英文）
        self.stop_words = {
            # 中文停用词
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这",
            # 英文停用词
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once"
        }
        
        # 上下文记忆
        self.short_term_memory = []  # 短期记忆（最近10个交互）
        self.long_term_memory = []    # 长期记忆（重要事件）
        self.memory_threshold = 0.7   # 长期记忆阈值（重要性评分）
        
        # 语义推理：因果关系关键词
        self.causal_keywords = [
            "因为", "所以", "导致", "原因", "结果", "影响", "使得", "引发",
            "because", "so", "therefore", "cause", "result", "lead to", "due to"
        ]
        
        # 知识图谱（简化版，可扩展到外部）
        self.local_knowledge_graph = {
            "AI": ["机器学习", "深度学习", "自然语言处理", "计算机视觉"],
            "灵助": ["数字生命", "V180", "多Agent系统", "语义理解"],
            "Python": ["编程", "脚本", "数据分析", "AI开发"],
            "语义理解": ["自然语言处理", "知识图谱", "推理", "上下文"]
        }
        
        # 性能统计
        self.stats = {
            "total_queries": 0,
            "semantic_matches": 0,
            "causal_inferences": 0,
            "memory_retrievals": 0
        }
        
        print("CogniGram Bridge 增强版初始化完成")
    
    # ==================== 1. 语义理解引擎 ====================
    
    def understand_text(self, text: str, context: Optional[str] = None) -> Dict:
        """
        理解文本语义（轻量级实现）
        
        Args:
            text: 待理解文本
            context: 上下文（可选）
        
        Returns:
            {
                "keywords": List[str],  # 关键词
                "entities": List[str],   # 实体
                "intent": str,           # 意图（question/command/statement）
                "sentiment": float,      # 情感（-1到1）
                "complexity": float      # 复杂度（0-1）
            }
        """
        self.stats["total_queries"] += 1
        
        # 1. 提取关键词（去除停用词）
        words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
        keywords = [w for w in words if w not in self.stop_words]
        
        # 2. 识别实体（简化版：大写字母开头的英文 / 连续中文字符）
        entities = []
        # 英文实体（大写字母开头）
        english_entities = re.findall(r'\b[A-Z][a-zA-Z]*\b', text)
        entities.extend(english_entities)
        # 中文实体（连续2+中文字符）
        chinese_entities = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        entities.extend(chinese_entities)
        
        # 3. 判断意图
        intent = "statement"
        if "?" in text or "？" in text:
            intent = "question"
        elif any(text.startswith(w) for w in ["请", "帮我", "我想", "please", "help"]):
            intent = "command"
        
        # 4. 情感分析（简化版：基于情感词）
        positive_words = ["好", "棒", "喜欢", "开心", "成功", "good", "great", "excellent", "happy"]
        negative_words = ["差", "坏", "讨厌", "伤心", "失败", "bad", "poor", "hate", "sad"]
        
        sentiment = 0.0
        for w in positive_words:
            if w in text:
                sentiment += 0.2
        for w in negative_words:
            if w in text:
                sentiment -= 0.2
        sentiment = max(-1.0, min(1.0, sentiment))
        
        # 5. 计算复杂度（基于句子长度、生僻词比例）
        complexity = min(1.0, len(text) / 500)  # 500字符为满分
        
        # 6. 更新短期记忆
        self._update_short_term_memory(text, keywords, intent)
        
        return {
            "keywords": keywords[:10],  # 最多返回10个关键词
            "entities": list(set(entities)),
            "intent": intent,
            "sentiment": round(sentiment, 2),
            "complexity": round(complexity, 2),
            "message": "语义理解完成"
        }
    
    def _update_short_term_memory(self, text: str, keywords: List[str], intent: str):
        """更新短期记忆"""
        memory_entry = {
            "timestamp": str(datetime.now()),
            "text": text[:100],  # 只保存前100字符
            "keywords": keywords,
            "intent": intent
        }
        
        self.short_term_memory.append(memory_entry)
        
        # 只保留最近10个
        if len(self.short_term_memory) > 10:
            self.short_term_memory = self.short_term_memory[-10:]
    
    # ==================== 2. Multi-modal 理解 ====================
    
    def understand_multi_modal(self, text: Optional[str] = None, 
                              code: Optional[str] = None,
                              data: Optional[dict] = None) -> Dict:
        """
        Multi-modal 理解（文本 + 代码 + 结构化数据）
        
        Args:
            text: 文本输入
            code: 代码输入
            data: 结构化数据输入
        
        Returns:
            综合理解结果
        """
        results = {}
        
        if text:
            results["text_understanding"] = self.understand_text(text)
        
        if code:
            results["code_understanding"] = self._understand_code(code)
        
        if data:
            results["data_understanding"] = self._understand_data(data)
        
        # 跨模态融合（简化版）
        if len(results) > 1:
            results["fusion"] = self._fuse_multi_modal_results(results)
        
        return results
    
    def _understand_code(self, code: str) -> Dict:
        """理解代码（简化版：提取函数名、类名、导入语句）"""
        functions = re.findall(r'def\s+(\w+)\s*\(', code)
        classes = re.findall(r'class\s+(\w+)\s*[:\(]', code)
        imports = re.findall(r'(?:from|import)\s+(\w+)', code)
        
        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": len(code.splitlines()) / 100,  # 每100行算1复杂度
            "message": "代码理解完成"
        }
    
    def _understand_data(self, data: dict) -> Dict:
        """理解结构化数据（简化版：统计信息）"""
        return {
            "keys": list(data.keys()),
            "num_keys": len(data),
            "has_nested": any(isinstance(v, (dict, list)) for v in data.values()),
            "message": "数据理解完成"
        }
    
    def _fuse_multi_modal_results(self, results: Dict) -> Dict:
        """融合多模态结果（简化版）"""
        fusion = {
            "modality_count": len(results),
            "combined_keywords": [],
            "overall_intent": "mixed"
        }
        
        # 合并关键词
        for key in results:
            if "keywords" in results[key]:
                fusion["combined_keywords"].extend(results[key]["keywords"])
        
        fusion["combined_keywords"] = list(set(fusion["combined_keywords"]))[:15]
        
        return fusion
    
    # ==================== 3. 上下文记忆 ====================
    
    def retrieve_memory(self, query: str, memory_type: str = "both") -> List[Dict]:
        """
        检索记忆
        
        Args:
            query: 查询文本
            memory_type: "short", "long", "both"
        
        Returns:
            相关记忆列表
        """
        self.stats["memory_retrievals"] += 1
        
        query_keywords = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
        relevant_memories = []
        
        # 检索短期记忆
        if memory_type in ["short", "both"]:
            for memory in self.short_term_memory:
                memory_keywords = set(memory.get("keywords", []))
                overlap = len(query_keywords & memory_keywords)
                if overlap > 0:
                    memory["relevance"] = overlap / max(len(query_keywords), 1)
                    relevant_memories.append(memory)
        
        # 检索长期记忆
        if memory_type in ["long", "both"]:
            for memory in self.long_term_memory:
                memory_keywords = set(memory.get("keywords", []))
                overlap = len(query_keywords & memory_keywords)
                if overlap > 0:
                    memory["relevance"] = overlap / max(len(query_keywords), 1)
                    relevant_memories.append(memory)
        
        # 按相关性排序
        relevant_memories.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        return relevant_memories[:5]  # 返回最相关的5条
    
    def consolidate_memory(self):
        """记忆巩固：将重要的短期记忆转移到长期记忆"""
        for memory in self.short_term_memory:
            # 计算重要性（基于关键词数量、意图等）
            importance = len(memory.get("keywords", [])) / 10
            
            if importance >= self.memory_threshold:
                memory["importance"] = importance
                self.long_term_memory.append(memory)
        
        # 清空短期记忆
        self.short_term_memory = []
        
        return {
            "consolidated": len(self.long_term_memory),
            "message": "记忆巩固完成"
        }
    
    # ==================== 4. 语义推理 ====================
    
    def infer_causal_relationship(self, text: str) -> Dict:
        """
        推理因果关系
        
        Args:
            text: 包含因果关系的文本
        
        Returns:
            {"causal": bool, "cause": str, "effect": str}
        """
        self.stats["causal_inferences"] += 1
        
        # 检查是否包含因果关系关键词
        has_causal = any(kw in text for kw in self.causal_keywords)
        
        if not has_causal:
            return {"causal": False, "reason": "No causal keywords found"}
        
        # 简化版：假设 "因为 X，所以 Y" 模式
        if "因为" in text and "所以" in text:
            parts = text.split("因为")[1].split("所以")
            cause = parts[0].strip()
            effect = parts[1].strip() if len(parts) > 1 else ""
            return {"causal": True, "cause": cause, "effect": effect}
        
        # 英文模式："X because Y" 或 "Because Y, X"
        if "because" in text.lower():
            # 简化版：返回整句
            return {"causal": True, "text": text, "pattern": "because"}
        
        return {"causal": True, "text": text, "pattern": "unknown"}
    
    def analogical_reasoning(self, source_domain: str, target_domain: str) -> Dict:
        """
        类比推理：从源领域到目标领域的知识迁移
        
        Args:
            source_domain: 源领域
            target_domain: 目标领域
        
        Returns:
            {"similarity": float, "mapped_concepts": dict}
        """
        # 简化版：基于知识图谱的映射
        if source_domain in self.local_knowledge_graph:
            source_concepts = self.local_knowledge_graph[source_domain]
        else:
            source_concepts = [source_domain]
        
        if target_domain in self.local_knowledge_graph:
            target_concepts = self.local_knowledge_graph[target_domain]
        else:
            target_concepts = [target_domain]
        
        # 计算相似度（简化版：共同概念数量 / 总概念数量）
        common = set(source_concepts) & set(target_concepts)
        total = set(source_concepts) | set(target_concepts)
        similarity = len(common) / max(len(total), 1)
        
        return {
            "similarity_score": round(similarity, 2),
            "source_concepts": source_concepts,
            "target_concepts": target_concepts,
            "mapped_concepts": {s: t for s, t in zip(source_concepts, target_concepts)},
            "message": "类比推理完成"
        }
    
    # ==================== 5. 知识图谱接口 ====================
    
    def query_knowledge_graph(self, entity: str) -> Dict:
        """
        查询知识图谱
        
        Args:
            entity: 实体名称
        
        Returns:
            {"entity": str, "relations": list, "connected_entities": list}
        """
        if entity in self.local_knowledge_graph:
            return {
                "entity": entity,
                "relations": self.local_knowledge_graph[entity],
                "connected_entities": self.local_knowledge_graph[entity],
                "source": "local"
            }
        else:
            # 可扩展到外部知识图谱（如 DBpedia、Wikidata）
            return {
                "entity": entity,
                "relations": [],
                "connected_entities": [],
                "source": "none",
                "message": "实体未在本地知识图谱中找到"
            }
    
    def expand_knowledge_graph(self, entity: str, relations: List[str]):
        """扩展本地知识图谱"""
        if entity not in self.local_knowledge_graph:
            self.local_knowledge_graph[entity] = []
        
        self.local_knowledge_graph[entity].extend(relations)
        self.local_knowledge_graph[entity] = list(set(self.local_knowledge_graph[entity]))  # 去重
        
        return {
            "entity": entity,
            "relations": self.local_knowledge_graph[entity],
            "message": "知识图谱扩展完成"
        }
    
    # ==================== 统计信息 ====================
    
    def get_bridge_stats(self) -> Dict:
        """获取桥梁统计信息"""
        return {
            "stats": self.stats,
            "short_term_memory_size": len(self.short_term_memory),
            "long_term_memory_size": len(self.long_term_memory),
            "local_knowledge_graph_size": len(self.local_knowledge_graph),
            "message": "CogniGram Bridge 统计信息"
        }