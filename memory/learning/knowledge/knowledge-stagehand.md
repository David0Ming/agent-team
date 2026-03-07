# 知识卡片：Stagehand 浏览器自动化

## 来源
- **标题**: Stagehand革命性AI浏览器自动化框架
- **链接**: https://www.aivi.fyi/aiagents/introduce-stagehand
- **作者**: AI超元域
- **学习时间**: 2026-03-05

---

## 1️⃣ 复述

**Stagehand** 是 Browserbase 推出的 AI 浏览器自动化框架，结合 Playwright + AI。

**核心理念**: 在可控性和智能性之间找到平衡

**三大核心能力**:

1. **act()** - 自然语言执行操作
```python
await page.act("点击登录按钮")
await page.act("在搜索框输入'iPhone 15'")
```

2. **extract()** - 结构化提取数据
```python
result = await page.extract({
    instruction: "提取商品价格和库存",
    schema: z.object({price: z.number(), stock: z.string()})
})
```

3. **observe()** - 预览和缓存 AI 操作

**优势**:
- 生产级可靠（不像 Browser-Use 那么不可预测）
- 基于 Playwright，上手零门槛
- 智能缓存节省成本
- 支持本地 + 云端浏览器

**安装**:
```bash
pip install stagehand python-dotenv
```

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 表单自动填写
2. ✅ 电商价格监控
3. ✅ 自动化测试

---

## 3️⃣ 验证

1. Stagehand vs Chrome DevTools MCP 哪个好？
2. 和 OpenClaw 的 browser 工具对比？
3. 实际稳定性如何？

---

## 4️⃣ 记忆

- **act**: 自然语言操作
- **extract**: 结构化提取
- **observe**: 预览缓存
- **平衡**: 精确控制 + 智能处理

---

## 5️⃣ 用起来

**下一步**:
- [ ] 测试 Stagehand
- [ ] 对比不同浏览器自动化工具
