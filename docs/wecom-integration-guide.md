# 企业微信接入OpenClaw指南

> 基于企业微信官方智能机器人长连接API

## 核心信息

**官方文档**：https://developer.work.weixin.qq.com/document/path/101463

**连接方式**：WebSocket长连接（推荐）
- 地址：`wss://openws.work.weixin.qq.com`
- 优势：无需公网IP、低延迟、无需加解密

**官方SDK**：
- Node.js: [@wecom/aibot-node-sdk](https://www.npmjs.com/package/@wecom/aibot-node-sdk)
- Python: [aibot-python-sdk](https://dldir1.qq.com/wework/wwopen/bot/aibot-python-sdk-1.0.0.zip)

---

## 接入步骤

### 1. 获取凭证

在企业微信管理后台：
1. 进入智能机器人配置页面
2. 开启「API模式」
3. 选择「长连接」方式
4. 获取凭证：
   - **BotID**：机器人唯一标识
   - **Secret**：长连接专用密钥

⚠️ 注意：切换模式会导致现有连接失效

### 2. 安装SDK

```bash
# Node.js版本（推荐）
npm install -g @wecom/aibot-node-sdk

# 或Python版本
# 下载并解压aibot-python-sdk-1.0.0.zip
```

### 3. 连接流程

```
1. 建立WebSocket连接
   ↓
2. 发送订阅请求（aibot_subscribe）
   - 使用BotID + Secret认证
   ↓
3. 接收消息/事件回调
   ↓
4. 回复消息
   ↓
5. 保持心跳（每30秒）
```

---

## 支持的功能

### 接收消息类型
- ✅ 文本消息
- ✅ 图片消息（仅单聊）
- ✅ 图文混排
- ✅ 语音消息（仅单聊）
- ✅ 文件消息（仅单聊）
- ✅ 视频消息（仅单聊）

### 接收事件类型
- ✅ 进入会话事件（可回复欢迎语）
- ✅ 模板卡片点击事件
- ✅ 用户反馈事件
- ✅ 连接断开事件

### 发送消息类型
- ✅ 文本消息
- ✅ Markdown消息
- ✅ 模板卡片
- ✅ 流式消息
- ✅ 文件/图片/语音/视频

### 特殊功能
- ✅ 主动推送消息（无需用户触发）
- ✅ 流式消息（类似ChatGPT打字效果）
- ✅ 模板卡片交互

---

## 频率限制

- 单个会话：30条/分钟，1000条/小时
- 上传素材：30次/分钟，1000次/小时
- 连接数量：每个机器人同时只能1个连接

---

## 关键API

### 1. 订阅请求
```json
{
  "cmd": "aibot_subscribe",
  "headers": {"req_id": "REQUEST_ID"},
  "body": {
    "bot_id": "BOTID",
    "secret": "SECRET"
  }
}
```

### 2. 接收消息回调
```json
{
  "cmd": "aibot_msg_callback",
  "headers": {"req_id": "REQUEST_ID"},
  "body": {
    "msgid": "MSGID",
    "chattype": "single",  // single单聊 / group群聊
    "from": {"userid": "USERID"},
    "msgtype": "text",
    "text": {"content": "hello"}
  }
}
```

### 3. 回复消息
```json
{
  "cmd": "aibot_respond_msg",
  "headers": {"req_id": "REQUEST_ID"},  // 透传回调的req_id
  "body": {
    "msgtype": "markdown",
    "markdown": {"content": "**回复内容**"}
  }
}
```

### 4. 主动推送消息
```json
{
  "cmd": "aibot_send_msg",
  "headers": {"req_id": "REQUEST_ID"},
  "body": {
    "chatid": "USERID_OR_CHATID",
    "chat_type": 1,  // 1单聊 / 2群聊
    "msgtype": "markdown",
    "markdown": {"content": "主动推送"}
  }
}
```

### 5. 心跳
```json
{
  "cmd": "ping",
  "headers": {"req_id": "REQUEST_ID"}
}
```

---

## 实现方案

### 方案1：直接使用官方SDK（推荐）

**优势**：
- 官方维护，稳定可靠
- 自动处理心跳、重连
- 开箱即用

**步骤**：
1. 安装SDK
2. 创建OpenClaw插件封装SDK
3. 配置BotID和Secret

### 方案2：自己实现WebSocket客户端

**优势**：
- 完全控制
- 可定制化

**劣势**：
- 需要处理心跳、重连、错误
- 开发工作量大

**推荐使用方案1**

---

## 下一步行动

1. **获取凭证**：
   - 登录企业微信管理后台
   - 配置智能机器人
   - 获取BotID和Secret

2. **创建OpenClaw插件**：
   - 基于官方Node.js SDK
   - 封装为OpenClaw插件
   - 类似飞书插件的架构

3. **测试连接**：
   - 建立WebSocket连接
   - 测试收发消息
   - 验证主动推送

---

## 参考资料

- [企业微信智能机器人长连接文档](https://developer.work.weixin.qq.com/document/path/101463)
- [Node.js SDK](https://www.npmjs.com/package/@wecom/aibot-node-sdk)
- [企业微信开发者中心](https://developer.work.weixin.qq.com/)

---

**创建时间**：2026-03-18
**作者**：DJJ
