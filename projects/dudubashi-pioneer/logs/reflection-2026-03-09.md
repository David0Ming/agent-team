# 竞品数据抓取任务复盘 - 2026-03-09

## 执行过程回顾

### 遇到的问题

1. **URL访问问题**
   - 简单分享URL（只有uuid）无法访问，显示"清单暂不支持公开分享"
   - 需要完整URL（包含f=share, source, keyword等参数）才能访问
   - 浪费时间：约20分钟

2. **数据提取失败**
   - 第一次：用表格选择器 → 失败（选择器不对）
   - 第二次：用文本解析 → 失败（解析逻辑错误）
   - 第三次：用DOM选择器 → 成功
   - 浪费时间：约15分钟

3. **依赖缺失**
   - matplotlib未安装，可视化失败
   - 系统限制pip安装
   - 浪费时间：约5分钟

4. **需要人工干预**
   - 需要泽钢提供cookies
   - 需要泽钢提供完整URL
   - 不是真正的自动化

### 成功的部分

1. ✅ 最终成功抓取数据（小江巴士15个，熊猫哒12个）
2. ✅ 生成了完整的报告
3. ✅ 数据结构化存储

## 改进方案（下次实现真正自动化）

### 1. 配置文件管理

**创建 `config/newrank.json`**：
```json
{
  "competitors": {
    "小江巴士": {
      "url": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=qwiswt2tu9fo&uuid=qwiswt2tu9fo",
      "list_id": "qwiswt2tu9fo"
    },
    "熊猫哒巴士": {
      "url": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=ozs697lbubnf&uuid=ozs697lbubnf",
      "list_id": "ozs697lbubnf"
    }
  },
  "cookies_file": "newrank_cookies.json",
  "last_update": "2026-03-09"
}
```

**好处**：
- 完整URL集中管理
- 下次直接读取，无需人工提供
- 易于维护和更新

### 2. 依赖检查和自动安装

**在脚本开头添加**：
```python
def check_dependencies():
    required = ['playwright', 'matplotlib']
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"缺少依赖: {', '.join(missing)}")
        print("尝试安装...")
        import subprocess
        subprocess.run(['pip3', 'install', '--user'] + missing)
```

### 3. 数据清洗

**清理账号名称中的序号和换行符**：
```python
def clean_account_name(name):
    # 移除开头的序号（如"4\n"）
    import re
    name = re.sub(r'^\d+\n', '', name)
    # 移除换行符
    name = name.replace('\n', ' ')
    return name.strip()
```

### 4. 错误处理和Fallback

**如果抓取失败，使用上次数据**：
```python
def scrape_with_fallback(brand, url):
    try:
        data = scrape_newrank(brand, url)
        if data['total'] > 0:
            return data
    except Exception as e:
        print(f"抓取失败: {e}")
    
    # 使用上次数据
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    fallback_file = DATA_DIR / yesterday / f"{brand}_detailed.json"
    if fallback_file.exists():
        print(f"使用 {yesterday} 的数据")
        with open(fallback_file) as f:
            return json.load(f)
    
    return {"brand": brand, "total": 0, "accounts": []}
```

### 5. 定时任务集成

**添加到 `run_daily.py`**：
```python
# 在09:00执行时，同时抓取竞品数据
if current_hour == 9:
    print("抓取竞品数据...")
    subprocess.run(['python3', 'scripts/fetch_newrank_dom.py'])
    subprocess.run(['python3', 'scripts/generate_competitor_report.py'])
```

### 6. Session持久化（长期方案）

**使用agent-browser保存登录状态**：
```bash
# 登录后保存状态
agent-browser state save newrank_session.json

# 下次使用
agent-browser state load newrank_session.json
agent-browser open "URL"
```

## 关键经验总结

1. **先测试再编码**：先用简单脚本测试页面结构，再写完整逻辑
2. **配置外部化**：URL、cookies等配置应该独立管理
3. **依赖前置检查**：避免运行到一半才发现缺依赖
4. **数据验证**：抓取后检查数据质量（如熊猫哒的NewRank指数都是0）
5. **Fallback机制**：失败时有备用方案，不要完全依赖实时抓取

## 下次执行清单

- [ ] 创建 `config/newrank.json` 配置文件
- [ ] 在脚本中添加依赖检查
- [ ] 添加数据清洗函数
- [ ] 实现Fallback机制
- [ ] 集成到 `run_daily.py`
- [ ] 测试完整自动化流程

## 预期效果

下次执行时：
1. 无需人工提供URL和cookies
2. 自动检查和安装依赖
3. 抓取失败时自动使用上次数据
4. 每天09:00自动执行
5. 真正实现"一键运行"
