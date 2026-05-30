#!/bin/bash
# 灵助 (Lingzhu) 启动脚本
# 端口: 8000
cd /root/ai-stack/lingzhu
export PYTHONPATH=$(pwd):$PYTHONPATH
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
