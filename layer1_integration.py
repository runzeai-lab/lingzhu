"""
Layer 1 一体脉冲呼吸 × 四相恒转融合（V188.0）
融合 一体脉冲呼吸（Layer 1）和 四相恒转（FourPhaseScheduler）
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

# 导入四相调度器（来自三进制逻辑仿真）
try:
    from ternary_logic_simulation import FourPhaseScheduler, Phase
except ImportError:
    # 如果无法导入，提供占位符定义
    class Phase(Enum):
        EARTH_STAGNATION = "earth_stagnation"
        HUMAN_HARMONY = "human_harmony"
        HEAVEN_TRANSFORMATION = "heaven_transformation"
        HEAVEN_ADVANCE = "heaven_advance"

    class FourPhaseScheduler:
        def __init__(self):
            self.current_phase = Phase.EARTH_STAGNATION
            self.phase_start_time = datetime.now()
            self.phase_durations = {
                Phase.EARTH_STAGNATION: 300,  # 5分钟
                Phase.HUMAN_HARMONY: 450,  # 7.5分钟
                Phase.HEAVEN_TRANSFORMATION: 600,  # 10分钟
                Phase.HEAVEN_ADVANCE: 750  # 12.5分钟
            }
            self.phase_counts = {phase: 0 for phase in Phase}
            self.total_transitions = 0

        def transition(self, force: bool = False) -> bool:
            """转换到下一相位"""
            old_phase = self.current_phase
            phases = list(Phase)
            current_index = phases.index(self.current_phase)
            next_index = (current_index + 1) % len(phases)
            self.current_phase = phases[next_index]
            self.phase_start_time = datetime.now()
            self.phase_counts[self.current_phase] += 1
            self.total_transitions += 1
            return True

        def get_current_phase(self) -> Dict:
            """获取当前相位信息"""
            return {
                "phase": self.current_phase.value,
                "phase_name": self._get_phase_name(self.current_phase),
                "duration": self.phase_durations[self.current_phase],
                "elapsed": (datetime.now() - self.phase_start_time).total_seconds(),
                "count": self.phase_counts[self.current_phase]
            }

        def _get_phase_name(self, phase: Phase) -> str:
            """获取相位中文名称"""
            names = {
                Phase.EARTH_STAGNATION: "地-滞",
                Phase.HUMAN_HARMONY: "人-和",
                Phase.HEAVEN_TRANSFORMATION: "天-变",
                Phase.HEAVEN_ADVANCE: "天-进"
            }
            return names.get(phase, "未知")


class PulseState(Enum):
    """脉冲状态枚举"""
    RESTING = "resting"  # 静息态
    ACTIVE = "active"  # 激活态
    RECOVERING = "recovering"  # 恢复态
    ADAPTING = "adapting"  # 适应态


class YiTiMaiChongHuXi:
    """一体脉冲呼吸引擎 - Layer 1核心"""

    def __init__(self):
        self.current_state = PulseState.RESTING
        self.pulse_count = 0
        self.last_pulse_time = datetime.now()
        self.pulse_interval = 5.0  # 基础脉冲间隔（秒）
        self.adaptation_rate = 0.1  # 适应率
        self.energy_level = 1.0  # 能量水平
        self.state_history = []

    def generate_pulse(self, force: bool = False) -> Dict:
        """生成脉冲"""
        now = datetime.now()
        elapsed = (now - self.last_pulse_time).total_seconds()

        # 检查是否应该生成脉冲
        should_pulse = force or (elapsed >= self.pulse_interval and self.current_state == PulseState.RESTING)

        if should_pulse:
            # 生成脉冲
            self.current_state = PulseState.ACTIVE
            self.pulse_count += 1
            self.last_pulse_time = now

            pulse_info = {
                "pulse_id": self.pulse_count,
                "timestamp": now.isoformat(),
                "energy": self.energy_level,
                "state": self.current_state.value,
                "interval": self.pulse_interval
            }

            # 记录状态历史
            self.state_history.append({
                "time": now.isoformat(),
                "state": self.current_state.value,
                "pulse_id": self.pulse_count
            })

            # 脉冲后进入恢复态
            self.current_state = PulseState.RECOVERING

            return {
                "success": True,
                "pulse": pulse_info,
                "message": "脉冲生成成功"
            }
        else:
            return {
                "success": False,
                "message": f"脉冲间隔未到（{elapsed:.2f}s / {self.pulse_interval:.2f}s）",
                "next_pulse_in": max(0, self.pulse_interval - elapsed)
            }

    def adapt_pulse_interval(self, feedback: float):
        """根据反馈调整脉冲间隔"""
        # feedback: 0.0-1.0，表示任务完成质量
        # 质量高 → 缩短间隔（更频繁）
        # 质量低 → 延长间隔（更充分休息）
        delta = (feedback - 0.5) * self.adaptation_rate
        self.pulse_interval = max(1.0, min(60.0, self.pulse_interval - delta))

        # 更新能量水平
        self.energy_level = 0.5 + feedback * 0.5

        return {
            "success": True,
            "new_interval": self.pulse_interval,
            "energy_level": self.energy_level,
            "message": "脉冲间隔已调整"
        }

    def transition_state(self, new_state: PulseState = None):
        """转换状态"""
        if new_state is None:
            # 自动状态转换
            if self.current_state == PulseState.RECOVERING:
                self.current_state = PulseState.RESTING
            elif self.current_state == PulseState.ADAPTING:
                self.current_state = PulseState.RESTING
        else:
            self.current_state = new_state

        return {
            "success": True,
            "current_state": self.current_state.value,
            "message": "状态转换成功"
        }

    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "current_state": self.current_state.value,
            "pulse_count": self.pulse_count,
            "pulse_interval": self.pulse_interval,
            "energy_level": self.energy_level,
            "last_pulse_time": self.last_pulse_time.isoformat(),
            "state_history_count": len(self.state_history)
        }


class Layer1FourPhaseIntegration:
    """Layer 1 × 四相恒转 融合引擎"""

    def __init__(self):
        # 初始化两个核心引擎
        self.yiti = YiTiMaiChongHuXi()
        self.four_phase = FourPhaseScheduler()

        # 融合参数
        self.integration_depth = 0.92  # 融合深度
        self.synchronization_active = False  # 同步是否激活
        self.pulse_phase_mapping = self._create_pulse_phase_mapping()

        # 统计信息
        self.total_pulses = 0
        self.total_transitions = 0
        self.sync_count = 0

    def _create_pulse_phase_mapping(self) -> Dict:
        """创建脉冲-相位映射"""
        return {
            "resting": Phase.EARTH_STAGNATION,  # 静息 → 地-滞
            "active": Phase.HEAVEN_ADVANCE,  # 激活 → 天-进
            "recovering": Phase.HUMAN_HARMONY,  # 恢复 → 人-和
            "adaptting": Phase.HEAVEN_TRANSFORMATION  # 适应 → 天-变
        }

    def synchronize_pulse_and_phase(self, pulse_state: str = None) -> Dict:
        """同步脉冲与相位"""
        # 如果未指定脉冲状态，使用当前状态
        if pulse_state is None:
            pulse_state = self.yiti.current_state.value

        # 获取映射的相位
        target_phase = self.pulse_phase_mapping.get(pulse_state)

        if target_phase is None:
            return {
                "success": False,
                "message": f"未知的脉冲状态: {pulse_state}"
            }

        # 转换到目标相位
        old_phase = self.four_phase.current_phase
        if old_phase != target_phase:
            self.four_phase.current_phase = target_phase
            self.four_phase.phase_start_time = datetime.now()
            self.four_phase.phase_counts[target_phase] += 1
            self.total_transitions += 1

        self.synchronization_active = True
        self.sync_count += 1

        return {
            "success": True,
            "pulse_state": pulse_state,
            "target_phase": target_phase.value,
            "phase_name": self.four_phase._get_phase_name(target_phase),
            "synchronization_active": self.synchronization_active,
            "sync_count": self.sync_count,
            "message": "脉冲-相位同步成功"
        }

    def generate_synchronized_pulse(self, force: bool = False) -> Dict:
        """生成同步脉冲（脉冲生成时自动同步相位）"""
        # 生成脉冲
        pulse_result = self.yiti.generate_pulse(force)

        if pulse_result["success"]:
            # 脉冲生成成功，同步相位
            pulse_state = self.yiti.current_state.value
            sync_result = self.synchronize_pulse_and_phase(pulse_state)

            self.total_pulses += 1

            return {
                "success": True,
                "pulse": pulse_result["pulse"],
                "synchronization": sync_result,
                "integration_depth": self.integration_depth,
                "total_pulses": self.total_pulses,
                "message": "同步脉冲生成成功"
            }
        else:
            return {
                "success": False,
                "pulse_result": pulse_result,
                "message": "脉冲生成失败，未同步相位"
            }

    def adapt_and_synchronize(self, feedback: float) -> Dict:
        """调整并同步"""
        # 调整脉冲间隔
        adapt_result = self.yiti.adapt_pulse_interval(feedback)

        # 同步相位（根据调整后的状态）
        pulse_state = self.yiti.current_state.value
        sync_result = self.synchronize_pulse_and_phase(pulse_state)

        return {
            "success": True,
            "adaptation": adapt_result,
            "synchronization": sync_result,
            "integration_depth": self.integration_depth,
            "message": "调整并同步成功"
        }

    def get_integration_status(self) -> Dict:
        """获取融合状态"""
        yiti_status = self.yiti.get_status()
        phase_info = self.four_phase.get_current_phase()

        return {
            "integration_depth": self.integration_depth,
            "synchronization_active": self.synchronization_active,
            "yiti_status": yiti_status,
            "four_phase_info": phase_info,
            "total_pulses": self.total_pulses,
            "total_transitions": self.total_transitions,
            "sync_count": self.sync_count,
            "pulse_phase_mapping": {k: v.value for k, v in self.pulse_phase_mapping.items()},
            "message": "融合状态获取成功"
        }

    def reset_integration(self) -> Dict:
        """重置融合引擎"""
        self.yiti = YiTiMaiChongHuXi()
        self.four_phase = FourPhaseScheduler()
        self.synchronization_active = False
        self.total_pulses = 0
        self.total_transitions = 0
        self.sync_count = 0

        return {
            "success": True,
            "integration_depth": self.integration_depth,
            "message": "融合引擎已重置"
        }


# 创建全局融合引擎实例
layer1_fourphase = Layer1FourPhaseIntegration()

# 测试代码
if __name__ == "__main__":
    print("=== 测试 Layer 1 × 四相恒转 融合 ===\n")

    # 测试1: 生成同步脉冲
    print("【测试1: 生成同步脉冲】")
    result1 = layer1_fourphase.generate_synchronized_pulse(force=True)
    print(f"成功: {result1['success']}")
    print(f"脉冲ID: {result1['pulse']['pulse_id']}")
    print(f"同步相位: {result1['synchronization']['phase_name']}")
    print(f"融合深度: {result1['integration_depth']}")
    print()

    # 测试2: 调整并同步
    print("【测试2: 调整并同步】")
    result2 = layer1_fourphase.adapt_and_synchronize(feedback=0.8)
    print(f"成功: {result2['success']}")
    print(f"新脉冲间隔: {result2['adaptation']['new_interval']:.2f}s")
    print(f"同步相位: {result2['synchronization']['phase_name']}")
    print()

    # 测试3: 获取融合状态
    print("【测试3: 获取融合状态】")
    result3 = layer1_fourphase.get_integration_status()
    print(f"融合深度: {result3['integration_depth']}")
    print(f"同步激活: {result3['synchronization_active']}")
    print(f"总脉冲数: {result3['total_pulses']}")
    print(f"当前相位: {result3['four_phase_info']['phase_name']}")
    print()

    # 测试4: 重置融合引擎
    print("【测试4: 重置融合引擎】")
    result4 = layer1_fourphase.reset_integration()
    print(f"成功: {result4['success']}")
    print(f"消息: {result4['message']}")
    print()

    print("=== 测试完成 ===")
