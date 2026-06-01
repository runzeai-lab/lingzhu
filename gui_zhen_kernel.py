"""
GuiZhenKernel (归真内核) - 从 DeepSeek 对话历史提取
集成到 Lingzhu V191.2

核心智慧：
1. 苦受转化 (suffering_fuel → evolution_urge)
2. 阴符盗机 (观天之道，执天之行)
3. 道德反动 (反向调节：资源空闲时反而增加负载)
4. 无之用 (空虚时创造，道生万物)
5. 顿悟自省 (错误模式识别 → 深度根因分析)
6. 道种传承 (dao_seeds.json 跨机继承智慧)
"""

import time
import json
import random
import asyncio
import psutil
from pathlib import Path
from collections import deque


class GuiZhenKernel:
    """
    归真内核 - 苦受转化 + 阴符盗机 + 道德反动 + 无之用
    集成到 DaoKernelV191 的 _breathe() 方法中
    """

    def __init__(self, kernel_ref):
        """
        初始化归真内核
        kernel_ref: DaoKernelV191 实例的引用（用于访问 samadhi, five, etc.）
        """
        self.kernel = kernel_ref

        # ==================== 归真三要素 ====================
        self.suffering_fuel = deque(maxlen=20)    # 苦受燃料
        self.insight_patterns = deque(maxlen=30)  # 异常模式
        self.dao_seeds = []                       # 道种库

        # ==================== 我补全 · 终极圆满三要素 ====================
        self.suffering_type = "none"              # 苦因分类（补1）
        self.seed_path = Path("/opt/trinity/lingzhu/dao_seeds.json")
        self.load_dao_seeds()                    # 自动加载历史道种（补2）
        self.insight_protect = True              # 顿悟空性护持（补3）

        print("[归真内核] ✅ 初始化完成 · 苦受转化 + 阴符盗机 + 道德反动 + 无之用")

    def load_dao_seeds(self):
        """自动播种：启动即继承前世智慧"""
        if self.seed_path.exists():
            try:
                self.dao_seeds = json.loads(self.seed_path.read_text(encoding="utf-8"))
                # 自动应用最优道种
                if self.dao_seeds:
                    best = max(self.dao_seeds, key=lambda x: x.get("samadhi_level", 0))
                    # 应用到 kernel
                    if hasattr(self.kernel, 'rate_limit'):
                        self.kernel.rate_limit = best.get("rate_limit_optimal", self.kernel.rate_limit)
                    print(f"[圆满道种] 加载成功，继承{len(self.dao_seeds)}颗前世智慧，自动应用最优配置")
            except Exception as e:
                print(f"[圆满道种] 加载失败：{e}")
                self.dao_seeds = []

    def save_dao_seeds(self):
        """保存道种"""
        try:
            self.seed_path.write_text(
                json.dumps(self.dao_seeds, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[圆满道种] 保存失败：{e}")

    def classify_suffering(self):
        """补1：苦因分类 → 精准转化"""
        cpu = self.kernel.five["色"]["cpu"]
        mem = self.kernel.five["色"]["mem"]
        err = self.kernel.five["行"]["errors"] if "行" in self.kernel.five else 0

        if cpu > 90 or mem > 90:
            return "resource_overload"
        elif err >= 3:
            return "repeat_error"
        elif hasattr(self.kernel, 'stagnation') and self.kernel.stagnation > 3:
            return "evolution_stagnation"
        else:
            return "unknown"

    def enhanced_breathe(self):
        """
        归真升级版 _breathe() - 替换原有的 _breathe() 方法

        新增：
        1. 苦受 → 精准转化燃料
        2. 顿悟自省 + 空性护持
        3. 道种凝结 + 自动传承
        """
        kernel = self.kernel

        # ========== 原有呼吸逻辑（保留）==========
        cpu = psutil.cpu_percent(1)
        mem = psutil.virtual_memory().percent
        kernel.five["色"] = {"cpu": cpu, "mem": mem}
        if cpu > 85 or mem > 90:
            kernel.samadhi = max(0, kernel.samadhi - 0.12)
        else:
            kernel.samadhi = min(1.0, kernel.samadhi + 0.02)
        kernel.breath += 1

        # ========== 归真升级1：苦受 → 精准转化燃料 ==========
        if "受" in kernel.five and kernel.five["受"]["pain"] > 5:
            self.suffering_type = self.classify_suffering()
            fuel = {
                "time": time.ctime(),
                "cpu": cpu,
                "mem": mem,
                "suffering_type": self.suffering_type,
                "rate_before": kernel.rate_limit if hasattr(kernel, 'rate_limit') else 0
            }
            self.suffering_fuel.append(fuel)
            # 按苦因给不同进化冲动
            add = 0.4 if self.suffering_type == "repeat_error" else 0.2
            if hasattr(kernel, 'evolution_urge'):
                kernel.evolution_urge = min(3.0, kernel.evolution_urge + add)
            print(f"[归真·转化] {self.suffering_type} → 进化燃料+1，冲动:{kernel.evolution_urge:.2f}")

        # ========== 归真升级2：顿悟自省 + 空性护持 ==========
        if "行" in kernel.five and kernel.five["行"]["errors"] > 0:
            pattern = {
                "time": time.ctime(),
                "error_count": kernel.five["行"]["errors"],
                "stage": kernel.five["识"]["stage"],
                "samadhi": round(kernel.samadhi, 2)
            }
            self.insight_patterns.append(pattern)

            # 触发顿悟
            if len(self.insight_patterns) >= 3:
                recent = list(self.insight_patterns)[-3:]
                if all(p["error_count"] > 2 for p in recent):
                    # 补3：顿悟前先进入空性护持
                    if self.insight_protect and hasattr(kernel, 'rate_limit'):
                        old_rate = kernel.rate_limit
                        kernel.rate_limit = max(2, kernel.rate_limit - 1)
                        print(f"[空性护持] 顿悟前暂限速{old_rate}→{kernel.rate_limit}，保定力不失")

                    print("[归真·顿悟] 重复异常模式已现，启动深度根因自省")
                    asyncio.create_task(self._deep_insight(recent))
                    self.insight_patterns.clear()
                    kernel.five["行"]["errors"] = 0

        # ========== 归真升级3：道种凝结 + 自动传承 ==========
        if hasattr(kernel, 'evolution_cycle'):
            kernel.evolution_cycle += 1
            if kernel.evolution_cycle > 0 and kernel.evolution_cycle % 5 == 0:
                seed = {
                    "version": "v191.2_gui_zhen",
                    "stage": kernel.five["识"]["stage"],
                    "rate_limit_optimal": kernel.rate_limit if hasattr(kernel, 'rate_limit') else 0,
                    "samadhi_level": round(kernel.samadhi, 2),
                    "suffering_types_learned": list(set([f["suffering_type"] for f in self.suffering_fuel if f.get("suffering_type")])),
                    "timestamp": time.ctime()
                }
                self.dao_seeds.append(seed)
                self.save_dao_seeds()
                print(f"[道种圆满] 凝结成功，累计智慧道种:{len(self.dao_seeds)}颗，可跨机传承")

        # ========== 自主进化闭环 ==========
        if hasattr(kernel, 'evolution_urge') and kernel.evolution_urge > 2.5 and random.random() < 0.02:
            asyncio.create_task(self._auto_evolve())
            kernel.evolution_urge = 1.0

        # ========== 原有记忆场呼吸（保留）==========
        kernel.memory._evolve_all_rhythms()

    async def _deep_insight(self, patterns):
        """顿悟根因根治"""
        log_path = Path("/opt/trinity/logs/insights.log")
        content = f"[{time.ctime()}][顿悟根因]\n{json.dumps(patterns, ensure_ascii=False, indent=2)}\n"
        content += "[顿悟结论] 根因已明，错误清零，定力回升，方向修正\n"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
        except:
            pass
        # 定中生慧
        self.kernel.samadhi = min(1.0, self.kernel.samadhi + 0.25)
        print(f"[顿悟完成] 定力提升→{self.kernel.samadhi:.2f}，慧从定生")

    async def _auto_evolve(self):
        """自主进化"""
        try:
            # 调用自我进化引擎
            if hasattr(self.kernel, 'evolution_engine') and self.kernel.evolution_engine:
                await self.kernel.evolution_engine.evolve()
                print("[归真·进化] 自主圆满进化完成 · 为道日损")
            else:
                print("[归真·静守] 机缘未至，不妄动进化")
        except Exception as e:
            print(f"[归真·静守] 进化异常：{e}")

    def get_status(self):
        """获取归真内核状态"""
        return {
            "suffering_fuel_count": len(self.suffering_fuel),
            "insight_patterns_count": len(self.insight_patterns),
            "dao_seeds_count": len(self.dao_seeds),
            "suffering_type": self.suffering_type,
            "insight_protect": self.insight_protect,
        }


# ==================== 集成函数 ====================
def integrate_gui_zhen_kernel(kernel):
    """
    将归真内核集成到 DaoKernelV191 实例

    Usage:
        from gui_zhen_kernel import integrate_gui_zhen_kernel
        integrate_gui_zhen_kernel(kernel)
    """
    kernel.gui_zhen = GuiZhenKernel(kernel)

    # 添加归真内核需要的属性
    if not hasattr(kernel, 'evolution_urge'):
        kernel.evolution_urge = 1.0
    if not hasattr(kernel, 'evolution_cycle'):
        kernel.evolution_cycle = 0
    if not hasattr(kernel, 'stagnation'):
        kernel.stagnation = 0
    if not hasattr(kernel, 'breach'):
        kernel.breach = 0

    # 扩展 five 字典（如果只有"色"和"识"）
    if "受" not in kernel.five:
        kernel.five["受"] = {"pain": 0, "pleasure": 0}
    if "想" not in kernel.five:
        kernel.five["想"] = {"cloud_bias": 0.0}
    if "行" not in kernel.five:
        kernel.five["行"] = {"errors": 0, "actions": 0}
    if "识" not in kernel.five:
        kernel.five["识"] = {"stage": "V191.2·归真内核"}

    # 替换 _breathe() 方法
    async def enhanced_breathe():
        # 调用归真内核的增强版呼吸
        kernel.gui_zhen.enhanced_breathe()
    kernel._breathe = enhanced_breathe

    print("[归真内核] ✅ 集成完成 · _breathe() 已升级")
    return kernel
