#!/usr/bin/env python3
"""
QuantClaw Bridge - 灵助与QuantClaw的集成桥梁
QuantClaw是C++17高性能OpenClaw实现，运行在端口18800/18801

通信方式：
1. CLI调用（通过subprocess执行quantclaw命令）
2. WebSocket（通过websockets库连接Gateway）
3. HTTP（通过Control UI端口18801）
"""

import subprocess
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime


class QuantClawBridge:
    """
    QuantClaw 集成桥梁
    功能：
    1. 健康检查与状态监控
    2. Agent请求（发送消息给QuantClaw Agent）
    3. 会话管理
    4. 插件管理
    5. 配置管理
    6. OpenAI兼容接口代理
    """

    def __init__(self, quantclaw_path: str = "/root/QuantClaw/build/quantclaw",
                 gateway_port: int = 18800, control_ui_port: int = 18801,
                 timeout: int = 30):
        self.quantclaw_path = quantclaw_path
        self.gateway_port = gateway_port
        self.control_ui_port = control_ui_port
        self.timeout = timeout
        self.stats = {
            "total_calls": 0,
            "success_calls": 0,
            "failed_calls": 0,
            "last_call": None,
            "last_error": None
        }
        print(f"QuantClaw Bridge 初始化完成 (path={quantclaw_path}, gateway={gateway_port})")

    def _run_cli(self, args: List[str]) -> dict:
        """通过CLI执行QuantClaw命令"""
        self.stats["total_calls"] += 1
        self.stats["last_call"] = datetime.now().isoformat()

        try:
            cmd = [self.quantclaw_path] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd="/root/QuantClaw"
            )

            # 解析输出（CLI输出包含日志和JSON）
            stdout = result.stdout
            stderr = result.stderr

            # 尝试提取JSON输出
            json_output = None
            for line in stdout.split('\n'):
                line = line.strip()
                if line.startswith('{') or line.startswith('['):
                    try:
                        json_output = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue

            self.stats["success_calls"] += 1
            return {
                "success": True,
                "stdout": stdout,
                "stderr": stderr,
                "json": json_output,
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            self.stats["failed_calls"] += 1
            error_msg = f"CLI timeout after {self.timeout}s"
            self.stats["last_error"] = error_msg
            return {"success": False, "error": error_msg}

        except Exception as e:
            self.stats["failed_calls"] += 1
            error_msg = str(e)
            self.stats["last_error"] = error_msg
            return {"success": False, "error": error_msg}

    # ==================== 1. 健康检查与状态 ====================

    async def health_check(self) -> dict:
        """检查QuantClaw服务健康状态"""
        result = self._run_cli(["health"])
        return result

    async def get_status(self) -> dict:
        """获取QuantClaw运行状态"""
        result = self._run_cli(["status"])
        return result

    async def get_config(self, path: str = "") -> dict:
        """获取QuantClaw配置"""
        args = ["config", "get"]
        if path:
            args.append(path)
        result = self._run_cli(args)
        return result

    # ==================== 2. Agent请求 ====================

    async def send_agent_request(self, message: str, session_id: str = None,
                                  model: str = None, stream: bool = False) -> dict:
        """发送消息给QuantClaw Agent"""
        args = ["agent", "-m", message]
        if session_id:
            args.extend(["-s", session_id])
        if model:
            args.extend(["--model", model])
        result = self._run_cli(args)
        return result

    async def stop_agent(self, session_id: str = "default") -> dict:
        """停止Agent运行"""
        result = self._run_cli(["sessions", "reset", "-s", session_id])
        return result

    # ==================== 3. 会话管理 ====================

    async def list_sessions(self) -> dict:
        """列出所有会话"""
        result = self._run_cli(["sessions", "list"])
        return result

    async def get_session_history(self, session_id: str = "default") -> dict:
        """获取会话历史"""
        result = self._run_cli(["sessions", "history", "-s", session_id])
        return result

    async def delete_session(self, session_id: str) -> dict:
        """删除会话"""
        result = self._run_cli(["sessions", "delete", "-s", session_id])
        return result

    async def reset_session(self, session_id: str = "default") -> dict:
        """重置会话"""
        result = self._run_cli(["sessions", "reset", "-s", session_id])
        return result

    # ==================== 4. 插件管理 ====================

    async def list_plugins(self) -> dict:
        """列出所有插件"""
        result = self._run_cli(["plugins", "list"])
        return result

    async def list_plugin_tools(self) -> dict:
        """列出插件工具"""
        result = self._run_cli(["plugins", "tools"])
        return result

    async def list_plugin_services(self) -> dict:
        """列出插件服务"""
        result = self._run_cli(["plugins", "services"])
        return result

    async def list_plugin_providers(self) -> dict:
        """列出插件Provider"""
        result = self._run_cli(["plugins", "providers"])
        return result

    async def list_plugin_commands(self) -> dict:
        """列出插件命令"""
        result = self._run_cli(["plugins", "commands"])
        return result

    # ==================== 5. 配置管理 ====================

    async def reload_config(self) -> dict:
        """重新加载配置"""
        result = self._run_cli(["config", "reload"])
        return result

    # ==================== 6. 模型管理 ====================

    async def list_models(self) -> dict:
        """列出可用模型"""
        result = self._run_cli(["models", "list"])
        return result

    # ==================== 7. 统计信息 ====================

    def get_stats(self) -> dict:
        """获取桥接引擎统计信息"""
        return {
            "status": "active",
            "quantclaw_path": self.quantclaw_path,
            "gateway_port": self.gateway_port,
            "control_ui_port": self.control_ui_port,
            "total_calls": self.stats["total_calls"],
            "success_calls": self.stats["success_calls"],
            "failed_calls": self.stats["failed_calls"],
            "success_rate": f"{self.stats['success_calls'] / max(self.stats['total_calls'], 1) * 100:.1f}%",
            "last_call": self.stats["last_call"],
            "last_error": self.stats["last_error"]
        }

    # ==================== 7. OpenAI兼容接口 ====================

    async def chat_completions(self, messages: list, model: str = "qwen-max",
                                temperature: float = 0.7, max_tokens: int = 4096) -> dict:
        """通过QuantClaw调用OpenAI兼容接口"""
        args = ["chat", "-m", json.dumps(messages)]
        args.extend(["--model", model])
        args.extend(["--temperature", str(temperature)])
        args.extend(["--max-tokens", str(max_tokens)])
        result = self._run_cli(args)
        return result

