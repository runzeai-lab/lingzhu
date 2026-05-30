#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
颂钵疗愈365天内容生产引擎
功能：为微信公众号"五感六觉 润泽博士"生成颂钵疗愈主题文章
作者：灵助 V181.0
版本：V1.0.0
"""

import json
import os
import random
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional

# ============================================================
# 数据模型
# ============================================================

@dataclass
class SingingBowlTheme:
    """颂钵主题"""
    day: int
    title: str
    category: str           # 类别：起源/科学/疗愈/实践/哲学/生活
    keywords: list[str]
    chakra: Optional[str] = None    # 对应脉轮
    emotion: Optional[str] = None   # 对应情绪
    practice: Optional[str] = None  # 实践方法


@dataclass
class SingingBowlArticle:
    """颂钵文章"""
    day: int
    title: str
    category: str
    content: str
    publish_date: str
    word_count: int = 0
    
    def __post_init__(self):
        self.word_count = len(self.content)


# ============================================================
# 365天主题规划
# ============================================================

THEMES_365 = [
    # ── 第1-30天：颂钵缘起与基础知识 ──
    SingingBowlTheme(1, "颂钵缘起：来自喜马拉雅的声音疗愈", "起源", ["起源", "历史", "喜马拉雅"], "顶轮"),
    SingingBowlTheme(2, "什么是颂钵？——五千年的振动智慧", "起源", ["定义", "历史", "西藏"], "眉心轮"),
    SingingBowlTheme(3, "颂钵的材质之谜：七金属的秘密", "起源", ["七金属", "铜", "锡"], None),
    SingingBowlTheme(4, "颂钵的声音是怎样产生的？", "科学", ["泛音", "振动", "共振"], None),
    SingingBowlTheme(5, "颂钵音频的科学：脑波与频率", "科学", ["脑波", "α波", "θ波"], None, "焦虑"),
    SingingBowlTheme(6, "声波疗愈的原理：为什么声音能治愈？", "科学", ["声波", "细胞", "共振"], None),
    SingingBowlTheme(7, "颂钵与冥想：深度放松的捷径", "疗愈", ["冥想", "放松", "正念"], "海底轮"),
    SingingBowlTheme(8, "颂钵疗愈对睡眠的神奇效果", "疗愈", ["睡眠", "失眠", "深度睡眠"], None, "失眠"),
    SingingBowlTheme(9, "颂钵与压力：让皮质醇安静下来", "疗愈", ["压力", "皮质醇", "放松"], None, "压力"),
    SingingBowlTheme(10, "第一次听颂钵：你会有什么感受？", "实践", ["初体验", "感受", "体验"], None),
    SingingBowlTheme(11, "如何选择适合自己的颂钵？", "实践", ["选购", "音色", "大小"], None),
    SingingBowlTheme(12, "颂钵的演奏方法入门：敲击与环绕", "实践", ["演奏", "技巧", "入门"], None),
    SingingBowlTheme(13, "颂钵与呼吸：配合呼吸的疗愈练习", "实践", ["呼吸", "练习", "配合"], "心轮"),
    SingingBowlTheme(14, "颂钵疗愈的禁忌与注意事项", "实践", ["禁忌", "注意", "安全"], None),
    SingingBowlTheme(15, "颂钵与脉轮：七个能量中心的共振", "疗愈", ["脉轮", "能量", "七脉轮"], "顶轮"),
    
    # ── 第16-45天：七大脉轮专题 ──
    SingingBowlTheme(16, "海底轮的颂钵疗愈：根植大地，安全感", "疗愈", ["海底轮", "安全感", "红色"], "海底轮", "恐惧"),
    SingingBowlTheme(17, "脐轮的颂钵疗愈：创造力与情绪流动", "疗愈", ["脐轮", "创造力", "橙色"], "脐轮", "情绪"),
    SingingBowlTheme(18, "太阳神经丛的颂钵疗愈：自信与力量", "疗愈", ["太阳神经丛", "自信", "黄色"], "太阳神经丛轮", "低自尊"),
    SingingBowlTheme(19, "心轮的颂钵疗愈：爱与连接的中心", "疗愈", ["心轮", "爱", "绿色"], "心轮", "失恋"),
    SingingBowlTheme(20, "喉轮的颂钵疗愈：真实表达自己", "疗愈", ["喉轮", "表达", "蓝色"], "喉轮", "沟通障碍"),
    SingingBowlTheme(21, "眉心轮的颂钵疗愈：直觉与智慧", "疗愈", ["眉心轮", "直觉", "靛蓝"], "眉心轮"),
    SingingBowlTheme(22, "顶轮的颂钵疗愈：连接宇宙意识", "疗愈", ["顶轮", "宇宙意识", "紫色"], "顶轮"),
    SingingBowlTheme(23, "脉轮失衡的信号：身体在说什么？", "疗愈", ["失衡", "信号", "症状"], None),
    SingingBowlTheme(24, "七脉轮颂钵疗愈全套练习", "实践", ["全套", "完整", "练习"], None),
    SingingBowlTheme(25, "颂钵与经络：中西方能量体系的融合", "哲学", ["经络", "中医", "融合"], None),
    
    # ── 第26-60天：情绪疗愈专题 ──
    SingingBowlTheme(26, "用颂钵疗愈焦虑：5步情绪急救", "疗愈", ["焦虑", "急救", "5步"], None, "焦虑"),
    SingingBowlTheme(27, "颂钵与抑郁：声音如何打开心门", "疗愈", ["抑郁", "心门", "疗愈"], "心轮", "抑郁"),
    SingingBowlTheme(28, "愤怒情绪的颂钵释放练习", "实践", ["愤怒", "释放", "练习"], "太阳神经丛轮", "愤怒"),
    SingingBowlTheme(29, "悲伤与失落：颂钵陪你走过低谷", "疗愈", ["悲伤", "失落", "低谷"], "心轮", "悲伤"),
    SingingBowlTheme(30, "孤独感的颂钵疗愈：连接自我与世界", "疗愈", ["孤独", "连接", "自我"], "心轮", "孤独"),
    SingingBowlTheme(31, "恐惧与颂钵：让安全感在声音中生根", "疗愈", ["恐惧", "安全感", "根植"], "海底轮", "恐惧"),
    SingingBowlTheme(32, "自我批判的颂钵疗愈：温柔对待自己", "疗愈", ["自我批判", "温柔", "接纳"], "心轮"),
    SingingBowlTheme(33, "关系中的创伤：颂钵帮你重新相信爱", "疗愈", ["关系创伤", "相信", "爱"], "心轮"),
    SingingBowlTheme(34, "工作压力的颂钵急救包", "实践", ["工作压力", "急救", "放松"], None, "压力"),
    SingingBowlTheme(35, "睡前颂钵10分钟：深度放松入眠", "实践", ["睡前", "10分钟", "入眠"], None, "失眠"),
    
    # ── 第36-70天：科学与研究 ──
    SingingBowlTheme(36, "颂钵疗愈的科学研究：什么被证实了？", "科学", ["研究", "证实", "科学"], None),
    SingingBowlTheme(37, "声音与细胞：颂钵如何影响细胞振动", "科学", ["细胞", "振动", "影响"], None),
    SingingBowlTheme(38, "颂钵与神经可塑性：重塑大脑的声音", "科学", ["神经可塑性", "大脑", "重塑"], None),
    SingingBowlTheme(39, "双耳节拍：颂钵的脑波同步原理", "科学", ["双耳节拍", "脑波", "同步"], None),
    SingingBowlTheme(40, "颂钵的432Hz与444Hz：频率之争", "科学", ["频率", "432Hz", "444Hz"], None),
    SingingBowlTheme(41, "水与声音：颂钵对身体水分子的影响", "科学", ["水", "水分子", "影响"], None),
    SingingBowlTheme(42, "颂钵疗愈与心率变异性（HRV）", "科学", ["HRV", "心率", "变异性"], None),
    SingingBowlTheme(43, "声音浴（Sound Bath）的科学解析", "科学", ["声音浴", "Sound Bath", "解析"], None),
    SingingBowlTheme(44, "颂钵与痛觉：声音止痛的神经机制", "科学", ["痛觉", "止痛", "神经"], None),
    SingingBowlTheme(45, "颂钵与免疫系统：声音的免疫调节", "科学", ["免疫", "调节", "系统"], None),
    
    # ── 第46-80天：生活应用 ──
    SingingBowlTheme(46, "晨起颂钵：唤醒新一天的最佳方式", "生活", ["晨起", "唤醒", "早晨"], None),
    SingingBowlTheme(47, "颂钵与瑜伽：完美组合的身心练习", "生活", ["瑜伽", "组合", "练习"], None),
    SingingBowlTheme(48, "颂钵与正念饮食：感恩食物的声音仪式", "生活", ["正念", "饮食", "仪式"], None),
    SingingBowlTheme(49, "给孩子的颂钵疗愈：童年的声音礼物", "生活", ["孩子", "童年", "礼物"], None),
    SingingBowlTheme(50, "老年人与颂钵：声音护佑晚年安康", "生活", ["老年人", "晚年", "安康"], None),
    SingingBowlTheme(51, "孕期颂钵：给宝宝最温柔的声音胎教", "生活", ["孕期", "胎教", "宝宝"], None),
    SingingBowlTheme(52, "颂钵与工作空间：办公室里的声音疗愈", "生活", ["工作空间", "办公室", "疗愈"], None),
    SingingBowlTheme(53, "颂钵与家居风水：声音净化空间", "生活", ["家居", "风水", "净化"], None),
    SingingBowlTheme(54, "节假日与颂钵：特殊时刻的声音仪式", "生活", ["节假日", "仪式", "特殊"], None),
    SingingBowlTheme(55, "颂钵与宠物：动物的声音疗愈", "生活", ["宠物", "动物", "疗愈"], None),
    
    # ── 第56-100天：传统文化融合 ──
    SingingBowlTheme(56, "颂钵与道德经：无为而治的声音智慧", "哲学", ["道德经", "无为", "道"], None),
    SingingBowlTheme(57, "颂钵与易经：八卦与八音的奥秘", "哲学", ["易经", "八卦", "八音"], None),
    SingingBowlTheme(58, "颂钵与中医：五音疗五脏的传统智慧", "哲学", ["中医", "五音", "五脏"], None),
    SingingBowlTheme(59, "颂钵与禅：一声钟响，万念俱寂", "哲学", ["禅", "钟声", "寂静"], None),
    SingingBowlTheme(60, "颂钵与佛教：宇宙音声的觉悟之道", "哲学", ["佛教", "宇宙", "觉悟"], "顶轮"),
    SingingBowlTheme(61, "颂钵与印度教：OM音的神圣意义", "哲学", ["印度教", "OM", "神圣"], None),
    SingingBowlTheme(62, "颂钵与萨满：原始声音疗愈的智慧", "哲学", ["萨满", "原始", "智慧"], None),
    SingingBowlTheme(63, "颂钵与古埃及：声音神殿的秘密", "哲学", ["古埃及", "神殿", "秘密"], None),
    SingingBowlTheme(64, "颂钵与毕达哥拉斯：音乐与数学的宇宙", "哲学", ["毕达哥拉斯", "音乐", "数学"], None),
    SingingBowlTheme(65, "颂钵与现代量子物理：振动的本质", "哲学", ["量子物理", "振动", "本质"], None),
    
    # ── 第66-120天：深度疗愈专题 ──
    SingingBowlTheme(66, "童年创伤的颂钵疗愈之旅", "疗愈", ["童年创伤", "疗愈", "旅程"], "海底轮"),
    SingingBowlTheme(67, "原生家庭的声音疗愈：释放代际模式", "疗愈", ["原生家庭", "代际", "释放"], None),
    SingingBowlTheme(68, "颂钵与身体记忆：存储在肌肉里的情绪", "疗愈", ["身体记忆", "肌肉", "情绪"], None),
    SingingBowlTheme(69, "颂钵与创伤后应激障碍（PTSD）", "疗愈", ["PTSD", "创伤", "应激"], None),
    SingingBowlTheme(70, "颂钵与哀伤疗愈：用声音告别与放下", "疗愈", ["哀伤", "告别", "放下"], "心轮", "悲伤"),
    SingingBowlTheme(71, "自我价值感的颂钵重建", "疗愈", ["自我价值", "重建", "自信"], "太阳神经丛轮"),
    SingingBowlTheme(72, "边界感的颂钵疗愈：学会温柔说不", "疗愈", ["边界感", "说不", "温柔"], "太阳神经丛轮"),
    SingingBowlTheme(73, "颂钵与内在小孩：与童年自我和解", "疗愈", ["内在小孩", "和解", "童年"], "海底轮"),
    SingingBowlTheme(74, "完美主义的颂钵疗愈：接受不完美", "疗愈", ["完美主义", "接受", "不完美"], None),
    SingingBowlTheme(75, "控制欲的颂钵释放：学会流动", "疗愈", ["控制欲", "释放", "流动"], "脐轮"),
    
    # ── 第76-130天：实践技巧进阶 ──
    SingingBowlTheme(76, "颂钵冥想引导词：30分钟深度体验", "实践", ["引导词", "冥想", "30分钟"], None),
    SingingBowlTheme(77, "颂钵的呼吸技巧：腹式呼吸与声音同频", "实践", ["呼吸技巧", "腹式呼吸", "同频"], None),
    SingingBowlTheme(78, "颂钵与身体扫描：深度放松练习", "实践", ["身体扫描", "放松", "练习"], None),
    SingingBowlTheme(79, "颂钵与可视化冥想：声音与意象的旅程", "实践", ["可视化", "意象", "旅程"], None),
    SingingBowlTheme(80, "颂钵音乐创作入门：编织你的声音地图", "实践", ["音乐创作", "声音地图", "编织"], None),
    SingingBowlTheme(81, "颂钵小组练习：集体声音疗愈的力量", "实践", ["小组", "集体", "力量"], None),
    SingingBowlTheme(82, "颂钵与音叉：两种振动疗法的组合", "实践", ["音叉", "组合", "振动"], None),
    SingingBowlTheme(83, "颂钵与水晶钵：金属与水晶的对话", "实践", ["水晶钵", "金属", "对话"], None),
    SingingBowlTheme(84, "颂钵的清洁与保养：维护你的声音伴侣", "实践", ["清洁", "保养", "维护"], None),
    SingingBowlTheme(85, "颂钵疗愈师的修炼之路", "实践", ["疗愈师", "修炼", "成长"], None),
    
    # ── 第86-150天：四季与节气 ──
    SingingBowlTheme(86, "春分颂钵：新生与希望的声音仪式", "生活", ["春分", "新生", "希望"], None),
    SingingBowlTheme(87, "夏至颂钵：能量最强时刻的声音祝福", "生活", ["夏至", "能量", "祝福"], None),
    SingingBowlTheme(88, "秋分颂钵：收获与感恩的声音礼赞", "生活", ["秋分", "收获", "感恩"], None),
    SingingBowlTheme(89, "冬至颂钵：归根与静养的声音仪式", "生活", ["冬至", "归根", "静养"], None),
    SingingBowlTheme(90, "新年颂钵：新年第一声的祝福与启程", "生活", ["新年", "祝福", "启程"], None),
    SingingBowlTheme(91, "元宵颂钵：团圆与圆满的声音共鸣", "生活", ["元宵", "团圆", "圆满"], None),
    SingingBowlTheme(92, "清明颂钵：对逝去之人的声音悼念", "生活", ["清明", "追忆", "悼念"], None),
    SingingBowlTheme(93, "端午颂钵：驱邪避害的声音护佑", "生活", ["端午", "驱邪", "护佑"], None),
    SingingBowlTheme(94, "中秋颂钵：月圆时的声音感恩", "生活", ["中秋", "月圆", "感恩"], None),
    SingingBowlTheme(95, "重阳颂钵：敬老与长寿的声音祝福", "生活", ["重阳", "敬老", "长寿"], None),
    
    # ── 第96-180天：深度专题 ──
    SingingBowlTheme(96, "颂钵与死亡：声音陪伴最后的旅程", "哲学", ["死亡", "陪伴", "旅程"], None),
    SingingBowlTheme(97, "颂钵与梦境：声音打开潜意识的门", "疗愈", ["梦境", "潜意识", "门"], None),
    SingingBowlTheme(98, "颂钵与前世记忆：声音的时间之旅", "哲学", ["前世", "记忆", "时间"], None),
    SingingBowlTheme(99, "颂钵与灵魂碎片：找回失落的自己", "疗愈", ["灵魂", "碎片", "找回"], None),
    SingingBowlTheme(100, "颂钵100天：你经历了什么变化？", "实践", ["100天", "变化", "总结"], None),
]

# 生成剩余265天的主题（简化版，实际可以扩展）
ADDITIONAL_THEMES_TEMPLATE = [
    ("颂钵与{topic}：声音的{aspect}", "疗愈"),
    ("用颂钵疗愈{emotion}：{method}", "疗愈"),
    ("颂钵与{tradition}：{wisdom}的智慧", "哲学"),
    ("{season}的颂钵练习：{benefit}", "实践"),
    ("颂钵{number}：{title}", "生活"),
]

# 确保共有365个主题
def get_all_themes() -> list[SingingBowlTheme]:
    """获取所有365天主题"""
    themes = list(THEMES_365)
    # 为剩余天数生成主题
    extra_topics = [
        ("情绪管理", "身心合一"), ("自我关爱", "滋养身心"), ("人际关系", "和谐相处"),
        ("工作生涯", "平衡发展"), ("财富意识", "丰盛流动"), ("创造力", "释放潜能"),
        ("直觉", "内在声音"), ("感恩", "活在当下"), ("接纳", "放下执念"),
        ("蜕变", "破茧成蝶"), ("勇气", "面对恐惧"), ("宁静", "内在平和"),
        ("爱的能力", "无条件的爱"), ("信任", "相信宇宙"), ("喜悦", "找回快乐"),
        ("自由", "解除束缚"), ("智慧", "内在知晓"), ("力量", "激活潜能"),
        ("疗愈", "整合身心灵"), ("觉醒", "意识的升华"),
    ]
    day = 101
    while day <= 365:
        topic, aspect = extra_topics[(day - 101) % len(extra_topics)]
        themes.append(SingingBowlTheme(
            day=day,
            title=f"颂钵与{topic}：{aspect}的声音旅程",
            category="疗愈" if day % 3 != 0 else "实践",
            keywords=[topic, aspect, "颂钵"],
        ))
        day += 1
    return themes


# ============================================================
# 文章生成引擎
# ============================================================

class SingingBowlContentEngine:
    """颂钵疗愈365天内容生产引擎"""
    
    def __init__(self, output_dir: str = "output/singing_bowl_365"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.themes = get_all_themes()
    
    def get_theme(self, day: int) -> Optional[SingingBowlTheme]:
        """获取指定天数的主题"""
        for theme in self.themes:
            if theme.day == day:
                return theme
        return None
    
    def generate_article(self, day: int, publish_date: Optional[str] = None) -> SingingBowlArticle:
        """生成指定天数的文章"""
        theme = self.get_theme(day)
        if not theme:
            raise ValueError(f"未找到第{day}天的主题")
        
        if not publish_date:
            # 默认从2026-04-04起每天一篇
            start_date = datetime(2026, 4, 4)
            pub_date = start_date + timedelta(days=day - 1)
            publish_date = pub_date.strftime("%Y-%m-%d")
        
        content = self._generate_content(theme, day, publish_date)
        
        return SingingBowlArticle(
            day=day,
            title=theme.title,
            category=theme.category,
            content=content,
            publish_date=publish_date,
        )
    
    def _generate_content(self, theme: SingingBowlTheme, day: int, publish_date: str) -> str:
        """生成文章内容"""
        
        # 随机选择开篇引语
        opening_quotes = [
            "**「声音是宇宙的第一语言。」**\n—— 古印度智慧",
            "**「当颂钵发声，万物皆静。」**\n—— 西藏古谚",
            "**「振动即存在，存在即振动。」**\n—— 量子物理",
            "**「五音令人耳聋。」**\n—— 《道德经》第十二章",
            "**「天下皆知美之为美，斯恶已；皆知善之为善，斯不善已。」**\n—— 《道德经》",
            "**「音由心生，心由音转。」**\n—— 中医五音疗法",
        ]
        quote = opening_quotes[day % len(opening_quotes)]
        
        # 主题相关内容模板
        chakra_info = f"\n**对应脉轮**：{theme.chakra}" if theme.chakra else ""
        emotion_info = f"\n**适合情绪**：{theme.emotion}" if theme.emotion else ""
        keywords_str = "、".join(theme.keywords)
        
        # 根据类别生成不同风格的内容
        if theme.category == "科学":
            section2 = self._generate_science_section(theme)
        elif theme.category == "疗愈":
            section2 = self._generate_healing_section(theme)
        elif theme.category == "实践":
            section2 = self._generate_practice_section(theme)
        elif theme.category == "哲学":
            section2 = self._generate_philosophy_section(theme)
        else:  # 生活/起源
            section2 = self._generate_life_section(theme)
        
        content = f"""# {theme.title}

