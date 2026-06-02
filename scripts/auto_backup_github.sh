#!/bin/bash
# 自动备份到 GitHub（每次版本升级后自动调用）
# 修复：SOUL.md 不在项目根目录，改从 ~/.workbuddy/ 读取
# 推送方式：优先 SSH，不再依赖 GIT_SSL_NO_VERIFY

set -euo pipefail

PROJECT_DIR="/mnt/e/WorkBuddy/Claw"
cd "$PROJECT_DIR" || exit 1

# 1. 拉取最新（先 stash 未暂存变更，防止 pull 冲突）
echo "📥 [1/5] Stashing unstaged changes..."
git stash --include-untracked 2>&1 || true

echo "📥 [2/5] Pulling latest from origin/main..."
git pull --rebase origin main 2>&1 || echo "⚠️ 拉取失败，继续提交..."

echo "📤 [3/5] Restoring stashed changes..."
git stash pop 2>&1 || echo "⚠️ 无 stash 可恢复"

# 2. 添加所有变更
echo "📝 [4/5] Staging all changes..."
git add .

# 3. 提取版本号（优先 IDENTITY.md，备用 SOUL.md）
# IDENTITY.md 位置：C:\Users\RunzeAI\.workbuddy\IDENTITY.md
IDENTITY_PATH="/mnt/c/Users/RunzeAI/.workbuddy/IDENTITY.md"
SOUL_PATH="/mnt/c/Users/RunzeAI/.workbuddy/SOUL.md"

if [ -f "$IDENTITY_PATH" ]; then
    VERSION=$(grep -oP 'V\d+\.\d+' "$IDENTITY_PATH" | head -1)
fi

if [ -z "${VERSION:-}" ] && [ -f "$SOUL_PATH" ]; then
    VERSION=$(grep -oP 'V\d+\.\d+' "$SOUL_PATH" | head -1)
fi

VERSION="${VERSION:-V191.0}"
COMMIT_MSG="${1:-自动备份: $VERSION $(date +%Y-%m-%d_%H:%M:%S)}"

git commit -m "$COMMIT_MSG" 2>&1 || echo "⚠️ 无变更可提交"

# 4. 推送到 GitHub（SSH 方式，无需 GIT_SSL_NO_VERIFY）
echo "🚀 [5/5] Pushing to GitHub via SSH..."
git push origin main 2>&1
PUSH_EXIT=$?

if [ $PUSH_EXIT -eq 0 ]; then
    echo "✅ GitHub 备份完成: $COMMIT_MSG"
else
    echo "❌ 推送失败 (exit code: $PUSH_EXIT)，请检查网络或 SSH 密钥"
    exit $PUSH_EXIT
fi
