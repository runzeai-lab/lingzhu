"""
MCP 双模引擎（极简化版）
支持 Stdio + SSE 双模通信
"""

from typing import Dict, List, Optional


class MCPDualModeEngine:
    """MCP 双模引擎：支持 Stdio 和 SSE 两种通信模式（极简化版）"""
    
    def __init__(self, mode: str = "stdio", sse_port: int = 8080):
        """
        初始化 MCP 双模引擎
        
        Args:
            mode: 通信模式，"stdio" 或 "sse"
            sse_port: SSE 模式下的端口号
        """
        self.mode = mode
        self.sse_port = sse_port
        self.servers = {}  # {server_name: {"status": "stopped"}
        
    def get_server_status(self, server_name: str = None) -> Dict:
        """
        获取服务器状态（极简化版）
        """
        if server_name:
            if server_name not in self.servers:
                return {"error": f"服务器 {server_name} 未注册"}
            return {
                "name": server_name,
                "status": self.servers[server_name]["status"]
            }
        else:
            return {
                "mode": self.mode,
                "sse_port": self.sse_port if self.mode == "sse" else None,
                "servers": list(self.servers.keys())
            }
