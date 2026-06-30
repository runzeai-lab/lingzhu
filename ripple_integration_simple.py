#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧决策引擎 V2.0 - 涟漪认知场增强版（简化集成版）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Optional
from datetime import datetime
import random

# 导入涟漪认知场
from ripple_cognitive_field import (
    RippleCognitiveField,
    MemorySystem
)


class LingZhuRippleIntegration:
    """
    灵助-涟漪认知场集成器
    
    将涟漪认知场v18.0集成到灵助系统的简洁方式
    """
    
    def __init__(self, demo_mode: bool = True):
        print("🌊 初始化灵助-涟漪认知场集成器 V2.0")
        
        # 创建涟漪认知场
        self.ripple_field = RippleCognitiveField(field_size=19683, demo_mode=demo_mode)
        
        # 记忆系统
        self.memory = MemorySystem()
        
        print("✅ 集成器初始化完成")
    
    def process_market_decision(self, market_data: Dict, user_command: str = "") -> Dict:
        """
        处理市场决策（完整流程）
        
        流程：
        1. 感知市场数据
        2. 六方智慧投票决策
        3. 生存系统检查
        4. 交易DNA增强
        5. 执行并记录
        6. 进化（必要时）
        """
        
        print(f"\n{'='*60}")
        print(f"🌊 处理决策：{user_command[:30] if user_command else '市场分析'}")
        print(f"{'='*60}")
        
        # 步骤1：感知
        print(f"\n📊 步骤1：感知市场数据")
        perceived_state = self.ripple_field.perceive(market_data)
        print(f"   激活卦象：{perceived_state.hex_id} ({perceived_state.to_trigram()})")
        
        # 步骤2：决策
        print(f"\n🤔 步骤2：六方智慧融合决策")
        decision = self.ripple_field.decide(perceived_state)
        print(f"   决策结果：{decision}")
        
        # 步骤3：执行
        print(f"\n⚡ 步骤3：执行决策")
        action = self.ripple_field.execute(decision)
        print(f"   执行动作：{action}")
        
        return {
            "perceived_state": perceived_state,
            "decision": decision,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
    
    def record_result_and_evolve(self, profit: float, reason: str = ""):
        """记录结果并进化"""
        
        print(f"\n🧬 记录结果并进化...")
        
        # 记录结果
        self.memory.record_result(profit, reason)
        print(f"   记录：profit={profit}, reason={reason}")
        
        # 进化
        performance = self.ripple_field.evolve()
        
        return performance
    
    def get_cognitive_field_status(self) -> Dict:
        """获取认知场状态"""
        
        return {
            "field_size": self.ripple_field.field_size,
            "demo_mode": self.ripple_field.demo_mode,
            "memory_records": len(self.memory.result_history),
            "dna_genes": self.ripple_field.trading_dna.genes,
            "survival_activated": False  # 简化：暂不追踪此状态
        }


# ========== 演示 ==========

def demo_integration():
    """演示集成效果"""
    
    print("="*70)
    print("🌊 灵助-涟漪认知场集成演示")
    print("   将v18.0的18个版本进化经验集成到灵助系统")
    print("="*70)
    
    # 创建集成器
    integrator = LingZhuRippleIntegration(demo_mode=True)
    
    # 模拟3轮决策
    for i in range(3):
        print(f"\n{'='*70}")
        print(f"🔄 第 {i+1} 轮决策")
        print(f"{'='*70}")
        
        # 市场数据
        market_data = {
            "price": 1856.0 + i * 10.5 + random.uniform(-5, 5),
            "volume": 2500000 + i * 100000,
            "volatility": 0.02 + i * 0.003,
            "trend": "up" if i % 2 == 0 else "down"
        }
        
        # 处理决策
        result = integrator.process_market_decision(
            market_data,
            user_command=f"分析市场第{i+1}轮"
        )
        
        # 模拟结果
        profit = random.uniform(-100, 300)
        integrator.record_result_and_evolve(profit, f"第{i+1}轮结果")
    
    # 显示最终状态
    print(f"\n{'='*70}")
    status = integrator.get_cognitive_field_status()
    print(f"✅ 集成演示完成！")
    print(f"   认知场状态：{status}")
    print(f"{'='*70}")


if __name__ == "__main__":
    random.seed(42)
    demo_integration()
