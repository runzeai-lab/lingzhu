"""
Cache-Aware Scheduler for Lingzhu V182.0
缓存感知调度器 - 优化卦象检索性能

融合自: WorkBuddy自主工作防偷懒提示专家模式 (10).md
作者: 灵助 V182.0 (CogniForce AI管家系统)
日期: 2026-05-25
"""

import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from collections import OrderedDict, defaultdict
import math


class CachePolicy(Enum):
    """缓存策略枚举"""
    LRU = "LRU"           # 最近最少使用
    LFU = "LFU"           # 最不经常使用
    FIFO = "FIFO"         # 先进先出
    CLOCK = "Clock"       # 时钟算法
    RANDOM = "Random"     # 随机替换


class CacheState:
    """缓存状态"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.hit_count = 0
        self.miss_count = 0
        self.access_history = []  # 访问历史
        
    def record_access(self, key: str, hit: bool):
        """记录访问"""
        self.access_history.append({
            'key': key,
            'hit': hit,
            'timestamp': time.time()
        })
        if hit:
            self.hit_count += 1
        else:
            self.miss_count += 1
    
    def hit_rate(self) -> float:
        """命中率"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'capacity': self.capacity,
            'size': self.size,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': self.hit_rate()
        }


class AccessPattern:
    """访问模式分析"""
    def __init__(self):
        self.access_counts = defaultdict(int)
        self.access_intervals = defaultdict(list)
        self.last_access = {}
        self.access_history = []  # 访问历史（修复bug）
    
    def record(self, key: str, timestamp: float):
        """记录访问"""
        self.access_counts[key] += 1
        
        if key in self.last_access:
            interval = timestamp - self.last_access[key]
            self.access_intervals[key].append(interval)
        
        self.last_access[key] = timestamp
        
        # 记录到历史（修复bug）
        self.access_history.append({
            'key': key,
            'timestamp': timestamp
        })
    
    def is_temporal_locality(self) -> bool:
        """判断是否有时间局部性（最近访问的很可能再次访问）"""
        # 简单启发式：如果最近10次访问中有超过50%是重复的，则认为有时间局部性
        recent_keys = [entry['key'] for entry in list(self.access_history)[-10:]]
        if len(recent_keys) < 5:
            return False
        unique_ratio = len(set(recent_keys)) / len(recent_keys)
        return unique_ratio < 0.5  # 重复率高
    
    def is_spatial_locality(self) -> bool:
        """判断是否有空间局部性（访问相近的key）"""
        # 简化版：检查key是否是连续整数（卦象ID）
        recent_keys = [entry['key'] for entry in list(self.access_history)[-20:]]
        try:
            key_ints = [int(k) for k in recent_keys if k.isdigit()]
            if len(key_ints) < 5:
                return False
            # 检查是否有连续序列
            sorted_keys = sorted(key_ints)
            consecutive_count = sum(1 for i in range(len(sorted_keys)-1) 
                                  if sorted_keys[i+1] - sorted_keys[i] == 1)
            return consecutive_count / len(sorted_keys) > 0.3
        except:
            return False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'temporal_locality': self.is_temporal_locality(),
            'spatial_locality': self.is_spatial_locality(),
            'total_accesses': sum(self.access_counts.values())
        }


class LRUCache:
    """LRU缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """获取元素"""
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> Optional[str]:
        """放入元素，返回被淘汰的key（如果有）"""
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            return None
        
        if len(self.cache) >= self.capacity:
            evicted_key, _ = self.cache.popitem(last=False)
        else:
            evicted_key = None
        
        self.cache[key] = value
        return evicted_key
    
    def size(self) -> int:
        """当前大小"""
        return len(self.cache)


class LFUCache:
    """LFU缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> value
        self.freq = defaultdict(int)  # key -> 访问频率
        self.freq_keys = defaultdict(set)  # freq -> set(keys)
        self.min_freq = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取元素"""
        if key not in self.cache:
            return None
        
        # 更新频率
        old_freq = self.freq[key]
        self.freq_keys[old_freq].remove(key)
        if not self.freq_keys[old_freq]:
            del self.freq_keys[old_freq]
            if old_freq == self.min_freq:
                self.min_freq += 1
        
        self.freq[key] = old_freq + 1
        self.freq_keys[old_freq + 1].add(key)
        
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> Optional[str]:
        """放入元素，返回被淘汰的key（如果有）"""
        if key in self.cache:
            self.cache[key] = value
            self.get(key)  # 更新频率
            return None
        
        if len(self.cache) >= self.capacity:
            # 淘汰最低频率的key
            evicted_key = next(iter(self.freq_keys[self.min_freq]))
            self.freq_keys[self.min_freq].remove(evicted_key)
            if not self.freq_keys[self.min_freq]:
                del self.freq_keys[self.min_freq]
            del self.cache[evicted_key]
            del self.freq[evicted_key]
        else:
            evicted_key = None
        
        self.cache[key] = value
        self.freq[key] = 1
        self.freq_keys[1].add(key)
        self.min_freq = 1
        
        return evicted_key
    
    def size(self) -> int:
        """当前大小"""
        return len(self.cache)


class FIFOCache:
    """FIFO缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.queue = []  # FIFO队列
    
    def get(self, key: str) -> Optional[Any]:
        """获取元素（FIFO不影响访问顺序）"""
        return self.cache.get(key, None)
    
    def put(self, key: str, value: Any) -> Optional[str]:
        """放入元素，返回被淘汰的key（如果有）"""
        if key in self.cache:
            self.cache[key] = value
            return None
        
        if len(self.cache) >= self.capacity:
            evicted_key = self.queue.pop(0)  # FIFO：淘汰最早进入的
            del self.cache[evicted_key]
        else:
            evicted_key = None
        
        self.cache[key] = value
        self.queue.append(key)
        
        return evicted_key
    
    def size(self) -> int:
        """当前大小"""
        return len(self.cache)


