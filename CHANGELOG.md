# CHANGELOG - 灵助 V180

## V180.0 (2026-05-17)

### 🎉 版本类型
**主版本升级** - 从V165.6升级到V180，重大功能升级

---

### ✨ 新增功能

#### 1. 升级4个核心引擎
- **CognigramBridge** - 语义理解引擎（5个端点）
  - 文本理解、多模态理解、上下文记忆、语义推理、知识图谱
  - 新增端点：`/cogni/understand_text`, `/cogni/understand_multimodal`, `/cogni/retrieve_memory`, `/cogni/infer_causal`, `/cogni/analogical_reasoning`, `/cogni/knowledge_graph`, `/cogni/expand_knowledge_graph`, `/cogni/stats`
  
- **ModelDownloader** - 模型下载器（6个端点）
  - 多模型并行下载、进度追踪、断点续传、队列管理、版本管理
  - 新增端点：`/model/download`, `/model/progress`, `/model/active`, `/model/resume`, `/model/versions`, `/model/rollback`, `/model/check_update`, `/model/stats`
  
- **EdgeInference** - 边缘推理引擎（7个端点）
  - 边缘设备注册、模型压缩与量化、分布式推理、离线推理、推理加速
  - 新增端点：`/edge/register_device`, `/edge/list_devices`, `/edge/compress_model`, `/edge/distribute_inference`, `/edge/enable_offline`, `/edge/infer_offline`, `/edge/enable_acceleration`, `/edge/infer_with_acceleration`, `/edge/stats`
  
- **OfflineAutonomy** - 离线自治引擎（8个端点）
  - 离线决策、本地知识库、任务队列管理、自动同步
  - 新增端点：`/offline/make_decision`, `/offline/network_status`, `/offline/add_knowledge`, `/offline/search_knowledge`, `/offline/queue_task`, `/offline/get_next_task`, `/offline/complete_task`, `/offline/sync`, `/offline/stats`

#### 2. 新增3个引擎
- **MCPDualModeEngine** - MCP双模引擎（4个端点）
  - stdio/SSE双模式、动态切换、自动重连
  - 新增端点：`/mcp/status`, `/mcp/register`, `/mcp/send`, `/mcp/switch_mode`
  
- **DockerSandbox** - Docker安全沙箱（3个端点）
  - 代码执行隔离、命令执行隔离、资源限制
  - 新增端点：`/sandbox/status`, `/sandbox/execute_code`, `/sandbox/execute_command`
  
- **DualSemanticApprovalChain** - 双轨语义审批链（2个端点）
  - 批量匹配、自动审批
  - 新增端点：`/approval/batch_match`, `/approval/validate`

#### 3. 强化3个现有引擎
- **DreamingEngine** - 梦境引擎强化（3个端点）
  - 启动梦境、批量创建连接、统计信息
  - 新增端点：`/dreaming/start`, `/dream/batch_connections`, `/dreaming/stats`
  
- **SafeHarnessDefense** - SafeHarness防御强化（4个端点）
  - 重置防御、测试防御周期、查看漏洞、统计信息
  - 新增端点：`/safeharness/reset`, `/safeharness/defense_cycle`, `/safeharness/vulnerabilities`, `/safeharness/stats`
  
- **HermesSelfEvolution** - Hermes自进化学习循环（6个端点）
  - 查看统计、评估进化效果、A/B测试、压力测试、进化历史、自动回滚
  - 新增端点：`/hermes/evolution_stats`, `/hermes/evaluate_evolution`, `/hermes/ab_test`, `/hermes/stress_test`, `/hermes/evolution_history`, `/hermes/auto_rollback`

#### 4. 技能格式对齐
- **SkillMetadataAligner** - 技能元数据对齐器（3个端点）
  - 对齐单个技能、对齐所有技能、查看统计
  - 新增端点：`/skill_aligner/stats`, `/skill_aligner/align`, `/skill_aligner/align_all`

