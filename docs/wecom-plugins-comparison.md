# 企业微信OpenClaw插件对比

> 基于2026-03-18搜索结果

## 可用插件列表

### 1. @wecom/wecom-openclaw-plugin ⭐推荐

**维护者**：腾讯企业微信官方团队（Tencent WeCom Team）

**NPM地址**：https://www.npmjs.com/package/@wecom/wecom-openclaw-plugin

**GitHub**：https://github.com/WecomTeam/wecom-openclaw-plugin

**最新版本**：1.0.11（1天前更新）

**优势**：
- ✅ 官方维护，稳定可靠
- ✅ 持续更新（最近1天前）
- ✅ 官方支持，问题响应快
- ✅ 与企业微信API同步更新

**安装**：
```bash
npm i @wecom/wecom-openclaw-plugin
```

**配置示例**：
```json
{
  "channels": {
    "wecom": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["group_id_1", "group_id_2"]
    }
  }
}
```

---

### 2. @sunnoy/wecom

**维护者**：社区开发者 sunnoy

**GitHub**：https://github.com/sunnoy/openclaw-plugin-wecom

**特色功能**：
- 🌊 流式输出（Streaming）
- 🤖 动态Agent管理（每个用户/群独立Agent）
- 👥 群聊深度集成
- 🔐 指令白名单

**优势**：
- ✅ 功能丰富
- ✅ 支持流式打字效果
- ✅ 独立Agent隔离

**劣势**：
- ⚠️ 社区维护，非官方
- ⚠️ 有依赖问题报告（qrcode-terminal）
- ⚠️ 稳定性未知

**安装**：
```bash
# 如果已安装官方插件，需先卸载
openclaw plugins uninstall wecom-openclaw-plugin

# 安装社区插件
openclaw plugins install @sunnoy/wecom
```

---

### 3. BytePioneer-AI/openclaw-china

**维护者**：BytePioneer-AI

**GitHub**：https://github.com/BytePioneer-AI/openclaw-china

**特点**：
- 📦 中国插件集合包
- 支持：飞书、钉钉、QQ、企业微信、微信

**优势**：
- ✅ 一站式中国平台支持
- ✅ 统一配置管理

**劣势**：
- ⚠️ 集成包，可能过于臃肿
- ⚠️ 更新频率未知

---

## 对比总结

| 维度 | 官方插件 | sunnoy社区版 | openclaw-china |
|------|---------|-------------|----------------|
| 维护者 | 腾讯官方 | 社区 | 社区 |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 更新频率 | 高（1天前） | 中 | 未知 |
| 功能丰富度 | 标准 | 丰富 | 标准 |
| 流式输出 | ✅ | ✅ | ✅ |
| 独立Agent | ❓ | ✅ | ❓ |
| 官方支持 | ✅ | ❌ | ❌ |
| 依赖问题 | 无 | 有报告 | 未知 |

---

## 推荐方案

### 方案1：官方插件（推荐）⭐

**适合**：
- 追求稳定性
- 需要官方支持
- 生产环境使用

**安装**：
```bash
npm i @wecom/wecom-openclaw-plugin
```

### 方案2：社区增强版

**适合**：
- 需要高级功能（独立Agent、流式输出）
- 愿意承担一定风险
- 测试环境使用

**安装**：
```bash
openclaw plugins install @sunnoy/wecom
```

---

## 建议

**我的推荐**：使用官方插件 `@wecom/wecom-openclaw-plugin`

**理由**：
1. 腾讯官方维护，稳定可靠
2. 持续更新（1天前刚更新）
3. 与企业微信API同步
4. 无依赖问题
5. 官方支持渠道

**如果需要高级功能**：
- 可以先用官方插件验证连通性
- 稳定后再考虑社区增强版

---

**创建时间**：2026-03-18
**作者**：DJJ
