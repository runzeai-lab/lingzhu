#!/bin/bash
# Auto backup to GitHub (auto-triggered after each version upgrade)
# Fix: SOUL.md not in project root, read from ~/.workbuddy/
# Push: prefer SSH, no longer rely on GIT_SSL_NO_VERIFY

set -euo pipefail

PROJECT_DIR="/mnt/e/WorkBuddy/Claw"
cd "$PROJECT_DIR" || exit 1

# 1. Stash unstaged changes (including untracked) to avoid pull conflicts
echo "[1/5] Stashing unstaged changes..."
git stash --include-untracked 2>&1 || true

echo "[2/5] Pulling latest from origin/main..."
git pull --rebase origin main 2>&1 || echo "[WARN] Pull failed, continuing..."

echo "[3/5] Restoring stashed changes..."
git stash pop 2>&1 || echo "[WARN] No stash to restore"

# 2. Stage all changes
echo "[4/5] Staging all changes..."
git add .

# 3. Extract version (prefer IDENTITY.md, fallback to SOUL.md)
# IDENTITY.md location: C:\Users\RunzeAI\.workbuddy\IDENTITY.md
IDENTITY_PATH="/mnt/c/Users/RunzeAI/.workbuddy/IDENTITY.md"
SOUL_PATH="/mnt/c/Users/RunzeAI/.workbuddy/SOUL.md"

if [ -f "$IDENTITY_PATH" ]; then
    VERSION=$(grep -oP 'V\d+\.\d+' "$IDENTITY_PATH" | head -1)
fi

if [ -z "${VERSION:-}" ] && [ -f "$SOUL_PATH" ]; then
    VERSION=$(grep -oP 'V\d+\.\d+' "$SOUL_PATH" | head -1)
fi

VERSION="${VERSION:-V191.0}"
COMMIT_MSG="${1:-auto-backup: $VERSION $(date +%Y-%m-%d_%H:%M:%S)}"

git commit -m "$COMMIT_MSG" 2>&1 || echo "[WARN] No changes to commit"

# 4. Push to GitHub via SSH (no GIT_SSL_NO_VERIFY needed)
echo "[5/5] Pushing to GitHub via SSH..."
git push origin main 2>&1
PUSH_EXIT=$?

if [ $PUSH_EXIT -eq 0 ]; then
    echo "[OK] GitHub backup completed: $COMMIT_MSG"
else
    echo "[FAIL] Push failed, exit code: $PUSH_EXIT. Check SSH key or network."
    exit $PUSH_EXIT
fi
