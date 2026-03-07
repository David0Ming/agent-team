# Tavily Search vs 已有Search技能对比

**学习时间**: 2026-03-07  
**类型**: 技术/工具对比

---

## 1️⃣ 复述：Tavily是什么？

**Tavily**是专门为AI agents设计的搜索API，提供结构化、AI优化的搜索结果。

**核心特点**：
- 为LLM优化的搜索结果
- 结构化JSON输出
- 自动内容提取和清洗
- 支持深度研究模式

---

## 2️⃣ 应用：对比已有的Search功能

### OpenClaw内置web_search（Brave Search API）

**特点**：
- 通用搜索引擎
- 返回标准搜索结果（标题、URL、snippet）
- 需要手动提取和处理内容
- 适合快速查找信息

**使用场景**：
```python
web_search(query="OpenClaw features", count=5)
# 返回：标题、URL、摘要片段
```

### Tavily Search API

**特点**：
- **AI优化输出**：返回格式专门为LLM设计
- **自动内容提取**：自动抓取网页核心内容，去除广告
- **相关性评分**：每个结果带有相关性分数
- **深度搜索模式**：可以进行多步follow-up查询
- **实时性**：支持实时搜索最新信息

**使用场景**：
```python
tavily_search(query="OpenClaw features", search_depth="advanced")
# 返回：
# - 标题
# - URL
# - 完整内容（已清洗）
# - 相关性评分
# - 发布时间
```

---

## 3️⃣ 时机：什么时候用哪个？

### ✅ 用Tavily的场景
- **深度研究**：需要详细了解某个主题
- **内容提取**：需要获取网页完整内容
- **AI处理**：结果需要被AI进一步分析
- **多步查询**：需要基于第一次结果继续搜索
- **质量优先**：需要高质量、高相关性的结果

### ✅ 用Brave Search的场景
- **快速查找**：只需要标题和链接
- **简单搜索**：不需要深度内容
- **成本敏感**：Brave可能更便宜
- **已有集成**：OpenClaw已内置，无需额外配置

---

## 4️⃣ 验证：核心区别

| 特性 | Brave Search (web_search) | Tavily Search |
|------|---------------------------|---------------|
| **输出格式** | 标准搜索结果 | AI优化JSON |
| **内容提取** | 需要手动 | 自动提取 |
| **相关性评分** | 无 | 有 |
| **深度搜索** | 单次查询 | 支持多步 |
| **内容清洗** | 无 | 自动去广告 |
| **实时性** | 一般 | 强 |
| **成本** | 较低 | 较高 |
| **集成难度** | 已内置 | 需要配置 |

---

## 5️⃣ 记忆：关键要点

1. **Tavily = AI专用搜索**：专门为LLM设计，输出更适合AI处理
2. **自动内容提取**：Tavily自动抓取和清洗网页内容
3. **深度研究模式**：支持多步follow-up查询
4. **成本vs质量**：Tavily质量更高但成本也更高
5. **使用场景不同**：快速查找用Brave，深度研究用Tavily

---

## 📚 应用示例

### 示例1：快速查找（用Brave）
```python
# 场景：快速找到OpenClaw文档链接
web_search(query="OpenClaw documentation", count=3)
# 输出：标题、URL、简短摘要
# 优势：快速、简单、成本低
```

### 示例2：深度研究（用Tavily）
```python
# 场景：研究竞品的完整功能和用户评价
tavily_search(
    query="小江巴士 用户评价 服务质量",
    search_depth="advanced",
    max_results=10
)
# 输出：
# - 完整文章内容（已清洗）
# - 相关性评分
# - 发布时间
# - 自动follow-up相关查询
# 优势：内容完整、质量高、适合AI分析
```

### 示例3：竞品监控（推荐Tavily）
```python
# 场景：监控竞品最新动态
tavily_search(
    query="小江巴士 最新视频 2026",
    search_depth="basic",
    include_domains=["xiaohongshu.com", "douyin.com"]
)
# 优势：实时性强、内容完整、自动提取
```

---

## 🎯 下一步行动

1. **评估需求**：我们的搜索场景是快速查找还是深度研究？
2. **成本分析**：Tavily的成本是否可接受？
3. **集成测试**：如果需要Tavily，配置API key并测试
4. **应用到竞品监控**：考虑用Tavily改进竞品数据抓取

---

## ⚠️ 当前状态

- **Tavily技能安装失败**：skills.sh上的tavily技能缺少有效SKILL.md
- **web_search不可用**：缺少Brave API key
- **建议**：如果需要搜索功能，优先配置Brave API key（成本更低）
