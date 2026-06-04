import sqlite3
import time
import json
from typing import List, Dict, Optional
from datetime import datetime

class UnifiedTaskLedger:
    """统一任务账本：进化任务、自愈动作、蜂群任务全部归入"""
    
    def __init__(self, db_path: str = "/root/ai-stack/lingzhu/tasks.db"):
        self.db = sqlite3.connect(db_path)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 5,
                parent_id TEXT,
                assigned_agent TEXT,
                payload TEXT,
                heartbeat_at REAL,
                created_at REAL,
                completed_at REAL,
                result TEXT,
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3
            )
        """)
        self.db.commit()
    
    def create_task(self, task_id: str, task_type: str, payload: dict = None,
                    priority: int = 5, parent_id: str = None,
                    assigned_agent: str = None) -> str:
        """创建新任务"""
        self.db.execute(
            "INSERT OR REPLACE INTO tasks (id, task_type, status, priority, parent_id, assigned_agent, payload, heartbeat_at, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (task_id, task_type, 'pending', priority, parent_id, assigned_agent,
             json.dumps(payload or {}), time.time(), time.time())
        )
        self.db.commit()
        return task_id
    
    def update_heartbeat(self, task_id: str):
        """更新任务心跳"""
        self.db.execute("UPDATE tasks SET heartbeat_at=? WHERE id=?", (time.time(), task_id))
        self.db.commit()
    
    def get_lost_tasks(self, timeout: float = 30) -> List[Dict]:
        """获取心跳丢失的任务，用于自动恢复"""
        cutoff = time.time() - timeout
        cursor = self.db.execute(
            "SELECT id, task_type, status, assigned_agent, heartbeat_at FROM tasks WHERE heartbeat_at < ? AND status = 'in_progress'",
            (cutoff,)
        )
        return [{"task_id": row[0], "task_type": row[1], "status": row[2], 
                "assigned_agent": row[3], "heartbeat_at": row[4]} for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: str, status: str, result: str = None):
        """更新任务状态"""
        if status == "completed" or status == "failed":
            self.db.execute(
                "UPDATE tasks SET status=?, result=?, completed_at=? WHERE id=?",
                (status, result, time.time(), task_id)
            )
        else:
            self.db.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        self.db.commit()
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        cursor = self.db.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = cursor.fetchone()
        if row:
            columns = ["id", "task_type", "status", "priority", "parent_id", 
                      "assigned_agent", "payload", "heartbeat_at", "created_at", 
                      "completed_at", "result", "retry_count", "max_retries"]
            return dict(zip(columns, row))
        return None
    
    def get_task_result(self, task_id: str) -> Optional[str]:
        """获取任务结果"""
        task = self.get_task_status(task_id)
        if task and task["status"] == "completed":
            return task["result"]
        return None
    
    def list_tasks(self, status: str = None) -> List[Dict]:
        """列出所有任务，可选按状态过滤"""
        if status:
            cursor = self.db.execute("SELECT id, task_type, status, assigned_agent, created_at FROM tasks WHERE status=?", (status,))
        else:
            cursor = self.db.execute("SELECT id, task_type, status, assigned_agent, created_at FROM tasks")
        return [{"task_id": row[0], "task_type": row[1], "status": row[2],
                "assigned_agent": row[3], "created_at": row[4]} for row in cursor.fetchall()]
    
    def delete_task(self, task_id: str):
        """删除任务"""
        self.db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.db.commit()
