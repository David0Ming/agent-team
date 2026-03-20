# imap-smtp-email 增强功能测试

## 功能1：多账户支持 ✓

**实现文件**：
- `accounts.json.example` - 多账户配置示例
- `scripts/filter.js` - 支持读取多账户配置
- `scripts/summary.js` - 支持读取多账户配置

**配置格式**：
```json
{
  "accounts": [
    {
      "name": "账户名称",
      "imap": { "host": "...", "port": 993, "user": "...", "pass": "...", "tls": true },
      "smtp": { "host": "...", "port": 587, "secure": false, "user": "...", "pass": "...", "from": "..." }
    }
  ]
}
```

**使用方式**：
- 创建 `accounts.json` 文件（参考 `accounts.json.example`）
- 所有脚本自动检测并使用多账户配置
- 如果不存在 `accounts.json`，回退到 `.env` 单账户模式

## 功能2：智能过滤 ✓

**实现文件**：`scripts/filter.js`

**关键词分类**：
- 面试类：面试, interview, 面谈
- 简历类：简历, resume, 投递, cv
- 笔试类：笔试, test, assessment, 测评
- Offer类：offer, 录用, 入职, onboard
- 其他：不匹配以上关键词的邮件

**使用命令**：
```bash
# 检查所有账户
node scripts/filter.js

# 检查特定账户
node scripts/filter.js --account=qq-main

# 检查最近3天
node scripts/filter.js --days=3
```

**输出格式**：
- Markdown格式
- 按类别分组
- 显示：主题、发件人、时间、账户

## 功能3：邮件摘要与待办生成 ✓

**实现文件**：`scripts/summary.js`

**功能**：
1. 生成每日邮件摘要文件：`memory/daily/email-summary-YYYY-MM-DD.md`
2. 自动检测面试/笔试/学习活动邮件
3. 提取时间信息（支持多种格式）
4. 自动写入 `memory/projects.md` 对应分类：
   - 面试/笔试 → 工作代办
   - 学习活动 → 学习代办

**使用命令**：
```bash
node scripts/summary.js
```

**时间提取支持**：
- `12月25日 14:30`
- `2026-03-18 14:30`
- `3/18 14:30`

## 验证状态

✓ 语法检查通过（filter.js, summary.js）
✓ 文档已更新（SKILL.md）
✓ 配置示例已创建（accounts.json.example）
✓ 脚本可执行权限已设置

## 下一步

1. 复制 `accounts.json.example` 为 `accounts.json`
2. 填入真实账户信息
3. 运行测试命令验证功能
