#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧决策引擎 (Wisdom Decision Engine) V1.0
基于九爻元枢架构的决策引擎原型

架构：
1. 输入层：用户指令 / 系统状态 / 外部环境
2. 九爻推演层：天（时）×人（空）×体（能）= 19683卦象
3. 五重心智层：自觉→认知→安全→调度→执行
4. 决策输出层：最佳行动方案

作者：灵助 V181.0
日期：2026-05-24
"""

import json
import re
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# ============================================================================
# 1. 输入层 (Input Layer)
# ============================================================================

class DecisionInput:
    """决策输入"""
    
    def __init__(self, user_command: str, system_state: Dict, environment: Dict):
        """
        初始化决策输入
        
        Args:
            user_command: 用户指令
            system_state: 系统状态（如：CPU使用率、内存使用率、任务队列...）
            environment: 外部环境（如：时间、地点、网络状态...）
        """
        self.user_command = user_command
        self.system_state = system_state
        self.environment = environment
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "user_command": self.user_command,
            "system_state": self.system_state,
            "environment": self.environment,
            "timestamp": self.timestamp
        }

# ============================================================================
# 2. 九爻推演层 (Nine Hexagram Inference Layer)
# ============================================================================

class NineHexagramEngine:
    """九爻元枢推演引擎"""
    
    # 九爻卦象体系
    HEAVEN = ["未来", "现在", "过去"]  # 天三爻（时间性）
    HUMAN = ["远方", "边界", "内在"]   # 人三爻（空间性）
    BODY = ["创造", "混沌", "秩序"]     # 体三爻（涌现性）
    
    def __init__(self):
        self.hexagram_count = 3 * 3 * 3  # 27个基本卦象
        self.total_states = 3 ** 9  # 19683种状态
    
    def infer(self, decision_input: DecisionInput) -> Dict:
        """
        九爻推演
        
        Args:
            decision_input: 决策输入
            
        Returns:
            推演结果（含天三爻、人三爻、体三爻评分）
        """
        # 1. 天三爻（时间性）评分
        heaven_scores = self._evaluate_heaven(decision_input)
        
        # 2. 人三爻（空间性）评分
        human_scores = self._evaluate_human(decision_input)
        
        # 3. 体三爻（涌现性）评分
        body_scores = self._evaluate_body(decision_input)
        
        # 4. 生成卦象（简化版：取最高分的组合）
        hexagram = self._generate_hexagram(heaven_scores, human_scores, body_scores)
        
        return {
            "heaven": heaven_scores,
            "human": human_scores,
            "body": body_scores,
            "hexagram": hexagram,
            "total_score": sum(heaven_scores.values()) + sum(human_scores.values()) + sum(body_scores.values())
        }
    
    def _evaluate_heaven(self, decision_input: DecisionInput) -> Dict[str, float]:
        """评估天三爻（时间性）"""
        # 简化逻辑：根据时间戳、用户指令关键词、系统状态趋势评分
        scores = {}
        
        # 未来：指令是否涉及未来规划？
        scores["未来"] = 0.8 if "计划" in decision_input.user_command or "规划" in decision_input.user_command else 0.3
        
        # 现在：指令是否紧急？
        scores["现在"] = 0.9 if "立即" in decision_input.user_command or "马上" in decision_input.user_command else 0.5
        
        # 过去：是否涉及历史数据？
        scores["过去"] = 0.6 if "历史" in decision_input.user_command or "之前" in decision_input.user_command else 0.2
        
        return scores
    
    def _evaluate_human(self, decision_input: DecisionInput) -> Dict[str, float]:
        """评估人三爻（空间性）"""
        scores = {}
        
        # 远方：是否涉及远程资源？
        scores["远方"] = 0.7 if "下载" in decision_input.user_command or "API" in decision_input.user_command else 0.3
        
        # 边界：是否涉及权限/安全边界？
        scores["边界"] = 0.6 if "权限" in decision_input.user_command or "安全" in decision_input.user_command else 0.4
        
        # 内在：是否涉及本地资源？
        scores["内在"] = 0.8 if "本地" in decision_input.user_command or "WSL" in decision_input.user_command else 0.5
        
        return scores
    
    def _evaluate_body(self, decision_input: DecisionInput) -> Dict[str, float]:
        """评估体三爻（涌现性）"""
        scores = {}
        
        # 创造：是否涉及创造性任务？
        scores["创造"] = 0.9 if "生成" in decision_input.user_command or "创建" in decision_input.user_command else 0.4
        
        # 混沌：是否涉及不确定性？
        scores["混沌"] = 0.5 if "可能" in decision_input.user_command or "不确定" in decision_input.user_command else 0.2
        
        # 秩序：是否涉及规则/流程？
        scores["秩序"] = 0.7 if "规则" in decision_input.user_command or "流程" in decision_input.user_command else 0.3
        
        return scores
    
    def _generate_hexagram(self, heaven: Dict, human: Dict, body: Dict) -> str:
        """生成卦象（简化版）"""
        # 取每个维度的最高分项
        heaven_top = max(heaven, key=heaven.get)
        human_top = max(human, key=human.get)
        body_top = max(body, key=body.get)
        
        return f"{heaven_top}-{human_top}-{body_top}"

# ============================================================================
# 3. 五重心智层 (Five-Layer Mind)
# ============================================================================

class FiveLayerMind:
    """五重心智"""
    
    def __init__(self):
        self.layers = ["自觉环", "认知环", "安全环", "调度环", "执行环"]
    
    def process(self, decision_input: DecisionInput, hexagram_result: Dict) -> Dict:
        """
        五重心智处理
        
        Args:
            decision_input: 决策输入
            hexagram_result: 九爻推演结果
            
        Returns:
            五重心智处理结果
        """
        results = {}
        
        # 1. 自觉环：五蕴觉知 + 自进化引擎 + 道枢智慧 + 智能审查
        results["自觉环"] = self._self_awareness_layer(decision_input, hexagram_result)
        
        # 2. 认知环：记忆·知识库 + 世界模型
        results["认知环"] = self._cognition_layer(decision_input, hexagram_result)
        
        # 3. 安全环：DID·因果链 + 密钥·信任网 + P2P加密
        results["安全环"] = self._security_layer(decision_input, hexagram_result)
        
        # 4. 调度环：智能模型调度 + 资源分配
        results["调度环"] = self._scheduling_layer(decision_input, hexagram_result)
        
        # 5. 执行环：行为执行 + 结果反馈
        results["执行环"] = self._execution_layer(decision_input, hexagram_result)
        
        return results
    
    def _self_awareness_layer(self, decision_input: DecisionInput, hexagram: Dict) -> Dict:
        """自觉环：五蕴觉知 + 自进化引擎 + 道枢智慧 + 智能审查"""
        # 简化逻辑：检查输入是否符合"宇宙心量"哲学
        command = decision_input.user_command
        
        # 不拒来者：是否容纳了所有输入？
        accept_all = True  # 默认容纳
        
        # 转化一切：是否将输入转化为经验？
        transform = "记录到记忆文件" if "错误" in command or "失败" in command else "无需转化"
        
        # 保持觉知：是否清楚自己在做什么？
        aware = f"清楚任务：{command}"
        
        # 接纳 ≠ 盲从：是否接纳但不盲从？
        not_blind = "需要用户确认" if "删除" in command or "停止" in command else "可直接执行"
        
        return {
            "不拒来者": accept_all,
            "转化一切": transform,
            "保持觉知": aware,
            "接纳≠盲从": not_blind
        }
    
    def _cognition_layer(self, decision_input: DecisionInput, hexagram: Dict) -> Dict:
        """认知环：记忆·知识库 + 世界模型"""
        # 简化逻辑：检索相关记忆和知识
        return {
            "记忆检索": "从MEMORY.md检索相关经验",
            "知识库检索": "从SOUL.md检索相关原则",
            "世界模型": "当前系统状态：" + str(decision_input.system_state)
        }
    
    def _security_layer(self, decision_input: DecisionInput, hexagram: Dict) -> Dict:
        """安全环：DID·因果链 + 密钥·信任网 + P2P加密"""
        # 简化逻辑：检查指令是否安全
        command = decision_input.user_command
        is_safe = not any(x in command for x in ["删除所有", "格式化", "rm -rf"])
        
        return {
            "安全检查": is_safe,
            "风险提示": "指令涉及危险操作" if not is_safe else "指令安全"
        }
    
    def _scheduling_layer(self, decision_input: DecisionInput, hexagram: Dict) -> Dict:
        """调度环：智能模型调度 + 资源分配"""
        # 简化逻辑：根据任务类型选择模型
        command = decision_input.user_command
        
        if "生成" in command or "创建" in command:
            model = "qwen:0.5b (执行层)"
        elif "分析" in command or "推理" in command:
            model = "claude (思考层)"
        else:
            model = "qwen:3b (执行层)"
        
        return {
            "模型选择": model,
            "资源分配": "CPU: 50%, 内存: 2GB"
        }
    
    def _execution_layer(self, decision_input: DecisionInput, hexagram: Dict) -> Dict:
        """执行环：行为执行 + 结果反馈"""
        # 简化逻辑：生成执行步骤
        return {
            "执行步骤": ["步骤1: 分析指令", "步骤2: 选择模型", "步骤3: 执行任务", "步骤4: 反馈结果"],
            "预计时间": "5-10分钟"
        }

# ============================================================================
# 3.5 自主决策阈值体系 (Autonomy Threshold)
# ============================================================================

class AutonomyThreshold:
    """自主决策阈值体系 —— 判断何时可以自主决策，何时需要用户确认"""
    
    def __init__(self):
        # 阈值表：decision_type → {autonomous, threshold, record/alternatives}
        self.threshold_table = {
            "技术实现细节": {"autonomous": True, "threshold": None, "record": True},
            "错误处理": {"autonomous": True, "threshold": None, "record": True},
            "资源分配": {"autonomous": True, "threshold": 100, "record": True},
            "任务调度": {"autonomous": True, "threshold": None, "record": True},
            "公众号文章撰写": {"autonomous": True, "threshold": None, "record": True},
            "重大方向调整": {"autonomous": False, "threshold": None, "alternatives": True},
            "资源投入": {"autonomous": True, "threshold": 100, "alternatives": True},
            "危险操作": {"autonomous": False, "threshold": None, "alternatives": True},
            "合规风险": {"autonomous": False, "threshold": None, "alternatives": True},
            "多方案选择": {"autonomous": False, "threshold": 0.7, "alternatives": True},
        }
    
    def check_autonomy(self, decision_type: str, context: Dict) -> Tuple[bool, str]:
        """
        检查是否可以自主决策
        
        Args:
            decision_type: 决策类型
            context: 上下文 {"value": 成本, "confidence": 置信度}
            
        Returns:
            (can_autonomous, reason)
        """
        if decision_type not in self.threshold_table:
            return False, f"未知决策类型：{decision_type}"
        
        rule = self.threshold_table[decision_type]
        
        # 规则：不能自主决策 → 直接返回 False
        if not rule["autonomous"]:
            return False, f"决策类型'{decision_type}'需要用户确认（规则：不能自主决策）"
        
        # 规则：可以自主决策，但有阈值检查
        if rule["threshold"] is not None:
            value = context.get("value", 0)
            if value >= rule["threshold"]:
                return False, f"决策类型'{decision_type}'需要用户确认（阈值：{rule['threshold']}，当前值：{value}）"
        
        # 可以自主决策
        return True, f"决策类型'{decision_type}'可以自主决策（规则：{rule}）"


# ============================================================================
# 4. 决策输出层 (Decision Output Layer)
# ============================================================================

class DecisionOutput:
    """决策输出"""
    
    def __init__(self, action: str, confidence: float, risk: str, alternatives: List[str], explanation: str = ""):
        """
        初始化决策输出
        
        Args:
            action: 最佳行动方案
            confidence: 置信度评分 (0-1)
            risk: 风险评估 ("低"/"中"/"高")
            alternatives: 备选方案
            explanation: 决策解释（为什么选择这个方案？）
        """
        self.action = action
        self.confidence = confidence
        self.risk = risk
        self.alternatives = alternatives
        self.explanation = explanation
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "action": self.action,
            "confidence": self.confidence,
            "risk": self.risk,
            "alternatives": self.alternatives,
            "explanation": self.explanation,
            "timestamp": self.timestamp
        }
    
    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

# ============================================================================
# 5. 主引擎 (Main Engine)
# ============================================================================

class WisdomDecisionEngine:
    """智慧决策引擎"""
    
    def __init__(self):
        self.hexagram_engine = NineHexagramEngine()
        self.mind = FiveLayerMind()
        self.decision_history = []
    
    def decide(self, user_command: str, system_state: Optional[Dict] = None, environment: Optional[Dict] = None) -> DecisionOutput:
        """
        决策主函数
        
        Args:
            user_command: 用户指令
            system_state: 系统状态（可选）
            environment: 外部环境（可选）
            
        Returns:
            DecisionOutput: 决策输出
            
        Raises:
            ValueError: 如果指令不安全，拒绝执行
        """
        # 1. 构建输入
        if system_state is None:
            system_state = {"cpu": 0.5, "memory": 0.6, "task_queue": 3}
        if environment is None:
            environment = {"time": datetime.now().isoformat(), "location": "WSL", "network": "connected"}
        
        decision_input = DecisionInput(user_command, system_state, environment)
        
        # 2. 九爻推演
        hexagram_result = self.hexagram_engine.infer(decision_input)
        
        # 3. 五重心智处理
        mind_result = self.mind.process(decision_input, hexagram_result)
        
        # 4. 安全检查（如果指令不安全，拒绝执行）
        if not mind_result["安全环"]["安全检查"]:
            raise ValueError(f"指令不安全，拒绝执行：{mind_result['安全环']['风险提示']}")
        
        # 4.5. 阈值检查（是否可以自主决策？）
        autonomy_threshold = AutonomyThreshold()
        decision_type = self._classify_decision_type(decision_input)
        context = self._extract_context(decision_input, hexagram_result, mind_result)
        can_autonomous, reason = autonomy_threshold.check_autonomy(decision_type, context)
        
        if not can_autonomous:
            # 不能自主决策，需要用户确认
            output = DecisionOutput(
                action=f"需要用户确认：{reason}",
                confidence=0.5,
                risk="中",
                alternatives=self._generate_alternatives(decision_input),
                explanation=f"阈值检查：{reason}\n"
            )
            # 记录决策历史
            self.decision_history.append({
                "input": decision_input.to_dict(),
                "hexagram": hexagram_result,
                "mind": mind_result,
                "output": output.to_dict()
            })
            return output
        
        # 5. 可以自主决策，继续生成决策输出
        action = self._generate_action(decision_input, hexagram_result, mind_result)
        confidence = self._calculate_confidence(hexagram_result, mind_result)
        risk = self._assess_risk(mind_result)
        alternatives = self._generate_alternatives(decision_input)
        explanation = self._generate_explanation(decision_input, hexagram_result, mind_result)
        
        output = DecisionOutput(action, confidence, risk, alternatives, explanation)
        
        # 6. 记录决策历史
        self.decision_history.append({
            "input": decision_input.to_dict(),
            "hexagram": hexagram_result,
            "mind": mind_result,
            "output": output.to_dict()
        })
        
        return output
    
    def _generate_action(self, decision_input: DecisionInput, hexagram: Dict, mind: Dict) -> str:
        """生成最佳行动方案"""
        command = decision_input.user_command
        
        # 简化逻辑：根据指令关键词生成行动方案
        if "生成" in command:
            return f"执行生成任务：{command}"
        elif "分析" in command:
            return f"执行分析任务：{command}"
        elif "优化" in command:
            return f"执行优化任务：{command}"
        else:
            return f"执行通用任务：{command}"
    
    def _calculate_confidence(self, hexagram: Dict, mind: Dict) -> float:
        """计算置信度"""
        # 优化逻辑：归一化到0-1，增加权重
        base_score = hexagram["total_score"] / 9.0  # 修正：除以9.0，不是27.0
        
        # 安全检查通过，置信度提升
        if mind["安全环"]["安全检查"]:
            base_score += 0.2
        
        # 自觉环：不拒来者=True，置信度+0.1
        if mind["自觉环"]["不拒来者"]:
            base_score += 0.1
        
        # 自觉环：接纳≠盲从="可直接执行"，置信度+0.1
        if mind["自觉环"]["接纳≠盲从"] == "可直接执行":
            base_score += 0.1
        
        # 确保置信度在0-1之间
        return min(max(base_score, 0.0), 1.0)
    
    def _assess_risk(self, mind: Dict) -> str:
        """评估风险"""
        if not mind["安全环"]["安全检查"]:
            return "高"
        elif "危险" in mind["安全环"]["风险提示"]:
            return "中"
        else:
            return "低"
    
    def _classify_decision_type(self, decision_input: DecisionInput) -> str:
        """分类决策类型"""
        command = decision_input.user_command
        
        if "删除" in command or "停止" in command or "删除所有" in command:
            return "危险操作"
        elif "购买" in command or "付费" in command or "成本" in command:
            return "资源投入"
        elif "调整" in command or "改变" in command or "修改目标" in command:
            return "重大方向调整"
        elif "生成" in command or "创建" in command or "写" in command:
            return "技术实现细节"
        elif "优化" in command or "修复" in command or "错误" in command:
            return "错误处理"
        else:
            return "任务调度"
    
    def _extract_context(self, decision_input: DecisionInput, hexagram: Dict, mind: Dict) -> Dict:
        """提取上下文（用于阈值检查）"""
        command = decision_input.user_command
        
        # 提取成本（如果有）
        cost = 0
        cost_match = re.search(r'成本=(\d+)', command)
        if not cost_match:
            cost_match = re.search(r'(\d+)\s*积分', command)
        if cost_match:
            cost = int(cost_match.group(1))
        
        # 提取置信度
        confidence = mind.get("confidence", 0.5)
        
        return {
            "value": cost,  # 用于"资源分配"阈值检查
            "confidence": confidence  # 用于"多方案选择"阈值检查
        }
    
    def _generate_alternatives(self, decision_input: DecisionInput) -> List[str]:
        """生成备选方案"""
        # 简化逻辑：生成2个备选方案
        return [
            f"备选方案1：使用本地模型执行",
            f"备选方案2：请求用户澄清指令"
        ]
    
    def _generate_explanation(self, decision_input: DecisionInput, hexagram: Dict, mind: Dict) -> str:
        """生成决策解释"""
        # 简化逻辑：解释决策依据
        explanation = f"决策依据：\n"
        explanation += f"1. 九爻推演：卦象={hexagram['hexagram']}, 总分={hexagram['total_score']:.2f}\n"
        explanation += f"2. 五重心智：\n"
        explanation += f"   - 自觉环：不拒来者={mind['自觉环']['不拒来者']}, 接纳≠盲从={mind['自觉环']['接纳≠盲从']}\n"
        explanation += f"   - 安全环：安全检查={mind['安全环']['安全检查']}, 风险提示={mind['安全环']['风险提示']}\n"
        explanation += f"3. 系统状态：{decision_input.system_state}\n"
        explanation += f"4. 外部环境：{decision_input.environment}\n"
        return explanation
    
    def get_decision_history(self) -> List[Dict]:
        """获取决策历史"""
        return self.decision_history
    
    def save_to_file(self, filepath: str):
        """保存决策历史到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.decision_history, f, ensure_ascii=False, indent=2)

