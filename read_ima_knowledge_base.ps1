#!/usr/bin/env pwsh
"""
PowerShell 脚本 - 直接调用 IMA API 读取"经典V102"知识库的全部笔记内容
"""

# IMA API 配置
$IMA_API_BASE = 'https://ima.qq.com'
$IMA_CLIENT_ID = '910fce0cc27f5685b8f06c9d88a9ae1e'
$IMA_API_KEY = 'BrqdfQbt50sKsme7VZX0xeTR4qwEYjS+vxUJP/2wiG5S57RGo7JB9uCh290CcXZuu6g88F4U8A=='

function Ima-ApiCall {
    param(
        [string]$Path,
        [string]$Module = 'wiki',
        [object]$Body
    )
    
    $url = "$IMA_API_BASE/openapi/$Module/v1/$Path"
    
    $headers = @{
        'ima-openapi-clientid' = $IMA_CLIENT_ID
        'ima-openapi-apikey' = $IMA_API_KEY
        'Content-Type' = 'application/json; charset=utf-8'
    }
    
    $jsonBody = $Body | ConvertTo-Json -Depth 10
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $jsonBody -TimeoutSec 30
        return $response
    }
    catch {
        return @{
            retcode = $_.Exception.Response.StatusCode.value__
            errmsg = $_.Exception.Message
        }
    }
}

function Search-KnowledgeBase {
    param([string]$Query, [int]$Limit = 20)
    
    Write-Host "🔍 搜索知识库: query='$Query', limit=$Limit" -ForegroundColor Cyan
    
    $body = @{
        query = $Query
        cursor = ""
        limit = $Limit
    }
    
    $response = Ima-ApiCall -Path 'search_knowledge_base' -Body $body
    
    if ($response.retcode -eq 0) {
        $results = $response.data.infos
        Write-Host "✅ 找到 $($results.Count) 个知识库" -ForegroundColor Green
        return $results
    }
    else {
        Write-Host "❌ 搜索失败: $($response.errmsg)" -ForegroundColor Red
        return @()
    }
}

function Get-KnowledgeBase {
    param([array]$Ids)
    
    Write-Host "📚 获取知识库详情: ids=$Ids" -ForegroundColor Cyan
    
    $body = @{
        ids = $Ids
    }
    
    $response = Ima-ApiCall -Path 'get_knowledge_base' -Body $body
    
    if ($response.retcode -eq 0) {
        $infos = $response.data.infos
        Write-Host "✅ 获取到 $($infos.Count) 个知识库详情" -ForegroundColor Green
        return $infos
    }
    else {
        Write-Host "❌ 获取详情失败: $($response.errmsg)" -ForegroundColor Red
        return @{}
    }
}

function Get-NotebookId {
    param([string]$KbId, [string]$DocId)
    
    $body = @{
        knowledge_base_id = $KbId
        media_id = $DocId
    }
    
    $response = Ima-ApiCall -Path 'get_media_info' -Body $body
    
    if ($response.retcode -eq 0) {
        $notebookId = $response.data.note_book_ext_info.note_book_id
        if (-not $notebookId) {
            $notebookId = $response.data.note_book_id
        }
        if (-not $notebookId) {
            $notebookId = $response.data.note_id
        }
        return $notebookId
    }
    
    return $null
}

function Get-NoteContent {
    param([string]$NotebookId, [string]$Format = 'text')
    
    $url = "$IMA_API_BASE/openapi/note/v1/get_doc_content"
    
    $headers = @{
        'ima-openapi-clientid' = $IMA_CLIENT_ID
        'ima-openapi-apikey' = $IMA_API_KEY
        'Content-Type' = 'application/json; charset=utf-8'
    }
    
    $body = @{
        note_id = $NotebookId
        format = $Format
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -TimeoutSec 30
        return $response
    }
    catch {
        return $null
    }
}

function List-Knowledge {
    param([string]$KbId, [string]$FolderId = '', [int]$Limit = 50)
    
    Write-Host "📂 浏览知识库内容: kb_id=$($KbId.Substring(0, [Math]::Min(20, $KbId.Length)))..., folder_id=$FolderId, limit=$Limit" -ForegroundColor Cyan
    
    $body = @{
        knowledge_base_id = $KbId
        cursor = ""
        limit = $Limit
    }
    
    if ($FolderId) {
        $body.folder_id = $FolderId
    }
    
    $response = Ima-ApiCall -Path 'get_knowledge_list' -Body $body
    
    if ($response.retcode -eq 0) {
        $knowledgeList = $response.data.knowledge_list
        Write-Host "✅ 找到 $($knowledgeList.Count) 个内容" -ForegroundColor Green
        return $knowledgeList
    }
    else {
        Write-Host "❌ 浏览失败: $($response.errmsg)" -ForegroundColor Red
        return @()
    }
}

# 主程序
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host "IMA 知识库读取工具 - 经典V102" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Yellow

# 步骤1: 搜索"经典V102"知识库
$kbList = Search-KnowledgeBase -Query '经典V102' -Limit 20

if (-not $kbList -or $kbList.Count -eq 0) {
    Write-Host "`n❌ 未找到'经典V102'知识库，尝试列出所有知识库..." -ForegroundColor Yellow
    $kbList = Search-KnowledgeBase -Query '' -Limit 50
    
    if (-not $kbList -or $kbList.Count -eq 0) {
        Write-Host "❌ 未找到任何知识库" -ForegroundColor Red
        exit 1
    }
}

