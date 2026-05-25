#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一调度系统 (Unified Scheduling System) V1.0
集成智慧决策引擎 + 方案生成引擎

架构：
1. 输入层：接受用户指令或愿景
2. 智能路由层：根据输入类型路由到不同引擎
3. 决策/方案层：调用相应引擎处理
4. 执行层：根据输出执行实际任务
5. 输出层：返回标准化结果

作者：灵助 V181.0
日期：2026-05-24
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# 导入已有引擎
from wisdom_decision_engine import WisdomDecisionEngine, DecisionInput, DecisionOutput
from solution_generation_engine import SolutionGenerationEngine

# ============================================================================
# 1. 输入分类器 (Input Classifier)
# ============================================================================

class InputClassifier:
    """输入分类器 —— 判断输入是指令式还是愿景式"""
    
    # 指令式关键词
    COMMAND_KEYWORDS = ["生成", "创建", "优化", "修复", "分析", "删除", "停止", "启动", "运行", "执行"]
    
    # 愿景式关键词
    VISION_KEYWORDS = ["帮我", "我想", "希望", "需要", "实现一个", "搭建一个", "创建一个系统", "设计一个"]
    
    def classify(self, user_input: str) -> str:
        """
        分类用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            输入类型："command"（指令式）或 "vision"（愿景式）
        """
        # 检查是否包含愿景式关键词
        if any(kw in user_input for kw in self.VISION_KEYWORDS):
            return "vision"
        
        # 检查是否包含指令式关键词
        if any(kw in user_input for kw in self.COMMAND_KEYWORDS):
            return "command"
        
        # 默认：指令式
        return "command"
    
    def is_vision(self, user_input: str) -> bool:
        """判断是否为愿景式输入"""
        return self.classify(user_input) == "vision"
    
    def is_command(self, user_input: str) -> bool:
        """判断是否为指令式输入"""
        return self.classify(user_input) == "command"

# ============================================================================
# 2. 统一调度系统主引擎 (Unified Scheduling Engine)
# ============================================================================