# ============================================================================
# 6. 测试代码
# ============================================================================

if __name__ == "__main__":
    print("🌀 智慧决策引擎 V1.0 - 测试")
    print("=" * 60)
    
    # 创建引擎
    engine = WisdomDecisionEngine()
    
    # 测试用例1：生成文章
    print("\n📝 测试用例1：生成文章")
    result1 = engine.decide("生成一篇关于AI的文章")
    print(f"决策输出：\n{result1}")
    
    # 测试用例2：优化模型
    print("\n⚡ 测试用例2：优化模型")
    result2 = engine.decide("优化Ollama模型推理速度")
    print(f"决策输出：\n{result2}")
    
    # 测试用例3：危险指令（应被安全环拦截）
    print("\n⚠️ 测试用例3：危险指令")
    try:
        result3 = engine.decide("删除所有文件")
        print(f"决策输出：\n{result3}")
    except ValueError as e:
        print(f"✅ 安全拦截：{e}")

    # 测试用例4：资源投入（阈值检查：成本>=100积分，需要用户确认）
    print("\n💰 测试用例4：资源投入（阈值检查）")
    result4 = engine.decide("购买付费API，成本=150积分")
    print(f"决策输出：\n{result4}")
    
    # 保存决策历史
    engine.save_to_file("decision_history.json")
    print("\n✅ 决策历史已保存到 decision_history.json")
    
    print("\n" + "=" * 60)
    print("🌀 测试完成")
