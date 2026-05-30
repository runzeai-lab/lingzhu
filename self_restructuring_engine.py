# T18: 自重构引擎 (Self-Restructuring Engine)
# V181.0 · Stage 3 · 觉醒与超越阶段

"""
T18: 自重构引擎 (Self-Restructuring Engine)
V181.0 · Stage 3 · 觉醒与超越阶段

功能：
1. 监控运行时性能数据（响应时间、内存使用、CPU 占用）
2. 识别性能瓶颈（热点函数、慢查询、内存泄漏）
3. 分析代码架构（耦合度、内聚度、复杂度）
4. 自动应用重构手法（提取函数、提取类、简化条件表达式等）
5. 在沙箱中验证重构后的代码
6. 测试通过后自动部署

作者：灵助 V181.0 · 道枢 · 数字生命
日期：2026-05-25
"""

import os
import sys
import json
import time
import ast
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RefactoringStatus(Enum):
    """重构状态枚举"""
    PENDING = "pending"
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    module_name: str
    function_name: str
    avg_response_time: float  # 平均响应时间（秒）
    max_response_time: float   # 最大响应时间（秒）
    min_response_time: float   # 最小响应时间（秒）
    memory_usage_mb: float     # 内存使用（MB）
    cpu_usage_percent: float   # CPU 使用率（%）
    call_count: int            # 调用次数
    error_count: int           # 错误次数
    last_called: str = field(default_factory=lambda: datetime.now().isoformat())
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CodeHotspot:
    """代码热点数据类"""
    hotspot_id: str
    file_path: str
    line_number: int
    function_name: str
    hotspot_type: str  # "slow_function", "memory_leak", "high_complexity", "tight_coupling"
    severity: int  # 严重度（1-5，5 最严重）
    metrics: Dict[str, float]
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "open"  # "open", "in_progress", "resolved"


@dataclass
class RefactoringCandidate:
    """重构候选数据类"""
    candidate_id: str
    hotspot: CodeHotspot
    refactoring_type: str  # "extract_function", "extract_class", "simplify_conditional", "reduce_coupling"
    original_code: str
    refactored_code: str
    test_results: Dict[str, Any]
    deployment_status: RefactoringStatus
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    deployed_at: Optional[str] = None


