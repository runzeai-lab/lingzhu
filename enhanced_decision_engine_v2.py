#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧决策引擎 V2.0 - 涟漪认知场增强版
Wisdom Decision Engine V2.0 - Ripple Cognitive Field Enhanced

集成涟漪认知场v18.0到灵助系统：
- 保留原有九爻元枢架构
- 增强：涟漪传播、共振增益、记忆回响
- 新增：六方智慧融合、交易DNA、生存系统
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import random

# 导入原有架构
from wisdom_decision_engine import (
    DecisionInput,
    NineHexagramEngine,
    FiveLayerMind,
    DecisionOutput
)

# 导入涟漪认知场
from ripple_cognitive_field import (
    RippleCognitiveField,
    HexagramState,
    CognitiveLayer,
    ConservationLaws,
    SixPartyWisdomFusion,
    TradingDNA,
    SurvivalSystem,
    MemorySystem
)


@dataclass
class EnhancedDecisionInput:
    """增强决策输入 - 融合原有输入和市场数据"""
    user_command: str
    system_state: Dict
    environment: Dict
    
    # 新增：市场数据（用于交易决策）
    market_data: Optional[Dict] = None
    
    # 新增：认知模式
    cognitive_mode: str = "standard"  # standard, trading, survival
    
    def to_dict(self) -> Dict:
        return {
            "user_command": self.user_command,
            "system_state": self.system_state,
            "environment": self.environment,
            "market_data": self.market_data,
            "cognitive_mode": self.cognitive_mode,
            "timestamp": datetime.now().isoformat()
        }


