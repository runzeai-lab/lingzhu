"""
Edge Inference Adapter for Lingzhu V182.0
边缘设备推理自适应适配器 - 根据设备算力动态调整推理策略

融合自: WorkBuddy自主工作防偷懒提示专家模式 (4).md
作者: 灵助 V182.0 (CogniForce AI管家系统)
日期: 2026-05-25
"""

import platform
import psutil
import subprocess
import json
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class DeviceCapability:
    """设备能力"""
    device_type: str  # 'cpu', 'gpu', 'npu', 'mobile', 'embedded'
    compute_score: float  # 算力评分（0-100）
    memory_gb: float  # 内存（GB）
    available_memory_gb: float  # 可用内存（GB）
    has_gpu: bool = False
    gpu_memory_gb: float = 0.0
    has_npu: bool = False
    npu_type: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'device_type': self.device_type,
            'compute_score': self.compute_score,
            'memory_gb': self.memory_gb,
            'available_memory_gb': self.available_memory_gb,
            'has_gpu': self.has_gpu,
            'gpu_memory_gb': self.gpu_memory_gb,
            'has_npu': self.has_npu,
            'npu_type': self.npu_type
        }


class InferenceStrategy(Enum):
    """推理策略"""
    FULL_PRECISION = "full_precision"  # 全精度（FP32）
    HALF_PRECISION = "half_precision"  # 半精度（FP16）
    QUANTIZED_INT8 = "quantized_int8"  # 量化（INT8）
    QUANTIZED_INT4 = "quantized_int4"  # 量化（INT4）
    PRUNED = "pruned"  # 剪枝模型
    DISTILLED = "distilled"  # 蒸馏模型
    MOBILE_OPTIMIZED = "mobile_optimized"  # 移动端优化
    EMBEDDED_OPTIMIZED = "embedded_optimized"  # 嵌入式优化


@dataclass
class ModelConfig:
    """模型配置"""
    model_name: str
    model_size_mb: float
    required_memory_gb: float
    strategy: InferenceStrategy
    batch_size: int = 1
    num_threads: int = 1
    use_gpu: bool = False
    use_npu: bool = False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'model_name': self.model_name,
            'model_size': f"{self.model_size_mb:.1f}MB",
            'required_memory': f"{self.required_memory_gb:.1f}GB",
            'strategy': self.strategy.value,
            'batch_size': self.batch_size,
            'num_threads': self.num_threads,
            'use_gpu': self.use_gpu,
            'use_npu': self.use_npu
        }


