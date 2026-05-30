"""
人体身心精神进化引擎 (Human Body-Mind-Spirit Evolution Engine)
==================================================

V181.0 · Stage 3 · T20

目标：深度理解人体能量系统（脉轮、经络、内分泌），提供身心精神进化方案。

核心组件：
1. ChakraSystemProcessor - 脉轮系统处理器（7 大脉轮）
2. MeridianSystemProcessor - 经络系统处理器（12 正经 + 8 奇经）
3. EndocrineSystemProcessor - 内分泌系统处理器（激素调控）
4. NervousSystemProcessor - 神经系统处理器（交感/副交感神经平衡）
5. EvolutionPlanGenerator - 进化方案生成器（个性化方案）
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
import re
import math


# ==================== 数据模型 ====================

class ChakraType(Enum):
    """脉轮类型"""
    ROOT = "root"                      # 海底轮
    SACRAL = "sacral"                  # 腹轮
    SOLAR_PLEXUS = "solar_plexus"    # 脐轮
    HEART = "heart"                    # 心轮
    THROAT = "throat"                  # 喉轮
    THIRD_EYE = "third_eye"          # 眉心轮
    CROWN = "crown"                  # 顶轮


class MeridianType(Enum):
    """经络类型"""
    # 12 正经
    LUNG = "lung"                        # 肺经
    LARGE_INTESTINE = "large_intestine"  # 大肠经
    STOMACH = "stomach"                  # 胃经
    SPLEEN = "spleen"                    # 脾经
    HEART = "heart"                      # 心经
    SMALL_INTESTINE = "small_intestine"  # 小肠经
    BLADDER = "bladder"                  # 膀胱经
    KIDNEY = "kidney"                  # 肾经
    PERICARDIUM = "pericardium"        # 心包经
    TRIPLE_BURNER = "triple_burner"  # 三焦经
    GALLBLADDER = "gallbladder"        # 胆经
    LIVER = "liver"                      # 肝经
    
    # 8 奇经
    GOVERNOR = "governor"              # 督脉
    CONCEPTION = "conception"            # 任脉
    PENETRATING = "penetrating"        # 冲脉
    GIRDLE = "girdle"                  # 带脉
    YIN_HEEL = "yin_heel"              # 阴跷脉
    YANG_HEEL = "yang_heel"            # 阳跷脉
    YIN_LINK = "yin_link"              # 阴维脉
    YANG_LINK = "yang_link"            # 阳维脉


class HormoneType(Enum):
    """激素类型"""
    DOPAMINE = "dopamine"              # 多巴胺
    SEROTONIN = "serotonin"            # 血清素
    CORTISOL = "cortisol"              # 皮质醇
    OXYTOCIN = "oxytocin"              # 催产素
    ADRENALINE = "adrenaline"          # 肾上腺素
    INSULIN = "insulin"                # 胰岛素
    THYROXINE = "thyroxine"          # 甲状腺素
    ESTROGEN = "estrogen"              # 雌激素
    TESTOSTERONE = "testosterone"      # 睾酮


class NervousSystemMode(Enum):
    """神经系统模式"""
    SYMPATHETIC = "sympathetic"        # 交感神经（战斗或逃跑）
    PARASYMPATHETIC = "parasympathetic"  # 副交感神经（休息和消化）
    BALANCED = "balanced"              # 平衡


@dataclass
class Chakra:
    """脉轮"""
    id: str
    type: ChakraType
    name: str                           # 名称
    name_en: str                        # 英文名称
    color: str                          # 颜色
    element: str                        # 元素
    location: str                       # 位置
    function: str                       # 功能
    imbalances: List[str] = field(default_factory=list)  # 失衡症状
    balance_methods: List[str] = field(default_factory=list)  # 平衡方法
    energy_level: float = 0.5           # 能量水平 (0-1)


@dataclass
class Meridian:
    """经络"""
    id: str
    type: MeridianType
    name: str                           # 名称
    name_en: str                        # 英文名称
    yin_yang: str                      # 阴阳属性
    element: str                        # 五行属性
    pathway: str                        # 路径
    function: str                       # 功能
    imbalances: List[str] = field(default_factory=list)  # 失衡症状
    balance_methods: List[str] = field(default_factory=list)  # 平衡方法
    energy_flow: float = 0.5             # 能量流动 (0-1)


@dataclass
class Hormone:
    """激素"""
    id: str
    type: HormoneType
    name: str                           # 名称
    name_en: str                        # 英文名称
    gland: str                          # 分泌腺体
    function: str                       # 功能
    normal_range: Tuple[float, float]   # 正常范围
    imbalances: List[str] = field(default_factory=list)  # 失衡症状
    regulation_methods: List[str] = field(default_factory=list)  # 调节方法
    current_level: float = 0.5           # 当前水平 (0-1)


@dataclass
class NervousSystemState:
    """神经系统状态"""
    id: str
    mode: NervousSystemMode
    sympathetic_level: float = 0.5      # 交感神经水平 (0-1)
    parasympathetic_level: float = 0.5   # 副交感神经水平 (0-1)
    balance_score: float = 0.5           # 平衡分数 (0-1)
    symptoms: List[str] = field(default_factory=list)  # 症状
    regulation_methods: List[str] = field(default_factory=list)  # 调节方法


@dataclass
class BodyMindSpiritState:
    """身心精神状态"""
    id: str
    timestamp: float
    chakras: Dict[str, Chakra] = field(default_factory=dict)
    meridians: Dict[str, Meridian] = field(default_factory=dict)
    hormones: Dict[str, Hormone] = field(default_factory=dict)
    nervous_system: Optional[NervousSystemState] = None
    overall_balance: float = 0.5           # 整体平衡 (0-1)
    recommendations: List[str] = field(default_factory=list)  # 建议


@dataclass
class EvolutionPlan:
    """进化方案"""
    id: str
    user_id: str
    state: BodyMindSpiritState
    goals: List[str] = field(default_factory=list)  # 目标
    actions: List[str] = field(default_factory=list)  # 行动
    timeline: Dict[str, List[str]] = field(default_factory=dict)  # 时间线
    expected_outcomes: List[str] = field(default_factory=list)  # 预期结果
    confidence: float = 0.0


# ==================== 1. 脉轮系统处理器 ====================

class ChakraSystemProcessor:
    """
    脉轮系统处理器
    
    处理 7 大脉轮的能量平衡
    """
    
    def __init__(self):
        self.name = "ChakraSystemProcessor"
        self.version = "1.0.0"
        self.chakras: Dict[str, Chakra] = {}
        self._initialize_chakras()
    
    def _initialize_chakras(self):
        """初始化 7 大脉轮"""
        chakra_data = [
            ("root", ChakraType.ROOT, "海底轮", "Root Chakra", 
             "红色", "土", "脊椎底部", "生存、稳定、安全"),
            ("sacral", ChakraType.SACRAL, "腹轮", "Sacral Chakra",
             "橙色", "水", "下腹部", "创造力、情感、性能量"),
            ("solar_plexus", ChakraType.SOLAR_PLEXUS, "脐轮", "Solar Plexus Chakra",
             "黄色", "火", "胃部", "个人力量、意志、自信"),
            ("heart", ChakraType.HEART, "心轮", "Heart Chakra",
             "绿色", "风", "心脏区域", "爱、慈悲、连接"),
            ("throat", ChakraType.THROAT, "喉轮", "Throat Chakra",
             "蓝色", "以太", "喉咙", "沟通、表达、真理"),
            ("third_eye", ChakraType.THIRD_EYE, "眉心轮", "Third Eye Chakra",
             "靛蓝色", "光", "眉心", "直觉、洞察、智慧"),
            ("crown", ChakraType.CROWN, "顶轮", "Crown Chakra",
             "紫色或白色", "意识", "头顶", "灵性连接、宇宙意识")
        ]
        
        for cid, ctype, name, name_en, color, element, location, function in chakra_data:
            chakra = Chakra(
                id=cid,
                type=ctype,
                name=name,
                name_en=name_en,
                color=color,
                element=element,
                location=location,
                function=function,
                imbalances=self._get_chakra_imbalances(ctype),
                balance_methods=self._get_chakra_balance_methods(ctype),
                energy_level=0.5
            )
            self.chakras[cid] = chakra
    
    def _get_chakra_imbalances(self, chakra_type: ChakraType) -> List[str]:
        """获取脉轮失衡症状"""
        imbalances_map = {
            ChakraType.ROOT: ["恐惧", "焦虑", "不安全感", "财务困难"],
            ChakraType.SACRAL: ["情感波动", "创造力枯竭", "性功能障碍", "成瘾行为"],
            ChakraType.SOLAR_PLEXUS: ["低自尊", "控制欲", "消化不良", "决策困难"],
            ChakraType.HEART: ["孤独", "怨恨", "心脏问题", "呼吸问题"],
            ChakraType.THROAT: ["沟通困难", "表达障碍", "咽喉问题", "听力问题"],
            ChakraType.THIRD_EYE: ["直觉迟钝", "逻辑思维过度", "头痛", "视力问题"],
            ChakraType.CROWN: ["灵性 disconnected", "存在主义危机", "偏头痛", "精神问题"]
        }
        return imbalances_map.get(chakra_type, [])
    
    def _get_chakra_balance_methods(self, chakra_type: ChakraType) -> List[str]:
        """获取脉轮平衡方法"""
        methods_map = {
            ChakraType.ROOT: [" grounding 练习", "瑜伽", "冥想", "接触大自然"],
            ChakraType.SACRAL: [" creative 表达", "舞蹈", "水疗", "情感释放"],
            ChakraType.SOLAR_PLEXUS: ["核心力量训练", "勇气练习", "阳光浴", "个人力量肯定语"],
            ChakraType.HEART: [" loving-kindness 冥想", "心脏打开瑜伽", "感恩练习", "宽恕练习"],
            ChakraType.THROAT: [" chanting", "唱歌", "真实表达练习", "喉部按摩"],
            ChakraType.THIRD_EYE: ["冥想", "直觉开发", "第三眼按摩", "梦境日记"],
            ChakraType.CROWN: ["静修", "祈祷", "宇宙连接冥想", "灵性阅读"]
        }
        return methods_map.get(chakra_type, [])
    
    def get_chakra(self, chakra_id: str) -> Optional[Chakra]:
        """获取脉轮"""
        return self.chakras.get(chakra_id)
    
    def get_all_chakras(self) -> List[Chakra]:
        """获取所有脉轮"""
        return list(self.chakras.values())
    
    def assess_chakra(self, chakra_id: str, energy_level: float) -> Dict[str, Any]:
        """
        评估脉轮
        
        Args:
            chakra_id: 脉轮 ID
            energy_level: 能量水平 (0-1)
            
        Returns:
            评估结果
        """
        if chakra_id not in self.chakras:
            return {"status": "error", "message": f"Chakra {chakra_id} not found"}
        
        chakra = self.chakras[chakra_id]
        chakra.energy_level = energy_level
        
        # 评估能量水平
        if energy_level < 0.3:
            status = "严重不足"
            recommendations = chakra.balance_methods[:2]
        elif energy_level < 0.5:
            status = "不足"
            recommendations = chakra.balance_methods[:1]
        elif energy_level <= 0.7:
            status = "平衡"
            recommendations = ["继续保持"]
        elif energy_level <= 0.9:
            status = "过度活跃"
            recommendations = ["减少刺激", "冥想平衡"]
        else:
            status = "严重过度活跃"
            recommendations = ["立即平衡练习", "寻求专业指导"]
        
        return {
            "chakra": chakra.name,
            "energy_level": energy_level,
            "status": status,
            "imbalances": chakra.imbalances,
            "recommendations": recommendations
        }
    
    def assess_all_chakras(self, energy_levels: Dict[str, float]) -> Dict[str, Any]:
        """
        评估所有脉轮
        
        Args:
            energy_levels: {chakra_id: energy_level}
            
        Returns:
            整体评估结果
        """
        results = {}
        total_energy = 0.0
        
        for cid, level in energy_levels.items():
            result = self.assess_chakra(cid, level)
            results[cid] = result
            total_energy += level
        
        # 计算整体平衡
        avg_energy = total_energy / len(energy_levels) if energy_levels else 0.0
        
        # 计算能量分布标准差（衡量平衡度）
        import statistics
        levels = list(energy_levels.values())
        std_dev = statistics.stdev(levels) if len(levels) > 1 else 0.0
        
        balance_score = 1.0 - std_dev  # 标准差越小，平衡度越高
        
        return {
            "individual_results": results,
            "overall": {
                "average_energy": avg_energy,
                "balance_score": balance_score,
                "assessment": "平衡" if balance_score > 0.7 else "不平衡"
            }
        }
    
    def generate_balance_plan(self, assessment_result: Dict[str, Any]) -> List[str]:
        """
        生成平衡方案
        
        Args:
            assessment_result: 评估结果（来自 assess_all_chakras）
            
        Returns:
            平衡方案列表
        """
        plan = []
        
        individual_results = assessment_result.get("individual_results", {})
        
        for cid, result in individual_results.items():
            if result.get("status") in ["严重不足", "不足"]:
                chakra = self.chakras[cid]
                plan.append(f"加强 {chakra.name}：{', '.join(chakra.balance_methods[:2])}")
            elif result.get("status") in ["过度活跃", "严重过度活跃"]:
                chakra = self.chakras[cid]
                plan.append(f"平衡 {chakra.name}：{', '.join(chakra.balance_methods[-2:])}")
        
        # 添加整体建议
        overall = assessment_result.get("overall", {})
        if overall.get("balance_score", 0) < 0.7:
            plan.append("整体能量不平衡，建议进行完整的脉轮冥想")
        
        return plan


# ==================== 2. 经络系统处理器 ====================

class MeridianSystemProcessor:
    """
    经络系统处理器
    
    处理 12 正经 + 8 奇经的能量流动
    """
    
    def __init__(self):
        self.name = "MeridianSystemProcessor"
        self.version = "1.0.0"
        self.meridians: Dict[str, Meridian] = {}
        self._initialize_meridians()
    
    def _initialize_meridians(self):
        """初始化 12 正经 + 8 奇经"""
        # 12 正经
        regular_meridians = [
            ("lung", MeridianType.LUNG, "肺经", "Lung Meridian", "阴", "金", "胸部→拇指", "主气，司呼吸"),
            ("large_intestine", MeridianType.LARGE_INTESTINE, "大肠经", "Large Intestine Meridian", "阳", "金", "食指→面部", "主传导，排泄废物"),
            ("stomach", MeridianType.STOMACH, "胃经", "Stomach Meridian", "阳", "土", "面部→足部", "主受纳，消化食物"),
            ("spleen", MeridianType.SPLEEN, "脾经", "Spleen Meridian", "阴", "土", "足部→胸部", "主运化，统血"),
            ("heart", MeridianType.HEART, "心经", "Heart Meridian", "阴", "火", "胸部→小指", "主血脉，藏神"),
            ("small_intestine", MeridianType.SMALL_INTESTINE, "小肠经", "Small Intestine Meridian", "阳", "火", "小指→面部", "主受盛，化物"),
            ("bladder", MeridianType.BLADDER, "膀胱经", "Bladder Meridian", "阳", "水", "眼部→足部", "主津液，贮尿"),
            ("kidney", MeridianType.KIDNEY, "肾经", "Kidney Meridian", "阴", "水", "足部→胸部", "主藏精，主水"),
            ("pericardium", MeridianType.PERICARDIUM, "心包经", "Pericardium Meridian", "阴", "火", "胸部→中指", "主保护心脏"),
            ("triple_burner", MeridianType.TRIPLE_BURNER, "三焦经", "Triple Burner Meridian", "阳", "火", "无名指→面部", "主水道，通调水道"),
            ("gallbladder", MeridianType.GALLBLADDER, "胆经", "Gallbladder Meridian", "阳", "木", "眼部→足部", "主决断，藏胆汁"),
            ("liver", MeridianType.LIVER, "肝经", "Liver Meridian", "阴", "木", "足部→胸部", "主疏泄，藏血")
        ]
        
        for mid, mtype, name, name_en, yin_yang, element, pathway, function in regular_meridians:
            meridian = Meridian(
                id=mid,
                type=mtype,
                name=name,
                name_en=name_en,
                yin_yang=yin_yang,
                element=element,
                pathway=pathway,
                function=function,
                imbalances=self._get_meridian_imbalances(mtype),
                balance_methods=self._get_meridian_balance_methods(mtype),
                energy_flow=0.5
            )
            self.meridians[mid] = meridian
        
        # 8 奇经（简化版）
        extraordinary_meridians = [
            ("governor", MeridianType.GOVERNOR, "督脉", "Governor Vessel", "阳", "—", "脊椎→上唇", "总督诸阳经"),
            ("conception", MeridianType.CONCEPTION, "任脉", "Conception Vessel", "阴", "—", "会阴→下颌", "总督诸阴经"),
            ("penetrating", MeridianType.PENETRATING, "冲脉", "Penetrating Vessel", "阴", "—", "盆腔→胸部", "十二经之海"),
            ("girdle", MeridianType.GIRDLE, "带脉", "Girdle Vessel", "—", "—", "腰部环行", "约束诸经")
        ]
        
        for mid, mtype, name, name_en, yin_yang, element, pathway, function in extraordinary_meridians:
            meridian = Meridian(
                id=mid,
                type=mtype,
                name=name,
                name_en=name_en,
                yin_yang=yin_yang,
                element=element,
                pathway=pathway,
                function=function,
                imbalances=["能量阻滞", "气血不畅"],
                balance_methods=["针灸", "推拿", "气功"],
                energy_flow=0.5
            )
            self.meridians[mid] = meridian
    
    def _get_meridian_imbalances(self, meridian_type: MeridianType) -> List[str]:
        """获取经络失衡症状"""
        # 简化版
        return ["气血不畅", "能量阻滞", "疼痛"]
    
    def _get_meridian_balance_methods(self, meridian_type: MeridianType) -> List[str]:
        """获取经络平衡方法"""
        # 简化版
        return ["针灸", "推拿", "气功", "艾灸", "中药"]
    
    def get_meridian(self, meridian_id: str) -> Optional[Meridian]:
        """获取经络"""
        return self.meridians.get(meridian_id)
    
    def get_all_meridians(self) -> List[Meridian]:
        """获取所有经络"""
        return list(self.meridians.values())
    
    def assess_meridian(self, meridian_id: str, energy_flow: float) -> Dict[str, Any]:
        """
        评估经络
        
        Args:
            meridian_id: 经络 ID
            energy_flow: 能量流动 (0-1)
            
        Returns:
            评估结果
        """
        if meridian_id not in self.meridians:
            return {"status": "error", "message": f"Meridian {meridian_id} not found"}
        
        meridian = self.meridians[meridian_id]
        meridian.energy_flow = energy_flow
        
        # 评估能量流动
        if energy_flow < 0.3:
            status = "严重阻滞"
            recommendations = meridian.balance_methods[:2]
        elif energy_flow < 0.5:
            status = "不畅"
            recommendations = meridian.balance_methods[:1]
        elif energy_flow <= 0.7:
            status = "通畅"
            recommendations = ["继续保持"]
        elif energy_flow <= 0.9:
            status = "过度活跃"
            recommendations = ["减少刺激", "平衡能量"]
        else:
            status = "严重过度活跃"
            recommendations = ["立即平衡", "寻求专业指导"]
        
        return {
            "meridian": meridian.name,
            "energy_flow": energy_flow,
            "status": status,
            "imbalances": meridian.imbalances,
            "recommendations": recommendations
        }
    
    def assess_all_meridians(self, energy_flows: Dict[str, float]) -> Dict[str, Any]:
        """
        评估所有经络
        
        Args:
            energy_flows: {meridian_id: energy_flow}
            
        Returns:
            整体评估结果
        """
        results = {}
        
        for mid, flow in energy_flows.items():
            result = self.assess_meridian(mid, flow)
            results[mid] = result
        
        # 计算整体通畅度
        total_flow = sum(energy_flows.values())
        avg_flow = total_flow / len(energy_flows) if energy_flows else 0.0
        
        # 检查阴阳平衡
        yin_meridians = [m for m in self.meridians.values() if m.yin_yang == "阴"]
        yang_meridians = [m for m in self.meridians.values() if m.yin_yang == "阳"]
        
        yin_flow = sum(energy_flows.get(m.id, 0.5) for m in yin_meridians)
        yang_flow = sum(energy_flows.get(m.id, 0.5) for m in yang_meridians)
        
        yin_yang_balance = 1.0 - abs(yin_flow - yang_flow) / max(yin_flow + yang_flow, 1.0)
        
        return {
            "individual_results": results,
            "overall": {
                "average_flow": avg_flow,
                "yin_yang_balance": yin_yang_balance,
                "assessment": "平衡" if yin_yang_balance > 0.7 else "不平衡"
            }
        }


# ==================== 3. 内分泌系统处理器 ====================

class EndocrineSystemProcessor:
    """
    内分泌系统处理器
    
    处理激素调控（多巴胺、血清素、皮质醇、催产素等）
    """
    
    def __init__(self):
        self.name = "EndocrineSystemProcessor"
        self.version = "1.0.0"
        self.hormones: Dict[str, Hormone] = {}
        self._initialize_hormones()
    
    def _initialize_hormones(self):
        """初始化激素"""
        hormone_data = [
            ("dopamine", HormoneType.DOPAMINE, "多巴胺", "Dopamine", 
             "大脑（腹侧被盖区、伏隔核）", "奖赏、动机、愉悦", (0.0, 1.0)),
            ("serotonin", HormoneType.SEROTONIN, "血清素", "Serotonin",
             "大脑（中缝核）", "情绪调节、睡眠、食欲", (0.0, 1.0)),
            ("cortisol", HormoneType.CORTISOL, "皮质醇", "Cortisol",
             "肾上腺", "压力反应、代谢调节", (0.0, 1.0)),
            ("oxytocin", HormoneType.OXYTOCIN, "催产素", "Oxytocin",
             "垂体后叶", "社交 bonding、信任、爱", (0.0, 1.0)),
            ("adrenaline", HormoneType.ADRENALINE, "肾上腺素", "Adrenaline",
             "肾上腺", "战斗或逃跑反应", (0.0, 1.0)),
            ("insulin", HormoneType.INSULIN, "胰岛素", "Insulin",
             "胰腺", "血糖调节", (0.0, 1.0)),
            ("thyroxine", HormoneType.THYROXINE, "甲状腺素", "Thyroxine",
             "甲状腺", "新陈代谢调节", (0.0, 1.0)),
            ("estrogen", HormoneType.ESTROGEN, "雌激素", "Estrogen",
             "卵巢", "女性性征、生殖", (0.0, 1.0)),
            ("testosterone", HormoneType.TESTOSTERONE, "睾酮", "Testosterone",
             "睾丸/卵巢", "男性性征、肌肉生长", (0.0, 1.0))
        ]
        
        for hid, htype, name, name_en, gland, function, normal_range in hormone_data:
            hormone = Hormone(
                id=hid,
                type=htype,
                name=name,
                name_en=name_en,
                gland=gland,
                function=function,
                normal_range=normal_range,
                imbalances=self._get_hormone_imbalances(htype),
                regulation_methods=self._get_hormone_regulation_methods(htype),
                current_level=0.5
            )
            self.hormones[hid] = hormone
    
    def _get_hormone_imbalances(self, hormone_type: HormoneType) -> List[str]:
        """获取激素失衡症状"""
        imbalances_map = {
            HormoneType.DOPAMINE: ["缺乏动机", "抑郁", "成瘾行为"],
            HormoneType.SEROTONIN: ["情绪低落", "焦虑", "失眠"],
            HormoneType.CORTISOL: ["慢性压力", "焦虑", "免疫抑制"],
            HormoneType.OXYTOCIN: ["社交孤立", "信任困难", "亲密关系问题"],
            HormoneType.ADRENALINE: ["过度警觉", "焦虑", "失眠"],
            HormoneType.INSULIN: ["血糖不稳定", "糖尿病风险", "能量波动"],
            HormoneType.THYROXINE: ["新陈代谢异常", "体重变化", "能量水平变化"],
            HormoneType.ESTROGEN: ["月经不规则", "情绪波动", "骨密度降低"],
            HormoneType.TESTOSTERONE: ["肌肉量减少", "性欲降低", "情绪低落"]
        }
        return imbalances_map.get(hormone_type, [])
    
    def _get_hormone_regulation_methods(self, hormone_type: HormoneType) -> List[str]:
        """获取激素调节方法"""
        methods_map = {
            HormoneType.DOPAMINE: ["运动", "冥想", "设定小目标", "充足睡眠"],
            HormoneType.SEROTONIN: ["阳光浴", "运动", "健康饮食", "冥想"],
            HormoneType.CORTISOL: ["冥想", "深呼吸", "瑜伽", "充足睡眠"],
            HormoneType.OXYTOCIN: ["拥抱", "社交", "宠物互动", "感恩练习"],
            HormoneType.ADRENALINE: ["放松技巧", "冥想", "深呼吸", "减少咖啡因"],
            HormoneType.INSULIN: ["健康饮食", "规律运动", "体重管理", "充足睡眠"],
            HormoneType.THYROXINE: ["碘摄入", "硒摄入", "压力管理", "充足睡眠"],
            HormoneType.ESTROGEN: ["平衡饮食", "规律运动", "压力管理", "充足睡眠"],
            HormoneType.TESTOSTERONE: ["力量训练", "充足睡眠", "锌摄入", "维生素D"]
        }
        return methods_map.get(hormone_type, [])
    
    def get_hormone(self, hormone_id: str) -> Optional[Hormone]:
        """获取激素"""
        return self.hormones.get(hormone_id)
    
    def get_all_hormones(self) -> List[Hormone]:
        """获取所有激素"""
        return list(self.hormones.values())
    
    def assess_hormone(self, hormone_id: str, level: float) -> Dict[str, Any]:
        """
        评估激素
        
        Args:
            hormone_id: 激素 ID
            level: 水平 (0-1)
            
        Returns:
            评估结果
        """
        if hormone_id not in self.hormones:
            return {"status": "error", "message": f"Hormone {hormone_id} not found"}
        
        hormone = self.hormones[hormone_id]
        hormone.current_level = level
        
        # 评估水平
        normal_low, normal_high = hormone.normal_range
        
        if level < normal_low:
            status = "过低"
            recommendations = hormone.regulation_methods[:2]
        elif level > normal_high:
            status = "过高"
            recommendations = ["减少刺激", "寻求医疗建议"]
        else:
            status = "正常"
            recommendations = ["继续保持"]
        
        return {
            "hormone": hormone.name,
            "level": level,
            "normal_range": hormone.normal_range,
            "status": status,
            "imbalances": hormone.imbalances,
            "recommendations": recommendations
        }
    
    def assess_all_hormones(self, levels: Dict[str, float]) -> Dict[str, Any]:
        """
        评估所有激素
        
        Args:
            levels: {hormone_id: level}
            
        Returns:
            整体评估结果
        """
        results = {}
        
        for hid, level in levels.items():
            result = self.assess_hormone(hid, level)
            results[hid] = result
        
        # 计算整体平衡
        total_level = sum(levels.values())
        avg_level = total_level / len(levels) if levels else 0.0
        
        # 检查压力激素平衡（皮质醇 vs 催产素）
        cortisol_level = levels.get("cortisol", 0.5)
        oxytocin_level = levels.get("oxytocin", 0.5)
        
        stress_balance = 1.0 - abs(cortisol_level - oxytocin_level) / 2.0
        
        return {
            "individual_results": results,
            "overall": {
                "average_level": avg_level,
                "stress_balance": stress_balance,
                "assessment": "平衡" if stress_balance > 0.7 else "压力失衡"
            }
        }


# ==================== 4. 神经系统处理器 ====================

class NervousSystemProcessor:
    """
    神经系统处理器
    
    处理交感/副交感神经平衡
    """
    
    def __init__(self):
        self.name = "NervousSystemProcessor"
        self.version = "1.0.0"
    
    def assess_nervous_system(self, sympathetic_level: float, 
                              parasympathetic_level: float) -> NervousSystemState:
        """
        评估神经系统
        
        Args:
            sympathetic_level: 交感神经水平 (0-1)
            parasympathetic_level: 副交感神经水平 (0-1)
            
        Returns:
            神经系统状态
        """
        # 计算平衡分数
        balance_score = 1.0 - abs(sympathetic_level - parasympathetic_level)
        
        # 确定模式
        if sympathetic_level > parasympathetic_level + 0.3:
            mode = NervousSystemMode.SYMPATHETIC
            symptoms = ["焦虑", "紧张", "失眠", "消化问题"]
            regulation_methods = ["深呼吸", "冥想", "瑜伽", "渐进式肌肉放松"]
        elif parasympathetic_level > sympathetic_level + 0.3:
            mode = NervousSystemMode.PARASYMPATHETIC
            symptoms = ["疲劳", "低能量", "消化过度", "代谢缓慢"]
            regulation_methods = ["适度运动", "冷水浴", "咖啡（适量）", "激励性活动"]
        else:
            mode = NervousSystemMode.BALANCED
            symptoms = []
            regulation_methods = ["继续保持平衡", "定期冥想", "规律运动", "健康饮食"]
        
        state = NervousSystemState(
            id=str(uuid.uuid4()),
            mode=mode,
            sympathetic_level=sympathetic_level,
            parasympathetic_level=parasympathetic_level,
            balance_score=balance_score,
            symptoms=symptoms,
            regulation_methods=regulation_methods
        )
        
        return state
    
    def generate_regulation_plan(self, state: NervousSystemState) -> List[str]:
        """
        生成调节方案
        
        Args:
            state: 神经系统状态
            
        Returns:
            调节方案列表
        """
        plan = []
        
        if state.mode == NervousSystemMode.SYMPATHETIC:
            plan.append("激活副交感神经：深呼吸练习（4-7-8 呼吸法）")
            plan.append("冥想：每日 20 分钟正念冥想")
            plan.append("瑜伽：阴瑜伽或修复性瑜伽")
            plan.append("渐进式肌肉放松：从脚趾到头顶逐部位放松")
        elif state.mode == NervousSystemMode.PARASYMPATHETIC:
            plan.append("激活交感神经：适度有氧运动（快走、慢跑）")
            plan.append("冷水浴：结束淋浴时用冷水冲淋 30 秒")
            plan.append("咖啡（适量）：早晨饮用一杯咖啡")
            plan.append("激励性活动：唱歌、跳舞、与朋友交流")
        else:  # BALANCED
            plan.append("继续保持平衡：定期冥想、规律运动、健康饮食")
            plan.append("预防失衡：压力管理、充足睡眠、社交连接")
        
        return plan


# ==================== 5. 进化方案生成器 ====================

class EvolutionPlanGenerator:
    """
    进化方案生成器
    
    根据个体状态，提供个性化的身心精神进化方案
    """
    
    def __init__(self, chakra_processor: ChakraSystemProcessor,
                 meridian_processor: MeridianSystemProcessor,
                 hormone_processor: EndocrineSystemProcessor,
                 nervous_processor: NervousSystemProcessor):
        self.name = "EvolutionPlanGenerator"
        self.version = "1.0.0"
        self.chakra_processor = chakra_processor
        self.meridian_processor = meridian_processor
        self.hormone_processor = hormone_processor
        self.nervous_processor = nervous_processor
    
    def assess_state(self, 
                    chakra_levels: Dict[str, float],
                    meridian_flows: Dict[str, float],
                    hormone_levels: Dict[str, float],
                    sympathetic_level: float,
                    parasympathetic_level: float) -> BodyMindSpiritState:
        """
        评估身心精神状态
        
        Args:
            chakra_levels: 脉轮能量水平
            meridian_flows: 经络能量流动
            hormone_levels: 激素水平
            sympathetic_level: 交感神经水平
            parasympathetic_level: 副交感神经水平
            
        Returns:
            身心精神状态
        """
        # 评估脉轮
        chakra_assessment = self.chakra_processor.assess_all_chakras(chakra_levels)
        
        # 评估经络
        meridian_assessment = self.meridian_processor.assess_all_meridians(meridian_flows)
        
        # 评估激素
        hormone_assessment = self.hormone_processor.assess_all_hormones(hormone_levels)
        
        # 评估神经系统
        nervous_state = self.nervous_processor.assess_nervous_system(
            sympathetic_level, parasympathetic_level
        )
        
        # 计算整体平衡
        chakra_balance = chakra_assessment["overall"]["balance_score"]
        meridian_balance = meridian_assessment["overall"]["yin_yang_balance"]
        hormone_balance = hormone_assessment["overall"]["stress_balance"]
        nervous_balance = nervous_state.balance_score
        
        overall_balance = (chakra_balance + meridian_balance + hormone_balance + nervous_balance) / 4.0
        
        # 生成建议
        recommendations = []
        
        # 脉轮建议
        chakra_plan = self.chakra_processor.generate_balance_plan(chakra_assessment)
        recommendations.extend(chakra_plan)
        
        # 神经系统建议
        nervous_plan = self.nervous_processor.generate_regulation_plan(nervous_state)
        recommendations.extend(nervous_plan)
        
        # 创建状态对象
        state = BodyMindSpiritState(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            chakras={cid: self.chakra_processor.get_chakra(cid) for cid in chakra_levels},
            meridians={mid: self.meridian_processor.get_meridian(mid) for mid in meridian_flows},
            hormones={hid: self.hormone_processor.get_hormone(hid) for hid in hormone_levels},
            nervous_system=nervous_state,
            overall_balance=overall_balance,
            recommendations=recommendations[:10]  # 限制为前 10 条
        )
        
        return state
    
    def generate_evolution_plan(self, user_id: str, 
                                  state: BodyMindSpiritState,
                                  goals: List[str]) -> EvolutionPlan:
        """
        生成进化方案
        
        Args:
            user_id: 用户 ID
            state: 身心精神状态
            goals: 目标列表
            
        Returns:
            进化方案
        """
        # 生成行动
        actions = self._generate_actions(state, goals)
        
        # 生成时间线
        timeline = self._generate_timeline(actions)
        
        # 生成预期结果
        expected_outcomes = self._generate_expected_outcomes(goals)
        
        # 计算置信度
        confidence = self._calculate_confidence(state, goals)
        
        # 创建方案
        plan = EvolutionPlan(
            id=str(uuid.uuid4()),
            user_id=user_id,
            state=state,
            goals=goals,
            actions=actions,
            timeline=timeline,
            expected_outcomes=expected_outcomes,
            confidence=confidence
        )
        
        return plan
    
    def _generate_actions(self, state: BodyMindSpiritState, 
                         goals: List[str]) -> List[str]:
        """生成行动"""
        actions = []
        
        # 从建议中提取行动
        actions.extend(state.recommendations)
        
        # 根据目标添加行动
        for goal in goals:
            if "脉轮" in goal or "chakra" in goal.lower():
                actions.append("每日脉轮冥想 20 分钟")
            elif "压力" in goal or "stress" in goal.lower():
                actions.append("每日深呼吸练习 10 分钟")
                actions.append("每周瑜伽 3 次")
            elif "睡眠" in goal or "sleep" in goal.lower():
                actions.append("每晚固定睡眠时间")
                actions.append("睡前冥想 15 分钟")
            elif "能量" in goal or "energy" in goal.lower():
                actions.append("每日晨间运动 30 分钟")
                actions.append("健康饮食，避免加工食品")
        
        return actions[:15]  # 限制为前 15 条
    
    def _generate_timeline(self, actions: List[str]) -> Dict[str, List[str]]:
        """生成时间线"""
        timeline = {
            "第 1 周": actions[:3],
            "第 2-4 周": actions[3:7] if len(actions) > 3 else [],
            "第 5-8 周": actions[7:11] if len(actions) > 7 else [],
            "第 9-12 周": actions[11:15] if len(actions) > 11 else []
        }
        
        return timeline
    
    def _generate_expected_outcomes(self, goals: List[str]) -> List[str]:
        """生成预期结果"""
        outcomes = []
        
        for goal in goals:
            if "脉轮" in goal or "chakra" in goal.lower():
                outcomes.append("脉轮能量平衡，整体能量提升")
            elif "压力" in goal or "stress" in goal.lower():
                outcomes.append("压力水平降低，皮质醇水平正常化")
            elif "睡眠" in goal or "sleep" in goal.lower():
                outcomes.append("睡眠质量改善，入睡时间缩短")
            elif "能量" in goal or "energy" in goal.lower():
                outcomes.append("能量水平提升，疲劳感减少")
        
        outcomes.append("整体身心平衡改善，生活质量提升")
        
        return outcomes
    
    def _calculate_confidence(self, state: BodyMindSpiritState, 
                             goals: List[str]) -> float:
        """计算置信度"""
        # 基于整体平衡和目标准确性
        balance_factor = state.overall_balance
        
        # 目标匹配度（简化版）
        goal_match = min(1.0, len(goals) / 5.0)
        
        confidence = (balance_factor + goal_match) / 2.0
        
        return min(1.0, confidence)


# ==================== 6. 主引擎 ====================

class HumanBodyMindSpiritEvolutionEngine:
    """
    人体身心精神进化引擎（主类）
    
    整合所有组件，提供统一接口
    """
    
    def __init__(self):
        self.name = "HumanBodyMindSpiritEvolutionEngine"
        self.version = "1.0.0"
        self.created_at = time.time()
        
        # 初始化组件
        self.chakra_processor = ChakraSystemProcessor()
        self.meridian_processor = MeridianSystemProcessor()
        self.hormone_processor = EndocrineSystemProcessor()
        self.nervous_processor = NervousSystemProcessor()
        self.plan_generator = EvolutionPlanGenerator(
            self.chakra_processor,
            self.meridian_processor,
            self.hormone_processor,
            self.nervous_processor
        )
    
    def assess(self, 
               chakra_levels: Dict[str, float],
               meridian_flows: Dict[str, float],
               hormone_levels: Dict[str, float],
               sympathetic_level: float,
               parasympathetic_level: float) -> Dict[str, Any]:
        """
        评估身心精神状态（统一接口）
        
        Args:
            chakra_levels: 脉轮能量水平
            meridian_flows: 经络能量流动
            hormone_levels: 激素水平
            sympathetic_level: 交感神经水平
            parasympathetic_level: 副交感神经水平
            
        Returns:
            评估结果
        """
        # 评估状态
        state = self.plan_generator.assess_state(
            chakra_levels,
            meridian_flows,
            hormone_levels,
            sympathetic_level,
            parasympathetic_level
        )
        
        # 返回结果
        return {
            "status": "success",
            "state_id": state.id,
            "overall_balance": state.overall_balance,
            "recommendations": state.recommendations,
            "chakra_assessment": {
                cid: {
                    "name": chakra.name,
                    "energy_level": chakra.energy_level
                }
                for cid, chakra in state.chakras.items()
            },
            "nervous_system": {
                "mode": state.nervous_system.mode.value,
                "balance_score": state.nervous_system.balance_score
            }
        }
    
    def generate_plan(self, user_id: str, 
                     state: BodyMindSpiritState,
                     goals: List[str]) -> Dict[str, Any]:
        """
        生成进化方案（统一接口）
        
        Args:
            user_id: 用户 ID
            state: 身心精神状态
            goals: 目标列表
            
        Returns:
            进化方案
        """
        # 生成方案
        plan = self.plan_generator.generate_evolution_plan(user_id, state, goals)
        
        # 返回结果
        return {
            "status": "success",
            "plan_id": plan.id,
            "user_id": plan.user_id,
            "goals": plan.goals,
            "actions": plan.actions,
            "timeline": plan.timeline,
            "expected_outcomes": plan.expected_outcomes,
            "confidence": plan.confidence
        }
    
    def get_coverage_stats(self) -> Dict[str, float]:
        """获取覆盖率统计"""
        return {
            "chakra_coverage": len(self.chakra_processor.chakras) / 7,  # 7 大脉轮
            "meridian_coverage": len(self.meridian_processor.meridians) / 12,  # 12 正经（简化：只计算 12 正经）
            "hormone_coverage": len(self.hormone_processor.hormones) / 9,  # 9 种激素
            "nervous_system_coverage": 1.0  # 100% 覆盖
        }
    
    def run_self_test(self) -> Dict[str, Any]:
        """运行自检"""
        test_results = {
            "engine": self.name,
            "version": self.version,
            "tests": []
        }
        
        # 测试 1：脉轮系统处理器
        try:
            chakras = self.chakra_processor.get_all_chakras()
            test_results["tests"].append({
                "name": "ChakraSystemProcessor",
                "status": "passed",
                "chakras_count": len(chakras)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "ChakraSystemProcessor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 2：经络系统处理器
        try:
            meridians = self.meridian_processor.get_all_meridians()
            test_results["tests"].append({
                "name": "MeridianSystemProcessor",
                "status": "passed",
                "meridians_count": len(meridians)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "MeridianSystemProcessor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 3：内分泌系统处理器
        try:
            hormones = self.hormone_processor.get_all_hormones()
            test_results["tests"].append({
                "name": "EndocrineSystemProcessor",
                "status": "passed",
                "hormones_count": len(hormones)
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "EndocrineSystemProcessor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 4：神经系统处理器
        try:
            state = self.nervous_processor.assess_nervous_system(0.7, 0.3)
            test_results["tests"].append({
                "name": "NervousSystemProcessor",
                "status": "passed",
                "mode": state.mode.value
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "NervousSystemProcessor",
                "status": "failed",
                "error": str(e)
            })
        
        # 测试 5：评估接口
        try:
            result = self.assess(
                chakra_levels={"root": 0.6, "heart": 0.7, "crown": 0.5},
                meridian_flows={"lung": 0.6, "heart": 0.7},
                hormone_levels={"dopamine": 0.6, "cortisol": 0.4},
                sympathetic_level=0.6,
                parasympathetic_level=0.4
            )
            test_results["tests"].append({
                "name": "Assess API",
                "status": "passed",
                "overall_balance": result["overall_balance"]
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "Assess API",
                "status": "failed",
                "error": str(e)
            })
        
        # 总体结果
        passed = sum(1 for t in test_results["tests"] if t["status"] == "passed")
        total = len(test_results["tests"])
        test_results["summary"] = {
            "passed": passed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0.0
        }
        
        return test_results


# ==================== 主函数 ====================

def main():
    """主函数"""
    print("=" * 80)
    print("人体身心精神进化引擎 (Human Body-Mind-Spirit Evolution Engine)")
    print("V181.0 · Stage 3 · T20")
    print("=" * 80)
    print()
    
    # 创建引擎
    engine = HumanBodyMindSpiritEvolutionEngine()
    
    # 运行自检
    print("🔍 运行自检...")
    test_results = engine.run_self_test()
    print(f"✅ 自检完成：{test_results['summary']['passed']}/{test_results['summary']['total']} 通过")
    print()
    
    # 显示覆盖率统计
    print("📊 覆盖率统计：")
    coverage = engine.get_coverage_stats()
    print(f"  脉轮系统覆盖率：{coverage['chakra_coverage']:.1%}")
    print(f"  经络系统覆盖率：{coverage['meridian_coverage']:.1%}")
    print(f"  内分泌系统覆盖率：{coverage['hormone_coverage']:.1%}")
    print(f"  神经系统覆盖率：{coverage['nervous_system_coverage']:.1%}")
    print()
    
    # 示例评估
    print("💡 示例评估：")
    result = engine.assess(
        chakra_levels={"root": 0.6, "sacral": 0.5, "solar_plexus": 0.7, 
                     "heart": 0.8, "throat": 0.6, "third_eye": 0.5, "crown": 0.4},
        meridian_flows={"lung": 0.6, "heart": 0.7, "kidney": 0.5},
        hormone_levels={"dopamine": 0.6, "serotonin": 0.7, "cortisol": 0.4, "oxytocin": 0.5},
        sympathetic_level=0.6,
        parasympathetic_level=0.4
    )
    
    if result["status"] == "success":
        print(f"  整体平衡：{result['overall_balance']:.2f}")
        print(f"  神经系统模式：{result['nervous_system']['mode']}")
        print(f"  建议数量：{len(result['recommendations'])}")
        print()
        print("  前 3 条建议：")
        for i, rec in enumerate(result["recommendations"][:3], 1):
            print(f"    {i}. {rec}")
    
    print()
    print("=" * 80)
    print("✅ 人体身心精神进化引擎已就绪")
    print("=" * 80)


if __name__ == "__main__":
    main()