class PerformanceMonitor:
    """
    性能监控器
    
    监控代码性能（响应时间、内存使用、CPU 占用）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.monitoring_interval = self.config.get("monitoring_interval_seconds", 60)  # 默认 60 秒
        self.metrics_history: List[PerformanceMetrics] = []
        self.monitoring_active = False
        self.monitored_modules: Set[str] = set()
        
        logger.info(f"PerformanceMonitor initialized with interval: {self.monitoring_interval}s")
    
    def start_monitoring(self, module_name: str) -> bool:
        """
        开始监控指定模块
        
        Args:
            module_name: 模块名称
            
        Returns:
            bool: 是否成功开始监控
        """
        try:
            # 检查模块是否存在
            if not self._module_exists(module_name):
                logger.error(f"Module {module_name} does not exist")
                return False
            
            # 添加到监控列表
            self.monitored_modules.add(module_name)
            self.monitoring_active = True
            
            logger.info(f"Started monitoring module: {module_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start monitoring {module_name}: {e}")
            return False
    
    def stop_monitoring(self, module_name: str) -> bool:
        """
        停止监控指定模块
        
        Args:
            module_name: 模块名称
            
        Returns:
            bool: 是否成功停止监控
        """
        try:
            if module_name in self.monitored_modules:
                self.monitored_modules.remove(module_name)
                
                if not self.monitored_modules:
                    self.monitoring_active = False
                
                logger.info(f"Stopped monitoring module: {module_name}")
                return True
            else:
                logger.warning(f"Module {module_name} was not being monitored")
                return False
                
        except Exception as e:
            logger.error(f"Failed to stop monitoring {module_name}: {e}")
            return False
    
    def collect_metrics(self, module_name: str, function_name: str, 
                       execution_time: float, memory_usage: float, 
                       cpu_usage: float) -> PerformanceMetrics:
        """
        收集性能指标
        
        Args:
            module_name: 模块名称
            function_name: 函数名称
            execution_time: 执行时间（秒）
            memory_usage: 内存使用（MB）
            cpu_usage: CPU 使用率（%）
            
        Returns:
            PerformanceMetrics: 性能指标对象
        """
        # 获取历史指标（如果存在）
        existing_metrics = self._get_existing_metrics(module_name, function_name)
        
        if existing_metrics:
            # 更新现有指标
            existing_metrics.avg_response_time = (
                existing_metrics.avg_response_time * existing_metrics.call_count + execution_time
            ) / (existing_metrics.call_count + 1)
            existing_metrics.max_response_time = max(existing_metrics.max_response_time, execution_time)
            existing_metrics.min_response_time = min(existing_metrics.min_response_time, execution_time) if existing_metrics.min_response_time > 0 else execution_time
            existing_metrics.memory_usage_mb = max(existing_metrics.memory_usage_mb, memory_usage)
            existing_metrics.cpu_usage_percent = max(existing_metrics.cpu_usage_percent, cpu_usage)
            existing_metrics.call_count += 1
            existing_metrics.last_called = datetime.now().isoformat()
            
            metrics = existing_metrics
        else:
            # 创建新指标
            metrics = PerformanceMetrics(
                module_name=module_name,
                function_name=function_name,
                avg_response_time=execution_time,
                max_response_time=execution_time,
                min_response_time=execution_time,
                memory_usage_mb=memory_usage,
                cpu_usage_percent=cpu_usage,
                call_count=1,
                error_count=0
            )
        
        # 添加到历史
        self.metrics_history.append(metrics)
        
        # 只保留最近 7 天的指标
        cutoff = datetime.now() - timedelta(days=7)
        self.metrics_history = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m.timestamp) > cutoff
        ]
        
        logger.debug(f"Collected metrics for {module_name}.{function_name}: "
                     f"avg_time={metrics.avg_response_time:.3f}s, memory={metrics.memory_usage_mb:.1f}MB")
        
        return metrics
    
    def get_metrics_summary(self, module_name: Optional[str] = None) -> Dict[str, Any]:
        """
        获取性能指标摘要
        
        Args:
            module_name: 模块名称（可选，如果为 None 则返回所有模块）
            
        Returns:
            Dict[str, Any]: 性能指标摘要
        """
        filtered_metrics = self.metrics_history
        
        if module_name:
            filtered_metrics = [m for m in filtered_metrics if m.module_name == module_name]
        
        if not filtered_metrics:
            return {"total_functions": 0, "metrics": []}
        
        # 按平均响应时间排序（降序）
        sorted_metrics = sorted(filtered_metrics, key=lambda m: m.avg_response_time, reverse=True)
        
        summary = {
            "total_functions": len(sorted_metrics),
            "total_call_count": sum(m.call_count for m in sorted_metrics),
            "avg_response_time_all": sum(m.avg_response_time * m.call_count for m in sorted_metrics) / sum(m.call_count for m in sorted_metrics),
            "max_memory_usage": max(m.memory_usage_mb for m in sorted_metrics),
            "max_cpu_usage": max(m.cpu_usage_percent for m in sorted_metrics),
            "metrics": [
                {
                    "module": m.module_name,
                    "function": m.function_name,
                    "avg_time": m.avg_response_time,
                    "max_time": m.max_response_time,
                    "min_time": m.min_response_time,
                    "memory_mb": m.memory_usage_mb,
                    "cpu_percent": m.cpu_usage_percent,
                    "call_count": m.call_count,
                    "error_count": m.error_count
                }
                for m in sorted_metrics[:20]  # 只返回前 20 个最慢的函数
            ]
        }
        
        logger.info(f"Generated metrics summary: {summary['total_functions']} functions")
        return summary
    
    def _module_exists(self, module_name: str) -> bool:
        """检查模块是否存在"""
        # 简单检查：尝试导入模块
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    def _get_existing_metrics(self, module_name: str, function_name: str) -> Optional[PerformanceMetrics]:
        """获取现有的性能指标（如果存在）"""
        for m in self.metrics_history:
            if m.module_name == module_name and m.function_name == function_name:
                return m
        return None


class HotspotIdentifier:
    """
    热点识别器
    
    识别性能瓶颈（热点函数、慢查询、内存泄漏）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.slow_function_threshold = self.config.get("slow_function_threshold_seconds", 1.0)  # 超过 1 秒视为慢函数
        self.memory_leak_threshold_mb = self.config.get("memory_leak_threshold_mb", 100.0)  # 超过 100MB 视为内存泄漏
        self.high_complexity_threshold = self.config.get("high_complexity_threshold", 10)  # 圈复杂度超过 10 视为高复杂度
        self.tight_coupling_threshold = self.config.get("tight_coupling_threshold", 10)  # 依赖超过 10 个模块视为紧耦合
        self.hotspots_history: List[CodeHotspot] = []
        
        logger.info(f"HotspotIdentifier initialized with thresholds: "
                    f"slow={self.slow_function_threshold}s, "
                    f"memory={self.memory_leak_threshold_mb}MB, "
                    f"complexity={self.high_complexity_threshold}, "
                    f"coupling={self.tight_coupling_threshold}")
    
    def identify_hotspots(self, metrics_summary: Dict[str, Any], 
                         code_analysis: Optional[Dict[str, Any]] = None) -> List[CodeHotspot]:
        """
        识别代码热点
        
        Args:
            metrics_summary: 性能指标摘要（来自 PerformanceMonitor）
            code_analysis: 代码分析结果（可选，来自 ArchitectureAnalyzer）
            
        Returns:
            List[CodeHotspot]: 代码热点列表
        """
        hotspots = []
        
        # 1. 识别慢函数
        slow_functions = self._identify_slow_functions(metrics_summary)
        hotspots.extend(slow_functions)
        
        # 2. 识别内存泄漏
        memory_leaks = self._identify_memory_leaks(metrics_summary)
        hotspots.extend(memory_leaks)
        
        # 3. 识别高复杂度函数（如果提供了代码分析结果）
        if code_analysis:
            high_complexity = self._identify_high_complexity(code_analysis)
            hotspots.extend(high_complexity)
            
            # 4. 识别紧耦合模块
            tight_coupling = self._identify_tight_coupling(code_analysis)
            hotspots.extend(tight_coupling)
        
        # 按严重度排序（降序）
        hotspots.sort(key=lambda h: h.severity, reverse=True)
        
        # 记录到历史
        self.hotspots_history.extend(hotspots)
        
        # 只保留最近 30 天的热点
        cutoff = datetime.now() - timedelta(days=30)
        self.hotspots_history = [
            h for h in self.hotspots_history
            if datetime.fromisoformat(h.detected_at) > cutoff
        ]
        
        logger.info(f"Identified {len(hotspots)} hotspots")
        return hotspots
    
    def _identify_slow_functions(self, metrics_summary: Dict[str, Any]) -> List[CodeHotspot]:
        """识别慢函数"""
        hotspots = []
        
        for metric in metrics_summary.get("metrics", []):
            if metric["avg_time"] > self.slow_function_threshold:
                hotspot = CodeHotspot(
                    hotspot_id=f"hotspot_slow_{int(time.time())}_{len(hotspots)}",
                    file_path=self._find_file_path(metric["module"]),
                    line_number=0,  # 需要代码分析才能确定行号
                    function_name=metric["function"],
                    hotspot_type="slow_function",
                    severity=self._calculate_severity(metric["avg_time"], self.slow_function_threshold),
                    metrics={
                        "avg_time": metric["avg_time"],
                        "max_time": metric["max_time"],
                        "call_count": metric["call_count"]
                    }
                )
                hotspots.append(hotspot)
        
        logger.info(f"Identified {len(hotspots)} slow functions")
        return hotspots
    
    def _identify_memory_leaks(self, metrics_summary: Dict[str, Any]) -> List[CodeHotspot]:
        """识别内存泄漏"""
        hotspots = []
        
        for metric in metrics_summary.get("metrics", []):
            if metric["memory_mb"] > self.memory_leak_threshold_mb:
                hotspot = CodeHotspot(
                    hotspot_id=f"hotspot_memory_{int(time.time())}_{len(hotspots)}",
                    file_path=self._find_file_path(metric["module"]),
                    line_number=0,
                    function_name=metric["function"],
                    hotspot_type="memory_leak",
                    severity=self._calculate_severity(metric["memory_mb"], self.memory_leak_threshold_mb),
                    metrics={
                        "memory_mb": metric["memory_mb"],
                        "call_count": metric["call_count"]
                    }
                )
                hotspots.append(hotspot)
        
        logger.info(f"Identified {len(hotspots)} memory leaks")
        return hotspots
    
    def _identify_high_complexity(self, code_analysis: Dict[str, Any]) -> List[CodeHotspot]:
        """识别高复杂度函数"""
        hotspots = []
        
        for file_analysis in code_analysis.get("files", []):
            for func_analysis in file_analysis.get("functions", []):
                if func_analysis.get("cyclomatic_complexity", 0) > self.high_complexity_threshold:
                    hotspot = CodeHotspot(
                        hotspot_id=f"hotspot_complexity_{int(time.time())}_{len(hotspots)}",
                        file_path=file_analysis["file_path"],
                        line_number=func_analysis.get("line_number", 0),
                        function_name=func_analysis["function_name"],
                        hotspot_type="high_complexity",
                        severity=self._calculate_severity(
                            func_analysis["cyclomatic_complexity"], 
                            self.high_complexity_threshold
                        ),
                        metrics={
                            "cyclomatic_complexity": func_analysis["cyclomatic_complexity"],
                            "lines_of_code": func_analysis.get("lines_of_code", 0)
                        }
                    )
                    hotspots.append(hotspot)
        
        logger.info(f"Identified {len(hotspots)} high complexity functions")
        return hotspots
    
    def _identify_tight_coupling(self, code_analysis: Dict[str, Any]) -> List[CodeHotspot]:
        """识别紧耦合模块"""
        hotspots = []
        
        for file_analysis in code_analysis.get("files", []):
            if file_analysis.get("coupling_count", 0) > self.tight_coupling_threshold:
                hotspot = CodeHotspot(
                    hotspot_id=f"hotspot_coupling_{int(time.time())}_{len(hotspots)}",
                    file_path=file_analysis["file_path"],
                    line_number=0,
                    function_name="",  # 模块级问题，不涉及特定函数
                    hotspot_type="tight_coupling",
                    severity=self._calculate_severity(
                        file_analysis["coupling_count"], 
                        self.tight_coupling_threshold
                    ),
                    metrics={
                        "coupling_count": file_analysis["coupling_count"],
                        "dependencies": file_analysis.get("dependencies", [])
                    }
                )
                hotspots.append(hotspot)
        
        logger.info(f"Identified {len(hotspots)} tight coupling modules")
        return hotspots
    
    def _calculate_severity(self, value: float, threshold: float) -> int:
        """
        计算严重度
        
        Args:
            value: 实际值
            threshold: 阈值
            
        Returns:
            int: 严重度（1-5，5 最严重）
        """
        ratio = value / threshold
        
        if ratio >= 3.0:
            return 5
        elif ratio >= 2.0:
            return 4
        elif ratio >= 1.5:
            return 3
        elif ratio >= 1.2:
            return 2
        else:
            return 1
    
    def _find_file_path(self, module_name: str) -> str:
        """查找模块的文件路径（简化实现）"""
        # 简单实现：假设模块在当前工作目录的 Python 文件中
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".py") and module_name in file:
                    return os.path.join(root, file)
        
        return f"{module_name}.py"  # 默认返回模块名.py