> {quote}

---

## 颂钵日记 · 第{day}天 · {publish_date}

今天是我们共同踏上颂钵疗愈之旅的第 **{day}** 天。{self._get_day_intro(day)}

**今日主题**：{theme.title}  
**关键词**：{keywords_str}{chakra_info}{emotion_info}

---

{section2}

---

## 今日颂钵练习

{self._generate_practice_guide(theme)}

---

## 润泽博士的心得

{self._generate_personal_insight(theme, day)}

---

## 今日一句话

> **{self._get_daily_quote(theme, day)}**

---

*如果今天的内容对你有所启发，欢迎分享给需要它的朋友。*  
*颂钵的声音，是宇宙给我们最温柔的礼物。*

---

**作者**：润泽博士 · 颂钵疗愈师  
**公众号**：五感六觉 润泽博士  
**日期**：{publish_date}
"""
        return content
    
    def _get_day_intro(self, day: int) -> str:
        intros = [
            "感谢你坚持陪伴，你的每一次聆听都是对自己的深情滋养。",
            "每一天的颂钵练习，都是在为心灵开辟一片宁静的空间。",
            "颂钵的振动，穿越时间与空间，与你的细胞共鸣。",
            "在喧嚣的世界里，颂钵的声音是我们回归内在的桥梁。",
            "今天，让我们一起深入探索颂钵疗愈的智慧。",
        ]
        return intros[day % len(intros)]
    
    def _generate_science_section(self, theme: SingingBowlTheme) -> str:
        return f"""## 科学探索：{theme.title}

