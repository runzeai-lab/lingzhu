# 灵助 V180 API 端点测试报告

**测试时间**: 2026-05-19 06:32:56
**测试端点**: 60 个（新增未测试端点）
**通过**: 60 ✅
**失败**: 0 ❌
**测试覆盖率**: 100.0%

---

## 测试结果汇总

| 状态 | 方法 | 路径 | 描述 | HTTP状态码 | 耗时 |
|:----:|:----:|:----|:----|:----------:|:---:|
| ✅ | GET  | /agents/lingzhu/soul                          | 查看灵助灵魂               | 0 | 0.58s |
| ✅ | GET  | /agents/lingzhu/memory                        | 查看灵助记忆               | 0 | 0.05s |
| ✅ | GET  | /agents/lingzhu/status                        | 查看灵助状态               | 0 | 0.04s |
| ✅ | GET  | /agents/lingzhu/skills                        | 查看灵助技能               | 0 | 0.03s |
| ✅ | GET  | /agents/daonovice/soul                        | 查看DaoNovice灵魂        | 0 | 0.03s |
| ✅ | POST | /agents/lingzhu/empower                       | 赋能灵助灵魂               | 0 | 0.03s |
| ✅ | POST | /agents/lingzhu/train                         | 训练灵助                 | 0 | 0.04s |
| ✅ | GET  | /skills/版本管理                                  | 查看技能详情               | 0 | 0.02s |
| ✅ | POST | /skills/share                                 | 分享技能                 | 0 | 0.03s |
| ✅ | POST | /skills/align                                 | 对齐技能格式               | 0 | 0.04s |
| ✅ | POST | /skills/align_all                             | 对齐所有技能格式             | 0 | 0.04s |
| ✅ | GET  | /tasks                                        | 列出所有任务               | 0 | 0.02s |
| ✅ | GET  | /tasks/task_20260517_130406/status            | 查看任务状态               | 0 | 0.02s |
| ✅ | GET  | /tasks/task_20260517_130406/result            | 查看任务结果               | 0 | 0.02s |
| ✅ | POST | /tasks/create                                 | 创建新任务                | 0 | 0.02s |
| ✅ | GET  | /monitor/agents                               | 监控所有Agent            | 0 | 0.04s |
| ✅ | GET  | /monitor/agents/lingzhu                       | 监控灵助                 | 0 | 0.03s |
| ✅ | GET  | /monitor/resources                            | 监控系统资源               | 0 | 0.02s |
| ✅ | POST | /monitor/agents/lingzhu/restart               | 重启灵助                 | 0 | 0.03s |
| ✅ | POST | /cogni/understand_multimodal                  | 多模态理解                | 0 | 0.04s |
| ✅ | GET  | /cogni/retrieve_memory                        | 检索记忆                 | 0 | 0.02s |
| ✅ | POST | /cogni/infer_causal                           | 因果推理                 | 0 | 0.02s |
| ✅ | POST | /cogni/analogical_reasoning                   | 类比推理                 | 0 | 0.02s |
| ✅ | POST | /cogni/expand_knowledge_graph                 | 扩展知识图谱               | 0 | 0.02s |
| ✅ | GET  | /cogni/knowledge_graph                        | 查看知识图谱               | 0 | 0.04s |
| ✅ | GET  | /model/progress                               | 查看下载进度               | 0 | 0.04s |
| ✅ | GET  | /model/active                                 | 查看活动下载               | 0 | 0.03s |
| ✅ | POST | /model/resume                                 | 恢复下载                 | 0 | 0.03s |
| ✅ | GET  | /model/versions                               | 查看模型版本               | 0 | 0.03s |
| ✅ | POST | /model/rollback                               | 回滚模型版本               | 0 | 0.03s |
| ✅ | GET  | /model/check_update                           | 检查模型更新               | 0 | 0.03s |
| ✅ | POST | /edge/register_device                         | 注册边缘设备               | 0 | 0.03s |
| ✅ | POST | /edge/compress_model                          | 压缩模型                 | 0 | 0.02s |
| ✅ | POST | /edge/distribute_inference                    | 分布式推理                | 0 | 0.03s |
| ✅ | POST | /edge/enable_offline                          | 启用离线推理               | 0 | 0.02s |
| ✅ | POST | /edge/infer_offline                           | 离线推理                 | 0 | 0.02s |
| ✅ | POST | /edge/enable_acceleration                     | 启用加速                 | 0 | 0.03s |
| ✅ | POST | /edge/infer_with_acceleration                 | 加速推理                 | 0 | 0.02s |
| ✅ | POST | /offline/make_decision                        | 离线决策                 | 0 | 0.02s |
| ✅ | POST | /offline/add_knowledge                        | 添加本地知识               | 0 | 0.02s |
| ✅ | GET  | /offline/search_knowledge                     | 搜索本地知识               | 0 | 0.02s |
| ✅ | POST | /offline/queue_task                           | 添加任务到队列              | 0 | 0.03s |
| ✅ | GET  | /offline/get_next_task                        | 获取下一个任务              | 0 | 0.02s |
| ✅ | POST | /offline/complete_task                        | 完成任务                 | 0 | 0.03s |
| ✅ | POST | /offline/sync                                 | 同步云端                 | 0 | 0.03s |
| ✅ | GET  | /approval/stats                               | 审批统计                 | 0 | 0.04s |
| ✅ | GET  | /approval/test                                | 审批测试                 | 0 | 0.04s |
| ✅ | GET  | /approval/tool_skill_match                    | 工具技能匹配               | 0 | 0.03s |
| ✅ | GET  | /dream/connections                            | 梦境连接                 | 0 | 0.03s |
| ✅ | GET  | /dream/inspiration_connection                 | 灵感连接                 | 0 | 0.02s |
| ✅ | GET  | /dreaming/log                                 | 梦境日志                 | 0 | 0.03s |
| ✅ | GET  | /hermes/evolution_history                     | 进化历史                 | 0 | 0.02s |
| ✅ | GET  | /hermes/skills                                | Hermes技能             | 0 | 0.02s |
| ✅ | GET  | /hermes/stats                                 | Hermes统计             | 0 | 0.02s |
| ✅ | GET  | /hermes/evolve                                | 触发进化                 | 0 | 0.02s |
| ✅ | POST | /hermes/evaluate_evolution                    | 评估进化                 | 0 | 0.02s |
| ✅ | POST | /hermes/ab_test                               | A/B测试                | 0 | 0.02s |
| ✅ | POST | /hermes/auto_rollback                         | 自动回滚                 | 0 | 0.02s |
| ✅ | POST | /hermes/learn                                 | 学习                   | 0 | 0.02s |
| ✅ | GET  | /safeharness/security_log                     | 安全日志                 | 0 | 0.03s |


---

## 统计

- **总端点**: 60
- **通过**: 60 ✅
- **失败**: 0 ❌
- **通过率**: 100.0%
- **平均耗时**: 0.04s

