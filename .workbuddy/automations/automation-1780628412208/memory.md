# GitHub 每日备份 - 执行记录

## 2026-06-05 23:36
- **状态**: ✅ 成功
- **Commit**: ba73939 (自动备份: V191.2)
- **Push**: 8ff1e7a..ba73939 → origin/main
- **变更**: 1 file (新增 .gitignore E* 排除规则)
- **执行流程**: 
  1. WSL bash 执行脚本 → SSH 认证失败 + 脚本语法错误
  2. 切换 Git Bash 直接执行 → `git add` mmap 失败
  3. 排查根因：Git for Windows 2.54 mmap bug（非目录问题）
  4. 最终方案：WSL git add（成功）+ Git Bash SSH push（成功）
- **关键发现**: Git for Windows 的 mmap 问题与 `E` 特殊字符目录无关；该目录未追踪，移走后 git add 仍 fail。WSL git 2.43.0 完全正常

## 2026-06-07 23:01
- **状态**: ✅ 成功（无变更）
- **最新 Commit**: f7b1a6d (自动备份: V191.2)
- **变更**: 无新提交，工作区干净
- **执行流程**: 
  1. Git Bash `wsl` 路径转换问题 → 改用 `MSYS_NO_PATHCONV=1 wsl bash -c "..."` 
  2. WSL git stash → 无本地修改
  3. WSL git pull --rebase → SSH 认证失败（已知）
  4. WSL git add . + git commit → 工作区干净，无需提交
  5. 无需推送
- **关键发现**: `MSYS_NO_PATHCONV=1` 解决 Git Bash 调用 WSL 时的路径转换问题