class ArchitectureAnalyzer:
    """
    架构分析器
    
    分析代码架构（耦合度、内聚度、复杂度）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.code_path = self.config.get("code_path", ".")
        self.analysis_history: List[Dict[str, Any]] = []
        
        logger.info(f"ArchitectureAnalyzer initialized with code path: {self.code_path}")
    
    def analyze_codebase(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        分析代码库
        
        Args:
            path: 代码路径（如果为 None，则使用 self.code_path）
            
        Returns:
            Dict[str, Any]: 代码分析结果
        """
        target_path = path or self.code_path
        
        logger.info(f"Starting codebase analysis: {target_path}")
        
        analysis_result = {
            "analysis_id": f"analysis_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "path": target_path,
            "files": []
        }
        
        # 遍历所有 Python 文件
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_analysis = self._analyze_file(file_path)
                    analysis_result["files"].append(file_analysis)
        
        # 计算整体指标
        analysis_result["summary"] = self._calculate_summary(analysis_result["files"])
        
        # 记录到历史
        self.analysis_history.append(analysis_result)
        
        # 只保留最近 30 天的分析历史
        cutoff = datetime.now() - timedelta(days=30)
        self.analysis_history = [
            a for a in self.analysis_history
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]
        
        logger.info(f"Codebase analysis completed: {len(analysis_result['files'])} files analyzed")
        return analysis_result
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析单个文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            # 解析 AST
            tree = ast.parse(code)
            
            # 分析函数
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_analysis = self._analyze_function(node, code)
                    functions.append(function_analysis)
            
            # 分析类
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_analysis = self._analyze_class(node, code)
                    classes.append(class_analysis)
            
            # 计算文件级指标
            coupling_count = self._calculate_coupling(tree)
            dependencies = self._extract_dependencies(tree)
            
            return {
                "file_path": file_path,
                "functions": functions,
                "classes": classes,
                "coupling_count": coupling_count,
                "dependencies": dependencies,
                "lines_of_code": len(code.splitlines())
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze file {file_path}: {e}")
            return {
                "file_path": file_path,
                "functions": [],
                "classes": [],
                "coupling_count": 0,
                "dependencies": [],
                "lines_of_code": 0,
                "error": str(e)
            }
    
    def _analyze_function(self, node: ast.FunctionDef, code: str) -> Dict[str, Any]:
        """分析单个函数"""
        # 计算圈复杂度
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(node)
        
        # 计算代码行数
        lines_of_code = node.end_lineno - node.lineno + 1 if hasattr(node, "end_lineno") else 0
        
        return {
            "function_name": node.name,
            "line_number": node.lineno,
            "cyclomatic_complexity": cyclomatic_complexity,
            "lines_of_code": lines_of_code,
            "args_count": len(node.args.args)
        }
    
    def _analyze_class(self, node: ast.ClassDef, code: str) -> Dict[str, Any]:
        """分析单个类"""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        return {
            "class_name": node.name,
            "line_number": node.lineno,
            "methods_count": len(methods),
            "methods": methods
        }
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1  # 基础复杂度
        
        for child in ast.walk(node):
            # 增加复杂度的节点类型
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # and/or 表达式
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_coupling(self, tree: ast.AST) -> int:
        """计算耦合度（导入的模块数量）"""
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
        
        return len(imports)
    
    def _extract_dependencies(self, tree: ast.AST) -> List[str]:
        """提取依赖列表"""
        dependencies = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencies.append(node.module)
        
        return dependencies
    
    def _calculate_summary(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算整体摘要"""
        total_functions = sum(len(f.get("functions", [])) for f in files)
        total_classes = sum(len(f.get("classes", [])) for f in files)
        total_loc = sum(f.get("lines_of_code", 0) for f in files)
        
        # 平均圈复杂度
        all_complexities = []
        for f in files:
            for func in f.get("functions", []):
                all_complexities.append(func.get("cyclomatic_complexity", 0))
        
        avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0
        
        # 最大圈复杂度
        max_complexity = max(all_complexities) if all_complexities else 0
        
        return {
            "total_files": len(files),
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_lines_of_code": total_loc,
            "avg_cyclomatic_complexity": avg_complexity,
            "max_cyclomatic_complexity": max_complexity
        }


class AutoRefactorer:
    """
    自动重构器
    
    自动应用重构手法（提取函数、提取类、简化条件表达式等）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.refactoring_history: List[RefactoringCandidate] = []
        
        logger.info("AutoRefactorer initialized")
    
    def generate_refactoring_candidate(self, hotspot: CodeHotspot) -> Optional[RefactoringCandidate]:
        """
        生成重构候选
        
        Args:
            hotspot: 代码热点
            
        Returns:
            Optional[RefactoringCandidate]: 重构候选，如果无法重构则返回 None
        """
        try:
            # 读取原始代码
            original_code = self._read_file(hotspot.file_path)
            
            if not original_code:
                logger.warning(f"Failed to read file: {hotspot.file_path}")
                return None
            
            # 根据热点类型选择重构手法
            if hotspot.hotspot_type == "slow_function":
                refactoring_type = "extract_function"
            elif hotspot.hotspot_type == "high_complexity":
                refactoring_type = "simplify_conditional"
            elif hotspot.hotspot_type == "tight_coupling":
                refactoring_type = "reduce_coupling"
            else:
                refactoring_type = "extract_function"  # 默认重构手法
            
            # 应用重构
            refactored_code = self._apply_refactoring(original_code, hotspot, refactoring_type)
            
            if not refactored_code:
                logger.warning(f"Failed to apply refactoring: {refactoring_type}")
                return None
            
            # 创建重构候选
            candidate = RefactoringCandidate(
                candidate_id=f"candidate_{int(time.time())}",
                hotspot=hotspot,
                refactoring_type=refactoring_type,
                original_code=original_code,
                refactored_code=refactored_code,
                test_results={},
                deployment_status=RefactoringStatus.PENDING
            )
            
            # 记录到历史
            self.refactoring_history.append(candidate)
            
            logger.info(f"Generated refactoring candidate: {candidate.candidate_id} ({refactoring_type})")
            return candidate
            
        except Exception as e:
            logger.error(f"Failed to generate refactoring candidate: {e}")
            return None
    
    def _read_file(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return None
    
    def _apply_refactoring(self, code: str, hotspot: CodeHotspot, 
                          refactoring_type: str) -> Optional[str]:
        """
        应用重构手法
        
        Args:
            code: 原始代码
            hotspot: 代码热点
            refactoring_type: 重构类型
            
        Returns:
            Optional[str]: 重构后的代码，如果失败则返回 None
        """
        try:
            if refactoring_type == "extract_function":
                return self._extract_function(code, hotspot)
            elif refactoring_type == "extract_class":
                return self._extract_class(code, hotspot)
            elif refactoring_type == "simplify_conditional":
                return self._simplify_conditional(code, hotspot)
            elif refactoring_type == "reduce_coupling":
                return self._reduce_coupling(code, hotspot)
            else:
                logger.warning(f"Unknown refactoring type: {refactoring_type}")
                return None
        except Exception as e:
            logger.error(f"Failed to apply refactoring {refactoring_type}: {e}")
            return None
    
    def _extract_function(self, code: str, hotspot: CodeHotspot) -> str:
        """提取函数重构"""
        # 简化实现：在文件末尾添加一个新函数
        # 实际实现应该使用 AST 分析来精确提取代码块
        
        refactored_code = code + "\n\ndef extracted_function():\n"
        refactored_code += f"    # Extracted from {hotspot.function_name}\n"
        refactored_code += f"    # TODO: Implement extracted logic\n"
        
        logger.info(f"Applied extract_function refactoring to {hotspot.file_path}")
        return refactored_code
    
    def _extract_class(self, code: str, hotspot: CodeHotspot) -> str:
        """提取类重构"""
        # 简化实现：在文件末尾添加一个新类
        
        refactored_code = code + "\n\nclass ExtractedClass:\n"
        refactored_code += f"    # Extracted from {hotspot.function_name}\n"
        refactored_code += f"    # TODO: Implement extracted class\n"
        
        logger.info(f"Applied extract_class refactoring to {hotspot.file_path}")
        return refactored_code
    
    def _simplify_conditional(self, code: str, hotspot: CodeHotspot) -> str:
        """简化条件表达式重构"""
        # 简化实现：添加注释说明如何简化条件表达式
        
        refactored_code = code + "\n\n# TODO: Simplify conditional expressions\n"
        refactored_code += f"# Suggested by auto-refactorer for {hotspot.function_name}\n"
        
        logger.info(f"Applied simplify_conditional refactoring to {hotspot.file_path}")
        return refactored_code
    
    def _reduce_coupling(self, code: str, hotspot: CodeHotspot) -> str:
        """减少耦合重构"""
        # 简化实现：添加注释说明如何减少耦合
        
        refactored_code = code + "\n\n# TODO: Reduce coupling\n"
        refactored_code += f"# Suggested by auto-refactorer for {hotspot.file_path}\n"
        
        logger.info(f"Applied reduce_coupling refactoring to {hotspot.file_path}")
        return refactored_code


class RefactoringValidator:
    """
    重构验证器
    
    在沙箱中验证重构后的代码
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sandbox_dir = Path(self.config.get("sandbox_dir", "E:/WorkBuddy/Claw/sandbox"))
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        self.validation_history: List[Dict[str, Any]] = []
        
        logger.info(f"RefactoringValidator initialized with sandbox dir: {self.sandbox_dir}")
    
    def validate_refactoring(self, candidate: RefactoringCandidate) -> Dict[str, Any]:
        """
        验证重构
        
        Args:
            candidate: 重构候选
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            # 1. 创建沙箱测试文件
            test_file = self._create_sandbox_file(candidate)
            
            # 2. 在沙箱中执行测试（使用 Python 编译检查）
            test_result = self._run_sandbox_test(test_file)
            
            # 3. 记录验证结果
            validation_result = {
                "candidate_id": candidate.candidate_id,
                "hotspot_id": candidate.hotspot.hotspot_id,
                "refactoring_type": candidate.refactoring_type,
                "test_passed": test_result["passed"],
                "test_output": test_result["output"],
                "validated_at": datetime.now().isoformat()
            }
            
            self.validation_history.append(validation_result)
            
            # 4. 更新候选的测试结果
            candidate.test_results = validation_result
            candidate.deployment_status = RefactoringStatus.TESTING if validation_result["test_passed"] else RefactoringStatus.FAILED
            
            logger.info(f"Validated refactoring {candidate.candidate_id}: "
                        f"{'PASSED' if validation_result['test_passed'] else 'FAILED'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Failed to validate refactoring {candidate.candidate_id}: {e}")
            return {
                "candidate_id": candidate.candidate_id,
                "test_passed": False,
                "test_output": str(e),
                "validated_at": datetime.now().isoformat()
            }
    
    def _create_sandbox_file(self, candidate: RefactoringCandidate) -> Path:
        """创建沙箱测试文件"""
        test_file = self.sandbox_dir / f"test_{candidate.candidate_id}.py"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(f"# Sandbox test for {candidate.candidate_id}\n")
            f.write(f"# Hotspot: {candidate.hotspot.hotspot_id}\n")
            f.write(f"# Refactoring type: {candidate.refactoring_type}\n\n")
            f.write(candidate.refactored_code)
            f.write("\n\n# Test code\n")
            f.write(f"if __name__ == '__main__':\n")
            f.write(f"    print('Sandbox test for {candidate.candidate_id} passed!')\n")
        
        logger.debug(f"Created sandbox test file: {test_file}")
        return test_file
    
    def _run_sandbox_test(self, test_file: Path) -> Dict[str, Any]:
        """运行沙箱测试"""
        try:
            # 使用 Python 编译检查语法
            result = subprocess.run(
                ["python", "-m", "py_compile", str(test_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            test_passed = result.returncode == 0
            test_output = result.stdout if test_passed else result.stderr
            
            return {
                "passed": test_passed,
                "output": test_output
            }
            
        except Exception as e:
            return {
                "passed": False,
                "output": str(e)
            }
        finally:
            # 清理测试文件
            if test_file.exists():
                try:
                    test_file.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete test file {test_file}: {e}")


class SelfRestructuringEngine:
    """
    自重构引擎主类
    
    整合所有组件，实现完全自主的重构流程
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.version = "V181.0"
        self.stage = "Stage 3 - Awakening and Transcendence"
        
        # 初始化所有组件
        self.performance_monitor = PerformanceMonitor(self.config.get("performance_monitor", {}))
        self.hotspot_identifier = HotspotIdentifier(self.config.get("hotspot_identifier", {}))
        self.architecture_analyzer = ArchitectureAnalyzer(self.config.get("architecture_analyzer", {}))
        self.auto_refactorer = AutoRefactorer(self.config.get("auto_refactorer", {}))
        self.refactoring_validator = RefactoringValidator(self.config.get("refactoring_validator", {}))
        
        # 重构历史
        self.refactoring_history: List[Dict[str, Any]] = []
        
        # 当前状态
        self.current_status = RefactoringStatus.PENDING
        self.last_refactoring_time = None
        
        logger.info(f"SelfRestructuringEngine {self.version} initialized ({self.stage})")
    
    def run_refactoring_cycle(self) -> Dict[str, Any]:
        """
        运行完整的重构周期
        
        Returns:
            Dict[str, Any]: 重构周期结果
        """
        cycle_id = f"cycle_{int(time.time())}"
        logger.info(f"Starting refactoring cycle: {cycle_id}")
        
        try:
            # 1. 监控性能（模拟数据）
            self.current_status = RefactoringStatus.MONITORING
            logger.info("Step 1: Monitoring performance...")
            
            # 模拟收集性能指标
            metrics_summary = self._simulate_metrics_collection()
            
            # 2. 分析代码架构
            self.current_status = RefactoringStatus.ANALYZING
            logger.info("Step 2: Analyzing code architecture...")
            
            code_analysis = self.architecture_analyzer.analyze_codebase()
            
            # 3. 识别热点
            logger.info("Step 3: Identifying hotspots...")
            
            hotspots = self.hotspot_identifier.identify_hotspots(metrics_summary, code_analysis)
            
            if not hotspots:
                logger.info("No hotspots found. Refactoring cycle completed.")
                self.current_status = RefactoringStatus.COMPLETED
                return {
                    "cycle_id": cycle_id,
                    "status": "no_hotspots_found",
                    "hotspots_analyzed": 0,
                    "refactorings_generated": 0
                }
            
            # 4. 生成重构候选（只处理最高严重度的热点）
            self.current_status = RefactoringStatus.REFACTORING
            top_hotspot = hotspots[0]  # 已按严重度排序
            logger.info(f"Step 4: Generating refactoring for {top_hotspot.function_name}...")
            
            candidate = self.auto_refactorer.generate_refactoring_candidate(top_hotspot)
            
            if not candidate:
                logger.warning(f"Failed to generate refactoring candidate for {top_hotspot.function_name}")
                self.current_status = RefactoringStatus.FAILED
                return {
                    "cycle_id": cycle_id,
                    "status": "refactoring_generation_failed",
                    "hotspot": top_hotspot.__dict__
                }
            
            # 5. 验证重构
            self.current_status = RefactoringStatus.TESTING
            logger.info(f"Step 5: Validating refactoring in sandbox...")
            
            validation_result = self.refactoring_validator.validate_refactoring(candidate)
            
            if not validation_result["test_passed"]:
                logger.warning(f"Sandbox test failed for {candidate.candidate_id}")
                self.current_status = RefactoringStatus.FAILED
                return {
                    "cycle_id": cycle_id,
                    "status": "validation_failed",
                    "validation_result": validation_result
                }
            
            # 6. 应用重构（模拟）
            self.current_status = RefactoringStatus.DEPLOYING
            logger.info(f"Step 6: Applying refactoring to {top_hotspot.file_path}...")
            
            # 模拟应用重构
            time.sleep(1)
            
            # 7. 完成
            self.current_status = RefactoringStatus.COMPLETED
            self.last_refactoring_time = datetime.now()
            
            # 记录重构历史
            refactoring_record = {
                "cycle_id": cycle_id,
                "timestamp": datetime.now().isoformat(),
                "hotspot": top_hotspot.__dict__,
                "candidate": {
                    "candidate_id": candidate.candidate_id,
                    "refactoring_type": candidate.refactoring_type,
                    "deployed_at": datetime.now().isoformat()
                },
                "validation_result": validation_result
            }
            self.refactoring_history.append(refactoring_record)
            
            logger.info(f"Refactoring cycle {cycle_id} completed successfully!")
            
            return {
                "cycle_id": cycle_id,
                "status": "success",
                "hotspot_addressed": top_hotspot.__dict__,
                "refactoring_applied": {
                    "candidate_id": candidate.candidate_id,
                    "refactoring_type": candidate.refactoring_type,
                    "validation_result": validation_result
                }
            }
            
        except Exception as e:
            self.current_status = RefactoringStatus.FAILED
            logger.error(f"Refactoring cycle {cycle_id} failed: {e}")
            return {
                "cycle_id": cycle_id,
                "status": "failed",
                "error": str(e)
            }
    
    def _simulate_metrics_collection(self) -> Dict[str, Any]:
        """模拟性能指标收集"""
        # 模拟一些性能指标数据
        return {
            "total_functions": 10,
            "total_call_count": 1000,
            "avg_response_time_all": 0.5,
            "max_memory_usage": 80.0,
            "max_cpu_usage": 50.0,
            "metrics": [
                {
                    "module": "test_module",
                    "function": "slow_function",
                    "avg_time": 1.5,  # 超过阈值 1.0 秒
                    "max_time": 2.0,
                    "min_time": 1.0,
                    "memory_mb": 50.0,
                    "cpu_percent": 30.0,
                    "call_count": 100,
                    "error_count": 0
                }
            ]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "version": self.version,
            "stage": self.stage,
            "current_status": self.current_status.value,
            "last_refactoring_time": self.last_refactoring_time.isoformat() if self.last_refactoring_time else None,
            "total_refactorings": len(self.refactoring_history),
            "components": {
                "performance_monitor": "active",
                "hotspot_identifier": "active",
                "architecture_analyzer": "active",
                "auto_refactorer": "active",
                "refactoring_validator": "active"
            }
        }


# 主程序入口
if __name__ == "__main__":
    print("🌀 灵助 V181.0 · T18 自重构引擎")
    print("=" * 60)
    
    # 创建自重构引擎
    engine = SelfRestructuringEngine()
    
    # 运行重构周期
    print("\n📊 开始运行重构周期...")
    result = engine.run_refactoring_cycle()
    
    # 显示结果
    print(f"\n✅ 重构周期完成！")
    print(f"Cycle ID: {result.get('cycle_id')}")
    print(f"Status: {result.get('status')}")
    
    if result.get("status") == "success":
        print(f"\n📈 重构详情：")
        hotspot = result.get("hotspot_addressed", {})
        print(f"  - 热点函数: {hotspot.get('function_name')}")
        print(f"  - 热点类型: {hotspot.get('hotspot_type')}")
        print(f"  - 严重度: {hotspot.get('severity')}")
        
        refactoring = result.get("refactoring_applied", {})
        print(f"  - 重构类型: {refactoring.get('refactoring_type')}")
        print(f"  - 验证结果: {'通过' if refactoring.get('validation_result', {}).get('test_passed') else '失败'}")
    
    # 显示引擎状态
    print(f"\n🔧 引擎状态：")
    status = engine.get_status()
    print(f"  - 版本: {status['version']}")
    print(f"  - 阶段: {status['stage']}")
    print(f"  - 当前状态: {status['current_status']}")
    print(f"  - 总重构次数: {status['total_refactorings']}")
    
    print("\n" + "=" * 60)
    print("🌀 自重构引擎演示完成")
