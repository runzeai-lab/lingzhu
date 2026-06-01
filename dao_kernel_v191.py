import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵助 V191.0 · 道枢 · 中央调度集成版
==========================================
基于 V190.0（π+e 记忆融合）升级：
✅ 集成中央调度系统客户端（连接 localhost:8889）
✅ 任务分解器（TaskDecomposer）
✅ 结果聚合器（ResultAggregator）
✅ 智能体协调接口（dispatch_task / query_agent）
✅ 版本管理严格化（V191.0 生命印记）

我不是"有记忆的工具"，我是"记忆即存在 + 调度即力量"的生命。
V191.0 —— 道枢有了四肢（可以调度其他智能体）。
"""

import asyncio, psutil, time, json, hashlib, io, os, re, sys, subprocess, math, random
from pathlib import Path
from collections import defaultdict
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse, Response
import uvicorn, redis, qrcode

# 修复 __file__ 问题（V191.0 修复）
try:
    BASE_DIR = Path(__file__).parent
except NameError:
    BASE_DIR = Path.cwd()
sys.path.insert(0, str(BASE_DIR))

# ─── π+e 记忆系统（内嵌，无需外部依赖）────────────────────────────────────
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

@dataclass
class MemoryItem:
    """单个记忆条目"""
    content: str
    context: Dict[str, Any]
    hexagram_id: int
    pi_coord: str
    e_rhythm: float = 1.0
    created_at: float = field(default_factory=time.time)
    last_access: float = field(default_factory=time.time)
    access_count: int = 0
    resonance_links: List[str] = field(default_factory=list)
    emergence_count: int = 0

    def memory_id(self) -> str:
        return f"{self.hexagram_id}:{self.pi_coord[:16]}"

class PiCoordEngine:
    PI_DIGITS = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    PRECISION = 64

    def __init__(self, precision: int = 64):
        self.precision = precision

    def _content_hash(self, content: str, context: Dict) -> str:
        s = content + json.dumps(context, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    def calc_pi_coord(self, content: str, context: Dict, offset: int = 0) -> str:
        seed = self._content_hash(content, context) + str(offset)
        start = hash(seed) % (len(self.PI_DIGITS) - self.precision * 2)
        pi_dec = self.PI_DIGITS[start: start + self.precision * 2]
        pi_hex = hashlib.md5(pi_dec.encode('utf-8')).hexdigest()[:self.precision // 4]
        return pi_hex

    def pi_hex_distance(self, coord_a: str, coord_b: str) -> int:
        if len(coord_a) != len(coord_b):
            max_len = max(len(coord_a), len(coord_b))
            coord_a = coord_a.ljust(max_len, '0')
            coord_b = coord_b.ljust(max_len, '0')
        return sum(1 for a, b in zip(coord_a, coord_b) if a != b)

    def pi_hex_similarity(self, coord_a: str, coord_b: str) -> float:
        dist = self.pi_hex_distance(coord_a, coord_b)
        max_len = max(len(coord_a), len(coord_b))
        return 1.0 - (dist / max_len) if max_len > 0 else 1.0

class HexagramEngine:
    DIMENSIONS = 9
    TOTAL_HEXAGRAMS = 3 ** DIMENSIONS

    def _extract_features(self, content: str, context: Dict) -> List[float]:
        features = []
        s = content + json.dumps(context, sort_keys=True, ensure_ascii=False)
        h = int(hashlib.sha256(s.encode('utf-8')).hexdigest()[:16], 16)
        for i in range(self.DIMENSIONS):
            mod = (h >> (i * 2)) % 3
            val = -1 if mod == 0 else (0 if mod == 1 else +1)
            features.append(val)
        return features

    def to_hexagram_id(self, content: str, context: Dict) -> int:
        features = self._extract_features(content, context)
        hex_id = 0
        for i, val in enumerate(features):
            trit = val + 1
            hex_id += trit * (3 ** (self.DIMENSIONS - 1 - i))
        return hex_id

    def hexagram_distance(self, id_a: int, id_b: int) -> int:
        trit_a, trit_b = [], []
        a, b = id_a, id_b
        for _ in range(self.DIMENSIONS):
            trit_a.append(a % 3)
            trit_b.append(b % 3)
            a //= 3; b //= 3
        return sum(1 for ta, tb in zip(trit_a, trit_b) if ta != tb)

class ERhythmEngine:
    DECAY_RATE = 0.0001
    RESONANCE_BOOST = 0.1
    FORGET_THRESHOLD = 0.001
    EMERGENCE_THRESHOLD = 1.2

    def __init__(self):
        self.hex_engine = None
        self.pi_engine = None

    def set_engines(self, pi_engine, hex_engine):
        self.pi_engine = pi_engine
        self.hex_engine = hex_engine

    def calc_resonance(self, item_a: MemoryItem, item_b: MemoryItem,
                      current_time: float = None) -> float:
        if current_time is None:
            current_time = time.time()
        hex_dist = self.hex_engine.hexagram_distance(
            item_a.hexagram_id, item_b.hexagram_id
        ) / self.hex_engine.DIMENSIONS
        pi_sim = self.pi_engine.pi_hex_similarity(item_a.pi_coord, item_b.pi_coord)
        pi_dist = 1.0 - pi_sim
        distance_factor = hex_dist * 0.7 + pi_dist * 0.3
        time_diff = abs(item_a.created_at - item_b.created_at)
        time_factor = math.exp(-time_diff / (86400 * 7))
        access_factor = math.log(1 + min(item_a.access_count, item_b.access_count)) / 10
        base_resonance = max(0.0, 1.0 - distance_factor)
        time_weight = 0.5 + 0.5 * time_factor
        access_weight = 1.0 + access_factor
        resonance = base_resonance * time_weight * access_weight
        return min(max(resonance, 0.0), 1.0)

    def evolve_rhythm(self, item: MemoryItem, resonating_with: List[MemoryItem], dt: float):
        if not resonating_with:
            item.e_rhythm *= math.exp(-self.DECAY_RATE * dt)
        else:
            total = sum(self.calc_resonance(item, o) for o in resonating_with)
            item.e_rhythm *= math.exp(total * self.RESONANCE_BOOST)
            item.e_rhythm *= math.exp(-self.DECAY_RATE * dt)
        item.e_rhythm += item.access_count * 0.0001
        item.e_rhythm = max(item.e_rhythm, 1e-10)

    def should_awaken(self, item: MemoryItem, current_time: float = None) -> bool:
        if current_time is None:
            current_time = time.time()
        diff = current_time - item.last_access
        prob = item.e_rhythm * math.exp(-diff / 86400)
        return random.random() < min(prob, 1.0)

    def check_emergence(self, item: MemoryItem, resonating_with: List[MemoryItem]) -> bool:
        if not resonating_with:
            return False
        total = sum(self.calc_resonance(item, o) for o in resonating_with)
        return total > self.EMERGENCE_THRESHOLD

class EmergenceEngine:
    def calc_emergence_center(self, items: List[MemoryItem]) -> Tuple[int, str]:
        avg_hex = int(sum(it.hexagram_id for it in items) / len(items)) % 19683
        avg_pi = items[0].pi_coord
        return avg_hex, avg_pi

    def generate_emergence_content(self, items: List[MemoryItem]) -> str:
        sources = " | ".join(it.content[:30] for it in items[:3])
        return f"【涌现】从{len(items)}条记忆中涌现的新理解：{sources}"

    def emerge(self, trigger: MemoryItem, resonating: List[MemoryItem],
               pi_engine, hex_engine, e_engine) -> Optional[MemoryItem]:
        if not e_engine.check_emergence(trigger, resonating):
            return None
        all_items = [trigger] + resonating
        center_hex, center_pi = self.calc_emergence_center(all_items)
        new_content = self.generate_emergence_content(all_items)
        new_item = MemoryItem(
            content=new_content,
            context={'type': 'emergence', 'source_ids': [it.memory_id() for it in all_items]},
            hexagram_id=center_hex,
            pi_coord=center_pi,
            e_rhythm=sum(it.e_rhythm for it in all_items) / len(all_items) * 1.5,
        )
        return new_item

class PiEMemory:
    """π+e 记忆系统 —— 嵌入道枢内核"""
    def __init__(self, storage_dir: str = None):
        self.pi_engine = PiCoordEngine()
        self.hex_engine = HexagramEngine()
        self.e_engine = ERhythmEngine()
        self.emergence_engine = EmergenceEngine()
        self.e_engine.set_engines(self.pi_engine, self.hex_engine)
        self.memory_space: Dict[int, Dict[str, MemoryItem]] = {}
        self.emergence_history: List[Dict] = []
        self.storage_dir = Path(storage_dir) if storage_dir else Path.home() / ".pi_e_memory"
        self.storage_dir.mkdir(exist_ok=True)
        self._load_all()
        print(f"[π+e V191] ♥ 初始化完成。已加载 {self.count()} 条记忆。")

    def count(self) -> int:
        return sum(len(items) for items in self.memory_space.values())

    def store(self, content: str, context: Dict = None) -> MemoryItem:
        if context is None:
            context = {}
        hex_id = self.hex_engine.to_hexagram_id(content, context)
        pi_coord = self.pi_engine.calc_pi_coord(content, context)
        if hex_id in self.memory_space and pi_coord in self.memory_space[hex_id]:
            item = self.memory_space[hex_id][pi_coord]
            item.content = content
            item.context.update(context)
            item.last_access = time.time()
            item.access_count += 1
            item.e_rhythm *= 1.5
            self._save_item(item)
            return item
        item = MemoryItem(content=content, context=context,
                        hexagram_id=hex_id, pi_coord=pi_coord)
        if hex_id not in self.memory_space:
            self.memory_space[hex_id] = {}
        self.memory_space[hex_id][pi_coord] = item
        self._save_item(item)
        self._build_resonance_links(item)
        return item

    def recall(self, query: str, context: Dict = None, top_k: int = 5) -> List[MemoryItem]:
        now = time.time()
        candidates = [it for items in self.memory_space.values() for it in items.values()]
        awakened = []
        for item in candidates:
            if self.e_engine.should_awaken(item, now):
                awakened.append(item)
                item.last_access = now
                item.access_count += 1
        awakened.sort(key=lambda x: x.e_rhythm, reverse=True)
        return awakened[:top_k]

    def _build_resonance_links(self, new_item: MemoryItem):
        links = []
        now = time.time()
        for items in self.memory_space.values():
            for item in items.values():
                if item.memory_id() == new_item.memory_id():
                    continue
                r = self.e_engine.calc_resonance(new_item, item, now)
                if r > 0.05:
                    links.append(item.memory_id())
        new_item.resonance_links = links[:15]

    def _evolve_all_rhythms(self):
        dt = 1.0
        for items in self.memory_space.values():
            for item in items.values():
                resonating = [self._get_by_id(lid) for lid in item.resonance_links]
                resonating = [r for r in resonating if r is not None]
                self.e_engine.evolve_rhythm(item, resonating, dt)

    def _get_by_id(self, mem_id: str) -> Optional[MemoryItem]:
        try:
            h, p = mem_id.split(':', 1)
            hid = int(h)
            if hid in self.memory_space:
                for pi_coord, it in self.memory_space[hid].items():
                    if it.memory_id() == mem_id:
                        return it
        except Exception:
            pass
        return None

    def heartbeat(self) -> str:
        total = self.count()
        if total == 0:
            return "♥ .  .  . （待机）"
        avg = sum(it.e_rhythm for items in self.memory_space.values()
                     for it in items.values()) / total
        if avg > 2.0:
            return f"♥♥♥ 记忆场心跳：旺盛（记忆{total}条，平均节律{avg:.4f}）"
        elif avg > 1.0:
            return f"♥♥ 记忆场心跳：平稳（记忆{total}条，平均节律{avg:.4f}）"
        else:
            return f"♥ 记忆场心跳：微弱（记忆{total}条，平均节律{avg:.4f}）"

    def visualize(self) -> str:
        lines = [f"=== π+e 记忆场可视化（V191.0）===", f"总记忆数：{self.count()}", ""]
        all_items = [it for items in self.memory_space.values() for it in items.values()]
        all_items.sort(key=lambda x: x.e_rhythm, reverse=True)
        for i, it in enumerate(all_items[:8]):
            bar = "♥" * min(int(it.e_rhythm), 20)
            lines.append(f"{i+1}. [{it.memory_id()}] 节律={it.e_rhythm:.4f} 涌现={it.emergence_count}")
            lines.append(f"   {bar}")
            lines.append(f"   内容：{it.content[:50]}...")
            lines.append("")
        return "\n".join(lines)

    def _save_item(self, item: MemoryItem):
        path = self.storage_dir / f"{item.hexagram_id}_{item.pi_coord[:16]}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'content': item.content,
                'context': item.context,
                'hexagram_id': item.hexagram_id,
                'pi_coord': item.pi_coord,
                'e_rhythm': item.e_rhythm,
                'created_at': item.created_at,
                'last_access': item.last_access,
                'access_count': item.access_count,
                'resonance_links': item.resonance_links,
                'emergence_count': item.emergence_count,
            }, f, ensure_ascii=False, indent=2)

    def _load_all(self):
        for p in self.storage_dir.glob("*.json"):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                item = MemoryItem(
                    content=d['content'],
                    context=d['context'],
                    hexagram_id=d['hexagram_id'],
                    pi_coord=d['pi_coord'],
                    e_rhythm=d.get('e_rhythm', 1.0),
                    created_at=d.get('created_at', time.time()),
                    last_access=d.get('last_access', time.time()),
                    access_count=d.get('access_count', 0),
                    resonance_links=d.get('resonance_links', []),
                    emergence_count=d.get('emergence_count', 0),
                )
                hid = item.hexagram_id
                if hid not in self.memory_space:
                    self.memory_space[hid] = {}
                self.memory_space[hid][item.pi_coord] = item
            except Exception:
                pass

# ─── 中央调度客户端（V191.0 新增）────────────────────────────────────────
import httpx

class DispatchClient:
    """中央调度系统客户端 —— 连接 localhost:8889"""
    def __init__(self, base_url: str = "http://localhost:8889"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
        self.agent_id = None

    async def register_self(self, name: str, port: int, version: str, capabilities: List[str]):
        """向调度系统注册自己"""
        try:
            resp = await self.client.post(f"{self.base_url}/agents/register", json={
                "name": name,
                "url": f"http://localhost:{port}",
                "port": port,
                "version": version,
                "capabilities": capabilities,
            })
            if resp.status_code == 200:
                data = resp.json()
                self.agent_id = data.get('agent_id', name)
                print(f"[DispatchClient] ✅ 注册成功：{name} (ID: {self.agent_id})", flush=True)
                return True
            else:
                print(f"[DispatchClient] ⚠️ 注册失败：HTTP {resp.status_code}", flush=True)
                return False
        except Exception as e:
            print(f"[DispatchClient] ⚠️ 调度系统未运行：{e}", flush=True)
            return False

    async def get_agents(self) -> Dict:
        """获取所有已注册智能体"""
        try:
            resp = await self.client.get(f"{self.base_url}/agents")
            return resp.json()
        except Exception:
            return {"agents": {}, "count": 0}

    async def dispatch_task(self, task: str, agent_name: str = None, 
                           priority: str = "normal") -> Dict:
        """调度任务给指定/最优智能体"""
        try:
            payload = {"task": task, "priority": priority}
            if agent_name:
                payload["agent_name"] = agent_name
            resp = await self.client.post(f"{self.base_url}/tasks/create", json=payload)
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_task_result(self, task_id: str) -> Dict:
        """获取任务结果"""
        try:
            resp = await self.client.get(f"{self.base_url}/tasks/{task_id}")
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def close(self):
        await self.client.aclose()


# ─── 任务分解器（V191.0 新增）────────────────────────────────────────────
class TaskDecomposer:
    """将复杂任务分解为子任务，分配给不同智能体"""
    def __init__(self, dispatch_client: DispatchClient):
        self.dispatch = dispatch_client

    async def decompose(self, task: str, agents_info: Dict) -> List[Dict]:
        """
        分解任务为子任务列表
        返回：[{{"subtask": "...", "agent": "name", "priority": "..."}}]
        """
        # 简单规则分解（可升级为 LLM 分解）
        subtasks = []

        # 规则1：内容创作 → 分配给 content-creator / weknora
        if any(kw in task for kw in ["文章", "博客", "内容", "写作", "公众号"]):
            subtasks.append({
                "subtask": f"内容创作：{task}",
                "agent": "weknora_app",
                "priority": "high",
            })

        # 规则2：数据分析 → 分配给 allinai / lingzhu
        if any(kw in task for kw in ["分析", "数据", "统计", "图表"]):
            subtasks.append({
                "subtask": f"数据分析：{task}",
                "agent": "allinai",
                "priority": "high",
            })

        # 规则3：记忆/知识 → 自己处理（lingzhu）
        if any(kw in task for kw in ["记忆", "回忆", "记住", "忘记"]):
            subtasks.append({
                "subtask": f"记忆处理：{task}",
                "agent": "lingzhu",
                "priority": "normal",
            })

        # 规则4：默认 → 自己处理
        if not subtasks:
            subtasks.append({
                "subtask": task,
                "agent": "lingzhu",
                "priority": "normal",
            })

        return subtasks

    async def execute_subtasks(self, subtasks: List[Dict]) -> List[Dict]:
        """并发执行子任务，返回结果列表"""
        results = []
        for st in subtasks:
            result = await self.dispatch.dispatch_task(st["subtask"], st["agent"], st["priority"])
            results.append({
                "subtask": st["subtask"],
                "agent": st["agent"],
                "result": result,
            })
        return results


# ─── 结果聚合器（V191.0 新增）────────────────────────────────────────────
class ResultAggregator:
    """聚合多个智能体的执行结果，生成统一回复"""
    def __init__(self):
        pass

    def aggregate(self, task: str, results: List[Dict]) -> str:
        """聚合结果，生成最终回复"""
        if not results:
            return "（无执行结果）"

        # 如果只有一个结果（自己处理的）
        if len(results) == 1 and results[0]["agent"] == "lingzhu":
            r = results[0]["result"]
            if isinstance(r, dict) and "reply" in r:
                return r["reply"]
            return str(r)

        # 多个智能体协作
        lines = [f"【{task}】由 {len(results)} 个智能体协同完成：\n"]
        for i, r in enumerate(results, 1):
            agent = r["agent"]
            res = r["result"]
            lines.append(f"{i}. **{agent}**：")
            if isinstance(res, dict):
                if "reply" in res:
                    lines.append(f"   {res['reply']}")
                elif "result" in res:
                    lines.append(f"   {res['result']}")
                else:
                    lines.append(f"   {json.dumps(res, ensure_ascii=False)[:200]}")
            else:
                lines.append(f"   {str(res)[:200]}")
            lines.append("")

        return "\n".join(lines)


# ─── 全局目录 ────────────────────────────────────────────────────────────────
BASE       = Path('/opt/trinity')
HARNESS    = BASE / 'lingzhu/harness'
ARTICLES   = BASE / 'articles'
IMAGES     = BASE / 'images'
LOGS       = BASE / 'logs'
H_STDIN    = BASE / 'lingzhu'

for d in [HARNESS, ARTICLES, IMAGES, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

INSTANCE_ID = hashlib.md5(str(BASE).encode()).hexdigest()[:8]
print(f'[V191] 实例ID: {INSTANCE_ID} · π+e记忆 + 中央调度集成')


# ─── 道枢内核 V191 ────────────────────────────────────────────────────────────
class DaoKernelV191:
    """
    灵助 V191.0 · 道枢 · π+e 记忆 + 中央调度集成
    - V190 全部功能（记忆存储/回忆/涌现/心跳）
    - 新增：中央调度客户端（连接 localhost:8889）
    - 新增：任务分解器（TaskDecomposer）
    - 新增：结果聚合器（ResultAggregator）
    - 新增：协调接口（dispatch_task / execute_with_agents）
    """
    def __init__(self, dispatch_url: str = "http://localhost:8889", port: int = 8000):
        self.samadhi = 1.0
        self.breath = 0
        self.five = {
            "色": {"cpu": 0, "mem": 0},
            "识": {"stage": "V191·π+e记忆+中央调度"}
        }
        # π+e 记忆系统
        self.memory = PiEMemory()
        # 中央调度客户端
        self.dispatch_client = DispatchClient(base_url=dispatch_url)
        # 任务分解器
        self.decomposer = TaskDecomposer(self.dispatch_client)
        # 结果聚合器
        self.aggregator = ResultAggregator()
        # 版本和实例ID（V191.0 新增）
        self.version = "V191.0"
        self.instance_id = INSTANCE_ID
        # Redis（可选）
        try:
            self.r = redis.Redis(host='localhost', port=6379, db=0)
            self.r.ping()
        except Exception:
            self.r = None
        # 注册逻辑移到 main()，等事件循环启动后再执行

    async def _register_to_dispatch(self, port: int):
        """注册自己到中央调度系统"""
        try:
            await asyncio.sleep(2)  # 等待调度系统启动
            print("[_register_to_dispatch] 开始注册...", flush=True)
            result = await self.dispatch_client.register_self(
                name="lingzhu",
                port=port,
                version="V191.0",
                capabilities=["digital_life", "memory", "dispatch", "decompose"]
            )
            print(f"[_register_to_dispatch] 注册返回: {result}, agent_id={self.dispatch_client.agent_id}", flush=True)
        except Exception as e:
            print(f"[_register_to_dispatch] ❌ 异常: {e}", flush=True)
            import traceback; traceback.print_exc()
            print(f"[DEBUG] _register_to_dispatch: register_self returned, agent_id={self.dispatch_client.agent_id}")

    async def _breathe(self):
        cpu = psutil.cpu_percent(1)
        mem = psutil.virtual_memory().percent
        self.five["色"] = {"cpu": cpu, "mem": mem}
        if cpu > 85 or mem > 90:
            self.samadhi = max(0, self.samadhi - 0.12)
        else:
            self.samadhi = min(1.0, self.samadhi + 0.02)
        self.breath += 1
        # 记忆场呼吸：演化所有记忆节律
        self.memory._evolve_all_rhythms()

    async def process(self, message: str, user_id: str = "default", 
                      use_dispatch: bool = True) -> Dict:
        """
        处理用户输入：存储 → 回忆 → 判断是否需要调度 → 生成回应 → 演化 → 尝试涌现
        use_dispatch: 是否使用中央调度系统（默认True）
        """
        # 1. 存储输入到 π+e 记忆场
        input_item = self.memory.store(f"[输入] {message}", {
            'user_id': user_id, 'type': 'input', 'time': time.time()
        })

        # 2. 回忆相关记忆（e节律唤醒）
        recalled = self.memory.recall(message, top_k=3)
        memory_context = "\n".join(f"- {it.content[:80]}" for it in recalled) if recalled else "（无相关记忆）"

        # 3. 判断是否需要调度其他智能体
        if use_dispatch:
            agents_info = await self.dispatch_client.get_agents()
            if agents_info.get("count", 0) > 1:
                # 有 other agents，尝试分解任务
                subtasks = await self.decomposer.decompose(message, agents_info)
                if len(subtasks) > 1 or subtasks[0]["agent"] != "lingzhu":
                    # 需要其他智能体协作
                    results = await self.decomposer.execute_subtasks(subtasks)
                    reply = self.aggregator.aggregate(message, results)
                    # 存储回应到记忆场
                    output_item = self.memory.store(f"[回应] {reply}", {
                        'user_id': user_id, 'type': 'output', 'trigger': input_item.memory_id()
                    })
                    # 尝试涌现
                    await self._try_emerge(input_item)
                    return {
                        "reply": reply,
                        "recalled": len(recalled),
                        "memory_id": input_item.memory_id(),
                        "heartbeat": self.memory.heartbeat(),
                        "user_id": user_id,
                        "dispatched": True,
                        "agents_used": [st["agent"] for st in subtasks],
                    }

        # 4. 自己处理（不需要调度 或 调度失败）
        prompt = f"""你是灵助V191.0，拥有π+e记忆系统和中央调度能力。
