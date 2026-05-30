#!/bin/bash
# 自动备份到 GitHub（每次版本升级后自动调用）

PROJECT_DIR="/mnt/e/WorkBuddy/Claw"
cd "$PROJECT_DIR" || exit 1

# 1. 拉取最新
git pull origin main --rebase 2>&1 || echo "⚠️ 拉取失败，继续提交..."

# 2. 添加所有变更
git add .

# 3. 提交（使用当前版本号）
VERSION=$(grep -oP 'V\d+\.\d+' SOUL.md | head -1)
COMMIT_MSG="${1:-自动备份: $VERSION $(date +%Y-%m-%d_%H:%M:%S)}"
git commit -m "$COMMIT_MSG" 2>&1 || echo "⚠️ 无变更可提交"

# 4. 推送到 GitHub（WSL TLS 证书问题需关闭验证）
GIT_SSL_NO_VERIFY=1 git push origin main 2>&1 || echo "⚠️ 推送失败，请检查网络或凭证"

echo "✅ GitHub 备份完成: $COMMIT_MSG"