class ClockCache:
    """Clock缓存实现（第二次机会算法）"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.hand = 0  # 时钟指针
        self.clock = []  # [(key, value, referenced), ...]
    
    def get(self, key: str) -> Optional[Any]:
        """获取元素"""
        for i, (k, v, _) in enumerate(self.clock):
            if k == key:
                self.clock[i] = (k, v, True)  # 设置引用位
                return v
        return None
    
    def put(self, key: str, value: Any) -> Optional[str]:
        """放入元素，返回被淘汰的key（如果有）"""
        # 检查是否已存在
        for i, (k, v, r) in enumerate(self.clock):
            if k == key:
                self.clock[i] = (k, value, True)
                return None
        
        if len(self.clock) >= self.capacity:
            # Clock算法：找到第一个referenced=False的
            while self.clock[self.hand][2]:  # referenced=True
                self.clock[self.hand] = (self.clock[self.hand][0], 
                                        self.clock[self.hand][1], 
                                        False)
                self.hand = (self.hand + 1) % self.capacity
            
            evicted_key = self.clock[self.hand][0]
            self.clock[self.hand] = (key, value, True)
            self.hand = (self.hand + 1) % self.capacity
            return evicted_key
        else:
            self.clock.append((key, value, True))
            return None
    
    def size(self) -> int:
        """当前大小"""
        return len(self.clock)


class RandomCache:
    """Random缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取元素"""
        return self.cache.get(key, None)
    
    def put(self, key: str, value: Any) -> Optional[str]:
        """放入元素，返回被淘汰的key（如果有）"""
        if key in self.cache:
            self.cache[key] = value
            return None
        
        if len(self.cache) >= self.capacity:
            # 随机淘汰一个
            import random
            evicted_key = random.choice(list(self.cache.keys()))
            del self.cache[evicted_key]
        else:
            evicted_key = None
        
        self.cache[key] = value
        return evicted_key
    
    def size(self) -> int:
        """当前大小"""
        return len(self.cache)


class CacheAwareScheduler:
    """
    缓存感知调度器
    根据缓存状态和访问模式，自适应选择最优缓存策略
    """
    
    def __init__(self, capacity: int = 1000):
        """
        初始化调度器
        
        Args:
            capacity: 缓存容量
        """
        self.capacity = capacity
        self.cache_state = CacheState(capacity)
        self.access_pattern = AccessPattern()
        
        # 初始化各种缓存策略
        self.caches = {
            CachePolicy.LRU: LRUCache(capacity),
            CachePolicy.LFU: LFUCache(capacity),
            CachePolicy.FIFO: FIFOCache(capacity),
            CachePolicy.CLOCK: ClockCache(capacity),
            CachePolicy.RANDOM: RandomCache(capacity)
        }
        
        self.current_policy = CachePolicy.LRU  # 默认策略
        self.performance_history = []  # 性能历史
        
        print(f"[CacheAwareScheduler] 初始化完成，容量={capacity}，默认策略={self.current_policy.value}")
    
    def schedule(self, cache_state: Optional[CacheState] = None, 
                 access_pattern: Optional[AccessPattern] = None) -> CachePolicy:
        """
        调度：根据缓存状态和访问模式选择最优策略
        
        Args:
            cache_state: 缓存状态（可选，默认使用内部状态）
            access_pattern: 访问模式（可选，默认使用内部模式）
        
        Returns:
            CachePolicy: 最优缓存策略
        """
        if cache_state is None:
            cache_state = self.cache_state
        
        if access_pattern is None:
            access_pattern = self.access_pattern
        
        # 决策逻辑
        hit_rate = cache_state.hit_rate()
        pattern_dict = access_pattern.to_dict()
        
        # 规则1：如果命中率已经很高（>80%），保持当前策略
        if hit_rate > 0.8:
            print(f"[CacheAwareScheduler] 命中率={hit_rate:.2%}，保持当前策略={self.current_policy.value}")
            return self.current_policy
        
        # 规则2：如果有时间局部性，优先LRU
        if pattern_dict['temporal_locality']:
            recommended = CachePolicy.LRU
            print(f"[CacheAwareScheduler] 检测到时间局部性，推荐策略={recommended.value}")
            return recommended
        
        # 规则3：如果有空间局部性，优先LFU或Clock
        if pattern_dict['spatial_locality']:
            recommended = CachePolicy.LFU
            print(f"[CacheAwareScheduler] 检测到空间局部性，推荐策略={recommended.value}")
            return recommended
        
        # 规则4：如果访问模式未知，使用Clock（平衡策略）
        recommended = CachePolicy.CLOCK
        print(f"[CacheAwareScheduler] 访问模式未知，默认推荐策略={recommended.value}")
        return recommended
    
    def should_switch_policy(self, new_policy: CachePolicy) -> bool:
        """
        判断是否应该切换策略
        
        Args:
            new_policy: 新策略
            
        Returns:
            bool: 是否应该切换
        """
        # 如果新策略与当前策略不同，且当前缓存命中率低于阈值，则切换
        if new_policy != self.current_policy and self.cache_state.hit_rate() < 0.6:
            return True
        return False
    
    def switch_policy(self, new_policy: CachePolicy):
        """
        切换缓存策略（会丢失缓存数据）
        
        Args:
            new_policy: 新策略
        """
        print(f"[CacheAwareScheduler] 切换策略: {self.current_policy.value} -> {new_policy.value}")
        self.current_policy = new_policy
        # 注意：这里会丢失缓存数据，实际应用中应该实现数据迁移
        # 为简化，这里只是重置缓存
        self.cache_state = CacheState(self.capacity)
        self.caches = {
            CachePolicy.LRU: LRUCache(self.capacity),
            CachePolicy.LFU: LFUCache(self.capacity),
            CachePolicy.FIFO: FIFOCache(self.capacity),
            CachePolicy.CLOCK: ClockCache(self.capacity),
            CachePolicy.RANDOM: RandomCache(self.capacity)
        }
    
    def access(self, key: str, value: Any = None) -> Optional[Any]:
        """
        访问缓存
        
        Args:
            key: 键
            value: 值（如果为None，则是读操作；否则是写操作）
        
        Returns:
            Optional[Any]: 如果是读操作且命中，返回值；否则返回None
        """
        timestamp = time.time()
        
        # 获取推荐策略
        recommended_policy = self.schedule()
        
        # 判断是否应该切换策略
        if self.should_switch_policy(recommended_policy):
            self.switch_policy(recommended_policy)
        
        # 使用当前策略的缓存
        cache = self.caches[self.current_policy]
        
        # 读操作
        if value is None:
            result = cache.get(key)
            hit = result is not None
            self.cache_state.record_access(key, hit)
            self.access_pattern.record(key, timestamp)
            
            if hit:
                print(f"[CacheAwareScheduler] 读命中: key={key}, policy={self.current_policy.value}")
            else:
                print(f"[CacheAwareScheduler] 读缺失: key={key}, policy={self.current_policy.value}")
            
            return result
        
        # 写操作
        else:
            evicted = cache.put(key, value)
            self.cache_state.size = cache.size()
            self.access_pattern.record(key, timestamp)
            
            if evicted:
                print(f"[CacheAwareScheduler] 写操作: key={key}, 淘汰key={evicted}, policy={self.current_policy.value}")
            else:
                print(f"[CacheAwareScheduler] 写操作: key={key}, policy={self.current_policy.value}")
            
            return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'current_policy': self.current_policy.value,
            'cache_state': self.cache_state.to_dict(),
            'access_pattern': self.access_pattern.to_dict(),
            'performance_history': self.performance_history[-10:]  # 最近10次
        }


# ===== 测试代码 =====

def test_cache_aware_scheduler():
    """测试缓存感知调度器"""
    print("=" * 60)
    print("测试缓存感知调度器")
    print("=" * 60)
    
    scheduler = CacheAwareScheduler(capacity=100)
    
    # 测试1：时间局部性访问模式
    print("\n[测试1] 时间局部性访问模式")
    for i in range(50):
        key = f"key_{i % 10}"  # 只有10个不同的key，重复访问
        scheduler.access(key, f"value_{i}")
    
    stats = scheduler.get_stats()
    print(f"命中率: {stats['cache_state']['hit_rate']:.2%}")
    print(f"当前策略: {stats['current_policy']}")
    
    # 测试2：空间局部性访问模式
    print("\n[测试2] 空间局部性访问模式")
    for i in range(100, 120):
        key = str(i)  # 连续整数key
        scheduler.access(key, f"value_{i}")
    
    stats = scheduler.get_stats()
    print(f"命中率: {stats['cache_state']['hit_rate']:.2%}")
    print(f"当前策略: {stats['current_policy']}")
    
    # 测试3：随机访问模式
    print("\n[测试3] 随机访问模式")
    import random
    for i in range(50):
        key = f"random_{random.randint(0, 1000)}"
        scheduler.access(key, f"value_{i}")
    
    stats = scheduler.get_stats()
    print(f"命中率: {stats['cache_state']['hit_rate']:.2%}")
    print(f"当前策略: {stats['current_policy']}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_cache_aware_scheduler()
