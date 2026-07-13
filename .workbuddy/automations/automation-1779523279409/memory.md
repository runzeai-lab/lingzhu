# GitHub 自动备份 - 执行记忆

## 2026-07-03 23:00
- **状态**: ✅ 推送成功（双 commit）
- **Commits**: da89a42 (cleanup 642 abs-path files) + d491b6d (log update)
- **文件数**: 646 + 1 = 647 files, 35 insertions, 1595 deletions
- **变更文件**: automation memory + MEMORY.md + backup_log.txt + 642 个 E:/ 绝对路径文件删除
- **方式**: WSL git add -u + commit + Git Bash SSH push
- **踩坑**: 642 个历史误跟踪的 E:/ 绝对路径文件（debug_screenshots, xiaohongshu_user_data_v2/v3, nul 等）一直存在 index 中未清理。每次备份都报"被删除"状态。`git update-index --force-remove` 对 E:/README.md 报"outside repository"错误，但 `git add -u` 可以接受文件系统中的"已删除"状态。解决方案：批量 `git add -u` 把所有 deletion 暂存，然后 commit 清理。
- **修复方案**: 建立 `git add -u` 工作流处理误跟踪的绝对路径文件

## 2026-07-04 23:01
- **状态**: ✅ 推送成功
- **Commit**: 2548331 (`auto-backup: V191.4`)
- **文件数**: 1 file changed, 8 insertions
- **变更文件**: .workbuddy/memory/2026-07-02.md
- **方式**: WSL git commit + Git Bash SSH push
- **备注**: 工作区只有 1 个新文件（memory 日记），备份轻量顺利

## 2026-07-02 23:01
- **状态**: ✅ 推送成功
- **Commit**: 200a9a3 (`auto-backup: V191.4 2026-07-02_23:01:34`)
- **文件数**: 3 files changed, 16 insertions(+)
- **变更文件**: automation memory + MEMORY.md + backup_log.txt
- **方式**: WSL git commit + Git Bash SSH push
- **备注**: 工作区只有 3 个元数据文件变更，无代码改动，备份轻量

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

## 2026-07-02 16:07
- **状态**: ✅ Everything up-to-date
- **Commit**: 611eff3 (`auto-backup: V191.4 2026-06-30_23:11:57`)
- **文件数**: 0 新变更（仓库已完全同步）
- **方式**: WSL git 验证 working tree clean + Git Bash SSH push 认 remote up-to-date
- **踩坑**: Windows Git 2.54 mmap bug 导致 `git status`/`git add -A` 失效，`GIT_DISABLE_MMAP=1` 可绕过 status 但 add -A 仍崩溃；WSL git 正常运行无 mmap 问题；WSL 无 SSH 密钥无法 pull/push，需 Git Bash 做 push
- **经验**: Windows Git mmap bug 是持久性问题，备份流程应始终优先 WSL git 做 commit 操作 + Git Bash SSH 做 push
