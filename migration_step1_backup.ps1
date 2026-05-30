# 迁移 .workbuddy 到 E 盘
$src = "C:\Users\RunzeAI\.workbuddy"
$dst = "E:\WorkBuddy\.workbuddy"

Write-Output "=== 开始备份 .workbuddy ==="
Write-Output "源目录: $src"
Write-Output "目标目录: $dst"

# 创建目标目录
if (-not (Test-Path $dst)) {
    New-Item -ItemType Directory -Path $dst -Force | Out-Null
    Write-Output "✅ 目标目录已创建"
} else {
    Write-Output "✅ 目标目录已存在"
}

# 使用 robocopy 复制（跳过锁定文件）
$robocopyArgs = @(
    "`"$src`"",
    "`"$dst`"",
    "/E",           # 复制所有子目录（包括空目录）
    "/R:1",        # 失败重试1次
    "/W:1",        # 重试间隔1秒
    "/XF", "Cookies*", "*.lock", "*.tmp",  # 跳过锁定文件
    "/XD", "app\session\Network",            # 跳过锁定的网络会话目录
    "/NDL",        # 不记录目录名
    "/NFL",        # 不记录文件名
    "/NC",         # 不显示复制进度
    "/NS",         # 不显示文件大小
    "/NP"          # 不显示复制百分比
)

Write-Output "正在复制文件（跳过被锁定的文件）..."
$result = Start-Process "robocopy.exe" -ArgumentList $robocopyArgs -Wait -PassThru -NoNewWindow
$exitCode = $result.ExitCode

Write-Output "Robocopy 完成，退出码: $exitCode (0-7=成功，8+=失败)"

# 统计结果
$copied = (Get-ChildItem $dst -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Output "✅ 已复制文件数: $copied"

if ($exitCode -le 7) {
    Write-Output "✅ 备份成功！可以执行迁移了。"
    Write-Output "下一步：以管理员身份运行 migration_step2.ps1 完成迁移+创建符号链接"
} else {
    Write-Output "⚠️ 备份部分失败，请检查日志"
}