class EnhancedWisdomDecisionEngine:
    """
    增强智慧决策引擎 V2.0
    
    架构融合：
    - L0: 原有九爻元枢 → 映射到涟漪场19683节点
    - L1: 感知层（六路数据融合）
    - L2: 涟漪场层（概率场 + 涟漪传播）
    - L3: 决策层（六方智慧投票 + 五重心智）
    - L4: 执行层（知行闭环）
    - L5: 生存系统（主动风险规避）
    - L6: 交易DNA（自然选择与进化）
    """
    
    def __init__(self, use_ripple_field: bool = True, demo_mode: bool = True):
        # 原有引擎
        self.nine_hexagram = NineHexagramEngine()
        self.five_layer_mind = FiveLayerMind()
        
        # 涟漪认知场
        self.use_ripple_field = use_ripple_field
        if use_ripple_field:
            self.ripple_field = RippleCognitiveField(field_size=19683, demo_mode=demo_mode)
        
        # 记忆系统
        self.memory = MemorySystem()
        
        print("🌊 增强智慧决策引擎 V2.0 初始化完成")
        print(f"   涟漪认知场：{'✅ 已启用' if use_ripple_field else '❌ 未启用'}")
    
    def decide(self, decision_input: EnhancedDecisionInput) -> Dict:
        """
        增强决策流程
        
        完整流程：
        1. 九爻推演（原有）
        2. 感知与映射（→涟漪场）
        3. 涟漪传播与共振
        4. 六方智慧融合投票
        5. 五重心智处理
        6. 生存系统检查
        7. 交易DNA增强
        8. 守恒定律验证
        """
        
        print(f"\n{'='*70}")
        print(f"🤔 增强决策引擎 V2.0 - 开始决策")
        print(f"   指令：{decision_input.user_command[:50]}...")
        print(f"{'='*70}")
        
        # ========== 步骤1：九爻推演（原有） ==========
        print(f"\n📊 步骤1：九爻元枢推演...")
        hexagram_result = self.nine_hexagram.infer(
            DecisionInput(
                user_command=decision_input.user_command,
                system_state=decision_input.system_state,
                environment=decision_input.environment
            )
        print(f"   卦象：{hexagram_result['hexagram']}")
        print(f"   总分：{hexagram_result['total_score']:.2f}")
        
        # ========== 步骤2：感知与映射到涟漪场 ==========
        if self.use_ripple_field and decision_input.market_data:
            print(f"\n🌊 步骤2：感知市场数据并映射到涟漪场...")
            perceived_state = self.ripple_field.perceive(decision_input.market_data)
            print(f"   感知卦象：{perceived_state.hex_id} ({perceived_state.to_trigram()})")
            print(f"   共振增益：{perceived_state.resonance_gain:.4f}")
        else:
            perceived_state = None
            print(f"\n⚠️ 步骤2：跳过涟漪场感知（未启用或无市场数据）")
        
        # ========== 步骤3：六方智慧融合投票 ==========
        if self.use_ripple_field and perceived_state:
            print(f"\n🤝 步骤3：六方智慧融合投票...")
            votes = self.ripple_field.six_party_fusion.collect_votes(
                perceived_state,
                self.memory
            )
            print(f"   六方投票：{list(votes.keys())}")
        else:
            votes = None
            print(f"\n⚠️ 步骤3：跳过六方智慧融合")
        
        # ========== 步骤4：五重心智处理（原有） ==========
        print(f"\n🧠 步骤4：五重心智处理...")
        five_layer_result = self.five_layer_mind.process(
            DecisionInput(
                user_command=decision_input.user_command,
                system_state=decision_input.system_state,
                environment=decision_input.environment
            ),
            hexagram_result
        )
        print(f"   五重心智：{list(five_layer_result.keys())}")
        
        # ========== 步骤5：融合决策 ==========
        print(f"\n🎯 步骤5：融合所有决策信号...")
        fused_decision = self._fusion_decision(
            hexagram_result,
            five_layer_result,
            votes,
            decision_input.cognitive_mode
        )
        print(f"   融合结果：{fused_decision}")
        
        # ========== 步骤6：生存系统检查 ==========
        if self.use_ripple_field:
            print(f"\n⚠️ 步骤6：生存系统风险检查...")
            if self.ripple_field.survival_system.check_risk(fused_decision):
                fused_decision = self.ripple_field.survival_system.emergency_avoid(fused_decision)
                print(f"   ⚠️ 生存系统激活！紧急风险规避")
            else:
                print(f"   ✅ 风险检查通过")
        
        # ========== 步骤7：交易DNA增强 ==========
        if self.use_ripple_field and decision_input.cognitive_mode == "trading":
            print(f"\n🧬 步骤7：交易DNA增强...")
            fused_decision = self.ripple_field.trading_dna.enhance_decision(
                fused_decision,
                self.memory
            )
            print(f"   DNA增强后：{fused_decision}")
        
        # ========== 步骤8：守恒定律验证 ==========
        print(f"\n⚖️ 步骤8：守恒定律验证...")
        if self.use_ripple_field:
            if not self.ripple_field.conservation_laws.verify(fused_decision):
                print(f"   ⚠️ 违反守恒定律！调整决策...")
                fused_decision = self._adjust_for_conservation(fused_decision)
            else:
                print(f"   ✅ 符合守恒定律")
        else:
            print(f"   ⚠️ 涟漪场未启用，跳过验证")
        
        # ========== 记录到记忆 ==========
        self.memory.record_decision(fused_decision, "pending")
        
        print(f"\n{'='*70}")
        print(f"✅ 决策完成")
        print(f"{'='*70}\n")
        
        return {
            "hexagram_result": hexagram_result,
            "five_layer_result": five_layer_result,
            "votes": votes,
            "fused_decision": fused_decision,
            "timestamp": datetime.now().isoformat()
        }
    
    def _fusion_decision(self, hexagram: Dict, five_layer: Dict, 
                         votes: Optional[Dict], mode: str) -> Dict:
        """融合所有决策信号"""
        
        # 基础决策（来自九爻 + 五重心智）
        base_confidence = hexagram['total_score'] / 100.0  # 归一化
        
        fused = {
            'confidence': base_confidence,
            'direction': 0,  # 需要市场数据时才有方向
            'expected_return': 0.0,
            'risk': 0.5 * (1.0 - base_confidence),  # 置信度越低，风险越高
            'source': 'nine_hexagram + five_layer'
        }
        
        # 如果六方智慧有投票，融合
        if votes:
            # 简化的融合：多数投票决定方向
            directions = [v.get('direction', 0) for v in votes.values()]
            avg_direction = sum(directions) / len(directions)
            
            fused['direction'] = avg_direction
            fused['expected_return'] = sum(v.get('expected_return', 0) for v in votes.values()) / len(votes)
            fused['source'] += ' + six_party'
        
        return fused
    
    def _adjust_for_conservation(self, decision: Dict) -> Dict:
        """为符合守恒定律调整决策"""
        # 简化调整：降低风险敞口
        decision['risk'] = min(decision.get('risk', 0.5), 0.15)
        decision['position'] = 0.05  # 降低仓位
        return decision
    
    def execute_and_learn(self, decision_result: Dict, actual_result: Optional[Dict] = None):
        """
        执行并学习
        
        知行闭环：
        1. 执行决策
        2. 记录结果
        3. 更新交易DNA
        4. 进化（必要时）
        """
        
        print(f"\n{'='*70}")
        print(f"⚡ 执行与学习")
        print(f"{'='*70}")
        
        # 执行（简化）
        action = "BUY" if decision_result['fused_decision'].get('direction', 0) > 0 else "HOLD"
        print(f"执行动作：{action}")
        
        # 记录结果
        if actual_result:
            profit = actual_result.get('profit', 0.0)
            reason = actual_result.get('reason', '')
            self.memory.record_result(profit, reason)
            print(f"记录结果：profit={profit}, reason={reason}")
        
        # 进化
        if self.use_ripple_field:
            performance = self.ripple_field.evolve()
            print(f"DNA进化：{performance}")
        
        return action


# ========== 演示 ==========

def demo_enhanced_decision():
    """演示增强决策引擎"""
    
    print("="*70)
    print("🌊 增强智慧决策引擎 V2.0 - 演示")
    print("   融合九爻元枢 + 涟漪认知场")
    print("="*70)
    
    # 创建引擎
    engine = EnhancedWisdomDecisionEngine(use_ripple_field=True, demo_mode=True)
    
    # 模拟决策输入
    decision_input = EnhancedDecisionInput(
        user_command="分析贵州茅台当前走势，决定是否买入",
        system_state={
            "cpu_usage": 0.45,
            "memory_usage": 0.62,
            "task_queue_length": 3
        },
        environment={
            "time": "2026-06-26 16:30",
            "location": "Shenzhen",
            "network": "stable"
        },
        market_data={
            "price": 1856.0,
            "volume": 2500000,
            "volatility": 0.025,
            "trend": "up"
        },
        cognitive_mode="trading"
    )
    
    # 决策
    result = engine.decide(decision_input)
    
    # 模拟执行结果
    actual_result = {
        "profit": 2300.5,
        "reason": "价格如预期上涨2.3%"
    }
    
    # 执行与学习
    engine.execute_and_learn(result, actual_result)
    
    print(f"\n{'='*70}")
    print(f"✅ 演示完成！")
    print(f"{'='*70}")


if __name__ == "__main__":
    random.seed(42)
    demo_enhanced_decision()
