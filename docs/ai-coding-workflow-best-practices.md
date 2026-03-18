# AI编码工作流最佳实践

> 基于Addy Osmani（Google Chrome工程师）2026年工作流

## 核心原则

**AI是强大的配对程序员，需要明确指导、上下文和监督，而不是自主判断。**

---

## 1. 先规划，后编码（Specs Before Code）

### 为什么
不要直接扔需求给AI，先定义问题和解决方案。

### 怎么做
1. **头脑风暴规格**：与AI迭代讨论，直到需求和边界清晰
2. **编写spec.md**：包含需求、架构决策、数据模型、测试策略
3. **生成项目计划**：用推理模型将spec拆解为逻辑任务
4. **迭代优化计划**：编辑并让AI批评/改进，直到连贯完整
5. **然后才开始编码**

### 关键引用
> "It's like doing a waterfall in 15 minutes" - 快速结构化规划让后续编码更顺畅

---

## 2. 小块迭代（Small Iterative Chunks）

### 为什么
避免让AI一次生成大量代码，会导致混乱和不一致。

### 怎么做
- 将项目拆解为小任务/票据
- 一次实现一个功能、修复一个bug
- 每个块足够小，AI能在上下文内处理
- 完成一块 → 测试 → 下一块

### 反面案例
> "Like 10 devs worked on it without talking to each other" - 一次性生成大量代码的后果

---

## 3. 提供充分上下文（Extensive Context）

### 为什么
AI只能和你提供的上下文一样好。

### 怎么做
- **代码上下文**：相关文件、API文档、技术约束
- **"脑内倾倒"**：高层目标、好的解决方案示例、要避免的方法
- **工具辅助**：
  - gitingest / repo2txt：打包代码库
  - Context7 MCP：自动上下文
- **明确指导**：用注释和规则引导AI

### 关键技巧
```
"Here is the current implementation of X. 
We need to extend it to do Y, 
but be careful not to break Z."
```

---

## 4. 选择合适的模型（Right Model）

### 原则
- 不同模型有不同"个性"
- 一个模型卡住时，换另一个
- 使用最新的"pro"级模型
- 可以并行尝试多个模型交叉验证

### Addy的选择
> "I gravitate towards Gemini for coding because the interaction feels more natural"

---

## 5. 人类在环（Human in the Loop）

### 核心规则
**永远不要盲目信任AI输出。**

### 怎么做
- **把AI当作过度自信的初级开发者**
- 阅读每一行AI生成的代码
- 运行测试验证功能
- 代码审查（手动+AI辅助）
- 只合并你理解的代码

### 测试驱动
- 规划阶段就生成测试列表
- 写代码 → 运行测试 → 修复 → 循环
- 强测试实践 = AI飞得更高

### AI审查AI
用第二个模型审查第一个的代码：
```
"Can you review this function for any errors or improvements?"
```

---

## 6. 频繁提交（Commit Often）

### 为什么
提交是"存档点"，让你能撤销AI的错误。

### 怎么做
- 每个小任务后立即提交
- 清晰的commit message
- 小提交便于定位问题
- 使用分支/worktree隔离AI实验

### 原则
> "Treat commits as save points in a game"

---

## 7. 自定义AI行为（Customize Behavior）

### 方法
1. **规则文件**：CLAUDE.md / GEMINI.md
   - 编码风格、lint规则、偏好模式
2. **系统指令**：全局配置AI行为
3. **示例引导**：展示期望的输出格式

### 示例规则
```markdown
- Use 4 spaces indent
- Avoid arrow functions in React
- Prefer descriptive variable names
- Code should pass ESLint
- If unsure, ask for clarification rather than making up an answer
```

---

## 8. 拥抱测试和自动化（Testing & Automation）

### 为什么
AI在有强自动化的环境中工作最好。

### 怎么做
- **CI/CD**：每次提交自动运行测试
- **Linter**：强制代码风格
- **反馈循环**：
  - AI写代码 → CI测试 → 失败日志 → AI修复 → 重复

### 效果
> "Like having an extremely fast junior dev whose work is instantly checked by a tireless QA engineer"

---

## 9. 持续学习（Continuous Learning）

### 关键洞察
**AI放大你的技能，不是替代。**

### 实践
- 审查AI代码时学习新模式
- 调试AI错误时加深理解
- 让AI解释其代码和理由
- 定期不用AI编码，保持原始技能

### 真相
> "AI rewards existing best practices" - 资深工程师用AI效果最好

---

## 总结：AI辅助工程 vs AI自动化工程

**我们的定位**：AI-Augmented Engineering

- AI是配对程序员，不是自主编码者
- 人类是高级开发者，AI加速执行
- 保持经典软件工程纪律
- 人类保持在环，指导方向

**关键心态**：
> "The developer + AI duo is far more powerful than either alone, 
> and the developer half of that duo has to hold up their end."

---

## 参考资料

- [Addy Osmani - My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [AI-Assisted Engineering Book (O'Reilly)](https://beyond.addy.ie/)
