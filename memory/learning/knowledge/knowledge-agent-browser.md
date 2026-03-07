# agent-browser - 浏览器自动化工具

**学习时间**: 2026-03-07  
**来源**: Vercel Labs  
**类型**: 工具/技能

---

## 1️⃣ 复述：这是什么？

agent-browser是专门为AI agents设计的浏览器自动化CLI工具。

**核心工作流程**：
```
open → snapshot -i → interact → re-snapshot
```

**关键特性**：
- **元素引用系统**：用@e1, @e2引用元素，避免复杂CSS选择器
- **认证保险库**：加密保存登录凭证
- **会话持久化**：保存登录状态，避免重复登录
- **安全特性**：内容边界、域名白名单、操作策略
- **移动测试**：支持iOS设备模拟

---

## 2️⃣ 应用：我们哪里可以用？

### 场景1：嘟嘟巴士竞品监控
**当前问题**：需要抓取小红书/抖音竞品数据，可能需要登录  
**解决方案**：
```bash
# 保存登录凭证
agent-browser auth save xiaohongshu --url https://xiaohongshu.com/login --username user

# 自动登录并抓取
agent-browser auth login xiaohongshu
agent-browser open "https://xiaohongshu.com/user/xiaojiang_bus"
agent-browser snapshot -i
agent-browser get text @e1  # 获取视频标题
agent-browser screenshot --full  # 截图保存
```

### 场景2：飞书权限配置（P1任务）
**当前问题**：需要配置飞书应用权限，可能需要网页操作  
**解决方案**：用agent-browser自动化配置流程

### 场景3：学习资源获取
**当前问题**：需要搜索和下载学习视频  
**解决方案**：自动化搜索、筛选、下载流程

---

## 3️⃣ 时机：什么时候使用？

### ✅ 适合使用的场景
- 需要与网页交互（点击、填表、滚动）
- 需要处理需要登录的页面
- 需要保存会话状态（避免重复登录）
- 需要截图或生成PDF
- 需要处理动态加载的内容（等待网络空闲）
- web_fetch不够用时（无法处理JavaScript渲染）

### ❌ 不适合的场景
- 简单的静态页面抓取（用web_fetch更快）
- 有API可用时（API更稳定、更快）
- 不需要交互的页面

---

## 4️⃣ 验证：核心命令

### 基础流程
```bash
# 1. 打开网页
agent-browser open https://example.com

# 2. 获取可交互元素（带引用@e1, @e2...）
agent-browser snapshot -i

# 3. 交互
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser select @e3 "option"

# 4. 等待加载
agent-browser wait --load networkidle

# 5. 重新获取快照（页面变化后必须重新snapshot）
agent-browser snapshot -i

# 6. 关闭
agent-browser close
```

### 认证和会话
```bash
# 保存登录凭证（加密）
echo "password" | agent-browser auth save mysite --url https://example.com/login --username user --password-stdin

# 使用保存的凭证登录
agent-browser auth login mysite

# 保存会话状态
agent-browser state save session.json

# 加载会话状态
agent-browser state load session.json
```

### 安全特性
```bash
# 内容边界（标记不可信内容）
export AGENT_BROWSER_CONTENT_BOUNDARIES=1

# 域名白名单
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
```

---

## 5️⃣ 记忆：关键要点

1. **元素引用会失效**：页面变化后必须重新snapshot
2. **会话管理**：用auth save/login或state save/load避免重复登录
3. **安全第一**：使用域名白名单和内容边界
4. **等待加载**：用`wait --load networkidle`确保页面完全加载
5. **命令链**：可以用`&&`连接多个命令

---

## 📚 资源

- GitHub: https://github.com/vercel-labs/agent-browser
- 文档: https://skills.sh/vercel-labs/agent-browser/agent-browser
- 安装: `npm install -g agent-browser`

---

## 🎯 下一步行动

1. **安装工具**：`npm install -g agent-browser`
2. **测试基础流程**：打开一个简单网页，测试snapshot和click
3. **应用到竞品监控**：改进嘟嘟巴士的竞品数据抓取
4. **集成到run_daily.py**：自动化竞品监控流程
