#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
可视化仪表板后端API (Visualization Dashboard API) V1.0
提供API端点，从统一调度系统获取数据
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入统一调度系统
from unified_scheduling_system import UnifiedSchedulingSystem

# 创建FastAPI应用
app = FastAPI(title="灵助可视化仪表板 API", description="提供调度状态、决策过程、系统健康数据", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 简化：允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化统一调度系统
scheduler = UnifiedSchedulingSystem()

# ============================================================================
# 数据模型
# ============================================================================

class SystemStateUpdate(BaseModel):
    """系统状态更新模型"""
    updates: Dict[str, Any]

class EnvironmentUpdate(BaseModel):
    """环境更新模型"""
    updates: Dict[str, Any]

# ============================================================================
# API端点
# ============================================================================

@app.get("/")
async def root():
    """根路径 - API信息"""
    return {
        "name": "灵助可视化仪表板 API",
        "version": "1.0.0",
        "description": "提供调度状态、决策过程、系统健康数据",
        "endpoints": [
            "/api/system-state",
            "/api/environment",
            "/api/execution-history",
            "/api/decision-history",
            "/api/solution-history",
            "/api/dashboard-data"
        ]
    }

@app.get("/api/system-state")
async def get_system_state():
    """获取系统状态"""
    try:
        state = scheduler.get_system_state()
        return {
            "success": True,
            "data": state,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统状态失败: {str(e)}")

@app.get("/api/environment")
async def get_environment():
    """获取环境信息"""
    try:
        state = scheduler.get_system_state()
        return {
            "success": True,
            "data": state.get("environment", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取环境信息失败: {str(e)}")

@app.get("/api/execution-history")
async def get_execution_history(limit: int = 10):
    """获取执行历史"""
    try:
        history = scheduler.get_execution_history(limit=limit)
        return {
            "success": True,
            "data": history,
            "total": len(history),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取执行历史失败: {str(e)}")

@app.get("/api/decision-history")
async def get_decision_history():
    """获取决策历史"""
    try:
        history = scheduler.get_decision_history()
        return {
            "success": True,
            "data": history,
            "total": len(history),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取决策历史失败: {str(e)}")

@app.get("/api/solution-history")
async def get_solution_history():
    """获取方案生成历史"""
    try:
        history = scheduler.get_solution_history()
        return {
            "success": True,
            "data": history,
            "total": len(history),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取方案生成历史失败: {str(e)}")

@app.get("/api/dashboard-data")
async def get_dashboard_data():
    """获取仪表板所有数据（一次性获取所有数据）"""
    try:
        # 获取系统状态
        system_state = scheduler.get_system_state()
        
        # 获取执行历史（最近10条）
        execution_history = scheduler.get_execution_history(limit=10)
        
        # 获取决策历史
        decision_history = scheduler.get_decision_history()
        
        # 获取方案生成历史
        solution_history = scheduler.get_solution_history()
        
        # 整合数据
        dashboard_data = {
            "system_state": system_state,
            "execution_history": execution_history,
            "decision_history": decision_history,
            "solution_history": solution_history,
            "summary": {
                "system_state_count": 1,
                "execution_history_count": len(execution_history),
                "decision_history_count": len(decision_history),
                "solution_history_count": len(solution_history)
            }
        }
        
        return {
            "success": True,
            "data": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取仪表板数据失败: {str(e)}")

@app.post("/api/system-state/update")
async def update_system_state(update: SystemStateUpdate):
    """更新系统状态"""
    try:
        scheduler.update_system_state(update.updates)
        return {
            "success": True,
            "message": "系统状态更新成功",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新系统状态失败: {str(e)}")

@app.post("/api/environment/update")
async def update_environment(update: EnvironmentUpdate):
    """更新环境信息"""
    try:
        scheduler.update_environment(update.updates)
        return {
            "success": True,
            "message": "环境信息更新成功",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新环境信息失败: {str(e)}")

# ============================================================================
# 健康检查
# ============================================================================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 主函数
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # 启动服务
    print("🌀 可视化仪表板后端API V1.0 - 启动中...")
    print("=" * 60)
    print(f"访问地址: http://localhost:9000")
    print(f"API文档: http://localhost:9000/docs")
    print(f"健康检查: http://localhost:9000/health")
    print("=" * 60)
    
    # 启动uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
