"""
AgentMatrix (Agent母体) - 从 DeepSeek 对话历史提取
集成到 ALLINAI V7.0

核心能力：
1. 感知任务需求（perceive_and_create）
2. 设计Agent蓝图（deep_analyze）
3. 生成Agent代码和Dockerfile
4. 动态注册到 docker-compose 并部署
5. 实现"道生万物"的Agent自繁殖能力
"""

import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any


class AgentMatrix:
    """
    Agent母体：万物生成之源
    能感知需求，设计并创造出新的、专门化的子Agent
    """

    def __init__(self, kernel):
        """
        初始化Agent母体
        kernel: ALLINAI_V7 实例的引用（提供总体觉知和任务执行能力）
        """
        self.kernel = kernel  # ALLINAI内核，提供任务执行能力
        self.agents_dir = Path("./generated_agents")
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.active_agents = {}

        print("[Agent母体] ✅ 初始化完成 · 道生万物能力已就绪")

    async def perceive_and_create(self, task_description: str) -> Dict[str, Any]:
        """
        最高级能力：感知任务，并创造Agent
        返回：{"status": "success", "agent_id": "...", "port": ..., "message": "..."}
        """
        print(f"[Agent母体] 感知到新需求：'{task_description}'")

        # 1. 分析任务，设计Agent蓝图 (道生一)
        design = await self._deep_analyze(task_description)

        # 2. 生成Agent代码和Dockerfile (一生二)
        agent_code = self._generate_agent_code(design)
        dockerfile = self._generate_dockerfile(design)

        # 3. 部署并注册Agent (二生三)
        agent_id = design['agent_name']
        port = design['port']
        agent_folder = self.agents_dir / agent_id
        agent_folder.mkdir(parents=True, exist_ok=True)

        (agent_folder / "main.py").write_text(agent_code, encoding='utf-8')
        (agent_folder / "Dockerfile").write_text(dockerfile, encoding='utf-8')
        (agent_folder / "requirements.txt").write_text(design['requirements'], encoding='utf-8')

        # 4. 动态注册进docker-compose，使其运行 (三生万物)
        try:
            self._register_agent_to_compose(agent_id, port)
            # 尝试启动（如果docker可用）
            try:
                subprocess.run(
                    ["docker", "compose", "-f", "./docker-compose.yml", "up", "-d", agent_id],
                    check=True,
                    capture_output=True,
                    timeout=60
                )
                print(f"[Agent母体] ✅ 新Agent '{agent_id}' 已诞生，运行在端口 {port}")
                self.active_agents[agent_id] = design
                return {
                    "status": "success",
                    "agent_id": agent_id,
                    "port": port,
                    "message": f"Agent '{agent_id}' 已创建并启动"
                }
            except subprocess.TimeoutExpired:
                print(f"[Agent母体] ⚠️ 启动超时，但文件已生成")
                return {
                    "status": "partial",
                    "agent_id": agent_id,
                    "port": port,
                    "message": "Agent文件已生成，但启动超时"
                }
            except Exception as e:
                print(f"[Agent母体] ⚠️ 启动失败：{e}")
                return {
                    "status": "created",
                    "agent_id": agent_id,
                    "port": port,
                    "message": f"Agent文件已生成，但启动失败：{e}"
                }
        except Exception as e:
            print(f"[Agent母体] ❌ 创建失败：{e}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def _deep_analyze(self, task_description: str) -> Dict[str, Any]:
        """
        深度分析任务需求，设计Agent蓝图
        这是"道生一"的过程：从需求到设计
        """
        # 简化版：基于规则生成设计
        # 完整版：调用LLM分析任务，生成详细设计

        # 生成唯一Agent名称
        import hashlib
        task_hash = hashlib.md5(task_description.encode('utf-8')).hexdigest()[:8]
        agent_name = f"agent_{task_hash}"

        # 分配端口（从 9000 开始）
        port = 9000 + len(self.active_agents)

        # 分析任务类型，确定能力
        capabilities = []
        if "分析" in task_description or "数据" in task_description:
            capabilities.append("data_analysis")
        if "写作" in task_description or "文章" in task_description:
            capabilities.append("content_creation")
        if "搜索" in task_description or "查询" in task_description:
            capabilities.append("search")
        if not capabilities:
            capabilities.append("general")

        design = {
            'agent_name': agent_name,
            'description': task_description,
            'port': port,
            'capabilities': capabilities,
            'requirements': 'fastapi\nuvicorn\nhttpx\n',
            'core_logic_placeholder': f'# 核心逻辑：{task_description}',
        }

        print(f"[Agent母体] 设计蓝图完成：{agent_name} (port={port}, capabilities={capabilities})")
        return design

    def _generate_agent_code(self, design: Dict[str, Any]) -> str:
        """
        根据设计蓝图，生成Python Agent代码
        这是"一生二"的过程：从设计到代码
        """
        agent_name = design['agent_name']
        port = design['port']
        capabilities = design.get('capabilities', [])
        placeholder = design.get('core_logic_placeholder', '')

        code = f'''# Agent: {agent_name}
# 功能: {design['description']}
# 生成自: 灵助·道生万物 Agent母体

import asyncio
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="{agent_name}")

@app.get("/")
async def root():
    return {{"agent": "{agent_name}", "status": "alive", "capabilities": {capabilities}}}

@app.post("/execute")
async def execute(task: dict):
    """执行任务"""
    # TODO: 实现具体任务逻辑
    result = f"Agent {agent_name} 收到任务：{{task.get('task', '')}}"
    return {{"status": "success", "result": result}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port={port})
'''
        return code

    def _generate_dockerfile(self, design: Dict[str, Any]) -> str:
        """
        生成Dockerfile
        """
        port = design['port']
        return f'''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
EXPOSE {port}
'''

    def _register_agent_to_compose(self, agent_id: str, port: int):
        """
        动态修改主docker-compose.yml，加入新Agent
        这是"二生三"的过程：从代码到运行
        """
        compose_path = Path("./docker-compose.yml")

        # 如果不存在，创建一个基础的
        if not compose_path.exists():
            base_compose = '''version: '3.8'
services:
  # AGENT_MARKER - 新Agent将插入此处
'''
            compose_path.write_text(base_compose, encoding='utf-8')

        current = compose_path.read_text(encoding='utf-8')

        new_service = f'''
  {agent_id}:
    build: ./generated_agents/{agent_id}
    container_name: {agent_id}
    ports: ["{port}:{port}"]
    restart: unless-stopped
    networks: [dao_net]
'''

        # 简单插入（实际应使用yaml库安全操作）
        if "# AGENT_MARKER" in current:
            updated = current.replace("# AGENT_MARKER", f"# AGENT_MARKER\n{new_service}")
        else:
            updated = current + "\n" + new_service

        compose_path.write_text(updated, encoding='utf-8')
        print(f"[Agent母体] ✅ {agent_id} 已注册到 docker-compose.yml")

    def get_status(self) -> Dict[str, Any]:
        """获取Agent母体状态"""
        return {
            "active_agents_count": len(self.active_agents),
            "active_agents": list(self.active_agents.keys()),
            "agents_dir": str(self.agents_dir),
        }


# ==================== 集成函数 ====================
def integrate_agent_matrix(kernel):
    """
    将Agent母体集成到 ALLINAI_V7 实例

    Usage:
        from agent_matrix import integrate_agent_matrix
        integrate_agent_matrix(kernel)
    """
    kernel.agent_matrix = AgentMatrix(kernel)

    print("[Agent母体] ✅ 集成完成 · 道生万物能力已激活")
    return kernel
