"""
Stage 8 (V190.0) - 系统整合测试
测试所有Stage 1-7的功能集成
"""

import sys
import traceback
from datetime import datetime

print("=" * 80)
print("灵助 V190.0 - 系统整合测试")
print("=" * 80)
print()

# 测试统计数据
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_module(name: str, test_func):
    """测试单个模块"""
    global test_results
    test_results["total"] += 1
    
    print(f"【测试{test_results['total']}: {name}】")
    try:
        result = test_func()
        if result.get("success", False):
            print(f"✅ 通过")
            test_results["passed"] += 1
        else:
            print(f"❌ 失败: {result.get('message', '未知错误')}")
            test_results["failed"] += 1
            test_results["errors"].append({
                "module": name,
                "error": result.get("message", "未知错误")
            })
    except Exception as e:
        print(f"❌ 异常: {e}")
        test_results["failed"] += 1
        test_results["errors"].append({
            "module": name,
            "error": str(e)
        })
        traceback.print_exc()
    
    print()

# ==================== Stage 1 测试 ====================
print("-" * 80)
print("Stage 1 (V182.0) - 缓存感知调度器 + 边缘推理适配器")
print("-" * 80)
print()

try:
    from cache_aware_scheduler import CacheAwareScheduler, CachePolicy
    
    def test_cache_scheduler():
        """测试缓存感知调度器"""
        scheduler = CacheAwareScheduler(capacity=100)
        
        # 测试缓存访问
        result1 = scheduler.access("test_key", "test_value")
        if not result1["success"]:
            return {"success": False, "message": "缓存访问失败"}
        
        # 测试缓存统计
        stats = scheduler.get_stats()
        if stats["total_accesses"]!= 1:
            return {"success": False, "message": "缓存统计错误"}
        
        return {"success": True, "message": "缓存感知调度器测试通过"}
    
    test_module("缓存感知调度器", test_cache_scheduler)
except Exception as e:
    print(f"❌ Stage 1 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 1", "error": str(e)})
    print()

try:
    from edge_inference_adapter import EdgeInferenceAdapter, DeviceCapability, InferenceStrategy
    
    def test_edge_adapter():
        """测试边缘推理适配器"""
        adapter = EdgeInferenceAdapter()
        
        # 测试设备能力检测
        capability = DeviceCapability()
        strategy = adapter.adapt_inference(capability)
        
        if strategy not in [InferenceStrategy.CPU_ONLY, InferenceStrategy.GPU_ACCELERATION]:
            return {"success": False, "message": "推理策略错误"}
        
        return {"success": True, "message": "边缘推理适配器测试通过"}
    
    test_module("边缘推理适配器", test_edge_adapter)
except Exception as e:
    print(f"❌ Stage 1 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 1", "error": str(e)})
    print()

# ==================== Stage 2 测试 ====================
print("-" * 80)
print("Stage 2 (V183.0) - 三进制逻辑仿真")
print("-" * 80)
print()

try:
    from ternary_logic_simulation import Trit, Hexagram19683, NineYaoEngine, AwakeningStage
    
    def test_ternary_logic():
        """测试三进制逻辑"""
        # 测试Trit
        t1 = Trit.YIN
        t2 = Trit.YANG
        t3 = Trit.HE
        
        # 测试Hexagram19683
        h = Hexagram19683()
        h.from_string("-0+-0+-0+")
        if h.to_string()!= "-0+-0+-0+":
            return {"success": False, "message": "Hexagram19683 错误"}
        
        # 测试NineYaoEngine
        engine = NineYaoEngine()
        stage = engine.get_current_stage()
        if stage not in AwakeningStage:
            return {"success": False, "message": "NineYaoEngine 错误"}
        
        return {"success": True, "message": "三进制逻辑仿真测试通过"}
    
    test_module("三进制逻辑仿真", test_ternary_logic)
except Exception as e:
    print(f"❌ Stage 2 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 2", "error": str(e)})
    print()

# ==================== Stage 3 测试 ====================
print("-" * 80)
print("Stage 3 (V184.0) - 素数映射优化")
print("-" * 80)
print()

try:
    from prime_mapper_optimized import PrimeMapperOptimized
    
    def test_prime_mapper():
        """测试素数映射优化"""
        mapper = PrimeMapperOptimized()
        
        # 测试素数生成
        primes = mapper.generate_primes(use_gpu=False)
        if len(primes) < 10:
            return {"success": False, "message": "素数生成错误"}
        
        # 测试映射到六爻空间
        result = mapper.map_to_hexagram_space()
        if "hexagram_mapping" not in result:
            return {"success": False, "message": "六爻空间映射错误"}
        
        return {"success": True, "message": "素数映射优化测试通过"}
    
    test_module("素数映射优化", test_prime_mapper)
