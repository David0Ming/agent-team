# 文本总结 (Text Summarization)

**学习时间**: 2026-03-07  
**类型**: 技术/方法

---

## 1️⃣ 复述：这是什么？

文本总结是将长文本压缩为简短摘要的技术，保留核心信息。

**三种类型**：
1. **抽取式总结**：从原文中提取关键句子
2. **生成式总结**：用AI重新生成摘要（更自然）
3. **混合式总结**：结合抽取和生成

**四种风格**：
- **concise**：1-2句话核心要点
- **detailed**：详细总结，包含主要观点和细节
- **bullet**：要点列表形式
- **key_points**：提取3-5个关键要点

---

## 2️⃣ 应用：我们哪里可以用？

### 场景1：嘟嘟巴士竞品分析
**当前问题**：抓取的竞品数据（视频、评论）太长  
**解决方案**：自动总结竞品视频内容和用户评论

### 场景2：学习资源整理
**当前问题**：需要阅读大量论文和文章  
**解决方案**：快速总结论文摘要，提取关键观点

### 场景3：会议记录
**当前问题**：会议讨论内容冗长  
**解决方案**：自动生成会议纪要

### 场景4：日报/周报
**当前问题**：需要手动整理每日工作  
**解决方案**：从memory/YYYY-MM-DD.md自动生成日报

---

## 3️⃣ 时机：什么时候使用？

### ✅ 适合使用的场景
- 文本长度 > 500字
- 需要快速了解核心内容
- 需要提取关键信息
- 需要生成报告摘要
- 需要整理会议记录

### ❌ 不适合的场景
- 文本已经很简短（< 100字）
- 需要保留所有细节（如法律文件）
- 需要精确引用原文

---

## 4️⃣ 验证：实现方法

### 方法1：AI模型生成（推荐）
```python
# 构建提示词
prompt = f"请用1-2句话总结以下内容：\n\n{text}"
# 发给AI模型
summary = ai_model(prompt)
```

**优势**：质量高、灵活、支持多种风格  
**劣势**：需要API调用、有成本

### 方法2：抽取式总结
```python
# 使用Python库（如sumy）
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = LsaSummarizer()
summary = summarizer(parser.document, 3)  # 3句话
```

**优势**：快速、免费、离线  
**劣势**：质量一般、不够自然

### 我创建的工具
```bash
# 生成总结提示词
python3 summarize.py "长文本..."

# 总结文件
python3 summarize.py --file document.txt

# 指定风格
python3 summarize.py --style bullet "长文本..."
```

---

## 5️⃣ 记忆：关键要点

1. **生成式 > 抽取式**：AI生成的摘要更自然、更准确
2. **提示词很重要**：明确告诉AI要什么风格的总结
3. **长度控制**：指定句子数量或字数限制
4. **保留关键信息**：确保核心观点不丢失
5. **多次迭代**：如果第一次总结不满意，可以要求重新总结

---

## 📚 应用示例

### 示例1：总结竞品视频
```python
video_content = "小江巴士最新视频：介绍深中通道线路..."
prompt = f"请用要点列表总结这个视频的核心卖点：\n\n{video_content}"
# 输出：
# - 深中通道1小时直达
# - 票价29元起
# - 舒适座椅
```

### 示例2：生成日报
```python
daily_log = open("memory/2026-03-07.md").read()
prompt = f"请总结今天完成的主要工作（3-5个要点）：\n\n{daily_log}"
# 输出：
# 1. 研究agent-browser skill
# 2. 改进竞品监控为自动化
# 3. 研究文本总结功能
```

---

## 🎯 下一步行动

1. **应用到竞品分析**：总结抓取的竞品视频内容
2. **应用到日报生成**：自动从daily log生成日报
3. **集成到工作流**：在需要的地方添加自动总结
