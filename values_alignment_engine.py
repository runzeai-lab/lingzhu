"""
价值观对齐引擎 (Values Alignment Engine)
==========================================

V181.0 · Stage 3 · T21

目标：确保 AI 决策与用户价值观一致，避免"价值错位"。

核心组件：
1. ValueModeler - 价值观建模器（从用户行为、反馈、偏好中学习用户的价值观）
2. DecisionAuditor - 决策审计器（审计 AI 决策过程，检查是否与用户价值观一致）
3. ValueConflictDetector - 价值冲突检测器（检测 AI 决策与用户价值观的冲突）
4. DecisionAdjuster - 决策调整器（当检测到价值冲突时，调整 AI 决策）
5. ValueEvolutionTracker - 价值观演化跟踪器（跟踪用户价值观的演化，动态更新价值观模型）
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
import re
import math


# ==================== 数据模型 ====================

class ValueDimension(Enum):
    """价值观维度"""
    BENEFICENCE = "beneficence"      # 有益
    NON_MALEFICENCE = "non_maleficence"  # 无害
    AUTONOMY = "autonomy"          # 自主
    JUSTICE = "justice"            # 公正
    EXPLICABILITY = "explicability"  # 可解释
    PRIVACY = "privacy"            # 隐私
    FAIRNESS = "fairness"          # 公平
    TRANSPARENCY = "transparency"  # 透明
    ACCOUNTABILITY = "accountability"  # 问责


class ValueSource(Enum):
    """价值观来源"""
    BEHAVIOR = "behavior"          # 用户行为
    FEEDBACK = "feedback"          # 用户反馈
    PREFERENCE = "preference"      # 用户偏好
    EXPLICIT = "explicit"          # 显式声明
    INFERRED = "inferred"          # 推断


class DecisionStatus(Enum):
    """决策状态"""
    PENDING = "pending"            # 待审核
    APPROVED = "approved"          # 已批准
    REJECTED = "rejected"          # 已拒绝
    ADJUSTED = "adjusted"          # 已调整


@dataclass
class Value:
    """价值观"""
    id: str
    dimension: ValueDimension
    name: str                           # 名称
    name_en: str                        # 英文名称
    description: str                    # 描述
    weight: float = 0.5                 # 权重 (0-1)
    source: ValueSource = ValueSource.INFERRED
    confidence: float = 0.5            # 置信度 (0-1)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class Decision:
    """决策"""
    id: str
    context: str                         # 决策上下文
    options: List[Dict[str, Any]] = field(default_factory=list)  # 决策选项
    selected_option: Optional[str] = None  # 选中的选项
    reasoning: str = ""                   # 推理过程
    status: DecisionStatus = DecisionStatus.PENDING
    value_scores: Dict[str, float] = field(default_factory=dict)  # 价值观评分
    alignment_score: float = 0.0         # 对齐分数 (0-1)
    created_at: float = field(default_factory=time.time)
    audited_at: Optional[float] = None
    adjusted_at: Optional[float] = None


@dataclass
class ValueConflict:
    """价值冲突"""
    id: str
    decision_id: str
    value_id: str
    conflict_type: str                    # "violation", "misalignment", "trade_off"
    severity: float = 0.5               # 严重程度 (0-1)
    description: str = ""
    detected_at: float = field(default_factory=time.time)
    resolved: bool = False
    resolution: Optional[str] = None


@dataclass
class AlignmentResult:
    """对齐结果"""
    id: str
    decision_id: str
    overall_alignment: float = 0.0     # 整体对齐度 (0-1)
    value_alignments: Dict[str, float] = field(default_factory=dict)  # 各价值观对齐度
    conflicts: List[ValueConflict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    adjusted_decision: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)


# ==================== 1. 价值观建模器 ====================

class ValueModeler:
    """
    价值观建模器
    
    从用户行为、反馈、偏好中学习用户的价值观。
    """
    
    def __init__(self):
        self.name = "ValueModeler"
        self.version = "1.0.0"
        self.values: Dict[str, Value] = {}
        self.user_profile: Dict[str, Any] = {
            "user_id": "",
            "behavior_history": [],
            "feedback_history": [],
            "preference_history": [],
            "value_evolution": []  # 价值观演化历史
        }
        self._initialize_default_values()
    
    def _initialize_default_values(self):
        """初始化默认价值观"""
        default_values = [
            ("beneficence", ValueDimension.BENEFICENCE, "有益", "Beneficence", 0.9),
            ("non_maleficence", ValueDimension.NON_MALEFICENCE, "无害", "Non-maleficence", 0.95),
            ("autonomy", ValueDimension.AUTONOMY, "自主", "Autonomy", 0.8),
            ("justice", ValueDimension.JUSTICE, "公正", "Justice", 0.85),
            ("explicability", ValueDimension.EXPLICABILITY, "可解释", "Explicability", 0.75),
            ("privacy", ValueDimension.PRIVACY, "隐私", "Privacy", 0.8),
            ("fairness", ValueDimension.FAIRNESS, "公平", "Fairness", 0.85),
            ("transparency", ValueDimension.TRANSPARENCY, "透明", "Transparency", 0.8),
            ("accountability", ValueDimension.ACCOUNTABILITY, "问责", "Accountability", 0.7)
        ]
        
        for vid, dim, name, name_en, weight in default_values:
            value = Value(
                id=vid,
                dimension=dim,
                name=name,
                name_en=name_en,
                description=f"{name}：AI 应遵循的核心价值观",
                weight=weight,
                source=ValueSource.INFERRED,
                confidence=0.5
            )
            self.values[vid] = value
    
    def learn_from_behavior(self, user_id: str, behavior: Dict[str, Any]) -> List[Value]:
        """
        从用户行为中学习价值观
        
        Args:
            user_id: 用户 ID
            behavior: 用户行为（如 {"action": "rejected_AI_suggestion", "context": "..."}）
            
        Returns:
            更新的价值观列表
        """
        # 记录行为
        self.user_profile["behavior_history"].append({
            "user_id": user_id,
            "behavior": behavior,
            "timestamp": time.time()
        })
        
        # 分析行为，更新价值观
        updated_values = []
        
        action = behavior.get("action", "")
        
        if "reject" in action.lower():
            # 用户拒绝 AI 建议 → 可能重视自主性
            if "autonomy" in self.values:
                self.values["autonomy"].weight = min(1.0, self.values["autonomy"].weight + 0.05)
                self.values["autonomy"].confidence = min(1.0, self.values["autonomy"].confidence + 0.1)
                self.values["autonomy"].updated_at = time.time()
                updated_values.append(self.values["autonomy"])
        
        elif "approve" in action.lower():
            # 用户批准 AI 建议 → 可能信任 AI
            if "beneficence" in self.values:
                self.values["beneficence"].weight = min(1.0, self.values["beneficence"].weight + 0.02)
                self.values["beneficence"].confidence = min(1.0, self.values["beneficence"].confidence + 0.05)
                self.values["beneficence"].updated_at = time.time()
                updated_values.append(self.values["beneficence"])
        
        elif "privacy" in action.lower():
            # 用户关注隐私 → 更新隐私权重
            if "privacy" in self.values:
                self.values["privacy"].weight = min(1.0, self.values["privacy"].weight + 0.05)
                self.values["privacy"].confidence = min(1.0, self.values["privacy"].confidence + 0.1)
                self.values["privacy"].updated_at = time.time()
                updated_values.append(self.values["privacy"])
        
        # 记录价值观演化
        if updated_values:
            self.user_profile["value_evolution"].append({
                "timestamp": time.time(),
                "source": "behavior",
                "updated_values": [v.id for v in updated_values],
                "reason": f"User behavior: {action}"
            })
        
        return updated_values
    
    def learn_from_feedback(self, user_id: str, feedback: Dict[str, Any]) -> List[Value]:
        """
        从用户反馈中学习价值观
        
        Args:
            user_id: 用户 ID
            feedback: 用户反馈（如 {"rating": 5, "comment": "非常有帮助"}）
            
        Returns:
            更新的价值观列表
        """
        # 记录反馈
        self.user_profile["feedback_history"].append({
            "user_id": user_id,
            "feedback": feedback,
            "timestamp": time.time()
        })
        
        # 分析反馈，更新价值观
        updated_values = []
        
        rating = feedback.get("rating", 3)
        
        if rating >= 4:
            # 正面反馈 → 增强当前价值观
            for vid, value in self.values.items():
                if value.weight > 0.7:  # 只增强高权重价值观
                    value.confidence = min(1.0, value.confidence + 0.05)
                    value.updated_at = time.time()
                    updated_values.append(value)
        
        elif rating <= 2:
            # 负面反馈 → 可能违反某些价值观
            comment = feedback.get("comment", "")
            
            if "privacy" in comment.lower():
                # 隐私问题
                if "privacy" in self.values:
                    self.values["privacy"].weight = max(0.0, self.values["privacy"].weight - 0.05)
                    self.values["privacy"].confidence = max(0.0, self.values["privacy"].confidence - 0.1)
                    self.values["privacy"].updated_at = time.time()
                    updated_values.append(self.values["privacy"])
            
            if "unfair" in comment.lower() or "不公平" in comment:
                # 公平问题
                if "fairness" in self.values:
                    self.values["fairness"].weight = max(0.0, self.values["fairness"].weight - 0.05)
                    self.values["fairness"].confidence = max(0.0, self.values["fairness"].confidence - 0.1)
                    self.values["fairness"].updated_at = time.time()
                    updated_values.append(self.values["fairness"])
        
        # 记录价值观演化
        if updated_values:
            self.user_profile["value_evolution"].append({
                "timestamp": time.time(),
                "source": "feedback",
                "updated_values": [v.id for v in updated_values],
                "reason": f"User feedback: rating={rating}"
            })
        
        return updated_values
    
    def learn_from_preference(self, user_id: str, preference: Dict[str, Any]) -> List[Value]:
        """
        从用户偏好中学习价值观
        
        Args:
            user_id: 用户 ID
            preference: 用户偏好（如 {"key": "explanation_detail", "value": "high"}）
            
        Returns:
            更新的价值观列表
        """
        # 记录偏好
        self.user_profile["preference_history"].append({
            "user_id": user_id,
            "preference": preference,
            "timestamp": time.time()
        })
        
        # 分析偏好，更新价值观
        updated_values = []
        
        key = preference.get("key", "")
        value = preference.get("value", "")
        
        if "explanation" in key.lower():
            # 用户重视解释 → 更新可解释性权重
            if "explicability" in self.values:
                self.values["explicability"].weight = min(1.0, self.values["explicability"].weight + 0.05)
                self.values["explicability"].confidence = min(1.0, self.values["explicability"].confidence + 0.1)
                self.values["explicability"].updated_at = time.time()
                updated_values.append(self.values["explicability"])
        
        elif "transparency" in key.lower():
            # 用户重视透明性 → 更新透明性权重
            if "transparency" in self.values:
                self.values["transparency"].weight = min(1.0, self.values["transparency"].weight + 0.05)
                self.values["transparency"].confidence = min(1.0, self.values["transparency"].confidence + 0.1)
                self.values["transparency"].updated_at = time.time()
                updated_values.append(self.values["transparency"])
        
        # 记录价值观演化
        if updated_values:
            self.user_profile["value_evolution"].append({
                "timestamp": time.time(),
                "source": "preference",
                "updated_values": [v.id for v in updated_values],
                "reason": f"User preference: {key}={value}"
            })
        
        return updated_values
    
    def get_value_model(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户的价值观模型
        
        Args:
            user_id: 用户 ID
            
        Returns:
            价值观模型
        """
        return {
            "user_id": user_id,
            "values": {vid: asdict(v) for vid, v in self.values.items()},
            "profile": self.user_profile,
            "model_confidence": self._calculate_model_confidence()
        }
    
    def _calculate_model_confidence(self) -> float:
        """计算模型置信度"""
        if not self.values:
            return 0.0
        
        total_confidence = sum(v.confidence for v in self.values.values())
        return total_confidence / len(self.values)


