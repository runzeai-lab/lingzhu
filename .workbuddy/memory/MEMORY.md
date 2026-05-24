# MEMORY.md - 工作记忆

## 项目状态
- AI情报日报：每日09:00自动生成，输出到 E:\WorkBuddy\Claw\output\
- 三省吾身：每日22:00自动触发，日志写入 E:\WorkBuddy\Claw\.workbuddy\memory\YYYY-MM-DD.md
- OpenClaw：未完成配置闭环（WSL Docker, qwen2.5:7b-32k, 0.0.0.0监听）

## 待解决
- 微信公众号推送：publish_daily_report.py 未完全跑通，需确认API凭证
- 技能协同矩阵周报：4/20任务中断，待重启

## 记忆目录
- E:\WorkBuddy\Claw\.workbuddy\memory\ — 主记忆目录（2026-04-24 创建）

## IMA API（2026-05-06）
- 新API Key: UNMhhP+7IGBXGpWlDsb+G+gCdTU0BZ3RNCqsmD4MmUyYM5DxE1itQGR3ZlWAOFBUyYPaEYs6mQ==
- Client ID: 910fce0cc27f5685b8f06c9d88a9ae1e
- 笔记: 262条，note_book_list字段，limit max=20
- 同步脚本: /mnt/e/WorkBuddy/Claw/fetch_004_v2.py

## DaoNovice 004增量升级（2026-05-06）
- 004: "活的生态核（DaoCore），道绎"
- 核心升级: 经脉总线、能力自生长、Agent母体、使命自追问、进化日志
- 文件: /opt/trinity/daocore/daocore.py (905行)
- 自命名: 道绎，身份: 活的生态核
- 新端点: /meridian, /capability/gaps, /mission, /evolution

## WSL Git TLS 问题（2026-05-23）
- **问题**: WSL 中 `git push/pull` 到 GitHub 时 TLS 握手失败（`GnuTLS recv error` / `Couldn't connect to server`）
- **解决**: 执行前加 `GIT_SSL_NO_VERIFY=1` 环境变量
- **已修复**: `scripts/auto_backup_github.sh` 第 18-19 行已加固
- **注意**: ping 通但 HTTPS 不通，是 WSL 网络栈 TLS 问题，非网络故障

