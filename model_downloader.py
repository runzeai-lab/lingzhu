import os
import sys
import json
import time
import threading
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from queue import PriorityQueue, Empty
import hashlib

class ModelDownloader:
    """
    模型下载器 - 支持多模型并行下载
    
    功能：
    1. 多模型并行下载（多线程）
    2. 下载进度追踪（每个模型的进度）
    3. 断点续传（支持中断后继续）
    4. 下载队列管理（优先级队列）
    5. 模型版本管理（版本检查、回滚）
    """
    
    def __init__(self, download_dir: str = "/tmp/models", max_parallel: int = 3):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.max_parallel = max_parallel
        
        # 下载任务队列（优先级队列）
        self.download_queue = PriorityQueue()
        self.queue_lock = threading.Lock()
        
        # 正在下载的任务
        self.active_downloads = {}  # {task_id: Thread}
        
        # 下载历史
        self.download_history = []
        
        # 模型版本库
        self.model_versions = {}  # {model_name: [version1, version2, ...]}
        
        # 统计信息
        self.stats = {
            "total_downloads": 0,
            "successful_downloads": 0,
            "failed_downloads": 0,
            "total_bytes_downloaded": 0
        }
        
        print(f"模型下载器初始化完成，下载目录：{download_dir}，最大并行数：{max_parallel}")
    
    # ==================== 1. 多模型并行下载 ====================
    
    def download_model(self, model_name: str, model_url: str, 
                     version: str = "latest", priority: int = 5) -> Dict:
        """
        添加模型下载任务到队列
        
        Args:
            model_name: 模型名称
            model_url: 模型下载URL
            version: 模型版本（默认 "latest"）
            priority: 优先级（1-10，1最高）
        
        Returns:
            {"task_id": str, "status": "queued"}
        """
        task_id = self._generate_task_id(model_name, version)
        
        task = {
            "task_id": task_id,
            "model_name": model_name,
            "model_url": model_url,
            "version": version,
            "priority": priority,
            "status": "queued",
            "progress": 0,
            "total_size": 0,
            "downloaded_size": 0,
            "start_time": None,
            "end_time": None,
            "error": None
        }
        
        # 添加到优先级队列
        self.download_queue.put((priority, task))
        
        # 启动下载线程（如果未达到最大并行数）
        self._start_next_download()
        
        return {
            "task_id": task_id,
            "status": "queued",
            "message": f"模型 {model_name} (版本 {version}) 已添加到下载队列"
        }
    
    def _start_next_download(self):
        """启动下一个下载任务（如果条件允许）"""
        with self.queue_lock:
            if len(self.active_downloads) >= self.max_parallel:
                return  # 已达到最大并行数
            
            try:
                priority, task = self.download_queue.get_nowait()
            except Empty:
                return  # 队列为空
            
            # 启动下载线程
            thread = threading.Thread(
                target=self._download_worker,
                args=(task,)
            )
            thread.start()
            
            self.active_downloads[task["task_id"]] = thread
            task["status"] = "downloading"
            task["start_time"] = str(datetime.now())
    
    def _download_worker(self, task: Dict):
        """下载工作线程"""
        task_id = task["task_id"]
        model_name = task["model_name"]
        model_url = task["model_url"]
        version = task["version"]
        
        try:
            # 模拟下载（简化版：实际应该用 requests 或 urllib）
            print(f"[下载任务 {task_id}] 开始下载 {model_name} (版本 {version})")
            
            # 模拟下载进度
            total_size = 100  # 简化：假设100MB
            task["total_size"] = total_size
            
            for progress in range(0, 101, 10):
                time.sleep(0.5)  # 模拟下载延迟
                task["progress"] = progress
                task["downloaded_size"] = total_size * progress / 100
                print(f"[下载任务 {task_id}] 进度：{progress}%")
            
            # 下载完成
            task["status"] = "completed"
            task["end_time"] = str(datetime.now())
            task["progress"] = 100
            
            # 更新统计
            self.stats["total_downloads"] += 1
            self.stats["successful_downloads"] += 1
            self.stats["total_bytes_downloaded"] += task["downloaded_size"]
            
            # 添加到下载历史
            self.download_history.append(task.copy())
            
            # 更新模型版本库
            if model_name not in self.model_versions:
                self.model_versions[model_name] = []
            self.model_versions[model_name].append({
                "version": version,
                "download_time": task["end_time"],
                "size": task["downloaded_size"]
            })
            
            print(f"[下载任务 {task_id}] 下载完成")
        
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            task["end_time"] = str(datetime.now())
            
            self.stats["total_downloads"] += 1
            self.stats["failed_downloads"] += 1
            
            print(f"[下载任务 {task_id}] 下载失败：{e}")
        
        finally:
            # 从活跃下载中移除
            with self.queue_lock:
                if task_id in self.active_downloads:
                    del self.active_downloads[task_id]
            
            # 尝试启动下一个下载
            self._start_next_download()
    
    # ==================== 2. 下载进度追踪 ====================
    
    def get_download_progress(self, task_id: str) -> Dict:
        """获取下载进度"""
        # 在活跃下载中查找
        if task_id in self.active_downloads:
            # 需要从任务中获取最新进度（简化版：从全局变量获取）
            return {
                "task_id": task_id,
                "status": "downloading",
                "message": "任务正在下载中"
            }
        
        # 在下载历史中查找
        for task in self.download_history:
            if task["task_id"] == task_id:
                return {
                    "task_id": task_id,
                    "status": task["status"],
                    "progress": task["progress"],
                    "total_size": task["total_size"],
                    "downloaded_size": task["downloaded_size"],
                    "message": f"任务已{task['status']}"
                }
        
        return {
            "task_id": task_id,
            "status": "not_found",
            "message": "任务未找到"
        }
    
    def list_active_downloads(self) -> List[Dict]:
        """列出正在下载的任务"""
        active = []
        for task_id in self.active_downloads:
            # 简化版：返回任务ID和状态
            active.append({
                "task_id": task_id,
                "status": "downloading"
            })
        return active
    
    # ==================== 3. 断点续传 ====================
    
    def resume_download(self, task_id: str) -> Dict:
        """
        断点续传：恢复中断的下载
        
        简化版：重新添加到队列
        """
        # 在下载历史中查找
        for task in self.download_history:
            if task["task_id"] == task_id and task["status"] == "failed":
                # 重新添加到队列
                task["status"] = "queued"
                self.download_queue.put((task["priority"], task))
                self._start_next_download()
                
                return {
                    "task_id": task_id,
                    "status": "queued",
                    "message": "下载已恢复"
                }
        
        return {
            "task_id": task_id,
            "status": "not_found",
            "message": "任务未找到或不需要恢复"
        }
    
    # ==================== 4. 下载队列管理 ====================
    
    def list_queue(self) -> List[Dict]:
        """列出下载队列（简化版：返回队列快照）"""
        # 简化版：由于 PriorityQueue 不支持遍历，返回空列表
        return []
    
    def cancel_download(self, task_id: str) -> Dict:
        """取消下载任务"""
        # 简化版：如果任务还在队列中，无法取消（PriorityQueue 不支持删除）
        # 如果任务正在下载，无法取消（需要线程协作）
        return {
            "task_id": task_id,
            "status": "cancel_requested",
            "message": "取消请求已发送（简化版：实际未取消）"
        }
    
    # ==================== 5. 模型版本管理 ====================
    
    def list_model_versions(self, model_name: str) -> List[Dict]:
        """列出模型的所有版本"""
        if model_name not in self.model_versions:
            return []
        return self.model_versions[model_name]
    
    def rollback_model(self, model_name: str, target_version: str) -> Dict:
        """
        回滚模型到指定版本
        
        简化版：只记录回滚操作，不实际回滚文件
        """
        if model_name not in self.model_versions:
            return {
                "model_name": model_name,
                "status": "failed",
                "message": "模型未找到"
            }
        
        versions = self.model_versions[model_name]
        target = next((v for v in versions if v["version"] == target_version), None)
        
        if not target:
            return {
                "model_name": model_name,
                "status": "failed",
                "message": f"版本 {target_version} 未找到"
            }
        
        # 简化版：记录回滚操作
        print(f"[版本管理] 模型 {model_name} 回滚到版本 {target_version}")
        
        return {
            "model_name": model_name,
            "rolled_back_to": target_version,
            "status": "success",
            "message": f"模型已回滚到版本 {target_version}（简化版：实际未回滚文件）"
        }
    
    def check_for_updates(self, model_name: str, current_version: str) -> Dict:
        """
        检查模型是否有更新
        
        简化版：随机返回是否有更新
        """
        import random
        has_update = random.choice([True, False])
        
        if has_update:
            new_version = f"{float(current_version) + 0.1:.1f}" if current_version.replace('.', '').isdigit() else "1.1"
            return {
                "model_name": model_name,
                "current_version": current_version,
                "latest_version": new_version,
                "has_update": True,
                "message": f"发现新版本 {new_version}"
            }
        else:
            return {
                "model_name": model_name,
                "current_version": current_version,
                "latest_version": current_version,
                "has_update": False,
                "message": "已是最新版本"
            }
    
    # ==================== 工具方法 ====================
    
    def _generate_task_id(self, model_name: str, version: str) -> str:
        """生成任务ID"""
        timestamp = int(time.time())
        return f"{model_name}_{version}_{timestamp}"
    
    def get_downloader_stats(self) -> Dict:
        """获取下载器统计信息"""
        return {
            "stats": self.stats,
            "active_downloads": len(self.active_downloads),
            "model_versions": len(self.model_versions),
            "download_history_count": len(self.download_history),
            "message": "下载器统计信息"
        }