### 现代科学的发现

近年来，声音疗愈领域的研究取得了令人振奋的进展。科学家们发现，颂钵产生的特定频率振动，能够与人体的生理节律产生深度共鸣。

**研究发现：**

1. **细胞层面**：振动频率在200-500Hz之间时，可以促进细胞膜的流动性，有助于营养物质的吸收和废物的排出。

2. **神经系统**：颂钵声波能够激活副交感神经系统，降低皮质醇水平（压力激素），促进血清素和多巴胺的分泌。

3. **脑波同步**：颂钵发出的复合音频包含多种谐波，这些谐波能够引导大脑产生α波（8-12Hz，放松状态）和θ波（4-8Hz，冥想状态）。

### 从传统到科学

颂钵疗愈并非只是玄学或迷信。在古代，喜马拉雅的僧侣们通过千年实践，发现了声音对身心的深刻影响。今天，现代科学用精密的仪器和实验数据，为这些古老智慧提供了科学背书。

**关键词解析**：{' · '.join(theme.keywords)}

### 实践意义

了解这些科学原理，能帮助我们更有意识地使用颂钵：

- 选择适合当前状态的频率
- 理解为什么某些声音让我们感到平静
- 更好地调整练习时间和方式"""
    
    def _generate_healing_section(self, theme: SingingBowlTheme) -> str:
        chakra_text = f"从{theme.chakra}的角度来看，" if theme.chakra else ""
        emotion_text = f"当我们感到{theme.emotion}时，" if theme.emotion else "当我们处于不平衡状态时，"
        
        return f"""## 深度疗愈：{theme.title}

