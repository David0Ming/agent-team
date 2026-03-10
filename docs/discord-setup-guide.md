# Discord 配置指南

## 前置准备

需要你手动完成以下步骤：

### 1. 创建 Discord Bot

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击 **New Application**，命名为 "OpenClaw"
3. 点击侧边栏 **Bot**，设置用户名
4. 启用 **Privileged Gateway Intents**：
   - ✅ Message Content Intent（必需）
   - ✅ Server Members Intent（推荐）
5. 点击 **Reset Token**，复制 Bot Token（保存好）

### 2. 添加 Bot 到服务器

1. 点击 **OAuth2** → **OAuth2 URL Generator**
2. 勾选权限：
   - `bot`
   - `applications.commands`
3. Bot Permissions 勾选：
   - View Channels
   - Send Messages
   - Read Message History
   - Embed Links
   - Attach Files
4. 复制生成的 URL，在浏览器打开，选择服务器，点击 **Continue**

### 3. 获取 ID

1. Discord 设置 → 高级 → 开启 **开发者模式**
2. 右键服务器图标 → **复制服务器 ID**
3. 右键你的头像 → **复制用户 ID**

### 4. 配置 OpenClaw

```bash
# 设置 Bot Token（替换 YOUR_BOT_TOKEN）
openclaw config set channels.discord.token '"YOUR_BOT_TOKEN"' --json
openclaw config set channels.discord.enabled true --json

# 重启 Gateway
openclaw gateway restart
```

### 5. 配对

1. 在 Discord 私信你的 Bot
2. Bot 会回复配对码
3. 批准配对：
```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

## 完成后

配对成功后，你就可以在 Discord 上和 OpenClaw 对话了。

---

**当前状态**：等待你提供 Bot Token 和 ID
