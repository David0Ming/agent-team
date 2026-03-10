# OpenClaw 完整恢复指南

## 备份清单

### 1. OpenClaw 核心目录
```bash
# 备份整个 .openclaw 目录（2.0G）
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw
```

### 2. Git 配置
```bash
# 备份 git 配置和凭证
cp ~/.gitconfig ~/backup/
cp ~/.git-credentials ~/backup/  # 包含 GitHub token
```

### 3. 工作区（已备份到 GitHub）
- 仓库：https://github.com/David0Ming/agent-team
- 分支：master

## 恢复步骤

### 1. 安装系统依赖
```bash
# Node.js v22.22.0
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3
sudo apt-get install -y python3 python3-pip
```

### 2. 安装 OpenClaw
```bash
npm install -g openclaw
```

### 3. 恢复配置
```bash
# 解压备份
tar -xzf openclaw-backup-YYYYMMDD.tar.gz -C ~/

# 恢复 git 配置
cp backup/.gitconfig ~/
cp backup/.git-credentials ~/
chmod 600 ~/.git-credentials
```

### 4. 恢复工作区（可选，如果需要最新版本）
```bash
cd ~/.openclaw/workspace
git pull origin master
```

### 5. 启动 OpenClaw
```bash
openclaw gateway start
```

## 验证

```bash
# 检查状态
openclaw status

# 检查配置
openclaw config get

# 查看日志
openclaw logs --follow
```

## 重要文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 核心配置 | ~/.openclaw/openclaw.json | OpenClaw 配置 |
| 工作区 | ~/.openclaw/workspace/ | 项目和记忆 |
| Agent配置 | ~/.openclaw/agents/ | 各 agent 配置 |
| 环境变量 | ~/.openclaw/.env | API keys |
| Git凭证 | ~/.git-credentials | GitHub token |
| Git配置 | ~/.gitconfig | Git 用户信息 |

## 注意事项

1. **敏感信息**：.env 和 .git-credentials 包含敏感信息，妥善保管
2. **权限**：恢复后检查 ~/.git-credentials 权限为 600
3. **版本**：确保 Node.js 版本匹配（v22.22.0）
4. **插件**：extensions/ 目录包含所有插件，会自动恢复

---

**创建时间**：2026-03-10
**作者**：DJJ