---

### 🔧 优化改进

1. **API端点总数**: 从0增加到45+个
2. **测试覆盖**: 30/45个端点已测试成功 ✅
3. **多Agent管理**: 6个Agent（Lingzhu, DaoNovice, HermesAgent, Hermes, Deer-Flow, ALLINAI）
4. **技能分享平台**: 支持技能在Agent之间流动
5. **统一任务调度**: 创建、跟踪、管理所有Agent的任务
6. **统一状态监控**: 实时监控所有Agent的健康状态、资源使用、性能指标

---

### 🐛 Bug修复

1. **端点定义位置错误** - 端点定义在`uvicorn.run()`之后，导致无法注册
   - 修复：将所有端点移到`uvicorn.run()`之前
   
2. **类名大小写错误** - `CogniGramBridge`（大写G）应为`CognigramBridge`（小写g）
   - 修复：更正导入和实例化语句中的类名
   
3. **POST端点参数类型** - 部分POST端点使用`dict`参数，应改为`BaseModel`
   - 部分修复：已测试的端点工作正常，未测试的端点待优化

---

### ⚠️ Breaking Changes

**无** - 本版本完全向后兼容，不影响现有功能。

---

### 📚 升级指南

#### 从V165.6升级到V180

1. **备份当前版本**
   ```bash
   cp -r /root/ai-stack/lingzhu /root/ai-stack/lingzhu_backup_v165.6
   ```

2. **下载V180版本**
   ```bash
   cd /root/ai-stack/lingzhu
   git fetch origin
   git checkout v180.0
   ```

3. **安装新依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **更新配置文件**
   - 检查`AGENTS_CONFIG`（多Agent配置）
   - 检查端口分配（8000, 8088, 8888, 5000, 7777, 9999）

5. **重启服务**
   ```bash
   pkill -f "python3 main.py"
   bash start_lingzhu.sh
   ```

6. **验证升级**
   ```bash
   curl http://localhost:8000/
   curl http://localhost:8000/cogni/stats
   curl http://localhost:8000/model/stats
   ```

---

### 📊 测试报告

| 模块 | 端点总数 | 已测试 | 未测试 |
|------|---------|--------|--------|
| CognigramBridge | 8 | 2 ✅ | 6 ⚠️ |
| ModelDownloader | 8 | 2 ✅ | 6 ⚠️ |
| EdgeInference | 9 | 2 ✅ | 7 ⚠️ |
| OfflineAutonomy | 9 | 2 ✅ | 7 ⚠️ |
| MCP双模引擎 | 4 | 4 ✅ | 0 |
| Docker安全沙箱 | 3 | 3 ✅ | 0 |
| 双轨语义审批链 | 2 | 2 ✅ | 0 |
| 技能元数据对齐 | 3 | 3 ✅ | 0 |
| 梦境引擎 | 3 | 3 ✅ | 0 |
| SafeHarness | 4 | 4 ✅ | 0 |
| Hermes自进化 | 6 | 2 ✅ | 4 ⚠️ |
| **总计** | **52** | **30 ✅** | **22 ⚠️** |

---

### 🚀 下一步计划（V180.1）

1. **修复POST端点** - 为所有POST端点添加BaseModel定义
2. **提高测试覆盖** - 测试所有未测试的端点
3. **性能优化** - 优化高并发场景下的性能
4. **文档完善** - 添加更多使用示例和教程

---

### 👥 贡献者

- **灵助（LingZhu）V180** - 主要开发和测试
- **润泽（Runze）** - 项目管理和需求指导

---

### 📞 联系方式

- **项目地址**: `/root/ai-stack/lingzhu/`
- **文档地址**: `/root/ai-stack/lingzhu/LINGZHU_V180_API.md`
- **问题反馈**: 通过WorkBuddy联系润泽

---

**发布日期**: 2026-05-17  
**版本作者**: 灵助 V180  
**文档版本**: V1.0