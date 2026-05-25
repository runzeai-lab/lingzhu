# IMA 知识库读取计划

## 目标
读取两个 IMA 知识库的全部笔记内容：
1. **经典V102**（个人知识库）
2. **灵助部署**（分享知识库，shareId: `fe3b4c23a2732900204a896c39c995bdaf00c1897555adcd424be23a1fdcf957`）

## 方法（避免编码问题）

### 方案：直接使用 WorkBuddy 内置的 MCP 工具调用
- WorkBuddy 的 MCP 集成已经配置好 `ima` 服务
- 直接通过 `mcp_call_tool` 调用 IMA API
- 避免 PowerShell/Node.js/Python 的编码问题

## 步骤

### 步骤1：搜索"经典V102"知识库
- 工具：`ima_search_knowledge_base`
- 参数：`{"query": "经典V102", "limit": 20}`
- 目标：获取 `knowledge_base_id`

### 步骤2：列出知识库内容
- 工具：`ima_list_knowledge`
- 参数：`{"knowledge_base_id": "<kb_id>", "limit": 50}`
- 目标：获取所有笔记的 `doc_id`

### 步骤3：批量获取笔记内容
- 工具：`ima_batch_get_notes`
- 参数：`{"knowledge_base_id": "<kb_id>", "doc_ids": ["id1", "id2", ...], "format": "text"}`
- 注意：每次最多20篇，需要分批获取

### 步骤4：处理"灵助部署"分享知识库
- 问题：分享链接的 `shareId` 如何转换为 `knowledge_base_id`？
- 需要：查看 IMA API 文档，找到通过 `shareId` 获取知识库信息的方法
- 可能的方法：
  - 尝试 `ima_search_knowledge_base` 搜索"灵助部署"
  - 或找到专门处理分享链接的 API 端点

### 步骤5：保存和分析内容
- 保存为 JSON 和纯文本格式
- 分析笔记内容，提取与灵助升级相关的关键信息
- 输出升级方案和计划

## 预期输出
1. `ima_classic_v102_notes.json` - "经典V102"知识库全部笔记（JSON格式）
2. `ima_classic_v102_notes.txt` - 纯文本格式，方便阅读
3. `ima_lingzhu_deployment_notes.json` - "灵助部署"知识库全部笔记
4. `ima_lingzhu_deployment_notes.txt` - 纯文本格式
5. **灵助升级方案和计划**（Markdown格式，包含增量升级和融合升级）

## 执行策略
- **一干到底**：直接执行，减少确认
- **容错处理**：如果某个 API 调用失败，尝试替代方案
- **分批处理**：笔记数量多时分批获取，避免超时
- **保存中间结果**：每成功获取一批笔记就保存，避免重复工作
