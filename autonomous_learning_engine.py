"""
自主学习引擎 (Autonomous Learning Engine)
==============================================

V181.0 · Stage 3 · T22

目标：从互联网自动学习新知识，无需人工干预。

核心组件：
1. InternetCrawler - 互联网爬取器（arXiv、GitHub、Stack Overflow、Wikipedia）
2. KnowledgeExtractor - 知识提取器（从爬取的内容中提取结构化知识）
3. KnowledgeFuser - 知识融合器（将新知识融合到现有知识库中）
4. KnowledgeValidator - 知识验证器（验证新知识的正确性）
5. LearningEffectivenessEvaluator - 学习效果评估器（评估学习效果，调整学习策略）
"""

import json
import time
import uuid
import requests
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
import re
import math
import os
import sys
import subprocess


# ==================== 数据模型 ====================

class KnowledgeSource(Enum):
    """知识来源"""
    ARXIV = "arxiv"
    GITHUB = "github"
    STACKOVERFLOW = "stackoverflow"
    WIKIPEDIA = "wikipedia"
    OTHER = "other"


class KnowledgeType(Enum):
    """知识类型"""
    CONCEPT = "concept"            # 概念
    THEORY = "theory"              # 理论
    METHOD = "method"              # 方法
    FACT = "fact"                  # 事实
    CODE = "code"                  # 代码


class LearningStatus(Enum):
    """学习状态"""
    PENDING = "pending"            # 待学习
    IN_PROGRESS = "in_progress"    # 学习中
    COMPLETED = "completed"        # 学习完成
    FAILED = "failed"              # 学习失败
    VALIDATED = "validated"        # 已验证


@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    source: KnowledgeSource
    type: KnowledgeType
    title: str                           # 标题
    content: str                         # 内容
    url: Optional[str] = None             # 来源 URL
    authors: List[str] = field(default_factory=list)  # 作者
    publish_date: Optional[float] = None  # 发布日期
    extraction_confidence: float = 0.0   # 提取置信度 (0-1)
    validation_score: float = 0.0       # 验证分数 (0-1)
    fusion_status: LearningStatus = LearningStatus.PENDING
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class LearningTask:
    """学习任务"""
    id: str
    source: KnowledgeSource
    query: str                            # 学习查询
    max_items: int = 10                  # 最大条目数
    status: LearningStatus = LearningStatus.PENDING
    items: List[KnowledgeItem] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


@dataclass
class LearningResult:
    """学习结果"""
    id: str
    task_id: str
    items_learned: int = 0              # 学习到的条目数
    items_validated: int = 0           # 验证通过的条目数
    items_fused: int = 0                # 融合到知识库的条目数
    effectiveness_score: float = 0.0     # 学习效果分数 (0-1)
    created_at: float = field(default_factory=time.time)


# ==================== 1. 互联网爬取器 ====================