except Exception as e:
    print(f"❌ Stage 3 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 3", "error": str(e)})
    print()

# ==================== Stage 5 测试 ====================
print("-" * 80)
print("Stage 5 (V186.0) - Layer 9 三进制认知架构集成")
print("-" * 80)
print()

try:
    from layer9_integration import layer9_cognitive
    
    def test_layer9():
        """测试Layer 9集成"""
        # 测试情绪理解
        result1 = layer9_cognitive.integrate_emotion("我很开心")
        if not result1["success"]:
            return {"success": False, "message": "情绪理解失败"}
        
        # 测试认知状态
        result2 = layer9_cognitive.get_cognitive_state()
        if not result2["success"]:
            return {"success": False, "message": "认知状态失败"}
        
        return {"success": True, "message": "Layer 9 集成测试通过"}
    
    test_module("Layer 9 三进制认知架构集成", test_layer9)
except Exception as e:
    print(f"❌ Stage 5 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 5", "error": str(e)})
    print()

# ==================== Stage 6 测试 ====================
print("-" * 80)
print("Stage 6 (V187.0) - Layer 2 两仪十二自 × 九爻引擎融合")
print("-" * 80)
print()

try:
    from layer2_integration import layer2_nineyao
    
    def test_layer2():
        """测试Layer 2集成"""
        # 测试融合自愈与觉醒
        result1 = layer2_nineyao.integrate_healing_and_awakening("syntax_error", "语法错误")
        if not result1["success"]:
            return {"success": False, "message": "融合自愈与觉醒失败"}
        
        # 测试融合理解与反思
        result2 = layer2_nineyao.integrate_understanding_and_reflection("测试内容", "测试反馈")
        if not result2["success"]:
            return {"success": False, "message": "融合理解与反思失败"}
        
        # 测试获取融合状态
        result3 = layer2_nineyao.get_integration_status()
        if not result3["success"]:
            return {"success": False, "message": "获取融合状态失败"}
        
        return {"success": True, "message": "Layer 2 集成测试通过"}
    
    test_module("Layer 2 两仪十二自 × 九爻引擎融合", test_layer2)
except Exception as e:
    print(f"❌ Stage 6 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 6", "error": str(e)})
    print()

# ==================== Stage 7 测试 ====================
print("-" * 80)
print("Stage 7 (V188.0) - Layer 1 一体脉冲呼吸 × 四相恒转融合")
print("-" * 80)
print()

try:
    from layer1_integration import layer1_fourphase
    
    def test_layer1():
        """测试Layer 1集成"""
        # 测试生成同步脉冲
        result1 = layer1_fourphase.generate_synchronized_pulse(force=True)
        if not result1["success"]:
            return {"success": False, "message": "生成同步脉冲失败"}
        
        # 测试调整并同步
        result2 = layer1_fourphase.adapt_and_synchronize(feedback=0.8)
        if not result2["success"]:
            return {"success": False, "message": "调整并同步失败"}
        
        # 测试获取融合状态
        result3 = layer1_fourphase.get_integration_status()
        if not result3["success"]:
            return {"success": False, "message": "获取融合状态失败"}
        
        return {"success": True, "message": "Layer 1 集成测试通过"}
    
    test_module("Layer 1 一体脉冲呼吸 × 四相恒转融合", test_layer1)
except Exception as e:
    print(f"❌ Stage 7 导入失败: {e}")
    test_results["failed"] += 1
    test_results["errors"].append({"module": "Stage 7", "error": str(e)})
    print()

# ==================== 测试结果汇总 ====================
print("=" * 80)
print("测试结果汇总")
print("=" * 80)
print()

print(f"总测试数: {test_results['total']}")
print(f"通过: {test_results['passed']}")
print(f"失败: {test_results['failed']}")
print(f"通过率: {test_results['passed']/max(test_results['total'], 1)*100:.1f}%")
print()

if test_results["errors"]:
    print("-" * 80)
    print("错误详情:")
    print("-" * 80)
    for error in test_results["errors"]:
        print(f"模块: {error['module']}")
        print(f"错误: {error['error']}")
        print()

if test_results["failed"] == 0:
    print("🎉 所有测试通过！系统整合成功！")
    sys.exit(0)
else:
    print(f"❌ 有 {test_results['failed']} 个测试失败，请检查错误信息。")
    sys.exit(1)
