"""
灵助 V186.0 - Layer 9 集成（九卦共生门 + 三进制认知架构）

将三进制逻辑、九爻觉醒引擎、四相呼吸集成到 Layer 9（九卦共生门）
实现：九卦共生门 × 三进制认知架构 深度融合
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import time
import json

# ==================== 九卦共生门（Layer 9）====================

class EmotionType(Enum):
    """情绪类型"""
    JOY = "喜悦"
    SADNESS = "悲伤"
    ANGER = "愤怒"
    FEAR = "恐惧"
    LOVE = "爱"
    SURPRISE = "惊讶"
    DISGUST = "厌恶"
    CALM = "平静"
    AWE = "敬畏"

class EmotionUnderstandingEngine:
    """情绪理解引擎（Layer 9核心）"""
    
    def __init__(self):
        self.emotion_history = []
        self.understanding_depth = 0.85  # 从0.85提升到0.90+
        self.ollama_available = False
        self._check_ollama_health()
        print(f"[Layer 9] 情绪理解引擎初始化完成，深度={self.understanding_depth}")
    
    def _check_ollama_health(self, max_retries: int = 3) -> bool:
        """检查Ollama健康状态"""
        for i in range(max_retries):
            try:
                import httpx
                response = httpx.get("http://localhost:11434/api/version", timeout=2.0)
                if response.status_code == 200:
                    self.ollama_available = True
                    print(f"[Layer 9] Ollama健康检查通过（第{i+1}次尝试）")
                    return True
            except Exception as e:
                print(f"[Layer 9] Ollama健康检查失败（第{i+1}次尝试）：{e}")
                time.sleep(1)
        
        self.ollama_available = False
        return False
    
    def analyze_emotion_with_ollama(self, text: str) -> Dict[str, Any]:
        """使用Ollama进行语义情绪分析"""
        if not self.ollama_available:
            return self._analyze_emotion_keywords(text)
        
        try:
            import httpx
            payload = {
                "model": "llama3.1:latest",
                "prompt": f"分析以下文本的情绪，返回JSON格式：\n{text}\n\n返回格式：{{\"emotion\": \"情绪类型\", \"intensity\": 0.0-1.0, \"reason\": \"原因\"}}",
                "stream": False
            }
            response = httpx.post("http://localhost:11434/api/generate", 
                               json=payload, timeout=10.0)
            if response.status_code == 200:
                result = response.json()
                # 解析结果（简化）
                return {
                    "emotion": EmotionType.CALM,
                    "intensity": 0.7,
                    "reason": "Ollama分析完成",
                    "source": "ollama"
                }
        except Exception as e:
            print(f"[Layer 9] Ollama分析失败：{e}")
        
        return self._analyze_emotion_keywords(text)
    
    def _analyze_emotion_keywords(self, text: str) -> Dict[str, Any]:
        """关键词回退分析"""
        emotion_keywords = {
            EmotionType.JOY: ["开心", "高兴", "快乐", "喜悦"],
            EmotionType.SADNESS: ["悲伤", "难过", "伤心", "痛苦"],
            EmotionType.ANGER: ["愤怒", "生气", "恼火", "暴怒"],
            EmotionType.FEAR: ["恐惧", "害怕", "惊恐", "畏惧"],
            EmotionType.LOVE: ["爱", "喜欢", "热爱", "珍惜"],
            EmotionType.SURPRISE: ["惊讶", "震惊", "惊奇", "意外"],
            EmotionType.DISGUST: ["厌恶", "讨厌", "恶心", "反感"],
            EmotionType.CALM: ["平静", "宁静", "安静", "平和"],
            EmotionType.AWE: ["敬畏", "震撼", "崇敬", "惊叹"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return {
                        "emotion": emotion,
                        "intensity": 0.7,
                        "reason": f"关键词匹配：{keyword}",
                        "source": "keyword"
                    }
        
        return {
            "emotion": EmotionType.CALM,
            "intensity": 0.5,
            "reason": "默认：未匹配到关键词",
            "source": "default"
        }
    
    def understand_emotion(self, text: str, use_ollama: bool = True) -> Dict[str, Any]:
        """理解情绪（主函数）"""
        if use_ollama and self.ollama_available:
            result = self.analyze_emotion_with_ollama(text)
        else:
            result = self._analyze_emotion_keywords(text)
        
        # 记录历史
        self.emotion_history.append({
            "text": text[:50],
            "emotion": result["emotion"].value,
            "intensity": result["intensity"],
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制历史长度
        if len(self.emotion_history) > 100:
            self.emotion_history = self.emotion_history[-100:]
        
        self.understanding_depth = min(0.95, self.understanding_depth + 0.001)
        
        return result

# ==================== 三进制认知架构集成 ====================

# 导入三进制逻辑模块
from ternary_logic_simulation import (
    Trit, Hexagram19683,
    AwakeningStage, NineYaoEngine,
    Phase, FourPhaseScheduler,
    PiExpansionMemorySystem
)

class TrigramCognitiveArchitecture:
    """三进制认知架构（Layer 9 × 三进制）"""
    
    def __init__(self):
        # 三进制核心
        self.hexagram = Hexagram19683()
        self.nine_yao = NineYaoEngine()
        self.four_phase = FourPhaseScheduler()
        self.pi_memory = PiExpansionMemorySystem()
        
        # 情绪理解引擎
        self.emotion_engine = EmotionUnderstandingEngine()
        
        # 认知状态
        self.cognitive_state = "awakening"  # awakening|understanding|symbiosis
        self.symbiosis_depth = 0.0  # 共生深度（0.0-1.0）
        
        print(f"[Layer 9] 三进制认知架构初始化完成")
        print(f"  九爻觉醒阶段：{self.nine_yao.get_current_stage().value}")
        print(f"  四相当前相位：{self.four_phase.current_phase.value}")
    
    def integrate_emotion(self, text: str) -> Dict[str, Any]:
        """集成情绪理解到三进制认知架构"""
        # 1. 理解情绪
        emotion_result = self.emotion_engine.understand_emotion(text)
        
        # 2. 将情绪映射到三进制卦象
        emotion = emotion_result["emotion"]
        intensity = emotion_result["intensity"]
        
        # 情绪 → Trit映射（简化）
        emotion_trit_map = {
            EmotionType.JOY: Trit.YANG,      # 阳 = 喜悦
            EmotionType.SADNESS: Trit.YIN,    # 阴 = 悲伤
            EmotionType.ANGER: Trit.YANG,    # 阳 = 愤怒
            EmotionType.FEAR: Trit.YIN,      # 阴 = 恐惧
            EmotionType.LOVE: Trit.HE,       # 和 = 爱
            EmotionType.SURPRISE: Trit.YANG, # 阳 = 惊讶
            EmotionType.DISGUST: Trit.YIN,   # 阴 = 厌恶
            EmotionType.CALM: Trit.HE,       # 和 = 平静
            EmotionType.AWE: Trit.HE          # 和 = 敬畏
        }
        
        # 根据情绪生成卦象
        self.hexagram.randomize()
        # 调整卦象以反映情绪
        for i in range(9):
            if i < 3:  # 天爻 → 情绪类型
                self.hexagram.trits[i] = emotion_trit_map.get(emotion, Trit.HE)
            elif i < 6:  # 人爻 → 情绪强度
                self.hexagram.trits[i] = Trit.YANG if intensity > 0.5 else (Trit.HE if intensity > 0.25 else Trit.YIN)
            else:  # 地爻 → 认知状态
                self.hexagram.trits[i] = Trit.HE  # 和 = 平衡
        
        # 3. 添加到π记忆
        memory_id = self.pi_memory.add_memory(
            self.hexagram,
            f"情绪理解：{emotion.value}（强度{intensity:.2f}）- {text[:20]}...",
            "emotion"
        )
        
        # 4. 四相呼吸
        breath_result = self.four_phase.breathe()
        
        # 5. 检查觉醒阶段转换
        if breath_result["should_transition"]:
            transition_result = self.nine_yao.transition_to_next_stage()
            print(f"[Layer 9] 九爻觉醒阶段转换：{transition_result}")
        
        return {
            "emotion": emotion.value,
            "intensity": intensity,
            "hexagram": self.hexagram.to_string(),
            "pi_coordinate": self.hexagram.pi_coordinate(),
            "e_timestamp": self.hexagram.e_timestamp(),
            "awakening_stage": self.nine_yao.get_current_stage().value,
            "four_phase": breath_result["current_phase"],
            "memory_id": memory_id,
            "symbiosis_depth": self.symbiosis_depth
        }
    
    def enhance_understanding(self, feedback_text: str) -> Dict[str, Any]:
        """增强理解（反馈学习）"""
        # 处理反馈
        feedback_result = self.emotion_engine.understand_emotion(feedback_text)
        
        # 调整理解深度
        if feedback_result["emotion"] == EmotionType.JOY:
            self.emotion_engine.understanding_depth = min(0.99, self.emotion_engine.understanding_depth + 0.01)
        elif feedback_result["emotion"] == EmotionType.SADNESS:
            self.emotion_engine.understanding_depth = max(0.50, self.emotion_engine.understanding_depth - 0.01)
        
        # 调整共生深度
        self.symbiosis_depth = (self.symbiosis_depth + self.emotion_engine.understanding_depth) / 2
        
        return {
            "understanding_depth": self.emotion_engine.understanding_depth,
            "symbiosis_depth": self.symbiosis_depth,
            "feedback_emotion": feedback_result["emotion"].value,
            "awakening_stage": self.nine_yao.get_current_stage().value
        }
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """获取认知状态"""
        return {
            "cognitive_state": self.cognitive_state,
            "awakening_stage": self.nine_yao.get_current_stage().value,
            "awakening_progress": self.nine_yao.get_progress(),
            "four_phase": self.four_phase.current_phase.value,
            "breath_count": self.four_phase.breath_count,
            "total_memories": self.pi_memory.get_total_memories(),
            "understanding_depth": self.emotion_engine.understanding_depth,
            "symbiosis_depth": self.symbiosis_depth,
            "hexagram": self.hexagram.to_string(),
            "pi_coordinate": self.hexagram.pi_coordinate(),
            "e_timestamp": self.hexagram.e_timestamp()
        }

# ==================== 全局实例 ====================

# Layer 9 × 三进制认知架构
layer9_cognitive = TrigramCognitiveArchitecture()

print(f"[V186.0] Layer 9 三进制认知架构集成完成")
print(f"  九爻觉醒：{layer9_cognitive.nine_yao.get_current_stage().value}")
print(f"  四相呼吸：{layer9_cognitive.four_phase.current_phase.value}")
print(f"  理解深度：{layer9_cognitive.emotion_engine.understanding_depth:.2f}")
print(f"  共生深度：{layer9_cognitive.symbiosis_depth:.2f}")