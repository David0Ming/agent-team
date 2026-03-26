# 嵌入式客户端模式研究

## 研究时间
2026-03-18 09:16

## DeerFlow的实现

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()

# Chat
response = client.chat("Analyze this paper", thread_id="my-thread")

# Streaming
for event in client.stream("hello"):
    if event.type == "messages-tuple":
        print(event.data["content"])

# Management
models = client.list_models()
skills = client.list_skills()
client.upload_files("thread-1", ["./report.pdf"])
```

**特点**：
- 进程内调用，无需HTTP
- 返回Gateway对齐的dict
- 支持流式和同步模式

## OpenClaw当前状态

### ✅ 已有的接口

**1. CLI工具**：
```bash
openclaw sessions          # 列出会话
openclaw sessions cleanup  # 清理会话
```

**2. Gateway HTTP API**：
- 端口：18789
- 需要token认证
- 支持WebSocket

**3. 第三方SDK**：
- Fast.io OpenClaw SDK
- Apify OpenClaw Assistant

### ❌ 缺少的功能

**官方Python客户端库**：
- 无法像DeerFlow那样进程内调用
- 必须通过HTTP或CLI

## 可行性分析

### 方案1：HTTP客户端封装（简单）

**实现**：
```python
import requests

class OpenClawClient:
    def __init__(self, base_url="http://localhost:18789", token=None):
        self.base_url = base_url
        self.token = token
    
    def chat(self, message, agent="main"):
        # 调用Gateway HTTP API
        pass
```

**优点**：
- 实现简单，几百行代码
- 不需要修改OpenClaw核心
- 可以立即使用

**缺点**：
- 仍需Gateway运行
- 有HTTP开销
- 不是真正的"嵌入式"

### 方案2：直接导入OpenClaw模块（复杂）

**实现**：
```python
# 类似DeerFlow的做法
from openclaw.core import Agent
from openclaw.gateway import Gateway

client = Agent(config="config.yaml")
response = client.chat("hello")
```

**优点**：
- 真正的进程内调用
- 零HTTP开销
- 完全控制

**缺点**：
- 需要OpenClaw重构（暴露Python API）
- OpenClaw是TypeScript写的，不是Python
- 工作量巨大

### 方案3：使用现有的sessions工具（实用）

**实现**：
```python
import subprocess
import json

def openclaw_chat(message, agent="main"):
    # 通过CLI调用
    result = subprocess.run(
        ["openclaw", "chat", message, "--agent", agent, "--json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)
```

**优点**：
- 利用现有CLI
- 无需额外开发
- 稳定可靠

**缺点**：
- 每次调用启动新进程
- 性能较差
- 不支持流式

## 结论与建议

### 短期（1-2周）：方案1 - HTTP客户端封装
创建简单的Python wrapper：
```python
# openclaw_client.py
class OpenClawClient:
    def chat(self, message): ...
    def list_models(self): ...
    def list_skills(self): ...
```

**理由**：
- 快速实现
- 满足基本需求
- 为长期方案积累经验

### 长期（3-6个月）：推动官方Python SDK
- 向OpenClaw社区提议
- 参考DeerFlow的实现
- 贡献代码

### 当前优先级：低
**原因**：
- 我们主要通过CLI/Web使用OpenClaw
- 没有紧急的编程集成需求
- 其他优化（记忆架构）更重要

**建议**：
- 标记为"长期待办"
- 先完成其他高优先级任务
- 有具体需求时再实施

