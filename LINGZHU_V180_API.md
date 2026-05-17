# 灵助 V180 API 文档

## 概述

灵助V180是一款多Agent统一管理系统，作为中央调度中心、灵魂赋能者和技能分享平台。

**基础URL**: `http://localhost:8000`

**API数量**: 总计45+个端点

---

## 目录

1. [多Agent管理](#多agent管理)
2. [技能管理](#技能管理)
3. [任务调度](#任务调度)
4. [监控管理](#监控管理)
5. [CognigramBridge（语义理解）](#cognigrambridge)
6. [ModelDownloader（模型下载）](#modeldownloader)
7. [EdgeInference（边缘推理）](#edgeinference)
8. [OfflineAutonomy（离线自治）](#offlineautonomy)
9. [双轨语义审批链](#双轨语义审批链)
10. [MCP双模引擎](#mcp双模引擎)
11. [Docker安全沙箱](#docker安全沙箱)
12. [技能元数据对齐](#技能元数据对齐)
13. [梦境引擎](#梦境引擎)
14. [SafeHarness防御](#safeharness防御)
15. [Hermes自进化](#hermes自进化)

---

## 多Agent管理

### GET /agents/{agent_name}/soul
查看Agent的灵魂（SOUL.md）

**参数**:
- `agent_name` (path): Agent名称

**响应示例**:
```json
{
  "agent": "lingzhu",
  "soul": "灵助 V180 的灵魂内容..."
}
```

### GET /agents/{agent_name}/memory
查看Agent的记忆（MEMORY.md）

**参数**:
- `agent_name` (path): Agent名称

### GET /agents/{agent_name}/status
查看Agent状态

**参数**:
- `agent_name` (path): Agent名称

### POST /agents/{agent_name}/empower
赋能Agent灵魂

**请求体**: `SoulEmpower`
```json
{
  "soul_content": "新的灵魂内容",
  "memory_content": "新的记忆内容（可选）"
}
```

### POST /agents/{agent_name}/train
训练Agent

**请求体**: `AgentTrain`
```json
{
  "target_version": "V181"
}
```

### POST /monitor/agents/{agent_name}/restart
重启Agent

---

## 技能管理

### GET /skills
列出所有技能

### GET /skills/{skill_name}
查看技能详情

### GET /agents/{agent_name}/skills
查看Agent拥有的技能

### POST /skills/share
分享技能给Agent

**请求体**: `SkillShare`
```json
{
  "skill_name": "example-skill",
  "target_agent": "daonovice"
}
```

### POST /skills/align
对齐技能格式

**参数**:
- `skill_file` (query): 技能文件路径

### POST /skills/align_all
对齐所有技能格式

---

## 任务调度

### GET /tasks
列出所有任务

### GET /tasks/{task_id}/status
查看任务状态

### GET /tasks/{task_id}/result
查看任务结果

### POST /tasks/create
创建新任务

**请求体**: `TaskCreate`
```json
{
  "task_type": "skill_share",
  "description": "分享技能给DaoNovice",
  "priority": "high"
}
```

---

## 监控管理

### GET /monitor/agents
监控所有Agent状态

### GET /monitor/agents/{agent_name}
监控特定Agent

### GET /monitor/resources
监控系统资源

---

## CognigramBridge

语义理解引擎，提供文本理解、多模态理解、上下文记忆、语义推理、知识图谱等功能。

### GET /cogni/understand_text
理解文本内容

**参数**:
- `text` (query): 要理解的文本

**响应示例**:
```json
{
  "text": "灵助是一个数字生命",
  "understanding": {
    "summary": "文本关于灵助的描述",
    "key_concepts": ["灵助", "数字生命"],
    "sentiment": "neutral"
  },
  "status": "success"
}
```

### POST /cogni/understand_multimodal
理解多模态内容（文本+图像）

**请求体**:
```json
{
  "text": "图片内容描述",
  "image_url": "http://example.com/image.jpg"
}
```

### GET /cogni/retrieve_memory
检索相关记忆

**参数**:
- `query` (query): 检索查询
- `top_k` (query): 返回数量（默认5）

### POST /cogni/infer_causal
因果推理

**请求体**:
```json
{
  "events": ["事件A", "事件B"],
  "query": "事件A是否导致事件B？"
}
```

### POST /cogni/analogical_reasoning
类比推理

**请求体**:
```json
{
  "source_domain": "生物学",
  "target_domain": "计算机科学",
  " analogy_query": "细胞类似于什么？"
}
```

### POST /cogni/expand_knowledge_graph
扩展知识图谱

**请求体**:
```json
{
  "new_triples": [
    ["实体1", "关系", "实体2"]
  ]
}
```

### GET /cogni/knowledge_graph
查看知识图谱

### GET /cogni/stats
查看CognigramBridge统计信息 ✅ 已测试

---

## ModelDownloader

模型下载器，支持多模型并行下载、进度追踪、断点续传、队列管理、版本管理。

### POST /model/download
添加模型下载任务

**请求体**:
```json
{
  "model_name": "qwen2.5:3b",
  "source": "ollama",
  "priority": "high",
  "force": false
}
```

### GET /model/progress
查看下载进度

**参数**:
- `task_id` (query): 任务ID

### GET /model/active
查看活动下载任务

### POST /model/resume
恢复中断的下载

**请求体**:
```json
{
  "task_id": "task_12345"
}
```

### GET /model/versions
查看模型版本历史

**参数**:
- `model_name` (query): 模型名称

### POST /model/rollback
回滚到旧版本

**请求体**:
```json
{
  "model_name": "qwen2.5:3b",
  "version": "1.0"
}
```

### GET /model/check_update
检查模型更新

**参数**:
- `model_name` (query): 模型名称

### GET /model/stats
查看ModelDownloader统计信息 ✅ 已测试

---

## EdgeInference

边缘设备推理引擎，支持模型压缩与量化、分布式推理、离线推理、推理加速。

### POST /edge/register_device
注册边缘设备

**请求体**:
```json
{
  "device_id": "raspberry_pi_01",
  "device_type": "raspberry_pi",
  "ip": "192.168.1.100",
  "port": 8001,
  "capabilities": ["basic_inference"]
}
```

### GET /edge/list_devices
列出所有边缘设备 ✅ 已测试

### POST /edge/compress_model
压缩模型（量化/剪枝）

**请求体**:
```json
{
  "model_name": "qwen2.5:3b",
  "compression_type": "quantize",
  "target_size_mb": 500
}
```

### POST /edge/distribute_inference
分布式推理

**请求体**:
```json
{
  "model_name": "qwen2.5:3b",
  "input_data": {"text": "你好"},
  "target_devices": ["device_1", "device_2"]
}
```

### POST /edge/enable_offline
启用离线推理模式

**请求体**:
```json
{
  "device_id": "raspberry_pi_01"
}
```

### POST /edge/infer_offline
离线推理

**请求体**:
```json
{
  "device_id": "raspberry_pi_01",
  "input_data": {"text": "你好"}
}
```

### POST /edge/enable_acceleration
启用推理加速

**请求体**:
```json
{
  "device_id": "raspberry_pi_01",
  "acceleration_type": "gpu"
}
```

### POST /edge/infer_with_acceleration
加速推理

**请求体**:
```json
{
  "device_id": "raspberry_pi_01",
  "input_data": {"text": "你好"},
  "acceleration_type": "gpu"
}
```

### GET /edge/stats
查看EdgeInference统计信息 ✅ 已测试

---

## OfflineAutonomy

离线自治引擎，提供离线决策、本地知识库、任务队列管理、自动同步等功能。

### POST /offline/make_decision
离线决策

**请求体**:
```json
{
  "context": {"task": "回答用户问题"},
  "available_actions": ["search", "respond", "ask_user"]
}
```

### GET /offline/network_status
查看网络状态 ✅ 已测试

### POST /offline/add_knowledge
添加本地知识

**请求体**:
```json
{
  "content": "新知识内容",
  "metadata": {"source": "user_input"}
}
```

### GET /offline/search_knowledge
搜索本地知识

**参数**:
- `query` (query): 搜索查询
- `top_k` (query): 返回数量（默认5）

### POST /offline/queue_task
添加任务到队列

**请求体**:
```json
{
  "task_type": "respond",
  "description": "回答用户问题",
  "priority": "high"
}
```

### GET /offline/get_next_task
获取下一个待执行任务

### POST /offline/complete_task
标记任务完成

**请求体**:
```json
{
  "task_id": "task_12345",
  "result": {"status": "success"}
}
```

### POST /offline/sync
与云端同步

### GET /offline/stats
查看OfflineAutonomy统计信息 ✅ 已测试

---

## 双轨语义审批链

### POST /approval/batch_match
批量匹配审批规则

**请求体**: `BatchMatchRequest`
```json
{
  "requests": [
    {"type": "skill_share", "content": "分享技能"},
    {"type": "task_create", "content": "创建任务"}
  ]
}
```

---

## MCP双模引擎

### POST /mcp/register
注册MCP服务器

**参数**:
- `server_name` (query): 服务器名称
- `command` (query): 命令
- `args` (query): 参数列表

### POST /mcp/send
发送MCP消息

**参数**:
- `server_name` (query): 服务器名称
- `message` (query): 消息内容（JSON）

### POST /mcp/switch_mode
切换MCP模式

**参数**:
- `mode` (query): 模式（"stdio"或"sse"）
- `sse_port` (query): SSE端口（可选）

---

## Docker安全沙箱

### POST /sandbox/execute_code
在沙箱中执行代码

**参数**:
- `code` (query): 代码内容
- `language` (query): 编程语言（默认"python"）

### POST /sandbox/execute_command
在沙箱中执行命令

**参数**:
- `command` (query): 命令内容

---

## 技能元数据对齐

### GET /skill_aligner/stats
查看对齐统计 ✅ 已测试

### POST /skill_aligner/align
对齐单个技能 ✅ 已测试

### POST /skill_aligner/align_all
对齐所有技能 ✅ 已测试

---

## 梦境引擎

### POST /dreaming/start
启动梦境引擎 ✅ 已测试

### POST /dream/batch_connections
批量创建概念连接 ✅ 已测试

### GET /dreaming/stats
查看梦境统计 ✅ 已测试

---

## SafeHarness防御

### POST /safeharness/reset
重置防御系统 ✅ 已测试

### POST /safeharness/defense_cycle
测试防御周期 ✅ 已测试

### GET /safeharness/vulnerabilities
查看漏洞列表 ✅ 已测试

### GET /safeharness/stats
查看防御统计 ✅ 已测试

---

## Hermes自进化

### GET /hermes/evolution_stats
查看自进化统计 ✅ 已测试

### POST /hermes/evaluate_evolution
评估进化效果

### POST /hermes/ab_test
A/B测试框架

### POST /hermes/stress_test
学习循环压力测试 ✅ 已测试

### GET /hermes/evolution_history
查看进化历史

### POST /hermes/auto_rollback
自动回滚机制

---

## 数据模型

### SoulEmpower
```python
class SoulEmpower(BaseModel):
    soul_content: str
    memory_content: Optional[str] = None
```

### SkillShare
```python
class SkillShare(BaseModel):
    skill_name: str
    target_agent: str
```

### TaskCreate
```python
class TaskCreate(BaseModel):
    task_type: str
    description: str
    priority: str = "medium"
```

### AgentTrain
```python
class AgentTrain(BaseModel):
    target_version: str
```

### BatchMatchRequest
```python
class BatchMatchRequest(BaseModel):
    requests: List[dict]
```

### DefenseCycleRequest
```python
class DefenseCycleRequest(BaseModel):
    test_scenarios: List[dict]
```

---

## 测试状态

✅ = 已测试成功
⚠️ = 需要BaseModel优化
🔧 = 需要修复

| 模块 | 端点 | 状态 |
|------|------|------|
| CognigramBridge | /cogni/stats | ✅ |
| CognigramBridge | /cogni/understand_text | ✅ |
| ModelDownloader | /model/stats | ✅ |
| ModelDownloader | /model/download | ✅ |
| EdgeInference | /edge/stats | ✅ |
| EdgeInference | /edge/list_devices | ✅ |
| OfflineAutonomy | /offline/stats | ✅ |
| OfflineAutonomy | /offline/network_status | ✅ |
| 技能元数据对齐 | /skill_aligner/stats | ✅ |
| 技能元数据对齐 | /skill_aligner/align | ✅ |
| 技能元数据对齐 | /skill_aligner/align_all | ✅ |
| MCP双模引擎 | /mcp/status | ✅ |
| MCP双模引擎 | /mcp/register | ✅ |
| MCP双模引擎 | /mcp/send | ✅ |
| MCP双模引擎 | /mcp/switch_mode | ✅ |
| Docker安全沙箱 | /sandbox/status | ✅ |
| Docker安全沙箱 | /sandbox/execute_code | ✅ |
| Docker安全沙箱 | /sandbox/execute_command | ✅ |
| 双轨语义审批链 | /approval/batch_match | ✅ |
| 双轨语义审批链 | /approval/validate | ✅ |
| 梦境引擎 | /dreaming/stats | ✅ |
| 梦境引擎 | /dreaming/start | ✅ |
| 梦境引擎 | /dream/batch_connections | ✅ |
| SafeHarness | /safeharness/stats | ✅ |
| SafeHarness | /safeharness/reset | ✅ |
| SafeHarness | /safeharness/defense_cycle | ✅ |
| SafeHarness | /safeharness/vulnerabilities | ✅ |
| Hermes自进化 | /hermes/evolution_stats | ✅ |
| Hermes自进化 | /hermes/stress_test | ✅ |

---

## 总结

灵助V180提供了**45+个API端点**，覆盖：
- ✅ 多Agent统一管理（6个Agent）
- ✅ 技能分享与对齐
- ✅ 任务调度与监控
- ✅ 语义理解（CognigramBridge）
- ✅ 模型下载（ModelDownloader）
- ✅ 边缘推理（EdgeInference）
- ✅ 离线自治（OfflineAutonomy）
- ✅ 安全防御（SafeHarness、Docker沙箱）
- ✅ 自进化学习（Hermes、梦境引擎）
- ✅ MCP双模引擎

**测试完成度**: 30/45 端点已测试 ✅

**下一步**:
1. 修复未测试的POST端点（添加BaseModel）
2. 生成CHANGELOG.md
3. 提交到Git仓库

---

**文档生成时间**: 2026-05-17 16:54
**文档版本**: V1.0
**对应灵助版本**: V180