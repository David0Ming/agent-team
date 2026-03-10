# 📋 PARA - 项目和领域管理

> 基于PARA方法：Projects（项目）、Areas（领域）、Resources（资源）、Archives（归档）

---

## 🎯 Projects（活跃项目）

> 具体的、有完成标准的短期任务

### 产品工作

- [ ] **P1: Shannon安全测试项目** (RICE: TBD)
  - 使用Shannon AI渗透测试工具测试嘟嘟巴士主营产品安全性
  - **状态**：暂缓（等待信息补充）
  - **负责人**：DMing（技术）、Dtester（测试）
  - **待办**：
    - [ ] 确认测试目标系统（用户端/后端API/管理后台）
    - [ ] 获取源代码仓库访问权限
    - [ ] 评估测试环境状态（Staging/Dev）
    - [ ] 申请Anthropic API Key
  - **文档**：`projects/shannon-security-test/`

- [ ] **P2: 飞书机器人上传文件权限+竞品可视化** (RICE: 10.0)
  - 配置飞书应用权限，上传文件能力
  - 把竞品信息设置成可视化图表并上传
  - 影响：50个团队成员 | 工作量：Large
  - **状态**：已暂缓（优先级不高）

- [ ] **P3: 给OpenClaw连接Discord** (RICE: 4.0)
  - 配置Discord频道，让OpenClaw可以发送消息
  - 影响：10个潜在用户 | 工作量：Medium

### 个人学习

- [ ] **学习三个中等题视频**
  - 找3个讲解中等难度题目的视频学习
  - 目标：掌握解题思路和方法

- [ ] **找合适的实验论文综述**
  - 搜索并阅读实验论文综述
  - 目标：掌握分析实验结果的方法

- [ ] **学习量化加速**
  - 学习模型量化技术（INT8/INT4量化）
  
- [ ] **显存优化**
  - 学习显存优化技术（梯度检查点、混合精度训练）

- [ ] **处理并发**
  - 学习并发处理技术（异步推理、批处理）

- [ ] **解决幻觉问题**
  - 学习减少LLM幻觉的方法（RAG、思维链）

- [ ] **数据调优**
  - 学习数据质量优化和微调技术

---

## 🏢 Areas（持续责任领域）

> 没有结束日期的持续责任

### 产品工作
- **嘟嘟巴士先锋引擎**：每日09:00自动生成10条视频prompt
  - 项目路径：`projects/dudubashi-pioneer/`
  - 工作流程：参考 `projects/dudubashi-pioneer/WORKFLOW.md`
  
- **海野山房酒店视频**：每日13:40自动生成5条视频prompt
  - 项目路径：`projects/haiye-hotel/`
  
- **竞品监控**：持续跟踪竞品动态
  - 项目路径：`projects/dudubashi-pioneer/`
  - 工作流程：参考 `projects/dudubashi-pioneer/WORKFLOW.md`
  - 执行命令：
    ```bash
    cd projects/dudubashi-pioneer
    python3 scripts/fetch_newrank_auto.py
    python3 scripts/generate_competitor_report.py
    ```
  - 配置文件：`projects/dudubashi-pioneer/config/newrank.json`
  - 输出位置：`projects/dudubashi-pioneer/competitor-data/YYYY-MM-DD/`

### Agent系统
- **Agent团队管理**：DJJ、DMing、David及子团队协作
- **系统维护**：OpenClaw配置、心跳监控、日志管理
- **知识管理**：技能索引、知识卡片、记忆系统

### 个人成长
- **AI/ML学习**：持续学习前沿技术
- **算法训练**：中等难度题目练习
- **产品能力**：RICE分析、PRD撰写

---

## 📚 Resources（资源）

> 学习材料和感兴趣的主题

- **技能库**：`~/.openclaw/workspace/skills/` (8个技能)
- **知识库**：`~/.openclaw/workspace/memory/learning/knowledge/` (38个知识卡片)
- **最佳实践**：PARA方法、Agent协作模式、产品管理框架

---

## 📦 Archives（归档）

> 已完成或不再活跃的项目

### 2026-03

- [x] **P0: 嘟嘟巴士prompt生成质量优化** (2026-03-07)
  - 质量从6.5/10提升到8.5/10
  - 重构为混合方案（规则引擎+AI生成+反思学习）

### 2026-02

- [x] **OpenClaw配置优化** (2026-02-28)
  - 配置memory-lancedb-pro插件
  - 拆分MEMORY.md为主题文件
  - 配置Agent人设和模型容灾

- [x] **Token Estimator Skill** (2026-02-28)
  - 创建token估算工具
  - 实现文件大小检测和模型选择

- [x] **Agent三层协作架构** (2026-03-03)
  - 身份层、操作层、知识层、共享层
  - 基于Shubham Saboo方法论

- [x] **海野山房酒店视频项目** (2026-03-07)
  - 自动化脚本和定时任务
  - 老板娘人设配置

---

## 🎯 下一步行动

**今天**：
- 无紧急任务

**本周**：
- 学习AI/ML相关主题（量化、显存优化等）

**本月**：
- 定期归档不活跃项目
- 清理未使用的知识卡片

---

**维护规则**：
- 每周检查Projects进度
- 每月归档完成的Projects
- 每季度评估Areas的价值
