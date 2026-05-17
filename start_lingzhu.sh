#!/bin/bash
cd /root/ai-stack/lingzhu
source venv/bin/activate
nohup python3 main.py > /tmp/lingzhu.log 2>&1 &
echo "LingZhu starting... Check /tmp/lingzhu.log for details."
sleep 2
ss -tuln | grep :8000 || echo "Port 8000 not listening yet. Check logs."
