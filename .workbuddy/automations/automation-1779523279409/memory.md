# GitHub 自动备份 - 执行记忆

## 2026-06-04 23:00
- **状态**: ✅ 推送成功
- **Commit**: 8124074 (`自动备份: V191.2 2026-06-04_23:00:51`)
- **文件数**: 1317 files changed, 31 insertions(+), 321 deletions(-)
- **方式**: WSL git commit + Git Bash SSH push
- **踩坑**: Windows Git 2.54 mmap bug → index 损坏；HEAD tree 含 641 个绝对路径文件(`E:/WorkBuddy/Claw/...`)，源于历史提交中 Chrome user data 被错误添加。WSL git 完成 `rm --cached` 清理 + commit，Git Bash 完成 SSH push。WSL 缺少 SSH 密钥，无法直接 push。
- **修复方案**: commit 用 WSL git（避开 Windows mmap bug），push 用 Git Bash SSH

## 2026-06-02 23:14
- **状态**: ✅ 推送成功
- **Commit**: a1a3dfa (`自动备份: V191.2 2026-06-02_23:14:36`)
- **文件数**: 4 files changed, 87 insertions(+), 118 deletions(-)
- **变更内容**: automation memory + backup_log.txt + auto_backup_github.sh + 2026-06-01.md
- **方式**: WSL SSH 推送（`git@github.com:runzeai-lab/lingzhu.git`）
- **踩坑**: 脚本含 Windows CRLF，WSL 执行报 `command not found`，需 `sed -i 's/\r$//'` 修复后执行
- **修复方案**: 执行前自动 `wsl sed -i 's/\r$//'` 转换换行符

## 2026-06-01 23:18
- **状态**: ✅ 推送成功
- **Commit**: 00cb0bb (`自动备份: V191.1 2026-06-01_23:18`)
- **文件数**: 2 files changed, 15 insertions(+), 6 deletions(-)
- **方式**: WSL SSH 推送
- **备注**: remote 已永久切为 SSH，不再受 HTTPS 443 阻断影响
