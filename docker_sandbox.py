"""
Docker 安全沙箱
在 Docker 容器中执行工具，隔离风险
"""

import subprocess
import tempfile
import os
import json
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DockerSandbox")


class DockerSandbox:
    """Docker 安全沙箱：在容器中执行工具"""
    
    def __init__(self, image: str = "python:3.12-slim", timeout: int = 300):
        """
        初始化 Docker 沙箱
        
        Args:
            image: Docker 镜像名称
            timeout: 执行超时时间（秒）
        """
        self.image = image
        self.timeout = timeout
        self.container_name = "lingzhu-sandbox"
        
    def execute_code(self, code: str, language: str = "python") -> Dict:
        """
        在 Docker 容器中执行代码
        
        Args:
            code: 代码字符串
            language: 编程语言（"python" 或 "bash"）
            
        Returns:
            包含执行结果的字典
        """
        if language == "python":
            return self._execute_python(code)
        elif language == "bash":
            return self._execute_bash(code)
        else:
            return {
                "success": False,
                "error": f"不支持的编程语言：{language}"
            }
    
    def _execute_python(self, code: str) -> Dict:
        """执行 Python 代码"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # 构建 Docker 命令
            docker_cmd = [
                "docker", "run",
                "--rm",
                "--name", self.container_name,
                f"--memory=512m",  # 内存限制
                f"--cpus=1.0",      # CPU 限制
                f"--timeout={self.timeout}",
                "-v", f"{temp_file}:/tmp/script.py",
                self.image,
                "python3", "/tmp/script.py"
            ]
            
            # 执行命令
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": None if result.returncode == 0 else result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"执行超时（{self.timeout}秒）"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def _execute_bash(self, script: str) -> Dict:
        """执行 Bash 脚本"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write("#!/bin/bash\n")
            f.write(script)
            temp_file = f.name
        
        try:
            # 构建 Docker 命令
            docker_cmd = [
                "docker", "run",
                "--rm",
                "--name", self.container_name,
                f"--memory=512m",
                f"--cpus=1.0",
                f"--timeout={self.timeout}",
                "-v", f"{temp_file}:/tmp/script.sh",
                self.image,
                "bash", "/tmp/script.sh"
            ]
            
            # 执行命令
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": None if result.returncode == 0 else result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"执行超时（{self.timeout}秒）"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def execute_command(self, command: str) -> Dict:
        """
        在 Docker 容器中执行命令（简化版）
        
        Args:
            command: 要执行的命令
            
        Returns:
            包含执行结果的字典
        """
        try:
            # 构建 Docker 命令
            docker_cmd = [
                "docker", "run",
                "--rm",
                "--name", self.container_name,
                f"--memory=512m",
                f"--cpus=1.0",
                f"--timeout={self.timeout}",
                self.image,
                "bash", "-c", command
            ]
            
            # 执行命令
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": None if result.returncode == 0 else result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"执行超时（{self.timeout}秒）"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_docker_available(self) -> bool:
        """检查 Docker 是否可用"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_sandbox_stats(self) -> Dict:
        """获取沙箱统计"""
        return {
            "image": self.image,
            "timeout": self.timeout,
            "docker_available": self.check_docker_available(),
            "container_name": self.container_name
        }