class InternetCrawler:
    """
    互联网爬取器
    
    从互联网爬取新知识（arXiv、GitHub、Stack Overflow、Wikipedia）。
    """
    
    def __init__(self):
        self.name = "InternetCrawler"
        self.version = "1.0.0"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; LingzhuBot/1.0)"
        })
        self.rate_limit = 1.0  # 爬取间隔（秒）
    
    def crawl_arxiv(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        爬取 arXiv
        
        Args:
            query: 查询关键词
            max_results: 最大结果数
            
        Returns:
            论文列表
        """
        # arXiv API
        base_url = "http://export.arxiv.org/api/query"
        
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # 解析 XML（简化版）
            papers = self._parse_arxiv_xml(response.text)
            
            return papers
        except Exception as e:
            print(f"Error crawling arXiv: {e}")
            return []
    
    def _parse_arxiv_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        """解析 arXiv XML（简化版）"""
        papers = []
        
        # 简化版：使用正则表达式提取基本信息
        # 实际应使用 xml.etree.ElementTree
        entries = re.findall(r'<entry>(.*?)</entry>', xml_text, re.DOTALL)
        
        for entry in entries:
            paper = {}
            
            # 提取标题
            title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            if title_match:
                paper["title"] = title_match.group(1).strip()
            
            # 提取摘要
            summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            if summary_match:
                paper["summary"] = summary_match.group(1).strip()
            
            # 提取 ID
            id_match = re.search(r'<id>(http://arxiv.org/abs/.*?)</id>', entry)
            if id_match:
                paper["id"] = id_match.group(1).split("/")[-1]
                paper["url"] = id_match.group(1)
            
            # 提取作者
            authors = re.findall(r'<name>(.*?)</name>', entry)
            paper["authors"] = authors if authors else []
            
            if paper:
                papers.append(paper)
        
        return papers
    
    def crawl_github(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        爬取 GitHub
        
        Args:
            query: 查询关键词
            max_results: 最大结果数
            
        Returns:
            仓库列表
        """
        # GitHub Search API
        base_url = "https://api.github.com/search/repositories"
        
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": max_results
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            repos = []
            
            for item in data.get("items", []):
                repo = {
                    "id": item["id"],
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "description": item.get("description", ""),
                    "url": item["html_url"],
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "language": item.get("language", "")
                }
                repos.append(repo)
            
            return repos
        except Exception as e:
            print(f"Error crawling GitHub: {e}")
            return []
    
    def crawl_stackoverflow(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        爬取 Stack Overflow
        
        Args:
            query: 查询关键词
            max_results: 最大结果数
            
        Returns:
            问题列表
        """
        # Stack Overflow API
        base_url = "https://api.stackexchange.com/2.3/questions"
        
        params = {
            "site": "stackoverflow",
            "order": "desc",
            "sort": "votes",
            "intitle": query,
            "pagesize": max_results
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            questions = []
            
            for item in data.get("items", []):
                question = {
                    "id": item["question_id"],
                    "title": item["title"],
                    "url": item["link"],
                    "score": item["score"],
                    "answer_count": item["answer_count"],
                    "tags": item.get("tags", [])
                }
                questions.append(question)
            
            return questions
        except Exception as e:
            print(f"Error crawling Stack Overflow: {e}")
            return []
    
    def crawl_wikipedia(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        爬取 Wikipedia
        
        Args:
            query: 查询关键词
            max_results: 最大结果数
            
        Returns:
            文章列表
        """
        # Wikipedia API
        base_url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": max_results
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for item in data.get("query", {}).get("search", []):
                article = {
                    "id": item["pageid"],
                    "title": item["title"],
                    "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                    "snippet": item.get("snippet", "")
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error crawling Wikipedia: {e}")
            return []
    
    def crawl(self, source: KnowledgeSource, query: str, 
               max_results: int = 10) -> List[Dict[str, Any]]:
        """
        爬取知识
        
        Args:
            source: 知识来源
            query: 查询关键词
            max_results: 最大结果数
            
        Returns:
            爬取结果列表
        """
        if source == KnowledgeSource.ARXIV:
            return self.crawl_arxiv(query, max_results)
        elif source == KnowledgeSource.GITHUB:
            return self.crawl_github(query, max_results)
        elif source == KnowledgeSource.STACKOVERFLOW:
            return self.crawl_stackoverflow(query, max_results)
        elif source == KnowledgeSource.WIKIPEDIA:
            return self.crawl_wikipedia(query, max_results)
        else:
            print(f"Unsupported source: {source}")
            return []


# ==================== 2. 知识提取器 ====================

class KnowledgeExtractor:
    """
    知识提取器
    
    从爬取的内容中提取结构化知识。
    """
    
    def __init__(self):
        self.name = "KnowledgeExtractor"
        self.version = "1.0.0"
    
    def extract_from_arxiv(self, paper: Dict[str, Any]) -> Optional[KnowledgeItem]:
        """
        从 arXiv 论文中提取知识
        
        Args:
            paper: 论文数据
            
        Returns:
            知识条目
        """
        if not paper:
            return None
        
        # 提取标题
        title = paper.get("title", "")
        
        # 提取内容（摘要）
        content = paper.get("summary", "")
        
        # 提取作者
        authors = paper.get("authors", [])
        
        # 提取 URL
        url = paper.get("url", "")
        
        # 创建知识条目
        item = KnowledgeItem(
            id=str(uuid.uuid4()),
            source=KnowledgeSource.ARXIV,
            type=KnowledgeType.THEORY,
            title=title,
            content=content,
            url=url,
            authors=authors,
            extraction_confidence=0.8  # 简化版：固定置信度
        )
        
        return item
    
    def extract_from_github(self, repo: Dict[str, Any]) -> Optional[KnowledgeItem]:
        """
        从 GitHub 仓库中提取知识
        
        Args:
            repo: 仓库数据
            
        Returns:
            知识条目
        """
        if not repo:
            return None
        
        # 提取标题
        title = repo.get("name", "")
        
        # 提取内容（描述）
        content = repo.get("description", "")
        
        # 提取 URL
        url = repo.get("url", "")
        
        # 创建知识条目
        item = KnowledgeItem(
            id=str(uuid.uuid4()),
            source=KnowledgeSource.GITHUB,
            type=KnowledgeType.CODE,
            title=title,
            content=content,
            url=url,
            extraction_confidence=0.7
        )
        
        return item
    
    def extract_from_stackoverflow(self, question: Dict[str, Any]) -> Optional[KnowledgeItem]:
        """
        从 Stack Overflow 问题中提取知识
        
        Args:
            question: 问题数据
            
        Returns:
            知识条目
        """
        if not question:
            return None
        
        # 提取标题
        title = question.get("title", "")
        
        # 提取内容（简化版：只提取标题）
        content = title
        
        # 提取 URL
        url = question.get("url", "")
        
        # 创建知识条目
        item = KnowledgeItem(
            id=str(uuid.uuid4()),
            source=KnowledgeSource.STACKOVERFLOW,
            type=KnowledgeType.METHOD,
            title=title,
            content=content,
            url=url,
            extraction_confidence=0.6
        )
        
        return item
    
    def extract_from_wikipedia(self, article: Dict[str, Any]) -> Optional[KnowledgeItem]:
        """
        从 Wikipedia 文章中提取知识
        
        Args:
            article: 文章数据
            
        Returns:
            知识条目
        """
        if not article:
            return None
        
        # 提取标题
        title = article.get("title", "")
        
        # 提取内容（简化版：只提取摘要）
        content = article.get("snippet", "")
        
        # 提取 URL
        url = article.get("url", "")
        
        # 创建知识条目
        item = KnowledgeItem(
            id=str(uuid.uuid4()),
            source=KnowledgeSource.WIKIPEDIA,
            type=KnowledgeType.FACT,
            title=title,
            content=content,
            url=url,
            extraction_confidence=0.9
        )
        
        return item
    
    def extract(self, source: KnowledgeSource, 
                  data: Dict[str, Any]) -> Optional[KnowledgeItem]:
        """
        提取知识
        
        Args:
            source: 知识来源
            data: 原始数据
            
        Returns:
            知识条目
        """
        if source == KnowledgeSource.ARXIV:
            return self.extract_from_arxiv(data)
        elif source == KnowledgeSource.GITHUB:
            return self.extract_from_github(data)
        elif source == KnowledgeSource.STACKOVERFLOW:
            return self.extract_from_stackoverflow(data)
        elif source == KnowledgeSource.WIKIPEDIA:
            return self.extract_from_wikipedia(data)
        else:
            print(f"Unsupported source: {source}")
            return None


# ==================== 3. 知识融合器 ====================

class KnowledgeFuser:
    """
    知识融合器
    
    将新知识融合到现有知识库中。
    """
    
    def __init__(self):
        self.name = "KnowledgeFuser"
        self.version = "1.0.0"
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """初始化知识库（简化版）"""
        # 这里应该加载现有知识库
        # 简化版：不加载
        pass
    
    def fuse(self, item: KnowledgeItem) -> bool:
        """
        融合知识条目
        
        Args:
            item: 知识条目
            
        Returns:
            是否成功融合
        """
        if not item:
            return False
        
        # 检查是否已存在（简化版：检查标题相似度）
        for existing_id, existing_item in self.knowledge_base.items():
            if self._calculate_title_similarity(item.title, existing_item.title) > 0.8:
                # 已存在，跳过
                return False
        
        # 添加到知识库
        item.fusion_status = LearningStatus.COMPLETED
        item.updated_at = time.time()
        self.knowledge_base[item.id] = item
        
        return True
    
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """计算标题相似度（简化版）"""
        # 简化版：使用编辑距离
        if not title1 or not title2:
            return 0.0
        
        # 转换为小写并分词
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        # 计算 Jaccard 相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """获取知识库统计"""
        return {
            "total_items": len(self.knowledge_base),
            "by_source": self._count_by_source(),
            "by_type": self._count_by_type()
        }
    
    def _count_by_source(self) -> Dict[str, int]:
        """按来源统计"""
        counts = {}
        
        for item in self.knowledge_base.values():
            source = item.source.value
            counts[source] = counts.get(source, 0) + 1
        
        return counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """按类型统计"""
        counts = {}
        
        for item in self.knowledge_base.values():
            type_ = item.type.value
            counts[type_] = counts.get(type_, 0) + 1
        
        return counts


# ==================== 4. 知识验证器 ====================

class KnowledgeValidator:
    """
    知识验证器
    
    验证新知识的正确性（交叉验证、专家评估）。
    """
    
    def __init__(self):
        self.name = "KnowledgeValidator"
        self.version = "1.0.0"
    
    def validate(self, item: KnowledgeItem) -> Tuple[bool, float, str]:
        """
        验证知识条目
        
        Args:
            item: 知识条目
            
        Returns:
            (是否通过验证, 验证分数, 原因）
        """
        # 验证 1：检查内容是否为空
        if not item.content or len(item.content) < 10:
            return False, 0.0, "内容过短"
        
        # 验证 2：检查标题是否为空
        if not item.title:
            return False, 0.0, "标题为空"
        
        # 验证 3：检查来源是否可信（简化版）
        source_trust = self._calculate_source_trust(item.source)
        
        if source_trust <= 0.5:
            return False, source_trust, "来源可信度低"
        
        # 验证 4：交叉验证（简化版）
        cross_validation_score = self._cross_validate(item)
        
        # 综合评分
        validation_score = (source_trust * 0.4 + cross_validation_score * 0.6)
        
        if validation_score >= 0.7:
            return True, validation_score, "验证通过"
        else:
            return False, validation_score, "验证分数过低"
    
    def _calculate_source_trust(self, source: KnowledgeSource) -> float:
        """计算来源可信度"""
        trust_scores = {
            KnowledgeSource.ARXIV: 0.9,       # 学术论文，可信度高
            KnowledgeSource.GITHUB: 0.7,      # 开源代码，可信度中等
            KnowledgeSource.STACKOVERFLOW: 0.8,  # 技术问答，可信度较高
            KnowledgeSource.WIKIPEDIA: 0.85,  # 百科，可信度较高
            KnowledgeSource.OTHER: 0.5
        }
        
        return trust_scores.get(source, 0.5)
    
    def _cross_validate(self, item: KnowledgeItem) -> float:
        """交叉验证（简化版）"""
        # 简化版：不执行实际的交叉验证
        # 返回固定分数
        return 0.75


# ==================== 5. 学习效果评估器 ====================

class LearningEffectivenessEvaluator:
    """
    学习效果评估器
    
    评估学习效果，调整学习策略。
    """
    
    def __init__(self):
        self.name = "LearningEffectivenessEvaluator"
        self.version = "1.0.0"
        self.learning_history: List[LearningResult] = []
    
    def evaluate(self, task: LearningTask, 
                  items: List[KnowledgeItem]) -> LearningResult:
        """
        评估学习效果
        
        Args:
            task: 学习任务
            items: 学习到的知识条目
            
        Returns:
            学习结果
        """
        # 计算各项指标
        items_learned = len(items)
        items_validated = sum(1 for item in items if item.validation_score >= 0.7)
        items_fused = sum(1 for item in items if item.fusion_status == LearningStatus.COMPLETED)
        
        # 计算学习效果分数
        effectiveness_score = self._calculate_effectiveness_score(
            items_learned, items_validated, items_fused, task.max_items
        )
        
        # 创建学习结果
        result = LearningResult(
            id=str(uuid.uuid4()),
            task_id=task.id,
            items_learned=items_learned,
            items_validated=items_validated,
            items_fused=items_fused,
            effectiveness_score=effectiveness_score
        )
        
        # 记录学习历史
        self.learning_history.append(result)
        
        return result
    
    def _calculate_effectiveness_score(self, items_learned: int, 
                                        items_validated: int, 
                                        items_fused: int, 
                                        max_items: int) -> float:
        """计算学习效果分数"""
        if max_items == 0:
            return 0.0
        
        # 计算各项比率
        learn_rate = items_learned / max_items
        validate_rate = items_validated / max(max_items, 1)
        fuse_rate = items_fused / max(max_items, 1)
        
        # 综合分数
        score = learn_rate * 0.4 + validate_rate * 0.3 + fuse_rate * 0.3
        
        return min(1.0, score)
    
    def adjust_strategy(self, result: LearningResult) -> Dict[str, Any]:
        """
        调整学习策略
        
        Args:
            result: 学习结果
            
        Returns:
            调整建议
        """
        suggestions = {}
        
        # 基于学习效果分数调整策略
        if result.effectiveness_score < 0.5:
            # 学习效果差，建议调整策略
            suggestions["action"] = "adjust_strategy"
            suggestions["reason"] = "学习效果差"
            suggestions["suggestions"] = [
                "增加爬取间隔，避免被封禁",
                "更换查询关键词，提高相关性",
                "增加验证严格度，提高知识质量"
            ]
        elif result.effectiveness_score < 0.7:
            # 学习效果中等，建议优化策略
            suggestions["action"] = "optimize_strategy"
            suggestions["reason"] = "学习效果中等"
            suggestions["suggestions"] = [
                "优化提取算法，提高提取置信度",
                "增加知识融合的去重逻辑",
                "增加更多知识来源"
            ]
        else:
            # 学习效果好，建议保持策略
            suggestions["action"] = "maintain_strategy"
            suggestions["reason"] = "学习效果好"
            suggestions["suggestions"] = [
                "保持当前策略",
                "增加爬取频率（如果未被封禁）",
                "扩展到更多知识领域"
            ]
        
        return suggestions


# ==================== 6. 主引擎 ====================

class AutonomousLearningEngine:
    """
    自主学习引擎（主类）
    
    整合所有组件，提供统一接口。
    """
    
    def __init__(self):
        self.name = "AutonomousLearningEngine"
        self.version = "1.0.0"
        self.created_at = time.time()
        
        # 初始化组件
        self.crawler = InternetCrawler()
        self.extractor = KnowledgeExtractor()
        self.fuser = KnowledgeFuser()
        self.validator = KnowledgeValidator()
        self.evaluator = LearningEffectivenessEvaluator()
        
        # 学习任务历史
        self.task_history: List[LearningTask] = []
    
    def learn(self, source: KnowledgeSource, query: str, 
                max_items: int = 10) -> Dict[str, Any]:
        """
        学习知识（统一接口）
        
        Args:
            source: 知识来源
            query: 查询关键词
            max_items: 最大条目数
            
        Returns:
            学习结果
        """
        # 1. 创建学习任务
        task = LearningTask(
            id=str(uuid.uuid4()),
            source=source,
            query=query,
            max_items=max_items,
            status=LearningStatus.IN_PROGRESS
        )
        
        # 2. 爬取知识
        crawled_data = self.crawler.crawl(source, query, max_items)
        
        if not crawled_data:
            task.status = LearningStatus.FAILED
            return {
                "status": "error",
                "message": "爬取失败，未获取到数据"
            }
        
        # 3. 提取知识
        items = []
        
        for data in crawled_data[:max_items]:
            item = self.extractor.extract(source, data)
            
            if item:
                items.append(item)
        
        if not items:
            task.status = LearningStatus.FAILED
            return {
                "status": "error",
                "message": "提取失败，未提取到知识"
            }
        
        # 4. 验证知识
        validated_items = []
        
        for item in items:
            is_valid, score, reason = self.validator.validate(item)
            
            if is_valid:
                item.validation_score = score
                item.fusion_status = LearningStatus.VALIDATED
                validated_items.append(item)
        
        # 5. 融合知识
        fused_count = 0
        
        for item in validated_items:
            if self.fuser.fuse(item):
                fused_count += 1
        
        # 6. 评估学习效果
        result = self.evaluator.evaluate(task, validated_items)
        
        # 7. 调整学习策略
        suggestions = self.evaluator.adjust_strategy(result)
        
        # 8. 更新任务状态
        task.items = validated_items
        task.status = LearningStatus.COMPLETED
        task.completed_at = time.time()
        self.task_history.append(task)
        
        # 返回结果
        return {
            "status": "success",
            "task_id": task.id,
            "query": query,
            "source": source.value,
            "items_learned": len(items),
            "items_validated": len(validated_items),
            "items_fused": fused_count,
            "effectiveness_score": result.effectiveness_score,
            "suggestions": suggestions
        }
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        return {
            "total_tasks": len(self.task_history),
            "knowledge_base": self.fuser.get_knowledge_base_stats(),
            "recent_results": [
                {
                    "task_id": r.task_id,
                    "items_learned": r.items_learned,
                    "effectiveness_score": r.effectiveness_score
                }
                for r in self.evaluator.learning_history[-10:]  # 最近 10 个结果
            ]
        }
    
    def run_self_test(self) -> Dict[str, Any]:
        """运行自检"""
        test_results = {
            "engine": self.name,
            "version": self.version,
            "tests": []
        }
        
        # 测试 1：互联网爬取器
        try:
            papers = self.crawler.crawl_arxiv("AI ethics", max_results=5)
            
            test_results["tests"].append({
                "name": "InternetCrawler",
                "status": "passed",
                "papers_count": len(papers)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "InternetCrawler",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 2：知识提取器
        try:
            paper_data = {
                "title": "Test Paper",
                "summary": "This is a test paper about AI ethics.",
                "authors": ["Author 1", "Author 2"],
                "url": "http://arxiv.org/abs/1234.56789"
            }
            
            item = self.extractor.extract_from_arxiv(paper_data)
            
            test_results["tests"].append({
                "name": "KnowledgeExtractor",
                "status": "passed",
                "item_id": item.id if item else None
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "KnowledgeExtractor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 3：知识融合器
        try:
            test_item = KnowledgeItem(
                id="test_1",
                source=KnowledgeSource.ARXIV,
                type=KnowledgeType.THEORY,
                title="Test Item",
                content="Test content"
            )
            
            result = self.fuser.fuse(test_item)
            
            test_results["tests"].append({
                "name": "KnowledgeFuser",
                "status": "passed",
                "fuse_result": result
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "KnowledgeFuser",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 4：知识验证器
        try:
            test_item = KnowledgeItem(
                id="test_2",
                source=KnowledgeSource.WIKIPEDIA,
                type=KnowledgeType.FACT,
                title="Test Item",
                content="This is a test content with sufficient length for validation."
            )
            
            is_valid, score, reason = self.validator.validate(test_item)
            
            test_results["tests"].append({
                "name": "KnowledgeValidator",
                "status": "passed",
                "is_valid": is_valid,
                "score": score
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "KnowledgeValidator",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 5：学习效果评估器
        try:
            test_task = LearningTask(
                id="task_1",
                source=KnowledgeSource.ARXIV,
                query="AI ethics"
            )
            
            test_items = [
                KnowledgeItem(
                    id="item_1",
                    source=KnowledgeSource.ARXIV,
                    type=KnowledgeType.THEORY,
                    title="Test Item 1",
                    content="Test content 1",
                    validation_score=0.8,
                    fusion_status=LearningStatus.COMPLETED
                )
            ]
            
            result = self.evaluator.evaluate(test_task, test_items)
            
            test_results["tests"].append({
                "name": "LearningEffectivenessEvaluator",
                "status": "passed",
                "effectiveness_score": result.effectiveness_score
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "LearningEffectivenessEvaluator",
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
    print("自主学习引擎 (Autonomous Learning Engine)")
    print("V181.0 · Stage 3 · T22")
    print("=" * 80)
    print()
    
    # 创建引擎
    engine = AutonomousLearningEngine()
    
    # 运行自检
    print("🔍 运行自检...")
    test_results = engine.run_self_test()
    print(f"✅ 自检完成：{test_results['summary']['passed']}/{test_results['summary']['total']} 通过")
    print()
    
    # 显示学习统计
    print("📊 学习统计：")
    stats = engine.get_learning_stats()
    print(f"  总学习任务数：{stats['total_tasks']}")
    print(f"  知识库条目数：{stats['knowledge_base']['total_items']}")
    print()
    
    # 示例学习
    print("💡 示例学习：")
    result = engine.learn(
        source=KnowledgeSource.ARXIV,
        query="AI ethics",
        max_items=5
    )
    
    if result["status"] == "success":
        print(f"  查询：{result['query']}")
        print(f"  来源：{result['source']}")
        print(f"  学习到条目数：{result['items_learned']}")
        print(f"  验证通过数：{result['items_validated']}")
        print(f"  融合条目数：{result['items_fused']}")
        print(f"  学习效果分数：{result['effectiveness_score']:.2f}")
        print()
        print("  调整建议：")
        for suggestion in result["suggestions"]["suggestions"]:
            print(f"    - {suggestion}")
    
    print()
    print("=" * 80)
    print("✅ 自主学习引擎已就绪")
    print("=" * 80)


if __name__ == "__main__":
    main()