### 理解这一疗愈主题

{emotion_text}身体和心灵都在发出求救信号。{chakra_text}颂钵的振动能够穿透表层的防御，直达内心深处，触动那些我们用语言无法表达的感受。

### 疗愈的三个层次

**第一层：身体层**

身体是情绪的容器。长期积累的紧张和压力，会以肌肉酸痛、睡眠障碍、消化问题等形式表现出来。颂钵的振动能够直接作用于肌肉组织，帮助释放身体层面的紧张。

**第二层：情绪层**

情绪是能量的流动。{emotion_text or '当情绪停滞时，'}颂钵的声音能够松动僵化的情绪模式，让能量重新流动起来。这个过程有时会伴随眼泪、叹息或身体的颤动——这些都是疗愈正在发生的信号。

**第三层：心灵层**

在最深处，颂钵疗愈触碰的是我们对自己、对他人、对生命的认知模式。当振动穿透所有的防御，我们可能会遇见最真实的自己。

### 为什么颂钵能够疗愈？

颂钵疗愈的核心原理是**共振**：

> 当颂钵发声时，它不仅是在发出声音，而是在创造一个振动场。在这个振动场中，我们身体中失去和谐的部分，会被温柔地"调音"，重新与整体同频。

这就像一个走调的音符，在整体和声中被温柔地带回正轨。"""
    
    def _generate_practice_section(self, theme: SingingBowlTheme) -> str:
        return f"""## 实践指南：{theme.title}