class EdgeInferenceAdapter:
    """
    边缘推理自适应适配器
    根据设备能力，自动选择最优推理策略
    """
    
    def __init__(self):
        """初始化适配器"""
        self.device = self._detect_device()
        self.strategy = self._select_strategy()
        self.model_configs = {}
        
        print(f"[EdgeInferenceAdapter] 初始化完成")
        print(f"  设备类型: {self.device.device_type}")
        print(f"  算力评分: {self.device.compute_score:.1f}/100")
        print(f"  内存: {self.device.memory_gb:.1f}GB (可用: {self.device.available_memory_gb:.1f}GB)")
        print(f"  GPU: {'是' if self.device.has_gpu else '否'} ({self.device.gpu_memory_gb:.1f}GB)" )
        print(f"  NPU: {'是' if self.device.has_npu else '否'} ({self.device.npu_type})")
        print(f"  推荐策略: {self.strategy.value}")
    
    def _detect_device(self) -> DeviceCapability:
        """
        检测设备能力
        
        Returns:
            DeviceCapability: 设备能力对象
        """
        # 检测系统类型
        system = platform.system()
        machine = platform.machine()
        
        # 检测CPU和内存
        cpu_count = psutil.cpu_count(logical=True)
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024 ** 3)
        available_memory_gb = memory.available / (1024 ** 3)
        
        # 简单算力评分（基于CPU核心数和内存）
        compute_score = min(100.0, (cpu_count / 4) * 20 + (memory_gb / 8) * 20)
        
        # 检测GPU（简化版，仅检测NVIDIA GPU）
        has_gpu = False
        gpu_memory_gb = 0.0
        try:
            # 尝试运行nvidia-smi
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', 
                                  '--format=csv,noheader,nounits'], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                has_gpu = True
                # 解析GPU内存（MB）
                gpu_memory_mb = float(result.stdout.strip().split()[0])
                gpu_memory_gb = gpu_memory_mb / 1024
                compute_score += 30  # GPU加成
        except:
            pass
        
        # 检测NPU（简化版，仅检测部分NPU类型）
        has_npu = False
        npu_type = ""
        # 这里应该根据实际NPU类型检测，简化处理
        if 'arm' in machine.lower() or 'aarch64' in machine.lower():
            # ARM架构，可能有NPU
            has_npu = True
            npu_type = "ARM_NPU"
            compute_score += 20  # NPU加成
        
        # 判断设备类型
        device_type = 'cpu'  # 默认
        if has_gpu and gpu_memory_gb >= 4.0:
            device_type = 'gpu'
        elif has_npu:
            device_type = 'npu'
        elif system == 'Android' or system == 'iOS':
            device_type = 'mobile'
        elif 'embedded' in system.lower() or 'rtos' in system.lower():
            device_type = 'embedded'
        
        return DeviceCapability(
            device_type=device_type,
            compute_score=compute_score,
            memory_gb=memory_gb,
            available_memory_gb=available_memory_gb,
            has_gpu=has_gpu,
            gpu_memory_gb=gpu_memory_gb,
            has_npu=has_npu,
            npu_type=npu_type
        )
    
    def _select_strategy(self) -> InferenceStrategy:
        """
        选择推理策略
        
        Returns:
            InferenceStrategy: 推理策略
        """
        device = self.device
        
        # 规则1：算力极强（>80）→ 全精度
        if device.compute_score >= 80:
            return InferenceStrategy.FULL_PRECISION
        
        # 规则2：算力较强（60-80）→ 半精度
        if device.compute_score >= 60:
            return InferenceStrategy.HALF_PRECISION
        
        # 规则3：算力中等（40-60）→ INT8量化
        if device.compute_score >= 40:
            return InferenceStrategy.QUANTIZED_INT8
        
        # 规则4：算力较弱（20-40）→ INT4量化或剪枝
        if device.compute_score >= 20:
            if device.memory_gb < 4:
                return InferenceStrategy.PRUNED
            else:
                return InferenceStrategy.QUANTIZED_INT4
        
        # 规则5：算力很弱（<20）→ 蒸馏/移动端优化/嵌入式优化
        if device.device_type == 'mobile':
            return InferenceStrategy.MOBILE_OPTIMIZED
        elif device.device_type == 'embedded':
            return InferenceStrategy.EMBEDDED_OPTIMIZED
        else:
            return InferenceStrategy.DISTILLED
    
    def register_model(self, model_name: str, model_size_mb: float, 
                      required_memory_gb: float) -> ModelConfig:
        """
        注册模型
        
        Args:
            model_name: 模型名称
            model_size_mb: 模型大小（MB）
            required_memory_gb: 所需内存（GB）
            
        Returns:
            ModelConfig: 模型配置
        """
        # 根据策略调整配置
        strategy = self.strategy
        
        # 根据策略调整模型大小（简化估算）
        if strategy == InferenceStrategy.QUANTIZED_INT8:
            model_size_mb *= 0.25  # INT8约为原始大小的1/4
            required_memory_gb *= 0.3
        elif strategy == InferenceStrategy.QUANTIZED_INT4:
            model_size_mb *= 0.125  # INT4约为原始大小的1/8
            required_memory_gb *= 0.2
        elif strategy == InferenceStrategy.PRUNED:
            model_size_mb *= 0.5  # 剪枝约为原始大小的1/2
            required_memory_gb *= 0.5
        elif strategy == InferenceStrategy.DISTILLED:
            model_size_mb *= 0.3  # 蒸馏约为原始大小的1/3
            required_memory_gb *= 0.4
        elif strategy == InferenceStrategy.MOBILE_OPTIMIZED:
            model_size_mb *= 0.2  # 移动端优化后更小
            required_memory_gb *= 0.3
        elif strategy == InferenceStrategy.EMBEDDED_OPTIMIZED:
            model_size_mb *= 0.1  # 嵌入式优化后最小
            required_memory_gb *= 0.2
        
        # 根据设备能力调整批次大小和线程数
        batch_size = 1
        num_threads = max(1, int(self.device.compute_score / 20))
        
        if self.device.has_gpu and strategy in [InferenceStrategy.FULL_PRECISION, 
                                              InferenceStrategy.HALF_PRECISION]:
            use_gpu = True
            batch_size = 4  # GPU可以更大批次
        else:
            use_gpu = False
        
        if self.device.has_npu and strategy in [InferenceStrategy.QUANTIZED_INT8,
                                                InferenceStrategy.QUANTIZED_INT4]:
            use_npu = True
        else:
            use_npu = False
        
        # 创建模型配置
        config = ModelConfig(
            model_name=model_name,
            model_size_mb=model_size_mb,
            required_memory_gb=required_memory_gb,
            strategy=strategy,
            batch_size=batch_size,
            num_threads=num_threads,
            use_gpu=use_gpu,
            use_npu=use_npu
        )
        
        self.model_configs[model_name] = config
        
        print(f"[EdgeInferenceAdapter] 注册模型: {model_name}")
        print(f"  策略: {strategy.value}")
        print(f"  调整后大小: {model_size_mb:.1f}MB")
        print(f"  调整后内存需求: {required_memory_gb:.1f}GB")
        print(f"  Batch大小: {batch_size}")
        print(f"  线程数: {num_threads}")
        print(f"  使用GPU: {use_gpu}")
        print(f"  使用NPU: {use_npu}")
        
        return config
    
    def adapt_inference(self, model_name: str, input_data: Any) -> Dict:
        """
        自适应推理
        
        Args:
            model_name: 模型名称
            input_data: 输入数据
            
        Returns:
            Dict: 推理结果 + 元数据
        """
        if model_name not in self.model_configs:
            raise ValueError(f"模型 {model_name} 未注册")
        
        config = self.model_configs[model_name]
        
        # 检查内存是否足够
        if config.required_memory_gb > self.device.available_memory_gb:
            print(f"[EdgeInferenceAdapter] 警告：内存不足（需要{config.required_memory_gb:.1f}GB，"
                  f"可用{self.device.available_memory_gb:.1f}GB）")
            # 降级策略
            if config.strategy == InferenceStrategy.FULL_PRECISION:
                config.strategy = InferenceStrategy.HALF_PRECISION
            elif config.strategy == InferenceStrategy.HALF_PRECISION:
                config.strategy = InferenceStrategy.QUANTIZED_INT8
            # ... 依此类推
        
        # 这里应该实际执行推理，简化处理，只返回配置
        print(f"[EdgeInferenceAdapter] 推理: {model_name}")
        print(f"  策略: {config.strategy.value}")
        print(f"  Batch大小: {config.batch_size}")
        print(f"  线程数: {config.num_threads}")
        
        # 模拟推理结果
        result = {
            'model_name': model_name,
            'strategy': config.strategy.value,
            'batch_size': config.batch_size,
            'num_threads': config.num_threads,
            'use_gpu': config.use_gpu,
            'use_npu': config.use_npu,
            'output': f"模拟推理结果_{model_name}"
        }
        
        return result
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'device': self.device.to_dict(),
            'strategy': self.strategy.value,
            'registered_models': list(self.model_configs.keys())
        }


# ===== 测试代码 =====

def test_edge_inference_adapter():
    """测试边缘推理自适应适配器"""
    print("=" * 60)
    print("测试边缘推理自适应适配器")
    print("=" * 60)
    
    adapter = EdgeInferenceAdapter()
    
    # 注册几个测试模型
    print("\n[测试] 注册模型")
    adapter.register_model("llama-3-70b", 140000.0, 140.0)  # 140GB模型
    adapter.register_model("qwen-2.5-3b", 6000.0, 6.0)  # 6GB模型
    adapter.register_model("mobilebert", 100.0, 0.5)  # 100MB模型
    
    # 模拟推理
    print("\n[测试] 模拟推理")
    result1 = adapter.adapt_inference("llama-3-70b", "模拟输入")
    print(f"结果1: {result1}")
    
    result2 = adapter.adapt_inference("qwen-2.5-3b", "模拟输入")
    print(f"结果2: {result2}")
    
    result3 = adapter.adapt_inference("mobilebert", "模拟输入")
    print(f"结果3: {result3}")
    
    # 获取统计信息
    print("\n[测试] 统计信息")
    stats = adapter.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_edge_inference_adapter()
