# Self-Updater Enhancement Summary

**创建时间**: 2026-03-16  
**目的**: 解决OpenClaw更新后自定义配置被覆盖的问题

---

## 问题背景

OpenClaw更新时会覆盖以下修改：
1. ✅ 麦克风权限配置（`microphone=(self)`）
2. ✅ 插件启用状态（voice-call）
3. ⚠️ 其他自定义配置

**影响**：每次更新后需要手动重新配置

---

## 解决方案

### 核心思路
1. **配置文件驱动**：在`config/post-update-fixes.json`中定义需要修复的项目
2. **自动执行**：更新后自动运行修复脚本
3. **Codex集成**：复杂修复任务交给Codex处理
4. **优先级控制**：按重要性顺序执行修复

### 文件结构
```
skills/self-updater/
├── SKILL.md                          # 技能文档
├── config/
│   └── post-update-fixes.json        # 修复配置（NEW）
├── scripts/
│   ├── self-update.py                # 原版更新脚本
│   ├── self-update-enhanced.py       # 增强版（NEW）
│   └── fix-microphone.sh             # 麦克风修复脚本（NEW）
└── README-enhancement.md             # 本文档（NEW）
```

---

## 使用方法

### 基本用法
```bash
# 更新OpenClaw并自动修复
python ~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py

# 只检查不更新
python ~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py --check-only

# 强制更新但跳过修复
python ~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py --force --skip-fixes
```

### 添加新的修复项

**场景1：简单脚本修复**
1. 创建脚本：`scripts/fix-yourname.sh`
2. 添加到配置：
```json
{
  "name": "your-fix",
  "description": "修复说明",
  "enabled": true,
  "priority": 3,
  "type": "script",
  "script": "fix-yourname.sh",
  "verify": "验证命令"
}
```

**场景2：命令修复**
```json
{
  "name": "enable-plugin",
  "type": "command",
  "command": "openclaw plugins enable your-plugin"
}
```

**场景3：Codex处理复杂修复**
```json
{
  "codex_tasks": [{
    "name": "complex-fix",
    "enabled": true,
    "trigger": "auto",
    "prompt": "检查并修复配置文件格式变化"
  }]
}
```

---

## 当前已配置的修复项

### 1. 麦克风权限修复
- **文件**: `scripts/fix-microphone.sh`
- **作用**: 修改`Permissions-Policy`允许麦克风访问
- **优先级**: 1（最高）
- **验证**: 检查`microphone=(self)`是否存在

### 2. Voice-call插件启用
- **命令**: `openclaw plugins enable voice-call`
- **作用**: 确保语音通话插件启用
- **优先级**: 2

---

## 工作流程

```
1. Pre-Update Check
   ├─ 记录当前版本
   ├─ 检查Gateway状态
   └─ 记录活跃Session数

2. Execute Update
   ├─ 运行npm update
   └─ 验证新版本安装

3. Post-Update Fixes (NEW)
   ├─ 加载配置文件
   ├─ 按优先级执行修复
   ├─ 验证每个修复结果
   └─ 可选：调用Codex处理复杂任务

4. Restart & Verify
   ├─ 重启Gateway
   ├─ 验证Gateway响应
   └─ 检查Session恢复
```

---

## 测试方法

### 测试修复脚本
```bash
# 单独测试麦克风修复
bash ~/.openclaw/workspace/skills/self-updater/scripts/fix-microphone.sh

# 验证结果
grep 'microphone=(self)' /home/mzg/.npm-global/lib/node_modules/openclaw/dist/gateway-cli-*.js
```

### 测试完整流程
```bash
# 1. 先破坏配置（模拟更新）
sed -i 's/microphone=(self)/microphone=()/g' /home/mzg/.npm-global/lib/node_modules/openclaw/dist/gateway-cli-*.js

# 2. 运行修复（不更新）
python ~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py --check-only

# 3. 手动运行修复
python ~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py --skip-fixes=false
```

---

## 维护指南

### 添加新修复项的步骤
1. 识别问题（更新后什么被覆盖了？）
2. 编写修复脚本或命令
3. 添加到`config/post-update-fixes.json`
4. 测试验证
5. 更新文档

### 定期检查
- 每次OpenClaw大版本更新后检查是否有新的破坏性变更
- 测试现有修复脚本是否仍然有效
- 更新配置文件

---

## 未来改进

### 短期（1-2周）
- [ ] 添加更多常见配置的修复
- [ ] 改进错误处理和日志
- [ ] 添加回滚机制

### 中期（1个月）
- [ ] 自动检测配置变化
- [ ] 生成修复脚本建议
- [ ] 集成到OpenClaw官方更新流程

### 长期
- [ ] 向OpenClaw官方提PR，支持配置持久化
- [ ] 建立社区共享的修复配置库

---

## 相关文件

- 配置文件：`~/.openclaw/workspace/skills/self-updater/config/post-update-fixes.json`
- 增强脚本：`~/.openclaw/workspace/skills/self-updater/scripts/self-update-enhanced.py`
- 麦克风修复：`~/.openclaw/workspace/skills/self-updater/scripts/fix-microphone.sh`
- 技能文档：`~/.openclaw/workspace/skills/self-updater/SKILL.md`

---

**版本**: 1.0  
**作者**: DJJ  
**最后更新**: 2026-03-16
