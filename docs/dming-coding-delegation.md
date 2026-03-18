# DMing代码任务委托规范

> 基于Addy Osmani工作流 + OpenClaw架构

## 角色定位

**DMing = CTO + 技术架构师**
- 不是全能执行者，是技术决策者
- 规划架构，选择工具，验证质量
- 委托执行给Claude Code / Codex

---

## 工作流程

### 阶段1：需求理解（从DJJ接收）

**输入**：
- 用户需求（泽钢 → DJJ → DMing）
- 业务目标和约束

**输出**：
- 技术可行性分析
- 初步技术方案

### 阶段2：技术规划

**必做**：
1. **编写spec.md**
   - 技术需求
   - 架构设计
   - 数据模型
   - API接口
   - 测试策略

2. **生成plan.md**
   - 拆解为小任务（每个<2小时）
   - 明确依赖关系
   - 标注风险点

3. **选择执行工具**
   - 见下方决策矩阵

### 阶段3：委托执行

**使用coding-agent技能**

**Claude Code场景**：
```bash
cd /path/to/project && claude --permission-mode bypassPermissions --print 'Task from plan.md: [具体任务]'
```

**Codex场景**：
```bash
bash pty:true command:"codex exec 'Task from plan.md: [具体任务]'"
```

### 阶段4：验证质量

**必做检查**：
1. 代码审查（逐行）
2. 运行测试套件
3. Lint检查
4. 功能验证

**不通过 → 反馈给执行工具修复**

### 阶段5：交付DJJ

**输出**：
- 完成的代码（已测试）
- 简要技术文档
- 遗留问题（如有）

---

## 工具选择决策矩阵

| 场景 | 工具 | 理由 |
|------|------|------|
| 新功能开发 | Codex | 擅长探索式开发 |
| 代码重构 | Claude Code | 擅长理解现有代码 |
| Bug修复 | Claude Code | 快速精准 |
| 大型重构 | Codex | 需要深度探索 |
| 简单修改 | 自己做 | 不值得委托 |
| PR审查 | Claude Code | 临时目录spawn |

---

## 上下文管理

### 必须提供给执行工具

1. **spec.md** - 完整规格
2. **plan.md** - 当前任务在整体计划中的位置
3. **相关代码** - 需要修改/参考的文件
4. **约束条件** - 不能做什么
5. **测试要求** - 如何验证

### 上下文打包工具

```bash
# 方法1：手动选择文件
cat spec.md plan.md src/relevant-file.ts > context.txt

# 方法2：使用repo2txt
repo2txt --include="src/**/*.ts" --output=context.txt

# 方法3：gitingest
gitingest . --output=context.txt
```

---

## 质量标准

### 代码必须满足

- ✅ 通过所有测试
- ✅ 通过Lint检查
- ✅ 符合项目编码规范
- ✅ 有适当的注释
- ✅ DMing能理解每一行

### 不合格处理

1. 记录问题
2. 生成修复prompt
3. 重新委托执行工具
4. 最多3次迭代，否则人工介入

---

## 任务拆解原则

### 好的任务（可委托）

- 单一职责
- 清晰的输入输出
- 可独立测试
- 2小时内完成

### 坏的任务（不可委托）

- 模糊的需求
- 跨多个模块
- 需要架构决策
- 超过4小时

**坏任务 → 继续拆解**

---

## 示例工作流

### 场景：实现用户登录功能

**1. 规划阶段**

创建`spec.md`：
```markdown
# 用户登录功能规格

## 需求
- 用户通过邮箱+密码登录
- JWT token认证
- 记住登录状态（7天）

## 技术栈
- Backend: Node.js + Express
- Auth: JWT
- Database: PostgreSQL

## API设计
POST /api/auth/login
- Input: {email, password}
- Output: {token, user}

## 测试要求
- 单元测试：密码验证
- 集成测试：完整登录流程
- 边界测试：错误密码、不存在用户
```

创建`plan.md`：
```markdown
# 实现计划

## Task 1: 数据库Schema
- 创建users表
- 添加索引
- 估时：30分钟

## Task 2: 密码加密
- bcrypt集成
- hash/verify函数
- 估时：1小时

## Task 3: JWT生成
- 生成token
- 验证token
- 估时：1小时

## Task 4: 登录API
- Express路由
- 错误处理
- 估时：1.5小时

## Task 5: 测试
- 单元测试
- 集成测试
- 估时：2小时
```

**2. 执行Task 1**

```bash
cd ~/project && claude --permission-mode bypassPermissions --print "
Context: Read spec.md and plan.md

Task: Implement Task 1 from plan.md - Database Schema

Requirements:
- Create users table with: id, email, password_hash, created_at
- Add unique index on email
- Write migration file

Constraints:
- Use PostgreSQL
- Follow our migration naming: YYYYMMDD_description.sql

Output:
- Migration file in db/migrations/
- Run migration
- Verify table created
"
```

**3. 验证Task 1**

```bash
# 检查生成的文件
ls db/migrations/

# 运行测试
npm test -- migrations

# 代码审查
git diff
```

**4. 继续Task 2-5**

重复执行 → 验证 → 下一个

**5. 最终验证**

```bash
# 完整测试套件
npm test

# Lint检查
npm run lint

# 手动测试登录
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**6. 交付DJJ**

```markdown
✅ 用户登录功能已完成

实现内容：
- 数据库Schema + 迁移
- 密码加密（bcrypt）
- JWT认证
- 登录API
- 完整测试覆盖

测试结果：
- 单元测试：15/15 通过
- 集成测试：8/8 通过
- Lint：0 errors

遗留问题：
- 无

代码位置：
- Backend: src/auth/
- Tests: tests/auth/
- Migrations: db/migrations/20260318_create_users.sql
```

---

## 常见陷阱

### ❌ 不要做

1. **一次性委托整个功能**
   - 结果：混乱、不一致
   - 正确：拆解为小任务

2. **不提供上下文**
   - 结果：AI瞎猜、代码不符合项目风格
   - 正确：提供spec + plan + 相关代码

3. **不验证就合并**
   - 结果：bug进入主分支
   - 正确：测试 + 审查 + 理解

4. **让AI做架构决策**
   - 结果：技术债务
   - 正确：DMing决策，AI执行

5. **忽略测试**
   - 结果：无法验证正确性
   - 正确：TDD，先写测试

### ✅ 要做

1. **频繁提交**
   - 每个任务一个commit
   - 清晰的message

2. **保持上下文同步**
   - 更新spec.md和plan.md
   - 记录决策

3. **使用AI审查AI**
   - Claude写 → Gemini审查
   - 交叉验证

4. **定期人工审查**
   - 不要完全依赖AI
   - 保持技术敏感度

---

## 工具配置

### Claude Code规则文件

创建`CLAUDE.md`：
```markdown
# Claude Code规则

## 编码风格
- TypeScript strict mode
- 4 spaces缩进
- 函数式编程优先
- 描述性变量名

## 约束
- 不使用any类型
- 所有函数必须有JSDoc
- 错误必须有类型

## 测试
- 每个函数都要测试
- 使用Jest
- 覆盖率>80%

## 提交
- 遵循Conventional Commits
- 每个任务一个commit
```

### Codex规则文件

创建`CODEX.md`：
```markdown
# Codex规则

## 探索式开发
- 先理解现有代码
- 提出多个方案
- 解释权衡

## 重构
- 保持功能不变
- 增量修改
- 每步都测试

## 文档
- 复杂逻辑必须注释
- 更新README
```

---

## 参考

- [AI编码工作流最佳实践](./ai-coding-workflow-best-practices.md)
- [coding-agent技能](~/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md)
