# QQ邮箱管理方案

> 让OpenClaw管理你的QQ邮箱，自动处理面试邀请等邮件

## 方案概述

使用OpenClaw官方的 **imap-smtp-email** 技能，通过IMAP/SMTP协议访问QQ邮箱。

**官方技能**：https://playbooks.com/skills/openclaw/skills/imap-smtp-email

---

## 核心功能

### 读取邮件
- ✅ 检查新邮件/未读邮件
- ✅ 获取邮件内容和附件
- ✅ 搜索邮件（按日期、发件人、主题）
- ✅ 标记已读/未读

### 发送邮件
- ✅ 发送纯文本/HTML邮件
- ✅ 支持抄送/密送
- ✅ 支持附件

### 智能处理
- ✅ 自动识别面试邀请
- ✅ 提取时间信息
- ✅ 统计面试安排
- ✅ 自动回复确认

---

## 安装步骤

### 1. 安装技能

```bash
npx playbooks add skill openclaw/skills --skill imap-smtp-email
```

或者使用find-skills技能：
```bash
# 在OpenClaw中执行
使用find-skills技能搜索"imap-smtp-email"并安装
```

### 2. 获取QQ邮箱授权码

**重要**：QQ邮箱不能直接使用密码，必须使用授权码。

**步骤**：
1. 登录QQ邮箱网页版
2. 点击右上角「设置」→「账号与安全」
3. 找到「安全设置」
4. 开启「POP3/IMAP/SMTP服务」
5. 点击「生成授权码」
6. 通过短信验证
7. 复制授权码（只显示一次，务必保存）

**官方文档**：https://service.mail.qq.com/detail/0/339

### 3. 配置环境变量

创建配置文件 `~/.openclaw/.env`（如果不存在）：

```bash
# QQ邮箱IMAP配置
IMAP_HOST=imap.qq.com
IMAP_PORT=993
IMAP_USER=你的QQ邮箱@qq.com
IMAP_PASS=你的授权码
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=true

# QQ邮箱SMTP配置
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_USER=你的QQ邮箱@qq.com
SMTP_PASS=你的授权码
SMTP_TLS=true
SMTP_REJECT_UNAUTHORIZED=true
```

**QQ邮箱服务器信息**：
- IMAP服务器：imap.qq.com，端口993（SSL）
- SMTP服务器：smtp.qq.com，端口465（SSL）或587（TLS）

---

## 使用示例

### 检查新邮件
```bash
# 检查未读邮件
imap-check

# 检查最近3天的邮件
imap-check --since 3
```

### 搜索面试邀请
```bash
# 搜索包含"面试"的邮件
imap-search --subject 面试

# 搜索特定发件人
imap-search --from hr@company.com

# 搜索最近7天的邮件
imap-search --since 7
```

### 获取邮件内容
```bash
# 获取指定邮件
imap-fetch --uid 12345

# 下载附件
imap-download --uid 12345
```

### 发送邮件
```bash
# 发送确认邮件
imap-send --to hr@company.com --subject "面试确认" --body "我确认参加面试"
```

---

## 智能功能设计

### 1. 自动识别面试邀请

创建技能：`skills/interview-manager/SKILL.md`

**功能**：
- 定时检查邮件（每小时）
- 识别面试邀请关键词
- 提取时间、地点、公司信息
- 生成面试日历

**关键词**：
- "面试邀请"
- "面试通知"
- "邀请您参加面试"
- "interview invitation"

### 2. 面试时间统计

**功能**：
- 统计本周/本月面试数量
- 按公司分类
- 按职位分类
- 生成时间表

### 3. 自动回复

**功能**：
- 识别需要确认的邮件
- 生成礼貌的确认回复
- 询问是否发送

---

## 安全注意事项

### 1. 授权码安全
- ❌ 不要将授权码提交到Git
- ✅ 使用环境变量存储
- ✅ 定期更换授权码
- ✅ 不要在公开场合分享

### 2. 邮件隐私
- ✅ 只读取必要的邮件
- ✅ 不存储敏感信息
- ✅ 定期清理日志

### 3. 访问控制
- ✅ 限制技能权限
- ✅ 只在需要时启用
- ✅ 监控异常访问

---

## 下一步行动

### 立即可做
1. **获取授权码**：登录QQ邮箱获取IMAP/SMTP授权码
2. **安装技能**：`npx playbooks add skill openclaw/skills --skill imap-smtp-email`
3. **配置环境变量**：在`~/.openclaw/.env`中添加配置
4. **测试连接**：运行`imap-check`验证

### 后续开发
1. **创建面试管理技能**：自动识别和统计面试邀请
2. **集成日历**：将面试时间同步到日历
3. **智能提醒**：面试前自动提醒

---

## 参考资料

- [OpenClaw IMAP-SMTP技能](https://playbooks.com/skills/openclaw/skills/imap-smtp-email)
- [QQ邮箱IMAP/SMTP设置](https://service.mail.qq.com/detail/0/339)
- [QQ邮箱授权码获取](https://blog.csdn.net/m0_62140641/article/details/142205387)

---

**创建时间**：2026-03-18
**作者**：DJJ