### 准备工作

在开始练习之前，请做以下准备：

1. **选择安静的空间**：找一个不会被打扰的地方，关闭手机或调至静音。
2. **舒适的姿势**：可以坐在垫子上、椅子上，或者躺下——选择让你感到最放松的姿势。
3. **意图设定**：闭上眼睛，在心中默默说："我现在开始颂钵练习，我愿意接受声音的疗愈。"

### 分步练习指南

**步骤一：调息（3-5分钟）**

- 深吸气，感受腹部隆起
- 缓慢呼气，让身体放松
- 重复5-7次，让呼吸逐渐平稳

**步骤二：颂钵演奏（10-20分钟）**

- 将颂钵放在掌心，或放在垫子上
- 用木槌轻轻敲击颂钵边缘
- 然后用木槌沿颂钵外沿缓慢、均匀地环绕
- 感受振动通过手掌传递到全身

**步骤三：静默聆听（5-10分钟）**

- 放下木槌，闭上眼睛
- 让颂钵的声音自然消散
- 在寂静中，感受振动的余韵

### 注意事项

- 刚开始练习时，每次15-20分钟即可
- 练习后喝一杯温水，帮助身体整合
- 如果感到不适，随时可以停止

**关键词**：{' · '.join(theme.keywords)}"""
    
    def _generate_philosophy_section(self, theme: SingingBowlTheme) -> str:
        return f"""## 哲学探索：{theme.title}

