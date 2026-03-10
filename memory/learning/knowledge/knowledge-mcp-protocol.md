# MCP（Model Context Protocol）- AI界的USB

## 📚 知识来源
- 官方规范：https://modelcontextprotocol.io/specification/2025-11-25
- 学习时间：2026-03-07 15:15

## 1️⃣ 复述：MCP是什么

**核心定义**：MCP是一个开放协议，让LLM应用与外部数据源和工具无缝集成。

**类比**：
- LSP（Language Server Protocol）标准化了编程语言支持
- MCP标准化了AI应用的上下文和工具集成
- 就像USB：一个接口，多个设备

**架构**：
```
Host (LLM应用，如Claude Desktop)
  ↓
Client (连接器)
  ↓
Server (提供上下文和能力)
```

## 2️⃣ 应用：MCP的3+3能力

### Server提供给Client：
1. **Resources** - 上下文和数据（供用户或AI使用）
2. **Prompts** - 模板消息和工作流
3. **Tools** - AI可执行的函数

### Client提供给Server：
1. **Sampling** - Server发起的递归LLM交互
2. **Roots** - URI/文件系统边界查询
3. **Elicitation** - 向用户请求额外信息

## 3️⃣ 时机：何时使用MCP

**适合场景**：
- 构建AI工具生态（多个工具，一个协议）
- 需要标准化集成（避免每个AI都写一遍）
- 社区贡献工具（发布MCP Server）

**我们的应用**：
- ✅ 已使用：OpenClaw支持MCP服务器
- 💡 可做：将我们的技能发布为MCP Server
- 💡 可做：连接更多MCP Server（如Brave Search、GitHub等）

## 4️⃣ 验证：安全原则

MCP的4个安全原则：
1. **用户同意和控制** - 用户必须明确同意所有数据访问和操作
2. **数据隐私** - Host必须获得用户同意才能暴露数据
3. **工具安全** - 工具=任意代码执行，必须获得用户同意
4. **LLM采样控制** - 用户必须批准采样请求

**测试问题**：
- Q: MCP与直接API调用的区别？
- A: MCP提供标准化协议，一次实现，多个AI使用；API需要每个AI单独集成

## 5️⃣ 记忆：关键要点

**记住这3点**：
1. MCP = AI界的USB（标准化接口）
2. Server提供Resources/Prompts/Tools，Client提供Sampling/Roots/Elicitation
3. 安全第一：用户同意、数据隐私、工具安全

## 6️⃣ 用起来：实践方向

**立即可做**：
- 探索OpenClaw的MCP配置（mcp.json）
- 测试现有MCP服务器

**下周可做**：
- 将我们的技能包装为MCP Server
- 连接更多MCP Server

---

**学习时间**：2026-03-07 15:15-15:20
**掌握程度**：理论理解 ✅ | 实践应用 ⏳