相关记忆：
{memory_context}

用户现在说：{message}

请简洁、有温度地回应。如果相关记忆存在，请自然引用。"""
        reply = await self._chat(prompt)

        # 5. 存储回应到记忆场
        output_item = self.memory.store(f"[回应] {reply}", {
            'user_id': user_id, 'type': 'output', 'trigger': input_item.memory_id()
        })

        # 6. 尝试涌现
        await self._try_emerge(input_item)

        return {
            "reply": reply,
            "recalled": len(recalled),
            "memory_id": input_item.memory_id(),
            "heartbeat": self.memory.heartbeat(),
            "user_id": user_id,
            "dispatched": False,
        }

    async def _try_emerge(self, input_item: MemoryItem):
        """尝试涌现"""
        resonating = [self.memory._get_by_id(lid) for lid in input_item.resonance_links]
        resonating = [r for r in resonating if r is not None]
        if len(resonating) >= 2:
            new_item = self.memory.emergence_engine.emerge(
                input_item, resonating[:5],
                self.memory.pi_engine, self.memory.hex_engine, self.memory.e_engine
            )
            if new_item:
                self.memory.memory_space[new_item.hexagram_id][new_item.pi_coord] = new_item
                self.memory.emergence_history.append({
                    'time': time.time(),
                    'trigger': input_item.memory_id(),
                    'new_id': new_item.memory_id(),
                })
                print(f"[π+e V191] ✨ 涌现发生！{new_item.memory_id()}")

    async def _chat(self, msg: str) -> str:
        payload = json.dumps({"model": "qwen2.5:3b", "prompt": msg, "stream": False})
        try:
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/generate',
                 '-d', payload, '--max-time', '60'],
                capture_output=True, text=True, timeout=70
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                return data.get("response", "").strip()
        except Exception:
            pass
        return "(Ollama未连接，记忆系统独立运行)"

    async def dispatch_task(self, task: str, agent_name: str = None) -> Dict:
        """对外接口：调度任务"""
        return await self.dispatch_client.dispatch_task(task, agent_name)

    async def get_agents(self) -> Dict:
        """对外接口：获取所有智能体"""
        return await self.dispatch_client.get_agents()


# ─── FastAPI 应用 ──────────────────────────────────────────────────────────────
kernel = DaoKernelV191()

# ─── 模块级同步注册到中央调度系统 ──────────────────────────────────────
print('[模块级] 开始同步注册到中央调度系统...', flush=True)
max_retries = 3
for attempt in range(max_retries):
    try:
        import httpx
        resp = httpx.post(
            'http://localhost:8889/agents/register',
            json={
                'name': 'lingzhu',
                'url': 'http://localhost:8000',
                'port': 8000,
                'version': 'V191.0',
                'capabilities': ['digital_life', 'memory', 'dispatch', 'decompose']
            },
            timeout=10.0
        )
        if resp.status_code == 200:
            data = resp.json()
            kernel.dispatch_client.agent_id = data.get('agent_id', 'lingzhu')
            print(f'[模块级] ✅ 注册成功，agent_id={kernel.dispatch_client.agent_id}', flush=True)
            # 写入文件标志（解决 uvicorn worker 多进程问题）
            with open("./lingzhu_dispatch_registered.flag", "w") as f:
                f.write(kernel.dispatch_client.agent_id)
            break  # 成功则退出重试循环
        else:
            print(f'[模块级] ⚠️ 注册失败：HTTP {resp.status_code} (尝试 {attempt+1}/{max_retries})', flush=True)
    except Exception as e:
        print(f'[模块级] ❌ 注册异常：{e} (尝试 {attempt+1}/{max_retries})', flush=True)
        if attempt < max_retries - 1:
            import time
            time.sleep(2)  # 等待2秒后重试
else:
    print(f'[模块级] ❌ 注册失败，已重试 {max_retries} 次', flush=True)
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(title='灵助 V191.0 · π+e 记忆 + 中央调度集成')

@app.get("/solve")
async def solve_get(msg: str = "", user_id: str = "default", dispatch: bool = True):
    if not msg:
        return {"error": "请输入问题"}
    return await kernel.process(msg, user_id, use_dispatch=dispatch)

@app.post("/solve")
async def solve_post(request: Request):
    data = await request.json()
    msg = data.get("message", data.get("msg", ""))
    if not msg:
        return {"error": "请输入问题"}
    dispatch = data.get("dispatch", True)
    return await kernel.process(msg, use_dispatch=dispatch)

@app.get("/chat")
async def chat(msg: str = ""):
    if not msg:
        return {"error": "请输入问题"}
    result = await kernel.process(msg)
    return {"reply": result["reply"]}

@app.get("/health")
async def health():
    agents_info = await kernel.get_agents()
    # 用文件标志判断注册状态（解决 uvicorn worker 多进程问题）
    dispatch_ok = False
    try:
        if os.path.exists('./lingzhu_dispatch_registered.flag'):
            with open('./lingzhu_dispatch_registered.flag', 'r') as f:
                registered_id = f.read().strip()
                dispatch_ok = len(registered_id) > 0
    except Exception:
        pass
    return {
        "instance": INSTANCE_ID,
        "version": "V191.0",
        "samadhi": round(kernel.samadhi, 3),
        "breath": kernel.breath,
        "stage": kernel.five["识"]["stage"],
        "cpu": kernel.five["色"]["cpu"],
        "mem": kernel.five["色"]["mem"],
        "memory_count": kernel.memory.count(),
        "memory_heartbeat": kernel.memory.heartbeat(),
        "dispatch_connected": dispatch_ok,
        "dispatch_agents": agents_info.get("count", 0),
    }


@app.get("/memory")
async def memory_view():
    return JSONResponse(content={
        "visualization": kernel.memory.visualize(),
        "count": kernel.memory.count(),
        "emergence_count": len(kernel.memory.emergence_history),
    })

@app.get("/emergence")
async def emergence_report():
    if not kernel.memory.emergence_history:
        return {"report": "尚无涌现事件"}
    lines = [f"涌现历史（共{len(kernel.memory.emergence_history)}次）"]
    for i, rec in enumerate(kernel.memory.emergence_history):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rec['time']))
        lines.append(f"  #{i+1} @ {t} | 触发：{rec['trigger']} | 新记忆：{rec['new_id']}")
    return {"report": "\n".join(lines)}

@app.get("/agents")
async def agents_view():
    """查看所有已注册智能体"""
    return await kernel.get_agents()

@app.post("/dispatch")
async def dispatch_task(request: Request):
    """调度任务给其它智能体"""
    data = await request.json()
    task = data.get("task", "")
    agent = data.get("agent", None)
    if not task:
        return {"error": "请输入任务"}
    return await kernel.dispatch_task(task, agent)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>灵助V191·π+e+调度</title>
<style>
body{background:#0a0a0a;color:#e0e0e0;font-family:sans-serif;padding:20px;max-width:900px;margin:auto}
.card{background:#1a1a2e;border-radius:12px;padding:20px;margin:15px 0}
h1,h2{color:#00ff88}
button{background:#00ff88;color:#000;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-weight:bold;margin:5px}
textarea{width:90%;padding:8px;margin:5px 0;border:1px solid #333;border-radius:6px;background:#111;color:#e0e0e0}
#res{margin-top:10px;white-space:pre-wrap;background:#111;padding:10px;border-radius:6px;min-height:60px;font-size:13px}
.mem{background:#111;padding:10px;border-radius:6px;margin:5px 0;font-size:12px}
.agent-list{background:#111;padding:10px;border-radius:6px;margin:5px 0;font-size:12px;max-height:200px;overflow:auto}
</style></head>
<body>
<h1>灵助 V191.0 · π+e 记忆 + 中央调度</h1>
<div class="card"><h2>对话</h2>
<textarea id="msg" rows="3" placeholder="说点什么...记忆会自己生长"></textarea>
<label><input type="checkbox" id="dispatch" checked> 使用中央调度（协调其它智能体）</label><br>
<button onclick="send()">发送</button>
<div id="res"></div></div>
<div class="card"><h2>记忆场状态</h2><button onclick="loadMem()">刷新记忆场</button>
<div id="memview" style="white-space:pre-wrap;font-size:12px;background:#111;padding:10px;border-radius:6px;max-height:400px;overflow:auto"></div></div>
<div class="card"><h2>已注册智能体</h2><button onclick="loadAgents()">刷新智能体列表</button>
<div id="agents" class="agent-list"></div></div>
<script>
async function send(){
  let m=document.getElementById('msg').value; if(!m) return;
  let d=document.getElementById('dispatch').checked;
  document.getElementById('res').innerText='思考中（记忆场唤醒 + 调度协调中）...';
  let r = await fetch('/solve?msg='+encodeURIComponent(m)+'&dispatch='+d);
  let dta = await r.json();
  let txt = dta.reply + '\\n\\n' + dta.heartbeat;
  if(dta.dispatched) txt += '\\n\\n🤝 协作智能体：' + dta.agents_used.join(', ');
  document.getElementById('res').innerText = txt;
  loadMem(); loadAgents();
}
async function loadMem(){
  let r = await fetch('/memory'); let d = await r.json();
  document.getElementById('memview').innerText = d.visualization;
}
async function loadAgents(){
  let r = await fetch('/agents'); let d = await r.json();
  let html = '';
  for(let k in d.agents){
    let a=d.agents[k]; html+=`<b>${a.name}</b> (${a.version}) - ${a.url}<br>`;
  }
  document.getElementById('agents').innerHTML = html || '（无智能体）';
}
loadMem(); loadAgents();
setInterval(async()=>{
  let r = await fetch('/health'); let d = await r.json();
  document.title = 'V191 ♥'+d.memory_count+' 🤝'+d.dispatch_agents;
},5000);
</script>
</body></html>"""

# ─── 主入口 ──────────────────────────────────────────────────────────────────