### 跨越时空的智慧

{theme.title}——这个主题将我们带入一个更深层的探索：声音与智慧的交汇处。

不同文化、不同时代的智者，都发现了声音与意识之间的神秘关联。这种关联，超越了语言和逻辑，直达存在的本质。

### 东西方视角

**东方智慧**

在中国传统文化中，"音"不仅仅是声音，更是宇宙运行的法则。《易经》中的八卦，与八种基本音调相对应；中医的五音疗法，用宫商角徵羽与五脏相配……

颂钵发出的声音，是这些古老智慧的现代体现。

**西方传统**

毕达哥拉斯说："数字是宇宙的语言。"他发现，音乐的和谐来自数字的比例关系，而这些比例也存在于天体运行之中——"天球音乐"的概念由此而来。

颂钵产生的泛音系列，正是这种数学和谐的完美体现。

### 当代意义

在这个信息过载、节奏飞快的时代，颂钵的声音为我们提供了一个停下来的理由：

> 停下来，聆听。不是聆听外界的噪音，而是聆听内在的寂静。

**关键词**：{' · '.join(theme.keywords)}

### 一点思考

今天，请带着这个问题去聆听颂钵：**声音从哪里来，又到哪里去？**

在声音与寂静的边界，也许你会找到自己最真实的答案。"""
    
    def _generate_life_section(self, theme: SingingBowlTheme) -> str:
        return f"""## 生活应用：{theme.title}

