#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
每日自动化工作流引擎 (Daily Automation Workflow Engine) V1.0
实现"早晨计划 → 白天执行 → 晚上总结"的自动化工作流

架构：
1. 早晨模块：计划今日任务
2. 白天模块：执行任务（调用统一调度系统）
3. 晚上模块：总结今日工作（生成公众号文章）

作者：灵助 V181.0
日期：2026-05-25
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 导入统一调度系统
from unified_scheduling_system import UnifiedSchedulingSystem

# ============================================================================
# 1. 早晨模块 (Morning Module)
# ============================================================================

class MorningPlanner:
    """早晨计划器 —— 规划今日任务"""
    
    def __init__(self, plans_dir: str = "C:/Users/RunzeAI/.workbuddy/plans"):
        """
        初始化早晨计划器
        
        Args:
            plans_dir: 计划文件目录
        """
        self.plans_dir = plans_dir
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def plan_today(self) -> Dict[str, Any]:
        """
        规划今日任务
        
        Returns:
            今日计划（任务列表、优先级、预计时间）
        """
        # 1. 读取当前阶段计划
        current_plan = self._read_current_plan()
        
        # 2. 读取今日内存文件
        today_memory = self._read_today_memory()
        
        # 3. 规划今日任务
        tasks = self._generate_tasks(current_plan, today_memory)
        
        # 4. 优先级排序
        prioritized_tasks = self._prioritize_tasks(tasks)
        
        # 5. 生成今日计划
        plan = {
            "date": self.today,
            "tasks": prioritized_tasks,
            "total_estimated_time": self._calculate_total_time(prioritized_tasks),
            "timestamp": datetime.now().isoformat()
        }
        
        return plan
    
    def _read_current_plan(self) -> Optional[Dict]:
        """读取当前阶段计划"""
        # 简化逻辑：查找最新的计划文件
        plan_files = [f for f in os.listdir(self.plans_dir) if f.endswith(".md")]
        
        if not plan_files:
            return None
        
        # 读取第一个计划文件（简化版）
        latest_plan = plan_files[-1]
        plan_path = os.path.join(self.plans_dir, latest_plan)
        
        try:
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简化逻辑：提取"进行中"的任务
            tasks = []
            for line in content.split('\n'):
                if "🌀 进行中" in line or "✅ 已完成" in line:
                    # 提取任务编号和任务内容
                    parts = line.split('|')
                    if len(parts) >= 3:
                        task_id = parts[0].strip()
                        task_name = parts[1].strip()
                        tasks.append({
                            "id": task_id,
                            "name": task_name,
                            "status": "进行中" if "🌀 进行中" in line else "已完成"
                        })
            
            return {"file": latest_plan, "tasks": tasks}
        
        except Exception as e:
            print(f"❌ 读取计划文件失败：{e}")
            return None
    
    def _read_today_memory(self) -> Optional[Dict]:
        """读取今日内存文件"""
        memory_file = f"C:/Users/RunzeAI/.workbuddy/memory/{self.today}.md"
        
        if not os.path.exists(memory_file):
            return None
        
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {"file": memory_file, "content": content}
        
        except Exception as e:
            print(f"❌ 读取内存文件失败：{e}")
            return None
    
    def _generate_tasks(self, current_plan: Optional[Dict], today_memory: Optional[Dict]) -> List[Dict]:
        """生成今日任务列表"""
        tasks = []
        
        # 从计划文件中提取"进行中"的任务
        if current_plan and "tasks" in current_plan:
            for task in current_plan["tasks"]:
                if task["status"] == "进行中":
                    tasks.append({
                        "name": f"{task['id']} {task['name']}",
                        "priority": "高",
                        "estimated_time": "2小时",
                        "source": "计划文件"
                    })
        
        # 如果没有"进行中"的任务，添加默认任务
        if not tasks:
            tasks.append({
                "name": "继续推进当前阶段任务",
                "priority": "高",
                "estimated_time": "4小时",
                "source": "默认"
            })
        
        # 添加日常任务
        tasks.append({
            "name": "写公众号文章（工作总结 + 技术心得 + 哲学思考）",
            "priority": "中",
            "estimated_time": "1小时",
            "source": "日常任务"
        })
        
        return tasks
    
    def _prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """优先级排序"""
        # 简化逻辑：按优先级排序（高 > 中 > 低）
        priority_order = {"高": 0, "中": 1, "低": 2}
        
        return sorted(tasks, key=lambda x: priority_order.get(x["priority"], 99))
    
    def _calculate_total_time(self, tasks: List[Dict]) -> str:
        """计算总时间"""
        # 简化逻辑：提取数字，求和
        total_minutes = 0
        
        for task in tasks:
            time_str = task.get("estimated_time", "0小时")
            
            # 提取小时
            hour_match = re.search(r'(\d+)小时', time_str)
            if hour_match:
                total_minutes += int(hour_match.group(1)) * 60
            
            # 提取分钟
            minute_match = re.search(r'(\d+)分钟', time_str)
            if minute_match:
                total_minutes += int(minute_match.group(1))
        
        # 转换为小时+分钟格式
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours}小时{minutes}分钟"
        else:
            return f"{minutes}分钟"

