# 2026-02-28 - Skill 学习笔记（model-usage & healthcheck）

## model-usage Skill

**用途**: 追踪 CodexBar CLI 的模型使用成本

**关键学习点**:
- 依赖外部工具 `codexbar`（macOS only，通过 brew 安装）
- 提供脚本 `model_usage.py` 分析成本 JSON
- 支持两种模式：`current`（最近使用）和 `all`（全部历史）
- 输出格式：文本或 JSON

**限制**:
- 仅支持 macOS（CodexBar CLI）
- Linux 支持待添加
- 对我们来说不太实用，因为我们用 OpenClaw 而不是 CodexBar

**与我们的关系**:
- 我们已经有 `session_status` 工具显示实时 token 使用
- 可以借鉴其成本分析逻辑，但不需要依赖 codexbar

---

## healthcheck Skill

**用途**: 主机安全加固和风险评估

**关键学习点**:
1. **模型自检**: 开始前检查是否使用 SOTA 模型（Opus 4.5+/GPT 5.2+）
2. **8 步工作流程**:
   - 0) 模型自检
   - 1) 建立上下文（只读检查）
   - 2) OpenClaw 安全审计
   - 3) 版本检查
   - 4) 确定风险容忍度
   - 5) 生成修复计划
   - 6) 提供执行选项
   - 7) 执行（需确认）
   - 8) 验证和报告

3. **安全检查清单**:
   - OS 版本和权限
   - 访问路径（本地/SSH/RDP）
   - 网络暴露（公网/IP/代理）
   - 备份状态
   - 磁盘加密
   - 自动安全更新
   - OpenClaw gateway 状态

4. **风险配置文件**:
   - Home/Workstation Balanced（最常见）
   - VPS Hardened（严格）
   - Developer Convenience（宽松）
   - Custom（自定义）

5. **OpenClaw 命令**:
   - `openclaw security audit [--deep] [--fix] [--json]`
   - `openclaw update status`
   - `openclaw cron add|list|runs|run`

**安全原则**:
- 任何状态改变都需要显式确认
- 不修改远程访问设置（除非确认用户连接方式）
- 提供回滚计划
- 敏感信息打码

---

## 学习总结

**Skill 设计模式观察**:
1. **healthcheck** 是复杂 workflow skill 的典范：
   - 清晰的步骤编号（0-8）
   - 每个步骤有明确的输入/输出
   - 多处需要用户确认（安全关键）
   - 提供多种执行选项（全自动/仅计划/仅关键/导出）

2. **model-usage** 是工具封装 skill：
   - 简单包装外部 CLI
   - 提供脚本处理数据
   - 依赖特定环境（macOS）

**下一步学习**:
- summarize（长文本总结）
- 可能还有其他有用的 skills 在目录里
