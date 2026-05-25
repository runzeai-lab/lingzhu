import json
import time
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class DeviceType(Enum):
    """边缘设备类型"""
    MOBILE = "mobile"           # 移动设备（手机、平板）
    IOT = "iot"                 # IoT 设备（传感器、微控制器）
    EMBEDDED = "embedded"       # 嵌入式设备（路由器、智能家电）
    EDGE_SERVER = "edge_server" # 边缘服务器（小型服务器）
    UNKNOWN = "unknown"         # 未知设备

class EdgeInference:
    """
    边缘推理引擎 - 支持边缘设备推理
    
    功能：
    1. 边缘设备支持（移动设备、IoT 设备、嵌入式设备）
    2. 模型压缩与量化（适应边缘设备资源限制）
    3. 分布式推理（多边缘设备协同）
    4. 离线推理支持（边缘设备可能断网）
    5. 推理加速（针对边缘设备的硬件加速）
    """
    
    def __init__(self, model_dir: str = "/tmp/edge_models", max_devices: int = 10):
        self.model_dir = model_dir
        self.max_devices = max_devices
        
        # 注册的设备
        self.registered_devices = {}  # {device_id: {type, status, resources}}
        
        # 模型压缩配置
        self.compression_config = {
            "quantization_bits": 8,      # 量化位数（8bit 或 16bit）
            "pruning_ratio": 0.3,        # 剪枝比例
            "knowledge_distillation": True  # 知识蒸馏
        }
        
        # 分布式推理任务
        self.distributed_tasks = []
        
        # 离线推理缓存
        self.offline_cache = {}
        
        # 硬件加速配置
        self.hardware_acceleration = {
            "gpu": False,    # GPU 加速（如果设备有 GPU）
            "npu": False,    # NPU 加速（神经网络加速芯片）
            "dsp": False,    # DSP 加速（数字信号处理器）
            "tpu": False     # TPU 加速（Tensor Processing Unit）
        }
        
        # 性能统计
        self.stats = {
            "total_inferences": 0,
            "offline_inferences": 0,
            "distributed_inferences": 0,
            "compressed_models": 0
        }
        
        print(f"边缘推理引擎初始化完成，模型目录：{model_dir}，最大设备数：{max_devices}")
    
    # ==================== 1. 边缘设备支持 ====================
    
    def register_device(self, device_id: str, device_type: DeviceType, 
                        resources: Dict = {}) -> Dict:
        """
        注册边缘设备
        
        Args:
            device_id: 设备ID
            device_type: 设备类型（DeviceType 枚举）
            resources: 设备资源（CPU、内存、存储等）
        
        Returns:
            {"status": "registered", "device_id": str}
        """
        if len(self.registered_devices) >= self.max_devices:
            return {
                "status": "failed",
                "reason": f"已达到最大设备数 {self.max_devices}",
                "message": "设备注册失败"
            }
        
        self.registered_devices[device_id] = {
            "type": device_type.value,
            "status": "online",
            "resources": resources,
            "registered_at": str(datetime.now()),
            "last_seen": str(datetime.now())
        }
        
        print(f"[边缘设备] 设备 {device_id} ({device_type.value}) 已注册")
        
        return {
            "status": "registered",
            "device_id": device_id,
            "message": f"设备 {device_id} 注册成功"
        }
    
    def unregister_device(self, device_id: str) -> Dict:
        """注销边缘设备"""
        if device_id not in self.registered_devices:
            return {
                "status": "failed",
                "reason": "Device not found",
                "message": "设备注销失败"
            }
        
        del self.registered_devices[device_id]
        
        print(f"[边缘设备] 设备 {device_id} 已注销")
        
        return {
            "status": "unregistered",
            "device_id": device_id,
            "message": f"设备 {device_id} 注销成功"
        }
    
    def list_devices(self) -> List[Dict]:
        """列出所有注册的设备"""
        return [
            {
                "device_id": device_id,
                "type": info["type"],
                "status": info["status"],
                "resources": info["resources"]
            }
            for device_id, info in self.registered_devices.items()
        ]
    
    def update_device_status(self, device_id: str, status: str) -> Dict:
        """更新设备状态（online/offline/busy）"""
        if device_id not in self.registered_devices:
            return {
                "status": "failed",
                "reason": "Device not found"
            }
        
        self.registered_devices[device_id]["status"] = status
        self.registered_devices[device_id]["last_seen"] = str(datetime.now())
        
        return {
            "status": "updated",
            "device_id": device_id,
            "new_status": status,
            "message": f"设备 {device_id} 状态已更新为 {status}"
        }
    
    # ==================== 2. 模型压缩与量化 ====================
    
    def compress_model(self, model_name: str, technique: str = "quantization") -> Dict:
        """
        压缩模型以适应边缘设备
        
        Args:
            model_name: 模型名称
            technique: 压缩技术（quantization/pruning/distillation）
        
        Returns:
            {"status": "compressed", "compressed_model_path": str}
        """
        self.stats["compressed_models"] += 1
        
        # 模拟压缩过程
        original_size = 100  # MB（简化版）
        
        if technique == "quantization":
            # 量化：降低权重精度（FP32 → INT8）
            compressed_size = original_size * (8 / 32)  # 32bit → 8bit
            compression_ratio = 0.25
        elif technique == "pruning":
            # 剪枝：移除不重要的权重
            pruning_ratio = self.compression_config["pruning_ratio"]
            compressed_size = original_size * (1 - pruning_ratio)
            compression_ratio = 1 - pruning_ratio
        elif technique == "distillation":
            # 知识蒸馏：训练小模型模仿大模型
            compressed_size = original_size * 0.1  # 小模型通常只有大模型的 10%
            compression_ratio = 0.1
        else:
            return {
                "status": "failed",
                "reason": f"Unknown technique: {technique}"
            }
        
        compressed_model_path = f"{self.model_dir}/{model_name}_compressed_{technique}.onnx"
        
        print(f"[模型压缩] 模型 {model_name} 压缩完成，技术：{technique}")
        print(f"  原始大小：{original_size}MB，压缩后：{compressed_size:.1f}MB，压缩比：{compression_ratio:.2f}")
        
        return {
            "status": "compressed",
            "original_model": model_name,
            "technique": technique,
            "original_size_mb": original_size,
            "compressed_size_mb": round(compressed_size, 1),
            "compression_ratio": round(compression_ratio, 2),
            "compressed_model_path": compressed_model_path,
            "message": f"模型压缩完成，压缩比 {compression_ratio:.2f}"
        }
    
    def quantize_model(self, model_name: str, bits: int = 8) -> Dict:
        """
        量化模型
        
        Args:
            model_name: 模型名称
            bits: 量化位数（8 或 16）
        """
        if bits not in [8, 16]:
            return {
                "status": "failed",
                "reason": "Only 8-bit or 16-bit quantization supported"
            }
        
        self.compression_config["quantization_bits"] = bits
        
        return self.compress_model(model_name, technique="quantization")
    
    # ==================== 3. 分布式推理 ====================
    
    def distribute_inference(self, model_name: str, input_data: Dict, 
                            device_ids: List[str] = []) -> Dict:
        """
        分布式推理：将推理任务分配到多个边缘设备
        
        Args:
            model_name: 模型名称
            input_data: 输入数据
            device_ids: 指定设备（为空则自动选择）
        
        Returns:
            {"task_id": str, "status": "distributed", "results": ...}
        """
        self.stats["distributed_inferences"] += 1
        
        # 选择设备
        if not device_ids:
            # 自动选择在线设备
            device_ids = [
                device_id for device_id, info in self.registered_devices.items()
                if info["status"] == "online"
            ]
        
        if not device_ids:
            return {
                "status": "failed",
                "reason": "No online devices available"
            }
        
        # 创建分布式任务
        task_id = f"dist_{model_name}_{int(time.time())}"
        
        task = {
            "task_id": task_id,
            "model_name": model_name,
            "input_data": input_data,
            "device_ids": device_ids,
            "status": "distributing",
            "created_at": str(datetime.now()),
            "results": []
        }
        
        self.distributed_tasks.append(task)
        
        print(f"[分布式推理] 任务 {task_id} 已创建，分配到 {len(device_ids)} 个设备")
        
        # 模拟分布式推理过程（简化版）
        import random
        for device_id in device_ids:
            # 模拟每个设备的推理结果
            device_result = {
                "device_id": device_id,
                "output": random.random(),  # 模拟输出
                "inference_time_ms": random.randint(10, 100)
            }
            task["results"].append(device_result)
        
        task["status"] = "completed"
        
        return {
            "task_id": task_id,
            "status": "completed",
            "device_count": len(device_ids),
            "results": task["results"],
            "message": f"分布式推理完成，使用了 {len(device_ids)} 个设备"
        }
    
    # ==================== 4. 离线推理支持 ====================
    
    def enable_offline_inference(self, model_name: str, cache_size: int = 100) -> Dict:
        """
        启用离线推理：将模型和推理结果缓存到本地
        
        Args:
            model_name: 模型名称
            cache_size: 缓存大小（MB）
        """
        if model_name not in self.offline_cache:
            self.offline_cache[model_name] = {
                "cached_at": str(datetime.now()),
                "cache_size_mb": cache_size,
                "cached_results": []
            }
        
        print(f"[离线推理] 模型 {model_name} 已启用离线缓存（{cache_size}MB）")
        
        return {
            "status": "offline_enabled",
            "model_name": model_name,
            "cache_size_mb": cache_size,
            "message": f"模型 {model_name} 离线推理已启用"
        }
    
    def infer_offline(self, model_name: str, input_data: Dict) -> Dict:
        """
        离线推理：使用本地缓存的模型
        
        Args:
            model_name: 模型名称
            input_data: 输入数据
        """
        self.stats["offline_inferences"] += 1
        
        if model_name not in self.offline_cache:
            return {
                "status": "failed",
                "reason": "Model not cached for offline inference"
            }
        
        # 检查缓存中是否有相似输入
        cached_results = self.offline_cache[model_name]["cached_results"]
        for cached in cached_results:
            # 简化版：如果输入完全匹配，直接返回缓存结果
            if cached["input"] == input_data:
                print(f"[离线推理] 命中缓存：{model_name}")
                return {
                    "status": "offline_hit",
                    "model_name": model_name,
                    "output": cached["output"],
                    "message": "离线推理命中缓存"
                }
        
        # 未命中缓存，执行推理（简化版：随机输出）
        import random
        output = {"result": random.random(), "confidence": random.random()}
        
        # 缓存结果
        cached_results.append({
            "input": input_data,
            "output": output,
            "cached_at": str(datetime.now())
        })
        
        # 限制缓存大小
        if len(cached_results) > 100:  # 最多缓存100个结果
            cached_results.pop(0)
        
        self.offline_cache[model_name]["cached_results"] = cached_results
        
        print(f"[离线推理] 推理完成（未命中缓存）：{model_name}")
        
        return {
            "status": "offline_miss",
            "model_name": model_name,
            "output": output,
            "message": "离线推理完成（结果已缓存）"
        }
    
    # ==================== 5. 推理加速 ====================
    
    def enable_hardware_acceleration(self, device_id: str, acceleration_type: str) -> Dict:
        """
        启用硬件加速
        
        Args:
            device_id: 设备ID
            acceleration_type: 加速类型（gpu/npu/dsp/tpu）
        """
        if device_id not in self.registered_devices:
            return {
                "status": "failed",
                "reason": "Device not found"
            }
        
        if acceleration_type not in ["gpu", "npu", "dsp", "tpu"]:
            return {
                "status": "failed",
                "reason": f"Unknown acceleration type: {acceleration_type}"
            }
        
        self.hardware_acceleration[acceleration_type] = True
        
        print(f"[推理加速] 设备 {device_id} 已启用 {acceleration_type} 加速")
        
        return {
            "status": "acceleration_enabled",
            "device_id": device_id,
            "acceleration_type": acceleration_type,
            "message": f"硬件加速 {acceleration_type} 已启用"
        }
    
    def infer_with_acceleration(self, model_name: str, input_data: Dict, 
                               acceleration_type: str = "gpu") -> Dict:
        """
        使用硬件加速推理
        
        Args:
            model_name: 模型名称
            input_data: 输入数据
            acceleration_type: 加速类型
        """
        if not self.hardware_acceleration.get(acceleration_type, False):
            return {
                "status": "failed",
                "reason": f"{acceleration_type} acceleration not enabled"
            }
        
        # 模拟加速推理（简化版：推理时间更短）
        import random
        
        # 无加速时的推理时间（模拟）
        base_time = 100  # ms
        
        # 加速后的推理时间
        acceleration_factors = {
            "gpu": 0.1,   # GPU 加速 10倍
            "npu": 0.05,  # NPU 加速 20倍
            "dsp": 0.2,   # DSP 加速 5倍
            "tpu": 0.02    # TPU 加速 50倍
        }
        
        accelerated_time = base_time * acceleration_factors.get(acceleration_type, 1.0)
        
        output = {
            "result": random.random(),
            "confidence": random.random(),
            "inference_time_ms": round(accelerated_time, 2)
        }
        
        print(f"[推理加速] 使用 {acceleration_type} 加速推理，时间：{accelerated_time:.2f}ms")
        
        self.stats["total_inferences"] += 1
        
        return {
            "status": "success",
            "model_name": model_name,
            "acceleration_type": acceleration_type,
            "inference_time_ms": round(accelerated_time, 2),
            "output": output,
            "message": f"推理完成（{acceleration_type} 加速）"
        }
    
    # ==================== 统计信息 ====================
    
    def get_edge_stats(self) -> Dict:
        """获取边缘推理统计信息"""
        return {
            "stats": self.stats,
            "registered_devices": len(self.registered_devices),
            "offline_cached_models": len(self.offline_cache),
            "distributed_tasks": len(self.distributed_tasks),
            "hardware_acceleration": self.hardware_acceleration,
            "message": "边缘推理统计信息"
        }