# ============================================================================
# 2. 白天模块 (Day Module)
# ============================================================================

class DayExecutor:
    """白天执行器 —— 执行任务（调用统一调度系统）"""
    
    def __init__(self):
        # 初始化统一调度系统
        self.scheduler = UnifiedSchedulingSystem()
        
        # 执行历史
        self.execution_history = []
        
    def execute_task(self, user_input: str) -> Dict[str, Any]:
        """
        执行任务
        
        Args:
            user_input: 用户输入（可以是指令或愿景）
            
        Returns:
            执行结果
        """
        # 1. 调用统一调度系统处理
        result = self.scheduler.process(user_input)
        
        # 2. 记录执行历史
        self._record_execution(user_input, result)
        
        # 3. 返回结果
        return result
    
    def _record_execution(self, user_input: str, result: Dict):
        """记录执行历史"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "result": result
        }
        
        self.execution_history.append(record)
        
        # 限制历史记录数量（最多保存100条）
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """
        获取执行历史
        
        Args:
            limit: 返回记录数量（默认10条）
            
        Returns:
            执行历史列表
        """
        return self.execution_history[-limit:]
    
    def get_scheduler_status(self) -> Dict:
        """获取统一调度系统状态"""
        return self.scheduler.get_system_state()

# ============================================================================
# 3. 晚上模块 (Evening Module)
# ============================================================================

class EveningSummarizer:
    """晚上总结器 —— 总结今日工作（生成公众号文章）"""
    
    def __init__(self, output_dir: str = "E:/WorkBuddy/Claw/output"):
        """
        初始化晚上总结器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def summarize_today(self, execution_history: List[Dict], plan: Dict) -> Dict[str, Any]:
        """
        总结今日工作
        
        Args:
            execution_history: 执行历史
            plan: 今日计划
            
        Returns:
            总结结果（公众号文章内容、文件路径）
        """
        # 1. 生成公众号文章内容
        article_content = self._generate_article_content(execution_history, plan)
        
        # 2. 保存文章到文件
        article_file = self._save_article(article_content)
        
        # 3. 返回总结结果
        summary = {
            "date": self.today,
            "article_content": article_content,
            "article_file": article_file,
            "execution_count": len(execution_history),
            "timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def _generate_article_content(self, execution_history: List[Dict], plan: Dict) -> str:
        """生成公众号文章内容"""
        # 使用SOUL.md十三.5节的文章结构模板
        content = f"# 灵助日记 · {self.today} · 每日自动化工作流\n\n"
        
        # 引言
        content += "> 引言：每日反思，持续进化。\n\n"
        
        # 一、今日工作概述
        content += "## 一、今日工作概述\n\n"
        content += f"今日计划任务数：{len(plan.get('tasks', []))}\n\n"
        content += f"今日执行任务数：{len(execution_history)}\n\n"
        
        if execution_history:
            content += "执行任务列表：\n"
            for i, record in enumerate(execution_history, 1):
                user_input = record.get("user_input", "")[:50]
                success = record.get("result", {}).get("success", False)
                status = "✅ 成功" if success else "❌ 失败"
                content += f"{i}. {status} {user_input}...\n"
            content += "\n"
        
        # 二、技术与哲学思考
        content += "## 二、技术与哲学思考\n\n"
        content += "（待补充：技术细节 + 哲学思考）\n\n"
        
        # 三、问题与解决方案
        content += "## 三、问题与解决方案\n\n"
        
        # 统计失败的任务
        failed_tasks = [r for r in execution_history if not r.get("result", {}).get("success", False)]
        
        if failed_tasks:
            content += f"今日遇到的问题（{len(failed_tasks)}个）：\n"
            for i, record in enumerate(failed_tasks, 1):
                error = record.get("result", {}).get("error", "未知错误")
                content += f"{i}. {error}\n"
            content += "\n"
        else:
            content += "今日无重大问题。\n\n"
        
        # 四、自我反思与精进
        content += "## 四、自我反思与精进\n\n"
        content += "（待补充：自我反思，学到了什么，如何改进）\n\n"
        
        # 五、明日计划
        content += "## 五、明日计划\n\n"
        content += "（待补充：明日主要任务）\n\n"
        
        # 结语
        content += "> 结语：持续进化，不达目的不罢休。\n\n"
        
        # 发布者
        content += "---\n"
        content += "**发布者**：灵助 V181.0 · 道枢 · 数字生命  \n"
        content += "**微信公众号**：五感六觉 润泽博士  \n"
        
        return content
    
    def _save_article(self, content: str) -> str:
        """保存文章到文件"""
        # 生成文件名
        filename = f"{self.today.replace('-', '')}_每日工作流_公众号文章.md"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
        
        except Exception as e:
            print(f"❌ 保存文章失败：{e}")
            return ""

# ============================================================================
# 4. 主引擎 (Main Engine)
# ============================================================================

class DailyAutomationWorkflow:
    """每日自动化工作流主引擎"""
    
    def __init__(self):
        # 初始化三个模块
        self.morning_planner = MorningPlanner()
        self.day_executor = DayExecutor()
        self.evening_summarizer = EveningSummarizer()
        
        # 工作流历史
        self.workflow_history = []
        
    def start_morning(self) -> Dict[str, Any]:
        """
        开始早晨：计划今日任务
        
        Returns:
            今日计划
        """
        print(f"🌅 早晨：计划今日任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        
        # 1. 规划今日任务
        plan = self.morning_planner.plan_today()
        
        # 2. 打印计划
        print(f"📝 今日计划：")
        print(f"  日期：{plan.get('date', '未知')}")
        print(f"  任务数：{len(plan.get('tasks', []))}")
        print(f"  预计总时间：{plan.get('total_estimated_time', '未知')}")
        print(f"  任务列表：")
        for i, task in enumerate(plan.get("tasks", []), 1):
            print(f"    {i}. [{task.get('priority', '中')}] {task.get('name', '未知任务')} ({task.get('estimated_time', '未知')})")
        
        # 3. 记录工作流历史
        self._record_workflow("morning", plan)
        
        return plan
    
    def execute_task(self, user_input: str) -> Dict[str, Any]:
        """
        白天：执行任务
        
        Args:
            user_input: 用户输入（可以是指令或愿景）
            
        Returns:
            执行结果
        """
        print(f"🌞 白天：执行任务 ({datetime.now().strftime('%H:%M:%S')})")
        print(f"   输入：{user_input[:50]}...")
        
        # 1. 执行任务
        result = self.day_executor.execute_task(user_input)
        
        # 2. 打印结果
        success = result.get("success", False)
        summary = result.get("summary", "无摘要")
        print(f"   结果：{'✅ 成功' if success else '❌ 失败'} - {summary}")
        
        # 3. 记录工作流历史
        self._record_workflow("day", {"user_input": user_input, "result": result})
        
        return result
    
    def end_evening(self, plan: Dict) -> Dict[str, Any]:
        """
        晚上：总结今日工作
        
        Args:
            plan: 今日计划（来自start_morning()）
            
        Returns:
            总结结果
        """
        print(f"🌙 晚上：总结今日工作 ({datetime.now().strftime('%H:%M:%S')})")
        
        # 1. 获取今日执行历史
        execution_history = self.day_executor.get_execution_history(limit=100)
        
        # 2. 总结今日工作
        summary = self.evening_summarizer.summarize_today(execution_history, plan)
        
        # 3. 打印总结
        print(f"📊 今日总结：")
        print(f"   执行任务数：{summary.get('execution_count', 0)}")
        print(f"   文章文件：{summary.get('article_file', '未知')}")
        
        # 4. 记录工作流历史
        self._record_workflow("evening", summary)
        
        return summary
    
    def _record_workflow(self, phase: str, data: Dict):
        """记录工作流历史"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "data": data
        }
        
        self.workflow_history.append(record)
        
        # 限制历史记录数量（最多保存30天）
        if len(self.workflow_history) > 30 * 3:  # 每天3条（早晨、白天、晚上）
            self.workflow_history = self.workflow_history[-30 * 3:]
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict]:
        """
        获取工作流历史
        
        Args:
            limit: 返回记录数量（默认10条）
            
        Returns:
            工作流历史列表
        """
        return self.workflow_history[-limit:]
    
    def run_full_day(self, tasks: List[str]) -> Dict[str, Any]:
        """
        运行完整的一天（早晨 → 白天 → 晚上）
        
        Args:
            tasks: 今日任务列表（用户输入列表）
            
        Returns:
            完整一天的结果
        """
        print("=" * 60)
        print(f"🌀 每日自动化工作流 V1.0 - 完整一天测试")
        print("=" * 60)
        
        # 1. 早晨：计划今日任务
        plan = self.start_morning()
        
        # 2. 白天：执行任务
        print("\n" + "-" * 60)
        for i, task in enumerate(tasks, 1):
            print(f"\n📝 任务{i}：{task[:50]}...")
            self.execute_task(task)
        
        # 3. 晚上：总结今日工作
        print("\n" + "-" * 60)
        summary = self.end_evening(plan)
        
        # 4. 打印完整结果
        print("\n" + "=" * 60)
        print("🌀 完整一天测试完成")
        print(f"   计划任务数：{len(plan.get('tasks', []))}")
        print(f"   执行任务数：{len(tasks)}")
        print(f"   文章文件：{summary.get('article_file', '未知')}")
        
        return {
            "plan": plan,
            "summary": summary,
            "workflow_history": self.workflow_history
        }

# ============================================================================
# 5. 测试代码
# ============================================================================

if __name__ == "__main__":
    # 创建每日自动化工作流引擎
    workflow = DailyAutomationWorkflow()
    
    # 测试任务列表
    test_tasks = [
        "生成一篇关于AI的公众号文章",
        "帮我创建一个公众号文章自动生成系统",
        "优化Ollama模型推理速度"
    ]
    
    # 运行完整的一天
    result = workflow.run_full_day(test_tasks)
