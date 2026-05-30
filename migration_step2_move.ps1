# 迁移 .workbuddy 到 E 盘 + 创建符号链接（需管理员权限）
# 使用前：确认 migration_step1_backup.ps1 已成功执行

$src = "C:\Users\RunzeAI\.workbuddy"
$dst = "E:\WorkBuddy\.workbuddy"
$link = "C:\Users\RunzeAI\.workbuddy"

Write-Output "=== 步骤2：迁移 + 创建符号链接 ==="

# 1. 确认备份已存在
if (-not (Test-Path $dst)) {
    Write-Output "❌ 目标目录不存在: $dst"
    Write-Output "请先运行 migration_step1_backup.ps1 完成备份"
    exit 1
}
Write-Output "✅ 备份目录已确认: $dst"

# 2. 完全退出 WorkBuddy 进程
Write-Output "正在关闭 WorkBuddy 进程..."
Get-Process "WorkBuddy" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
$stillRunning = Get-Process "WorkBuddy" -ErrorAction SilentlyContinue
if ($stillRunning) {
    Write-Output "⚠️ WorkBuddy 仍在运行，请手动关闭后重试"
    exit 1
}
Write-Output "✅ WorkBuddy 进程已关闭"

# 3. 删除原目录（移到回收站更安全，这里先改名备份）
$backupName = "$src.old_" + (Get-Date -Format "yyyyMMdd_HHmmss")
Write-Output "将原目录改名备份为: $backupName"
Move-Item $src $backupName -Force
Write-Output "✅ 原目录已备份（未丢失数据）"

# 4. 创建目录联接（Junction）= 符号链接
Write-Output "正在创建符号链接..."
cmd.exe /c "mklink /J `"$link`" `"$dst`""
if (Test-Path $link) {
    Write-Output "✅ 符号链接创建成功！"
    Write-Output "链接: $link → $dst"
} else {
    Write-Output "❌ 符号链接创建失败，请手动以管理员身份运行："
    Write-Output "  mklink /J `"$link`" `"$dst`""
    exit 1
}

# 5. 验证
Write-Output ""
Write-Output "=== 验证结果 ==="
cmd.exe /c "dir /A:L `"C:\Users\RunzeAI\`""
Write-Output ""
Write-Output "✅ 迁移完成！"
Write-Output "现在可以重新打开 WorkBuddy，点击更新按钮了。"
Write-Output "原文件安全保存在: $backupName"
Write-Output "如需恢复：删除链接，将 $backupName 改回 .workbuddy"