### 颂钵走进日常生活

颂钵疗愈不只是在特定场合才能体验的"仪式"——它可以完全融入我们的日常生活，成为滋养身心的日常习惯。

{theme.title}这个主题，正是要探索颂钵如何在这个特定的生活场景中发挥作用。

### 生活化的颂钵实践

**晨起仪式**

每天早晨，在正式开始一天的工作之前，给自己5-10分钟的颂钵时间。让颂钵的声音唤醒身体，设定当天的意图和能量。

**日间调节**

当感到压力、疲惫或情绪波动时，拿起颂钵，敲击3-5下，闭眼聆听声音消散的过程。这3分钟的暂停，往往比任何咖啡因都更有效。

**夜间放松**

睡前的颂钵练习是最受欢迎的应用场景之一。让颂钵的振动帮助你从白天的忙碌中脱身，进入深度放松的状态。

### 颂钵的家庭文化

把颂钵放在家中显眼的地方，不仅是装饰，更是一个随时可以触摸、体验的疗愈工具。家庭成员都可以参与，形成共同的声音仪式。

**关键词**：{' · '.join(theme.keywords)}"""
    
    def _generate_practice_guide(self, theme: SingingBowlTheme) -> str:
        if theme.chakra:
            return f"""**{theme.chakra}激活练习**（建议时长：15分钟）

1. 盘腿而坐，脊柱挺直，双手放在膝盖上
2. 将颂钵放在身前约30厘米处
3. 深呼吸三次，将注意力集中在{theme.chakra}对应的身体部位
4. 开始演奏颂钵，想象振动的能量球从颂钵流向对应脉轮
5. 随着声音环绕，感受那个部位开始放松、温热、扩展
6. 当声音渐弱，静默感受身体的变化
7. 以三声深呼吸结束练习"""
        elif theme.emotion:
            return f"""**{theme.emotion}情绪释放练习**（建议时长：20分钟）

1. 选择一个安静、温暖的空间
2. 坐下或躺下，让身体完全放松
3. 允许自己感受{theme.emotion}的存在，不抗拒、不压制
4. 开始演奏颂钵，让声音包围你
5. 如果眼泪来了，让它流；如果叹息来了，让它出
6. 随着振动，感受{theme.emotion}的能量慢慢松动、流动
7. 最后，做三次深呼吸，感谢自己允许疗愈发生"""
        else:
            return f"""**今日颂钵练习**（建议时长：15-20分钟）

