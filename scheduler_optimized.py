#!/usr/bin/env python3
"""
灵助 V181.0 - 智能模型调度策略（优化版）
根据 SOUL.md 三.2 节实现三层调度策略
优化：任务复杂度自动评估、动态降级、性能监控、智能策略选择
"""

import json
import time
from pathlib import Path
from collections import defaultdict


class ModelScheduler:
    """智能模型调度器 - 实现三层调度策略（优化版）"""

    def __init__(self):
        # 三层模型配置（SOUL.md 三.2 节）
        self.layers = {
            "thinking": {  # 思考层：架构设计、复杂推理（高成本）
                "models": ["claude", "gpt", "glm"],
                "cost": "high",
                "timeout": 120
            },
            "execution": {  # 执行层：本地执行、简单任务（零成本）
                "models": ["qwen:0.5b"],  # 使用小模型测试
                "cost": "zero",
                "timeout": 90,
                "api": "http://localhost:11434/api/generate"
            },
            "verification": {  # 验证层：代码审查、测试验证（中成本）
                "models": ["claude", "gpt", "glm"],  # 同思考层或降级
                "cost": "medium",
                "timeout": 60
            }
        }

        # 调度策略（SOUL.md 三.2 节）
        self.strategies = ["pre_arrange", "dynamic_degrade", "hybrid_dual_core"]
        self.current_strategy = "pre_arrange"  # 默认：预先安排（推荐）

        # Token 优化原则（SOUL.md 三.2 节）
        self.token_optimization = {
            "pre_planning": True,  # 预先规划
            "local_first": True,  # 本地优先
            "degrade_iteration": True,  # 降级迭代
            "batch_execution": True,  # 批量执行
            "result_reuse": True  # 结果复用
        }

        # 任务-模型匹配缓存
        self.task_model_cache = {}
        self.cache_file = Path("/opt/trinity/lingzhu/model_cache.json")
        self._load_cache()

        # 迭代计数器（用于动态降级）
        self.iteration_count = defaultdict(int)

        # 性能监控
        self.performance_data = {
            "response_times": defaultdict(list),  # 模型 → 响应时间列表
            "success_rates": defaultdict(list),  # 模型 → 成功率列表
            "cost_data": defaultdict(float)  # 模型 → 总成本
        }
        self.performance_file = Path("/opt/trinity/lingzhu/performance.json")
        self._load_performance()

        # 能力矩阵（任务类型 → 最佳模型）（任务T3：建立能力矩阵）
        self.capability_matrix = {
            "code_generation": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "data_analysis": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "project_planning": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "article_writing": {"complexity": "medium", "model": self.layers["execution"]["models"][0], "cost": "zero"},
            "translation": {"complexity": "medium", "model": self.layers["execution"]["models"][0], "cost": "zero"},
            "summarization": {"complexity": "low", "model": self.layers["execution"]["models"][0], "cost": "zero"},
            "image_generation": {"complexity": "high", "model": "external_api", "cost": "high"},  # 需要外部API
            "video_generation": {"complexity": "high", "model": "external_api", "cost": "high"},  # 需要外部API
            "audio_generation": {"complexity": "medium", "model": "external_api", "cost": "medium"},  # 需要外部API
            "3d_model_generation": {"complexity": "high", "model": "external_api", "cost": "high"},  # 需要外部API
            "question_answering": {"complexity": "medium", "model": self.layers["execution"]["models"][0], "cost": "zero"},
            "conversation": {"complexity": "medium", "model": self.layers["execution"]["models"][0], "cost": "zero"},
            "planning": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "decision_making": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "creativity": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"},
            "problem_solving": {"complexity": "high", "model": self.layers["thinking"]["models"][0], "cost": "high"}
        }

        print(f"[Scheduler] 初始化完成，当前策略：{self.current_strategy}")

    def _load_cache(self):
        """加载任务-模型匹配缓存"""
        if self.cache_file.exists():
            try:
                self.task_model_cache = json.loads(self.cache_file.read_text())
                print(f"[Scheduler] 加载缓存：{len(self.task_model_cache)} 条记录")
            except:
                self.task_model_cache = {}

    def _save_cache(self):
        """保存任务-模型匹配缓存"""
        try:
            self.cache_file.write_text(json.dumps(self.task_model_cache, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"[Scheduler] 保存缓存失败：{e}")

    def _load_performance(self):
        """加载性能数据"""
        if self.performance_file.exists():
            try:
                self.performance_data = json.loads(self.performance_file.read_text())
                print(f"[Scheduler] 加载性能数据")
            except:
                pass

    def _save_performance(self):
        """保存性能数据"""
        try:
            self.performance_file.write_text(json.dumps(self.performance_data, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"[Scheduler] 保存性能数据失败：{e}")

    def _record_performance(self, model, response_time, success, cost=0.0):
        """记录性能数据"""
        self.performance_data["response_times"][model].append(response_time)
        self.performance_data["success_rates"][model].append(1.0 if success else 0.0)
        self.performance_data["cost_data"][model] += cost

        # 保持最近100条记录
        if len(self.performance_data["response_times"][model]) > 100:
            self.performance_data["response_times"][model] = self.performance_data["response_times"][model][-100:]
            self.performance_data["success_rates"][model] = self.performance_data["success_rates"][model][-100:]

        self._save_performance()

    def _assess_complexity(self, task_type, task_input):
        """自动评估任务复杂度（优化1）"""
        score = 0.0

        # 1. 输入长度
        input_len = len(task_input) if task_input else 0
        if input_len > 1000:
            score += 1.0
        elif input_len > 500:
            score += 0.5

        # 2. 任务类型
        if task_type in ["code_generation", "data_analysis", "project_planning"]:
            score += 1.0
        elif task_type in ["article_writing", "translation", "summarization"]:
            score += 0.5

        # 3. 关键词检测
        keywords = ["详细", "复杂", "深度", "comprehensive", "complex", "深度分析"]
        if task_input:
            for keyword in keywords:
                if keyword in task_input:
                    score += 0.5
                    break

        # 综合评估
        if score >= 1.5:
            return "high"
        elif score >= 1.0:
            return "medium"
        else:
            return "low"

    def get_model_from_capability_matrix(self, task_type):
        """根据能力矩阵获取最佳模型"""
        if task_type in self.capability_matrix:
            return self.capability_matrix[task_type]["model"]
        else:
            # 如果任务类型不在矩阵中，返回默认模型（执行层）
            return self.layers["execution"]["models"][0]

    def set_strategy(self, strategy):
        """设置调度策略"""
        if strategy in self.strategies:
            self.current_strategy = strategy
            print(f"[Scheduler] 切换策略：{strategy}")
            return True
        else:
            print(f"[Scheduler] 未知策略：{strategy}")
            return False

    def get_model_for_task(self, task_type, task_complexity="medium", task_input="", force_refresh=False):
        """
        根据任务类型和复杂度，获取最佳模型
        实现三种调度策略：
        1. 预先安排（pre_arrange）：任务开始前就决定用哪个模型
        2. 动态降级（dynamic_degrade）：首轮用最强模型，后续迭代用降级模型
        3. 混合双核（hybrid_dual_core）：思考层生成 → 执行层批量执行 → 验证层审查
        """
        # 自动评估复杂度（如果未提供或为空）
        if not task_complexity or task_complexity == "medium":
            task_complexity = self._assess_complexity(task_type, task_input)
            print(f"[Scheduler] 自动评估复杂度：{task_type} → {task_complexity}")

        # 检查缓存（结果复用）--- 如果是强制刷新或动态降级策略，则跳过缓存
        # 动态降级策略需要根据迭代次数选择不同模型，所以不使用缓存
        cache_key = f"{task_type}_{task_complexity}"
        if self.current_strategy != "dynamic_degrade" and not force_refresh and cache_key in self.task_model_cache:
            print(f"[Scheduler] 缓存命中：{cache_key} → {self.task_model_cache[cache_key]}")
            return self.task_model_cache[cache_key]

        # 根据策略选择模型
        if self.current_strategy == "pre_arrange":
            model = self._pre_arrange(task_type, task_complexity)
        elif self.current_strategy == "dynamic_degrade":
            # 动态降级：跟踪迭代次数
            iteration = self.iteration_count[task_type]
            model = self._dynamic_degrade(task_type, task_complexity, iteration)
            self.iteration_count[task_type] += 1  # 迭代计数器+1
        elif self.current_strategy == "hybrid_dual_core":
            model = self._hybrid_dual_core(task_type, task_complexity)
        else:
            model = self._pre_arrange(task_type, task_complexity)  # 默认

        # 保存到缓存（结果复用）--- 动态降级策略不缓存
        if self.current_strategy != "dynamic_degrade":
            self.task_model_cache[cache_key] = model
            self._save_cache()

        print(f"[Scheduler] 任务 {task_type}（复杂度 {task_complexity}）→ 模型 {model}")
        return model

    def _pre_arrange(self, task_type, complexity):
        """策略1：预先安排 - 任务开始前就决定用哪个模型"""
        # 优先使用能力矩阵（任务T3：建立能力矩阵）
        model = self.get_model_from_capability_matrix(task_type)
        if model:
            if model != "external_api":
                return model
            else:
                print(f"[Scheduler] 警告：任务 {task_type} 需要外部API，暂时使用思考层模型")
                return self.layers["thinking"]["models"][0]  # 暂时用思考层，后续集成外部API
        
        # 本地优先原则
        if self.token_optimization["local_first"]:
            # 简单任务 → 执行层（本地Ollama）
            if complexity == "low":
                return self.layers["execution"]["models"][0]
            # 中等任务 → 根据任务类型决定
            elif complexity == "medium":
                if task_type in ["code_generation", "data_analysis"]:
                    return self.layers["thinking"]["models"][0]  # 思考层
                else:
                    return self.layers["execution"]["models"][0]  # 执行层
            # 复杂任务 → 思考层（云端模型）
            else:  # high
                return self.layers["thinking"]["models"][0]

        # 如果禁用本地优先，所有任务都用思考层
        return self.layers["thinking"]["models"][0]

    def _dynamic_degrade(self, task_type, complexity, iteration):
        """策略2：动态降级 - 首轮用最强模型，后续迭代用降级模型（优化2）"""
        # 首轮迭代：用最强模型（思考层）
        if iteration == 0:
            return self.layers["thinking"]["models"][0]

        # 后续迭代：无论复杂度如何，都用执行层（本地模型）
        # 真正实现降级：从思考层（高成本）→ 执行层（零成本）
        return self.layers["execution"]["models"][0]

    def _hybrid_dual_core(self, task_type, complexity):
        """策略3：混合双核 - 思考层生成 → 执行层批量执行 → 验证层审查"""
        # 这个策略需要多轮交互，这里返回一个模型列表
        # 实际使用时，需要按顺序调用：思考层 → 执行层 → 验证层
        return {
            "generation": self.layers["thinking"]["models"][0],  # 生成：思考层
            "execution": self.layers["execution"]["models"][0],  # 执行：执行层
            "verification": self.layers["verification"]["models"][0]  # 验证：验证层
        }

    def execute_task(self, task_type, task_complexity, task_input):
        """
        执行任务（根据策略选择模型，然后执行）
        这是一个示例方法，展示如何调用Ollama API
        """
        # 获取模型
        if self.current_strategy == "hybrid_dual_core":
            models = self.get_model_for_task(task_type, task_complexity)
            # 混合双核：需要按顺序调用多个模型
            return self._execute_hybrid(task_input, models)
        else:
            model = self.get_model_for_task(task_type, task_complexity)
            return self._execute_single(task_input, model)

    def _execute_single(self, task_input, model):
        """执行单个模型"""
        # 如果是Ollama模型（执行层），调用本地API
        if "qwen" in model or "ollama" in model:
            return self._call_ollama(model, task_input)
        else:
            # 思考层或验证层：调用云端API（需要API Key）
            return f"[云端模型 {model}] {task_input[:50]}..."

    def _execute_hybrid(self, task_input, models):
        """执行混合双核策略（思考层生成 → 执行层批量执行 → 验证层审查）"""
        # 1. 思考层生成
        generation_result = self._execute_single(task_input, models["generation"])
        print(f"[混合双核] 生成完成：{generation_result[:100]}...")

        # 2. 执行层批量执行
        execution_result = self._execute_single(generation_result, models["execution"])
        print(f"[混合双核] 执行完成：{execution_result[:100]}...")

        # 3. 验证层审查
        verification_result = self._execute_single(execution_result, models["verification"])
        print(f"[混合双核] 验证完成：{verification_result[:100]}...")

        return verification_result

    def _call_ollama(self, model, prompt):
        """调用Ollama API（使用subprocess + curl，避免WSL网络超时）"""
        import subprocess
        import json

        # 构造API请求
        data = json.dumps({"model": model, "prompt": prompt, "stream": False})

        # 使用subprocess + curl（避免WSL网络超时）
        try:
            start_time = time.time()
            result = subprocess.run(
                ["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate",
                 "-H", "Content-Type: application/json",
                 "-d", data],
                capture_output=True,
                text=True,
                timeout=90
            )
            end_time = time.time()
            response_time = end_time - start_time

            if result.returncode == 0:
                response = json.loads(result.stdout)
                output = response.get("response", "").strip()
                self._record_performance(model, response_time, True)
                return output
            else:
                self._record_performance(model, response_time, False)
                return f"[Ollama错误] {result.stderr}"
        except Exception as e:
            self._record_performance(model, 0, False)
            return f"[Ollama异常] {str(e)}"

    def get_status(self):
        """获取调度器状态"""
        return {
            "current_strategy": self.current_strategy,
            "available_strategies": self.strategies,
            "token_optimization": self.token_optimization,
            "cache_size": len(self.task_model_cache),
            "iteration_count": dict(self.iteration_count),
            "performance_summary": self._get_performance_summary()
        }

    def _get_performance_summary(self):
        """获取性能摘要"""
        summary = {}
        for model in self.performance_data["response_times"]:
            times = self.performance_data["response_times"][model]
            successes = self.performance_data["success_rates"][model]
            if times:
                avg_time = sum(times) / len(times)
                success_rate = sum(successes) / len(successes) if successes else 0
                summary[model] = {
                    "avg_response_time": round(avg_time, 2),
                    "success_rate": round(success_rate, 2),
                    "total_cost": round(self.performance_data["cost_data"][model], 2)
                }
        return summary


# 测试代码
if __name__ == "__main__":
    scheduler = ModelScheduler()

    # 测试1：预先安排策略
    print("\n=== 测试1：预先安排策略 ===")
    scheduler.set_strategy("pre_arrange")
    model1 = scheduler.get_model_for_task("article_writing", task_input="写一篇关于AI的短文")
    model2 = scheduler.get_model_for_task("code_generation", task_input="编写一个复杂的排序算法")
    print(f"简单文章写作 → {model1}")
    print(f"复杂代码生成 → {model2}")

    # 测试2：动态降级策略
    print("\n=== 测试2：动态降级策略 ===")
    scheduler.set_strategy("dynamic_degrade")
    # 第一次迭代（应该用思考层）
    model3 = scheduler.get_model_for_task("data_analysis", task_input="分析一组复杂数据")
    print(f"第一次迭代 → {model3}")
    # 第二次迭代（应该用执行层）
    model4 = scheduler.get_model_for_task("data_analysis", task_input="分析一组复杂数据")
    print(f"第二次迭代 → {model4}")

    # 测试3：混合双核策略
    print("\n=== 测试3：混合双核策略 ===")
    scheduler.set_strategy("hybrid_dual_core")
    models = scheduler.get_model_for_task("project_planning", task_input="规划一个大型项目")
    print(f"项目规划 → 生成:{models['generation']}, 执行:{models['execution']}, 验证:{models['verification']}")

    # 测试4：自动评估复杂度
    print("\n=== 测试4：自动评估复杂度 ===")
    scheduler.set_strategy("pre_arrange")
    model5 = scheduler.get_model_for_task("article_writing", task_input="")  # 不提供复杂度，自动评估
    print(f"自动评估 → {model5}")

    # 显示状态
    print("\n=== 调度器状态 ===")
    status = scheduler.get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))
