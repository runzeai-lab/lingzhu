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

## GitHub 备份经验教训（2026-05-25）
### 常见问题与解决方案
1. **WSL 挂载失败**：`/mnt/e` 不可用时，立即降级到 Git Bash 直接执行
2. **未暂存更改阻止 pull**：先 `git stash --include-untracked`，pull 后 `git stash pop`
3. **VERSION 提取失败**：`SOUL.md` 不在项目根目录，应从 `IDENTITY.md` 或硬编码版本号读取
4. **TLS 证书问题**：WSL 环境必须加 `GIT_SSL_NO_VERIFY=1`

### 备份脚本改进建议
- 在 `auto_backup_github.sh` 中添加环境检查（WSL `/mnt/e` 是否可用）
- 修改 VERSION 提取逻辑，优先从 `IDENTITY.md` 读取
- 在脚本中添加 `git status --short` 检查，如果有未暂存更改先 stash

### 自动化备份最佳实践
1. 先 pull rebase，再 push
2. 提交前检查是否有未追踪的大文件（如 `.coverage`）
3. 备份日志记录在 `scripts/backup_log.txt`，便于追溯
4. 自动化任务失败时，记录错误原因和解决方案到记忆文件

### 2026-05-24 实际操作经验（精华）
1. **后台任务超时留锁**：WSL/PowerShell 后台任务超时会在 `.git/index.lock` 留下锁文件，
   下次执行前必须 `rm -f .git/index.lock` 清理，并 `pkill -f git` 杀残留进程
2. **Rebase 冲突无交互解决**：终端是 dumb 时用 `GIT_EDITOR=true git rebase --continue` 绕过编辑器；
   冲突文件 `git add` 后继续即可
3. **WSL 脚本路径坑**：`auto_backup_github.sh` 里 `grep SOUL.md` 在 WSL `/mnt/e/` 下找不到文件，
   因为 SOUL.md 实际在 `C:\Users\RunzeAI\.workbuddy\`；建议备份脚本改用 Git Bash 直接执行
4. **推送被拒绝不要强推**：先 `git pull --rebase origin main`，解决冲突后再 push，强推会丢历史
5. **Git Bash 比 WSL 脚本更稳定**：涉及路径、锁文件、环境的操作，用 Git Bash 直接执行比绕 WSL 脚本更可靠


### 2026-07-02 Windows Git mmap bug 升级认知
1. **Windows Git 2.54 mmap bug 是持久性问题**：`git status`/`git add -A`/`git read-tree` 均会触发 `mmap failed: Invalid argument`
2. **`GIT_DISABLE_MMAP=1` 仅部分有效**：可绕过 `git status`，但 `git add -A` 仍会崩溃
3. **WSL git 完全无此问题**：所有 git 操作在 WSL 中正常执行，是 commit 操作的首选环境
4. **WSL 缺 SSH 密钥**：push/pull via SSH 需通过 Git Bash 执行
5. **最佳备份流程**：WSL git (commit) + Git Bash SSH (push)，沿用 2026-06-04 建立的模式
