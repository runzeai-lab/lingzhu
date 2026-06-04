#!/bin/bash
set -euo pipefail
cd /mnt/e/WorkBuddy/Claw

echo "=== [1/5] Removing absolute paths from HEAD ==="
git ls-tree -r HEAD --name-only | grep '^E:/' | while read f; do
    git rm --cached "$f" 2>/dev/null || true
done
echo "Done removing absolute paths"

echo "=== [2/5] Staging changes ==="
git add .
echo "Staged"

echo "=== [3/5] Getting version ==="
VERSION=$(grep -oP 'V\d+\.\d+' /mnt/c/Users/RunzeAI/.workbuddy/IDENTITY.md | head -1)
VERSION="${VERSION:-V191.0}"
COMMIT_MSG="自动备份: $VERSION $(date +%Y-%m-%d_%H:%M:%S)"

echo "=== [4/5] Commit: $COMMIT_MSG ==="
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

echo "=== [5/5] Pushing to GitHub ==="
git push origin main
echo "✅ GitHub 备份完成: $COMMIT_MSG"