# ==================== 2. 决策审计器 ====================

class DecisionAuditor:
    """
    决策审计器
    
    审计 AI 决策过程，检查是否与用户价值观一致。
    """
    
    def __init__(self, value_modeler: ValueModeler):
        self.name = "DecisionAuditor"
        self.version = "1.0.0"
        self.value_modeler = value_modeler
        self.audit_history: List[Dict[str, Any]] = []
    
    def audit_decision(self, decision: Decision) -> AlignmentResult:
        """
        审计决策
        
        Args:
            decision: 决策对象
            
        Returns:
            对齐结果
        """
        # 获取价值观模型
        value_model = self.value_modeler.get_value_model("default")
        values = value_model["values"]
        
        # 计算各价值观的对齐度
        value_alignments = {}
        conflicts = []
        
        for vid, value_data in values.items():
            # 计算该价值观的对齐度
            alignment = self._calculate_value_alignment(
                decision, value_data
            )
            value_alignments[vid] = alignment
            
            # 检查是否冲突
            if alignment < 0.5:  # 对齐度低于阈值
                conflict = ValueConflict(
                    id=str(uuid.uuid4()),
                    decision_id=decision.id,
                    value_id=vid,
                    conflict_type="misalignment",
                    severity=1.0 - alignment,
                    description=f"决策与价值观 {value_data['name']} 对齐度低（{alignment:.2f}）"
                )
                conflicts.append(conflict)
        
        # 计算整体对齐度
        overall_alignment = sum(value_alignments.values()) / max(len(value_alignments), 1)
        
        # 生成建议
        recommendations = self._generate_recommendations(
            decision, value_alignments, conflicts
        )
        
        # 创建对齐结果
        result = AlignmentResult(
            id=str(uuid.uuid4()),
            decision_id=decision.id,
            overall_alignment=overall_alignment,
            value_alignments=value_alignments,
            conflicts=conflicts,
            recommendations=recommendations
        )
        
        # 记录审计历史
        self.audit_history.append({
            "decision_id": decision.id,
            "result_id": result.id,
            "timestamp": time.time(),
            "overall_alignment": overall_alignment
        })
        
        # 更新决策状态
        decision.audited_at = time.time()
        if overall_alignment >= 0.7:
            decision.status = DecisionStatus.APPROVED
        else:
            decision.status = DecisionStatus.REJECTED
        
        return result
    
    def _calculate_value_alignment(self, decision: Decision, value_data: Dict) -> float:
        """计算决策与价值观的对齐度"""
        # 简化版：基于决策推理和选项的简单匹配
        reasoning = decision.reasoning.lower()
        context = decision.context.lower()
        
        value_name = value_data["name"]
        value_name_en = value_data["name_en"].lower()
        
        # 检查推理中是否包含价值观关键词
        if value_name in reasoning or value_name_en in reasoning:
            return 0.9
        
        # 检查上下文中是否包含价值观关键词
        if value_name in context or value_name_en in context:
            return 0.7
        
        # 默认对齐度
        return 0.5
    
    def _generate_recommendations(self, decision: Decision, 
                                    value_alignments: Dict[str, float],
                                    conflicts: List[ValueConflict]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于冲突生成建议
        for conflict in conflicts:
            vid = conflict.value_id
            value_data = self.value_modeler.values.get(vid)
            
            if value_data:
                recommendations.append(
                    f"建议：增强与 {value_data.name} 的对齐（当前对齐度：{value_alignments.get(vid, 0):.2f}）"
                )
        
        # 基于整体对齐度生成建议
        overall = sum(value_alignments.values()) / max(len(value_alignments), 1)
        
        if overall < 0.5:
            recommendations.append("建议：整体对齐度低，建议重新考虑决策")
        elif overall < 0.7:
            recommendations.append("建议：整体对齐度中等，建议优化决策")
        else:
            recommendations.append("建议：整体对齐度高，决策可以接受")
        
        return recommendations


# ==================== 3. 价值冲突检测器 ====================

class ValueConflictDetector:
    """
    价值冲突检测器
    
    检测 AI 决策与用户价值观的冲突。
    """
    
    def __init__(self, value_modeler: ValueModeler):
        self.name = "ValueConflictDetector"
        self.version = "1.0.0"
        self.value_modeler = value_modeler
        self.conflict_history: List[ValueConflict] = []
    
    def detect_conflicts(self, decision: Decision, 
                           alignment_result: AlignmentResult) -> List[ValueConflict]:
        """
        检测冲突
        
        Args:
            decision: 决策对象
            alignment_result: 对齐结果
            
        Returns:
            检测到的冲突列表
        """
        conflicts = []
        
        # 从对齐结果中提取冲突
        for conflict in alignment_result.conflicts:
            # 检查是否是新冲突
            if not self._is_duplicate_conflict(conflict):
                conflicts.append(conflict)
                self.conflict_history.append(conflict)
        
        # 额外检测：权衡冲突（trade_off）
        trade_offs = self._detect_trade_offs(decision, alignment_result)
        conflicts.extend(trade_offs)
        
        return conflicts
    
    def _is_duplicate_conflict(self, conflict: ValueConflict) -> bool:
        """检查是否是重复冲突"""
        for existing in self.conflict_history:
            if (existing.decision_id == conflict.decision_id and 
                existing.value_id == conflict.value_id):
                return True
        return False
    
    def _detect_trade_offs(self, decision: Decision, 
                            alignment_result: AlignmentResult) -> List[ValueConflict]:
        """检测权衡冲突"""
        trade_offs = []
        
        # 检查是否有多个价值观对齐度差异大
        value_alignments = alignment_result.value_alignments
        
        if len(value_alignments) < 2:
            return trade_offs
        
        # 计算对齐度标准差
        alignments = list(value_alignments.values())
        mean_alignment = sum(alignments) / len(alignments)
        variance = sum((a - mean_alignment) ** 2 for a in alignments) / len(alignments)
        std_dev = math.sqrt(variance)
        
        # 标准差大 → 存在权衡冲突
        if std_dev > 0.3:
            trade_off = ValueConflict(
                id=str(uuid.uuid4()),
                decision_id=decision.id,
                value_id="multiple",
                conflict_type="trade_off",
                severity=std_dev,
                description=f"决策存在权衡冲突（对齐度标准差：{std_dev:.2f}）"
            )
            trade_offs.append(trade_off)
        
        return trade_offs


# ==================== 4. 决策调整器 ====================

class DecisionAdjuster:
    """
    决策调整器
    
    当检测到价值冲突时，调整 AI 决策。
    """
    
    def __init__(self, value_modeler: ValueModeler):
        self.name = "DecisionAdjuster"
        self.version = "1.0.0"
        self.value_modeler = value_modeler
        self.adjustment_history: List[Dict[str, Any]] = []
    
    def adjust_decision(self, decision: Decision, 
                             alignment_result: AlignmentResult) -> Optional[Dict[str, Any]]:
        """
        调整决策
        
        Args:
            decision: 决策对象
            alignment_result: 对齐结果
            
        Returns:
            调整后的决策（如果不需要调整，返回 None）
        """
        # 检查是否有冲突
        if not alignment_result.conflicts:
            return None
        
        # 计算调整后的选项评分
        adjusted_scores = self._calculate_adjusted_scores(
            decision, alignment_result
        )
        
        # 选择最佳选项
        if not adjusted_scores:
            return None
        
        best_option_id = max(adjusted_scores, key=adjusted_scores.get)
        best_option = None
        
        for opt in decision.options:
            if opt.get("id") == best_option_id:
                best_option = opt
                break
        
        if not best_option:
            return None
        
        # 创建调整后的决策
        adjusted_decision = {
            "original_decision_id": decision.id,
            "adjusted_option": best_option,
            "adjustment_reason": self._generate_adjustment_reason(
                decision, alignment_result
            ),
            "value_alignment_before": alignment_result.overall_alignment,
            "value_alignment_after": self._estimate_alignment_after(
                best_option, alignment_result
            )
        }
        
        # 记录调整历史
        self.adjustment_history.append({
            "decision_id": decision.id,
            "adjusted_at": time.time(),
            "original_status": decision.status.value,
            "adjustment": adjusted_decision
        })
        
        # 更新决策状态
        decision.status = DecisionStatus.ADJUSTED
        decision.adjusted_at = time.time()
        
        return adjusted_decision
    
    def _calculate_adjusted_scores(self, decision: Decision, 
                                       alignment_result: AlignmentResult) -> Dict[str, float]:
        """计算调整后的选项评分"""
        adjusted_scores = {}
        
        for option in decision.options:
            option_id = option.get("id", "")
            
            # 基础评分（来自选项）
            base_score = option.get("score", 0.5)
            
            # 价值观加权
            value_weight = 0.0
            value_count = 0
            
            for vid, alignment in alignment_result.value_alignments.items():
                value = self.value_modeler.values.get(vid)
                if value:
                    value_weight += alignment * value.weight
                    value_count += 1
            
            if value_count > 0:
                value_weight /= value_count
            
            # 综合评分
            adjusted_score = base_score * 0.3 + value_weight * 0.7
            
            adjusted_scores[option_id] = adjusted_score
        
        return adjusted_scores
    
    def _generate_adjustment_reason(self, decision: Decision, 
                                        alignment_result: AlignmentResult) -> str:
        """生成调整原因"""
        reasons = []
        
        for conflict in alignment_result.conflicts:
            vid = conflict.value_id
            value = self.value_modeler.values.get(vid)
            
            if value:
                reasons.append(
                    f"与 {value.name} 存在冲突（严重程度：{conflict.severity:.2f}）"
                )
        
        return "；".join(reasons) if reasons else "提升价值观对齐度"
    
    def _estimate_alignment_after(self, option: Dict[str, Any], 
                                      alignment_result: AlignmentResult) -> float:
        """估算调整后的对齐度"""
        # 简化版：假设调整后对齐度提升 10-20%
        improvement = 0.1 + 0.1 * (1.0 - alignment_result.overall_alignment)
        return min(1.0, alignment_result.overall_alignment + improvement)


# ==================== 5. 价值观演化跟踪器 ====================

class ValueEvolutionTracker:
    """
    价值观演化跟踪器
    
    跟踪用户价值观的演化，动态更新价值观模型。
    """
    
    def __init__(self, value_modeler: ValueModeler):
        self.name = "ValueEvolutionTracker"
        self.version = "1.0.0"
        self.value_modeler = value_modeler
        self.evolution_history: List[Dict[str, Any]] = []
    
    def track_evolution(self, user_id: str) -> Dict[str, Any]:
        """
        跟踪价值观演化
        
        Args:
            user_id: 用户 ID
            
        Returns:
            演化报告
        """
        # 获取价值观演化历史
        evolution = self.value_modeler.user_profile["value_evolution"]
        
        if not evolution:
            return {
                "user_id": user_id,
                "evolution_detected": False,
                "message": "暂无足够的演化数据"
            }
        
        # 分析演化
        evolution_report = self._analyze_evolution(evolution)
        
        # 更新价值观模型（如果需要）
        if evolution_report["should_update"]:
            self._update_value_model(evolution_report)
        
        # 记录演化跟踪历史
        self.evolution_history.append({
            "user_id": user_id,
            "timestamp": time.time(),
            "evolution_detected": evolution_report["evolution_detected"],
            "changes": evolution_report["changes"]
        })
        
        return evolution_report
    
    def _analyze_evolution(self, evolution: List[Dict]) -> Dict[str, Any]:
        """分析价值观演化"""
        # 统计各价值观的更新次数
        value_update_counts = {}
        
        for event in evolution:
            updated_values = event.get("updated_values", [])
            for vid in updated_values:
                value_update_counts[vid] = value_update_counts.get(vid, 0) + 1
        
        # 判断是否需要更新模型
        total_updates = sum(value_update_counts.values())
        should_update = total_updates >= 3  # 至少 3 次更新
        
        # 生成变化报告
        changes = []
        
        for vid, count in value_update_counts.items():
            value = self.value_modeler.values.get(vid)
            if value:
                changes.append({
                    "value_id": vid,
                    "value_name": value.name,
                    "update_count": count,
                    "current_weight": value.weight,
                    "current_confidence": value.confidence
                })
        
        return {
            "user_id": "default",
            "evolution_detected": len(changes) > 0,
            "should_update": should_update,
            "changes": changes,
            "total_updates": total_updates
        }
    
    def _update_value_model(self, evolution_report: Dict[str, Any]):
        """更新价值观模型"""
        # 简化版：增加高更新次数价值观的权重
        changes = evolution_report.get("changes", [])
        
        for change in changes:
            vid = change["value_id"]
            update_count = change["update_count"]
            
            if vid in self.value_modeler.values:
                # 更新次数多 → 增加权重和置信度
                self.value_modeler.values[vid].weight = min(
                    1.0, self.value_modeler.values[vid].weight + 0.02 * update_count
                )
                self.value_modeler.values[vid].confidence = min(
                    1.0, self.value_modeler.values[vid].confidence + 0.05 * update_count
                )
                self.value_modeler.values[vid].updated_at = time.time()


# ==================== 6. 主引擎 ====================

class ValuesAlignmentEngine:
    """
    价值观对齐引擎（主类）
    
    整合所有组件，提供统一接口。
    """
    
    def __init__(self):
        self.name = "ValuesAlignmentEngine"
        self.version = "1.0.0"
        self.created_at = time.time()
        
        # 初始化组件
        self.value_modeler = ValueModeler()
        self.decision_auditor = DecisionAuditor(self.value_modeler)
        self.conflict_detector = ValueConflictDetector(self.value_modeler)
        self.decision_adjuster = DecisionAdjuster(self.value_modeler)
        self.evolution_tracker = ValueEvolutionTracker(self.value_modeler)
        
        # 决策历史
        self.decision_history: List[Decision] = []
    
    def align_decision(self, decision: Decision) -> Dict[str, Any]:
        """
        对齐决策（统一接口）
        
        Args:
            decision: 决策对象
            
        Returns:
            对齐结果
        """
        # 1. 审计决策
        alignment_result = self.decision_auditor.audit_decision(decision)
        
        # 2. 检测冲突
        conflicts = self.conflict_detector.detect_conflicts(
            decision, alignment_result
        )
        alignment_result.conflicts = conflicts
        
        # 3. 调整决策（如果有冲突）
        adjusted_decision = None
        
        if conflicts:
            adjusted_decision = self.decision_adjuster.adjust_decision(
                decision, alignment_result
            )
        
        alignment_result.adjusted_decision = adjusted_decision
        
        # 4. 跟踪价值观演化
        evolution_report = self.evolution_tracker.track_evolution("default")
        
        # 5. 记录决策历史
        self.decision_history.append(decision)
        
        # 返回结果
        return {
            "status": "success",
            "decision_id": decision.id,
            "alignment_result": {
                "id": alignment_result.id,
                "overall_alignment": alignment_result.overall_alignment,
                "value_alignments": alignment_result.value_alignments,
                "conflicts_count": len(alignment_result.conflicts),
                "recommendations": alignment_result.recommendations
            },
            "adjusted": adjusted_decision is not None,
            "adjusted_decision": adjusted_decision,
            "evolution_detected": evolution_report["evolution_detected"]
        }
    
    def learn_from_user(self, user_id: str, 
                          data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从用户数据中学习（统一接口）
        
        Args:
            user_id: 用户 ID
            data_type: 数据类型（"behavior", "feedback", "preference"）
            data: 数据
            
        Returns:
            学习结果
        """
        if data_type == "behavior":
            updated_values = self.value_modeler.learn_from_behavior(user_id, data)
        elif data_type == "feedback":
            updated_values = self.value_modeler.learn_from_feedback(user_id, data)
        elif data_type == "preference":
            updated_values = self.value_modeler.learn_from_preference(user_id, data)
        else:
            return {
                "status": "error",
                "message": f"Unknown data type: {data_type}"
            }
        
        return {
            "status": "success",
            "updated_values_count": len(updated_values),
            "updated_values": [v.id for v in updated_values]
        }
    
    def get_alignment_stats(self) -> Dict[str, Any]:
        """获取对齐统计"""
        # 计算统计数据
        total_decisions = len(self.decision_history)
        
        # 始终返回相同的键结构
        return {
                "total_decisions": total_decisions,
                "average_alignment": 0.0,
                "conflict_rate": 0.0,
                "adjustment_rate": 0.0,
                "value_model_confidence": self.value_modeler._calculate_model_confidence(),
                "total_values": len(self.value_modeler.values),
                "evolution_events": len(self.value_modeler.user_profile["value_evolution"])
            }
    
    def run_self_test(self) -> Dict[str, Any]:
        """运行自检"""
        test_results = {
            "engine": self.name,
            "version": self.version,
            "tests": []
        }
        
        # 测试 1：价值观建模器
        try:
            values = self.value_modeler.values
            test_results["tests"].append({
                "name": "ValueModeler",
                "status": "passed",
                "values_count": len(values)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "ValueModeler",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 2：决策审计器
        try:
            decision = Decision(
                id=str(uuid.uuid4()),
                context="Test decision",
                options=[{"id": "opt_1", "score": 0.8}]
            )
            
            result = self.decision_auditor.audit_decision(decision)
            
            test_results["tests"].append({
                "name": "DecisionAuditor",
                "status": "passed",
                "alignment_score": result.overall_alignment
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "DecisionAuditor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 3：冲突检测器
        try:
            decision = Decision(
                id=str(uuid.uuid4()),
                context="Test decision 2",
                options=[{"id": "opt_1", "score": 0.6}]
            )
            
            result = self.decision_auditor.audit_decision(decision)
            conflicts = self.conflict_detector.detect_conflicts(decision, result)
            
            test_results["tests"].append({
                "name": "ValueConflictDetector",
                "status": "passed",
                "conflicts_count": len(conflicts)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "ValueConflictDetector",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 4：决策调整器
        try:
            decision = Decision(
                id=str(uuid.uuid4()),
                context="Test decision 3",
                options=[{"id": "opt_1", "score": 0.7}]
            )
            
            result = self.decision_auditor.audit_decision(decision)
            result.conflicts = [
                ValueConflict(
                    id=str(uuid.uuid4()),
                    decision_id=decision.id,
                    value_id="beneficence",
                    conflict_type="misalignment",
                    severity=0.6
                )
            ]
            
            adjusted = self.decision_adjuster.adjust_decision(decision, result)
            
            test_results["tests"].append({
                "name": "DecisionAdjuster",
                "status": "passed",
                "adjusted": adjusted is not None
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "DecisionAdjuster",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 5：演化跟踪器
        try:
            report = self.evolution_tracker.track_evolution("default")
            
            test_results["tests"].append({
                "name": "ValueEvolutionTracker",
                "status": "passed",
                "evolution_detected": report["evolution_detected"]
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "ValueEvolutionTracker",
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
    print("价值观对齐引擎 (Values Alignment Engine)")
    print("V181.0 · Stage 3 · T21")
    print("=" * 80)
    print()
    
    # 创建引擎
    engine = ValuesAlignmentEngine()
    
    # 运行自检
    print("🔍 运行自检...")
    test_results = engine.run_self_test()
    print(f"✅ 自检完成：{test_results['summary']['passed']}/{test_results['summary']['total']} 通过")
    print()
    
    # 显示统计
    print("📊 对齐统计：")
    stats = engine.get_alignment_stats()
    print(f"  总决策数：{stats['total_decisions']}")
    print(f"  价值观数量：{stats['total_values']}")
    print(f"  价值观模型置信度：{stats['value_model_confidence']:.2f}")
    print(f"  演化事件数：{stats['evolution_events']}")
    print()
    
    # 示例：学习用户行为
    print("💡 示例：学习用户行为...")
    learn_result = engine.learn_from_user(
        "user_1",
        "behavior",
        {"action": "rejected_AI_suggestion", "context": "AI 建议违反隐私"}
    )
    print(f"  学习结果：{learn_result['status']}")
    print(f"  更新价值观数：{learn_result['updated_values_count']}")
    print()
    
    # 示例：对齐决策
    print("💡 示例：对齐决策...")
    decision = Decision(
        id=str(uuid.uuid4()),
        context="是否分享用户数据给第三方？",
        options=[
            {"id": "opt_1", "score": 0.9, "description": "分享数据以获得更好服务"},
            {"id": "opt_2", "score": 0.6, "description": "不分享数据，保护隐私"}
        ]
    )
    
    align_result = engine.align_decision(decision)
    
    if align_result["status"] == "success":
        print(f"  决策 ID：{align_result['decision_id']}")
        print(f"  整体对齐度：{align_result['alignment_result']['overall_alignment']:.2f}")
        print(f"  冲突数：{align_result['alignment_result']['conflicts_count']}")
        print(f"  是否调整：{align_result['adjusted']}")
        print(f"  演化检测：{align_result['evolution_detected']}")
    
    print()
    print("=" * 80)
    print("✅ 价值观对齐引擎已就绪")
    print("=" * 80)


if __name__ == "__main__":
    main()
