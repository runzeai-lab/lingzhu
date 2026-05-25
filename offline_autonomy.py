import json
import time
import threading
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum

class NetworkStatus(Enum):
    """网络状态"""
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degrated"  # 网络质量差

class OfflineAutonomy:
    """
    离线自治引擎 - 增强离线自治能力
    
    功能：
    1. 离线决策引擎（无网络时自主决策）
    2. 本地知识库（离线可访问）
    3. 任务队列管理（离线时缓存任务）
    4. 自动同步机制（网络恢复后自动同步）
    5. 离线状态监控（检测网络状态）
    """
    
    def __init__(self, data_dir: str = "/tmp/offline_autonomy", 
                 sync_interval: int = 300):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sync_interval = sync_interval  # 同步间隔（秒）
        
        # 网络状态
        self.network_status = NetworkStatus.ONLINE
        self.last_online_check = None
        
        # 离线决策引擎
        self.decision_rules = []
        self.decision_log = []
        
        # 本地知识库
        self.local_knowledge_base = []
        self.knowledge_index = {}  # {keyword: [knowledge_ids]}
        
        # 任务队列
        self.task_queue = []
        self.completed_tasks = []
        
        # 同步状态
        self.sync_status = "idle"  # idle, syncing, error
        self.sync_history = []
        
        # 监控线程
        self.monitor_thread = None
        self.stop_monitor = threading.Event()
        
        # 统计信息
        self.stats = {
            "total_decisions": 0,
            "offline_decisions": 0,
            "tasks_queued": 0,
            "tasks_synced": 0,
            "knowledge_items": 0
        }
        
        # 启动网络监控
        self._start_network_monitor()
        
        print(f"离线自治引擎初始化完成，数据目录：{data_dir}，同步间隔：{sync_interval}秒")
    
    # ==================== 1. 离线决策引擎 ====================
    
    def make_decision(self, context: Dict, available_info: List[Dict] = []) -> Dict:
        """
        离线决策：无网络时自主决策
        
        Args:
            context: 决策上下文（当前状态、目标等）
            available_info: 可获取的信息（本地知识库、缓存等）
        
        Returns:
            {
                "decision": str,      # 决策结果
                "confidence": float,  # 置信度（0-1）
                "reasoning": str,     # 推理过程
                "offline": bool        # 是否离线决策
            }
        """
        self.stats["total_decisions"] += 1
        
        # 检查网络状态
        is_offline = self.network_status != NetworkStatus.ONLINE
        
        if is_offline:
            self.stats["offline_decisions"] += 1
        
        # 简化版决策：基于规则和优先级
        decision = "default_action"
        confidence = 0.5
        reasoning = "默认决策（基于规则）"
        
        # 如果有决策规则，应用规则
        for rule in self.decision_rules:
            if self._match_rule(rule, context):
                decision = rule["action"]
                confidence = rule["confidence"]
                reasoning = rule["reasoning"]
                break
        
        # 记录决策日志
        decision_entry = {
            "timestamp": str(datetime.now()),
            "context": context,
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "offline": is_offline
        }
        self.decision_log.append(decision_entry)
        
        # 如果日志太大，保存到文件
        if len(self.decision_log) > 50:
            self._save_decision_log()
            self.decision_log = []
        
        return {
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "offline": is_offline,
            "message": "决策完成"
        }
    
    def _match_rule(self, rule: Dict, context: Dict) -> bool:
        """检查规则是否匹配上下文"""
        conditions = rule.get("conditions", {})
        
        for key, value in conditions.items():
            if key not in context:
                return False
            if context[key] != value:
                return False
        
        return True
    
    def add_decision_rule(self, rule_name: str, conditions: Dict, 
                           action: str, confidence: float = 0.8, 
                           reasoning: str = ""):
        """添加决策规则"""
        rule = {
            "name": rule_name,
            "conditions": conditions,
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning
        }
        
        self.decision_rules.append(rule)
        
        return {
            "status": "success",
            "rule_name": rule_name,
            "total_rules": len(self.decision_rules),
            "message": f"决策规则 {rule_name} 已添加"
        }
    
    def _save_decision_log(self):
        """保存决策日志到文件"""
        log_file = self.data_dir / f"decision_log_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                for entry in self.decision_log:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            print(f"[离线自治] 决策日志已保存到 {log_file}")
        except Exception as e:
            print(f"[离线自治] 保存决策日志失败：{e}")
    
    # ==================== 2. 本地知识库 ====================
    
    def add_knowledge(self, title: str, content: str, tags: List[str] = []) -> Dict:
        """添加知识到本地知识库"""
        knowledge_id = f"kb_{int(time.time())}"
        
        knowledge_item = {
            "id": knowledge_id,
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": str(datetime.now()),
            "accessed_at": str(datetime.now())
        }
        
        self.local_knowledge_base.append(knowledge_item)
        self.stats["knowledge_items"] += 1
        
        # 更新知识索引
        for tag in tags:
            if tag not in self.knowledge_index:
                self.knowledge_index[tag] = []
            self.knowledge_index[tag].append(knowledge_id)
        
        # 如果知识库太大，保存到文件
        if len(self.local_knowledge_base) > 100:
            self._save_knowledge_base()
            self.local_knowledge_base = []
        
        return {
            "status": "success",
            "knowledge_id": knowledge_id,
            "message": f"知识 {title} 已添加到本地知识库"
        }
    
    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索本地知识库"""
        results = []
        
        # 简化版搜索：在标题和内容中查找关键词
        keywords = query.lower().split()
        
        for item in self.local_knowledge_base:
            score = 0
            for keyword in keywords:
                if keyword in item["title"].lower() or keyword in item["content"].lower():
                    score += 1
            
            if score > 0:
                item["relevance_score"] = score / max(len(keywords), 1)
                results.append(item)
        
        # 按相关性排序
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # 更新访问时间
        for item in results[:limit]:
            item["accessed_at"] = str(datetime.now())
        
        return results[:limit]
    
    def _save_knowledge_base(self):
        """保存知识库到文件"""
        kb_file = self.data_dir / "knowledge_base.json"
        
        try:
            with open(kb_file, "w", encoding="utf-8") as f:
                json.dump(self.local_knowledge_base, f, ensure_ascii=False, indent=2)
            print(f"[离线自治] 知识库已保存到 {kb_file}")
        except Exception as e:
            print(f"[离线自治] 保存知识库失败：{e}")
    
    # ==================== 3. 任务队列管理 ====================
    
    def queue_task(self, task_type: str, task_data: Dict, priority: int = 5) -> Dict:
        """
        缓存任务（离线时）
        
        Args:
            task_type: 任务类型
            task_data: 任务数据
            priority: 优先级（1-10，1最高）
        """
        task_id = f"task_{int(time.time())}"
        
        task = {
            "task_id": task_id,
            "type": task_type,
            "data": task_data,
            "priority": priority,
            "status": "queued",
            "created_at": str(datetime.now()),
            "synced": False
        }
        
        self.task_queue.append(task)
        self.stats["tasks_queued"] += 1
        
        # 按优先级排序
        self.task_queue.sort(key=lambda x: x["priority"])
        
        return {
            "task_id": task_id,
            "status": "queued",
            "queue_position": len(self.task_queue),
            "message": f"任务 {task_id} 已添加到队列"
        }
    
    def get_next_task(self) -> Optional[Dict]:
        """获取下一个任务（在线时执行）"""
        if not self.task_queue:
            return None
        
        return self.task_queue[0]
    
    def complete_task(self, task_id: str, result: Dict = {}) -> Dict:
        """完成任务（在线时执行）"""
        for i, task in enumerate(self.task_queue):
            if task["task_id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = str(datetime.now())
                task["result"] = result
                
                self.completed_tasks.append(task)
                self.task_queue.pop(i)
                self.stats["tasks_synced"] += 1
                
                return {
                    "status": "success",
                    "task_id": task_id,
                    "message": f"任务 {task_id} 已完成"
                }
        
        return {
            "status": "failed",
            "reason": f"Task {task_id} not found",
            "message": "任务完成失败"
        }
    
    # ==================== 4. 自动同步机制 ====================
    
    def sync_with_server(self, server_url: str = "") -> Dict:
        """
        与服务器同步（网络恢复后自动调用）
        
        简化版：模拟同步过程
        """
        if self.network_status != NetworkStatus.ONLINE:
            return {
                "status": "failed",
                "reason": "Still offline",
                "message": "同步失败：仍处于离线状态"
            }
        
        self.sync_status = "syncing"
        
        # 模拟同步过程
        synced_count = 0
        
        for task in self.completed_tasks:
            if not task.get("synced", False):
                # 模拟上传任务结果
                task["synced"] = True
                synced_count += 1
        
        self.sync_status = "idle"
        
        sync_entry = {
            "timestamp": str(datetime.now()),
            "synced_count": synced_count,
            "status": "completed"
        }
        self.sync_history.append(sync_entry)
        
        return {
            "status": "success",
            "synced_count": synced_count,
            "total_completed": len(self.completed_tasks),
            "message": f"同步完成，上传了 {synced_count} 个任务结果"
        }
    
    # ==================== 5. 离线状态监控 ====================
    
    def _start_network_monitor(self):
        """启动网络监控线程"""
        def monitor_loop():
            while not self.stop_monitor.is_set():
                # 简化版：模拟网络检测
                import random
                
                # 模拟网络状态变化
                if random.random() > 0.3:  # 70%时间在线
                    new_status = NetworkStatus.ONLINE
                else:
                    new_status = NetworkStatus.OFFLINE
                
                if new_status != self.network_status:
                    print(f"[离线自治] 网络状态变化：{self.network_status.value} → {new_status.value}")
                    self.network_status = new_status
                    
                    # 如果恢复到在线，触发同步
                    if new_status == NetworkStatus.ONLINE:
                        print("[离线自治] 网络恢复，开始同步...")
                        self.sync_with_server()
                
                self.last_online_check = datetime.now()
                
                # 等待一段时间再检查
                time.sleep(10)  # 每10秒检查一次
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print("[离线自治] 网络监控线程已启动")
    
    def get_network_status(self) -> Dict:
        """获取网络状态"""
        return {
            "status": self.network_status.value,
            "last_check": str(self.last_online_check),
            "sync_status": self.sync_status,
            "message": "网络状态"
        }
    
    # ==================== 统计信息 ====================
    
    def get_autonomy_stats(self) -> Dict:
        """获取离线自治统计信息"""
        return {
            "stats": self.stats,
            "network_status": self.network_status.value,
            "sync_status": self.sync_status,
            "decision_rules_count": len(self.decision_rules),
            "task_queue_size": len(self.task_queue),
            "completed_tasks_count": len(self.completed_tasks),
            "local_knowledge_count": self.stats["knowledge_items"],
            "message": "离线自治统计信息"
        }