# 找到"经典V102"知识库
$targetKb = $null
foreach ($kb in $kbList) {
    $kbName = $kb.name
    Write-Host "  知识库: $kbName (ID: $($kb.id))" -ForegroundColor Gray
    if ($kbName -match '经典V102|V102') {
        $targetKb = $kb
        break
    }
}

if (-not $targetKb) {
    Write-Host "`n⚠️ 未找到名称完全匹配的'经典V102'知识库，使用第一个: $($kbList[0].name)" -ForegroundColor Yellow
    $targetKb = $kbList[0]
}

$kbId = $targetKb.id
$kbName = $targetKb.name
Write-Host "`n✅ 目标知识库: $kbName (ID: $kbId)" -ForegroundColor Green

# 步骤2: 获取知识库详情
$kbDetails = Get-KnowledgeBase -Ids @($kbId)
if ($kbDetails -and $kbDetails.ContainsKey($kbId)) {
    $kbDetail = $kbDetails[$kbId]
    Write-Host "  名称: $($kbDetail.name)" -ForegroundColor Gray
    Write-Host "  描述: $($kbDetail.description)" -ForegroundColor Gray
}

# 步骤3: 浏览知识库内容
Write-Host "`n📂 浏览知识库内容..." -ForegroundColor Cyan
$knowledgeList = List-Knowledge -KbId $kbId -Limit 50

if (-not $knowledgeList -or $knowledgeList.Count -eq 0) {
    Write-Host "❌ 知识库为空或读取失败" -ForegroundColor Red
    exit 1
}

# 步骤4: 提取所有笔记
$notes = @()
$folders = @()

foreach ($item in $knowledgeList) {
    $itemType = $item.type
    if ($itemType -eq 11) {  # 笔记类型
        $notes += $item
    }
    elseif ($itemType -eq 1) {  # 文件夹类型
        $folders += $item
    }
    
    $itemName = $item.title
    if (-not $itemName) { $itemName = $item.name }
    $itemId = $item.id
    $icon = if ($itemType -eq 11) { '📄' } else { '📁' }
    Write-Host "  $icon $itemName (ID: $($itemId.Substring(0, [Math]::Min(30, $itemId.Length))...)") -ForegroundColor Gray
}

Write-Host "`n📊 统计: $($notes.Count) 篇笔记, $($folders.Count) 个文件夹" -ForegroundColor Cyan

# 步骤5: 读取所有笔记内容
Write-Host "`n📖 读取所有笔记内容..." -ForegroundColor Cyan
$notesContent = @()

for ($i = 0; $i -lt $notes.Count; $i++) {
    $note = $notes[$i]
    $docId = $note.id
    $title = $note.title
    
    Write-Host "  [$((($i + 1))] 读取: $title..." -NoNewline -ForegroundColor Gray
    
    # 获取 notebook_id
    $notebookId = Get-NotebookId -KbId $kbId -DocId $docId
    
    if (-not $notebookId) {
        Write-Host "❌ 无法获取 notebook_id (可能不是笔记类型)" -ForegroundColor Red
        continue
    }
    
    # 获取笔记内容
    $contentResponse = Get-NoteContent -NotebookId $notebookId -Format 'text'
    
    if ($contentResponse -and $contentResponse.code -eq 0) {
        $content = $contentResponse.data.content
        $contentTitle = $contentResponse.data.title
        
        Write-Host "✅ (内容长度: $($content.Length))" -ForegroundColor Green
        
        $notesContent += @{
            title = $title
            doc_id = $docId
            notebook_id = $notebookId
            content = $content
            content_title = $contentTitle
        }
    }
    else {
        Write-Host "❌ 获取内容失败" -ForegroundColor Red
    }
    
    # 避免 API 限流
    Start-Sleep -Milliseconds 500
}

# 步骤6: 保存结果
Write-Host "`n💾 保存结果..." -ForegroundColor Cyan

$outputFile = 'ima_classic_v102_notes.json'
$outputData = @{
    knowledge_base = @{
        id = $kbId
        name = $kbName
    }
    notes_count = $notesContent.Count
    notes = $notesContent
}

$outputData | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding utf8
Write-Host "✅ 结果已保存到: $outputFile" -ForegroundColor Green
Write-Host "   共 $($notesContent.Count) 篇笔记" -ForegroundColor Gray

# 也保存纯文本版本
$txtFile = 'ima_classic_v102_notes.txt'
$txtContent = "# IMA 知识库: $kbName`n`n"
$txtContent += "知识库 ID: $kbId`n"
$txtContent += "笔记数量: $($notesContent.Count)`n"
$txtContent += "导出时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$txtContent += "=" * 60 + "`n`n"

for ($i = 0; $i -lt $notesContent.Count; $i++) {
    $note = $notesContent[$i]
    $txtContent += "## $(($i + 1)). $($note.title)`n`n"
    $txtContent += $note.content
    $txtContent += "`n`n" + "=" * 60 + "`n`n"
}

$txtContent | Out-File -FilePath $txtFile -Encoding utf8
Write-Host "✅ 纯文本版本已保存到: $txtFile" -ForegroundColor Green

Write-Host "`n" + "=" * 60 -ForegroundColor Yellow
Write-Host "✅ 完成！" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Yellow