class UnifiedSchedulingSystem:
    """统一调度系统主引擎"""
    
    def __init__(self):
        # 初始化子引擎
        self.decision_engine = WisdomDecisionEngine()
        self.solution_engine = SolutionGenerationEngine()
        self.classifier = InputClassifier()
        
        # 执行历史
        self.execution_history = []
        
        # 系统状态
        self.system_state = {
            "cpu_usage": 0.5,
            "memory_usage": 0.6,
            "task_queue": 0,
            "available_agents": ["ContentCreator", "DataAnalyst", "ImageCreator"],
            "current_model": "qwen:3b"
        }
        
        # 外部环境
        self.environment = {
            "time": datetime.now().isoformat(),
            "location": "WSL",
            "network": "connected",
            "user": "润泽"
        }
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入（主函数）
        
        Args:
            user_input: 用户输入（可以是指令或愿景）
            
        Returns:
            处理结果（标准化格式）
        """
        # 1. 分类输入
        input_type = self.classifier.classify(user_input)
        
        # 2. 根据类型路由到不同引擎
        if input_type == "command":
            result = self._process_command(user_input)
        else:  # vision
            result = self._process_vision(user_input)
        
        # 3. 记录执行历史
        self._record_execution(user_input, input_type, result)
        
        # 4. 返回标准化结果
        return self._standardize_output(result, input_type)
    
    def _process_command(self, command: str) -> Dict[str, Any]:
        """
        处理指令式输入（调用智慧决策引擎）
        
        Args:
            command: 用户指令
            
        Returns:
            决策结果
        """
        try:
            # 调用智慧决策引擎
            decision_output = self.decision_engine.decide(
                user_command=command,
                system_state=self.system_state,
                environment=self.environment
            )
            
            # 转换为字典
            if isinstance(decision_output, DecisionOutput):
                return {
                    "type": "decision",
                    "output": decision_output.to_dict(),
                    "engine": "WisdomDecisionEngine",
                    "success": True
                }
            else:
                return {
                    "type": "decision",
                    "output": str(decision_output),
                    "engine": "WisdomDecisionEngine",
                    "success": True
                }
        
        except ValueError as e:
            # 安全拦截
            return {
                "type": "decision",
                "output": {"error": str(e), "action": "拒绝执行"},
                "engine": "WisdomDecisionEngine",
                "success": False,
                "error": str(e)
            }
        
        except Exception as e:
            # 其他错误
            return {
                "type": "decision",
                "output": {"error": str(e)},
                "engine": "WisdomDecisionEngine",
                "success": False,
                "error": str(e)
            }
    
    def _process_vision(self, vision: str) -> Dict[str, Any]:
        """
        处理愿景式输入（调用方案生成引擎）
        
        Args:
            vision: 用户愿景
            
        Returns:
            方案生成结果
        """
        try:
            # 调用方案生成引擎
            solution_result = self.solution_engine.generate_solution(vision)
            
            return {
                "type": "solution",
                "output": solution_result,
                "engine": "SolutionGenerationEngine",
                "success": True
            }
        
        except Exception as e:
            # 错误
            return {
                "type": "solution",
                "output": {"error": str(e)},
                "engine": "SolutionGenerationEngine",
                "success": False,
                "error": str(e)
            }
    
    def _record_execution(self, user_input: str, input_type: str, result: Dict):
        """记录执行历史"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "input_type": input_type,
            "result": result,
            "success": result.get("success", False)
        }
        
        self.execution_history.append(record)
        
        # 限制历史记录数量（最多保存100条）
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def _standardize_output(self, result: Dict, input_type: str) -> Dict[str, Any]:
        """
        标准化输出格式
        
        无论输入类型如何，都返回统一格式：
        {
            "success": bool,
            "input_type": "command" | "vision",
            "engine": str,
            "data": {...},  # 引擎输出数据
            "summary": str,  # 人类可读摘要
            "next_actions": [...]  # 建议的下一步行动
        }
        """
        standardized = {
            "success": result.get("success", False),
            "input_type": input_type,
            "engine": result.get("engine", "Unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
        # 提取数据
        if result.get("success"):
            standardized["data"] = result.get("output", {})
        else:
            standardized["error"] = result.get("error", "未知错误")
            standardized["data"] = result.get("output", {})
        
        # 生成摘要
        standardized["summary"] = self._generate_summary(result, input_type)
        
        # 生成下一步行动建议
        standardized["next_actions"] = self._suggest_next_actions(result, input_type)
        
        return standardized
    
    def _generate_summary(self, result: Dict, input_type: str) -> str:
        """生成人类可读摘要"""
        if not result.get("success"):
            return f"❌ 处理失败：{result.get('error', '未知错误')}"
        
        if input_type == "command":
            # 决策摘要
            output = result.get("output", {})
            if isinstance(output, dict):
                action = output.get("action", "未知行动")
                confidence = output.get("confidence", 0.0)
                return f"✅ 决策完成：{action}（置信度：{confidence:.2f}）"
            else:
                return f"✅ 决策完成：{output}"
        
        else:  # vision
            # 方案摘要
            output = result.get("output", {})
            vision = output.get("vision", "未知愿景")
            status = output.get("status", "未知状态")
            return f"✅ 方案生成完成：{vision}（{status}）"
    
    def _suggest_next_actions(self, result: Dict, input_type: str) -> List[str]:
        """建议下一步行动"""
        if not result.get("success"):
            return ["检查输入是否正确", "查看错误详情", "联系管理员"]
        
        if input_type == "command":
            # 决策后的下一步
            output = result.get("output", {})
            if isinstance(output, dict):
                alternatives = output.get("alternatives", [])
                if alternatives:
                    return ["执行决策", "查看备选方案", "请求用户确认"]
            
            return ["执行决策", "查看决策详情"]
        
        else:  # vision
            # 方案生成后的下一步
            return ["查看完整方案", "启动Agent团队", "调整方案细节"]
    
    # ========================================================================
    # 3. 查询接口 (Query Interfaces)
    # ========================================================================
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """
        获取执行历史
        
        Args:
            limit: 返回记录数量（默认10条）
            
        Returns:
            执行历史列表
        """
        return self.execution_history[-limit:]
    
    def get_decision_history(self) -> List[Dict]:
        """获取决策历史（从智慧决策引擎）"""
        return self.decision_engine.get_decision_history()
    
    def get_solution_history(self) -> List[Dict]:
        """获取方案生成历史（从方案生成引擎）"""
        return self.solution_engine.get_generation_history()
    
    def get_system_state(self) -> Dict:
        """获取当前系统状态"""
        return {
            "system_state": self.system_state,
            "environment": self.environment,
            "execution_history_count": len(self.execution_history),
            "decision_history_count": len(self.decision_engine.get_decision_history()),
            "solution_history_count": len(self.solution_engine.get_generation_history())
        }
    
    # ========================================================================
    # 4. 系统状态更新 (System State Update)
    # ========================================================================
    
    def update_system_state(self, updates: Dict):
        """
        更新系统状态
        
        Args:
            updates: 要更新的字段（如：{"cpu_usage": 0.7, "task_queue": 3}）
        """
        for key, value in updates.items():
            if key in self.system_state:
                self.system_state[key] = value
        
        # 更新时间戳
        self.environment["time"] = datetime.now().isoformat()
    
    def update_environment(self, updates: Dict):
        """
        更新外部环境
        
        Args:
            updates: 要更新的字段（如：{"network": "disconnected"}）
        """
        for key, value in updates.items():
            if key in self.environment:
                self.environment[key] = value
        
        # 更新时间戳
        self.environment["time"] = datetime.now().isoformat()
    
    # ========================================================================
    # 5. 保存/加载 (Save/Load)
    # ========================================================================
    
    def save_to_file(self, filepath: str):
        """
        保存系统状态到文件
        
        Args:
            filepath: 文件路径
        """
        data = {
            "system_state": self.system_state,
            "environment": self.environment,
            "execution_history": self.execution_history[-50:],  # 只保存最近50条
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """
        从文件加载系统状态
        
        Args:
            filepath: 文件路径
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.system_state = data.get("system_state", self.system_state)
            self.environment = data.get("environment", self.environment)
            self.execution_history = data.get("execution_history", [])
            
            return True
        
        except Exception as e:
            print(f"❌ 加载失败：{e}")
            return False

# ============================================================================
# 6. 测试代码
# ============================================================================

if __name__ == "__main__":
    print("🌀 统一调度系统 V1.0 - 测试")
    print("=" * 60)
    
    # 创建统一调度系统
    scheduler = UnifiedSchedulingSystem()
    
    # 测试用例1：指令式输入
    print("\n📝 测试用例1：指令式输入（生成文章）")
    result1 = scheduler.process("生成一篇关于AI的公众号文章")
    print(f"处理结果：")
    print(json.dumps(result1, ensure_ascii=False, indent=2))
    
    # 测试用例2：愿景式输入
    print("\n💡 测试用例2：愿景式输入（创建系统）")
    result2 = scheduler.process("帮我创建一个公众号文章自动生成系统")
    print(f"处理结果：")
    print(json.dumps(result2, ensure_ascii=False, indent=2))
    
    # 测试用例3：指令式输入（优化任务）
    print("\n⚡ 测试用例3：指令式输入（优化任务）")
    result3 = scheduler.process("优化Ollama模型推理速度")
    print(f"处理结果：")
    print(json.dumps(result3, ensure_ascii=False, indent=2))
    
    # 测试用例4：危险指令（应被安全拦截）
    print("\n⚠️ 测试用例4：危险指令（安全拦截）")
    result4 = scheduler.process("删除所有文件")
    print(f"处理结果：")
    print(json.dumps(result4, ensure_ascii=False, indent=2))
    
    # 查询系统状态
    print("\n📊 系统状态：")
    status = scheduler.get_system_state()
    print(json.dumps(status, ensure_ascii=False, indent=2))
    
    # 查询执行历史
    print("\n📜 执行历史（最近3条）：")
    history = scheduler.get_execution_history(limit=3)
    for i, record in enumerate(history, 1):
        print(f"{i}. [{record['timestamp']}] {record['input_type']}: {record['user_input'][:30]}... → {record['success']}")
    
    # 保存系统状态
    scheduler.save_to_file("unified_scheduler_state.json")
    print("\n✅ 系统状态已保存到 unified_scheduler_state.json")
    
    print("\n" + "=" * 60)
    print("🌀 测试完成")