1. 找一个安静舒适的地方，关闭手机
2. 舒适地坐下，深呼吸3次，放松身体
3. 开始演奏颂钵，以均匀的速度环绕
4. 将注意力集中在声音上，让其他思绪自然飘过
5. 练习过程中保持自然呼吸，不刻意控制
6. 结束时，静默聆听声音消散，感受内心的宁静
7. 慢慢睁开眼睛，喝一杯温水"""
    
    def _generate_personal_insight(self, theme: SingingBowlTheme, day: int) -> str:
        insights = [
            f"在我多年的颂钵疗愈实践中，{theme.title}是让我最有感触的主题之一。每次演奏颂钵，我都会在振动中遇见不同的自己——有时是脆弱的，有时是强大的，有时是充满好奇的孩子。\n\n颂钵不会撒谎，它只是如实反映你内心的状态。当你听到它发出美妙和谐的声音时，那是你内心的平静；当你听到它发出刺耳的声音时，那是你内心的紧张。\n\n无论是哪种声音，都值得被聆听、被接受。",
            f"我第一次接触颂钵是在{day + 2020}年，一次偶然的机缘让我坐在了一个颂钵疗愈师面前。当颂钵响起的那一刻，我感到时间停止了——不是因为它有多神奇，而是因为我第一次真正地"在当下"。\n\n从那以后，颂钵成了我每日修行的核心工具。它不只是一个乐器，而是我通往内心的门。",
            f"今天分享{theme.title}这个主题，是因为我发现很多人在这个问题上有困惑和误解。\n\n颂钵疗愈不是魔法，不是玄学，也不是宗教仪式——它是一种基于声学原理、结合东西方智慧的身心健康实践。\n\n最重要的是：它是有效的。我见证了太多人通过颂钵练习，找回了健康、平静和自我。",
        ]
        return insights[day % len(insights)]
    
    def _get_daily_quote(self, theme: SingingBowlTheme, day: int) -> str:
        quotes = [
            "声音是宇宙给我们最温柔的礼物。",
            "在寂静中，颂钵的振动触碰了灵魂最深处。",
            "每一次敲击，都是一次新的开始。",
            "颂钵不问对错，只问是否愿意聆听。",
            "振动穿越语言，直达心灵。",
            "在声音与寂静之间，是真实的自己。",
            "颂钵告诉我们：和谐，原本就在我们内心。",
        ]
        return quotes[day % len(quotes)]
    
    def save_article(self, article: SingingBowlArticle) -> Path:
        """保存文章到文件"""
        filename = f"Day{article.day:03d}_{article.publish_date}_{article.title[:20]}.md"
        # 清理文件名中的特殊字符
        safe_filename = "".join(c for c in filename if c not in r'\/:*?"<>|')
        filepath = self.output_dir / safe_filename
        filepath.write_text(article.content, encoding="utf-8")
        return filepath
    
    def generate_batch(self, start_day: int, end_day: int) -> list[Path]:
        """批量生成文章"""
        paths = []
        for day in range(start_day, end_day + 1):
            try:
                article = self.generate_article(day)
                path = self.save_article(article)
                paths.append(path)
                print(f"✅ 第{day}天文章已生成：{path.name}（{article.word_count}字）")
            except Exception as e:
                print(f"❌ 第{day}天文章生成失败：{e}")
        return paths
    
    def generate_theme_list(self) -> str:
        """生成主题清单"""
        lines = ["# 颂钵疗愈365天主题清单\n"]
        categories = {}
        for theme in self.themes:
            if theme.category not in categories:
                categories[theme.category] = []
            categories[theme.category].append(theme)
        
        for cat, themes in categories.items():
            lines.append(f"\n## {cat}（{len(themes)}篇）\n")
            for t in themes:
                chakra = f" [{t.chakra}]" if t.chakra else ""
                lines.append(f"- 第{t.day:3d}天：{t.title}{chakra}")
        
        return "\n".join(lines)


# ============================================================
# 主程序
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="颂钵疗愈365天内容生产引擎")
    parser.add_argument("--start", type=int, default=1, help="开始天数")
    parser.add_argument("--end", type=int, default=7, help="结束天数")
    parser.add_argument("--list", action="store_true", help="显示主题清单")
    parser.add_argument("--day", type=int, help="生成指定天数的文章")
    args = parser.parse_args()
    
    engine = SingingBowlContentEngine()
    
    if args.list:
        theme_list = engine.generate_theme_list()
        list_path = Path("output/颂钵疗愈365天主题清单.md")
        list_path.parent.mkdir(exist_ok=True)
        list_path.write_text(theme_list, encoding="utf-8")
        print(f"✅ 主题清单已保存：{list_path}")
        print(f"总主题数：{len(engine.themes)}")
    elif args.day:
        article = engine.generate_article(args.day)
        path = engine.save_article(article)
        print(f"✅ 第{args.day}天文章已生成：{path}（{article.word_count}字）")
    else:
        print(f"📝 开始批量生成第{args.start}-{args.end}天文章...")
        paths = engine.generate_batch(args.start, args.end)
        print(f"\n🎉 共生成 {len(paths)} 篇文章，保存到：output/singing_bowl_365/")


if __name__ == "__main__":
    main()
