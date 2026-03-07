# 代码治理框架

## 目标
- 提升代码质量
- 统一代码风格
- 自动化审查减少人工负担

## 技术栈
- **ruff**: Python linter + formatter
- **pre-commit**: Git hook自动化

## 代码规范

### Python风格
- 遵循 PEP 8
- 最大行长: 100字符
- 使用类型提示(type hints)
- 文档字符串(docstring)使用Google风格

### 命名规范
- 函数: snake_case
- 类: PascalCase
- 常量: UPPER_SNAKE_CASE
- 私有变量: _leading_underscore

### 最佳实践
1. **单一职责**: 一个函数只做一件事
2. **DRY**: 不要重复自己
3. **YAGNI**: 不要预先设计你不需要的东西
4. **早返回**: 减少嵌套层级

## 自动化工具配置

### ruff配置 (.ruff.toml)
```toml
line-length = 100
target-version = "py39"

[lint]
select = ["E", "F", "W", "I", "N"]
ignore = ["E501"]

[format]
quote-style = "double"
indent-style = "space"
```

### pre-commit hook
每次commit自动检查:
- ruff format
- ruff check
-  trailing whitespace
-  merge conflict markers

## 审查流程
1. 开发时: IDE实时检查
2. commit前: pre-commit hook
3. CI/CD: GitHub Actions全面检查

## 责任人
- DMing团队执行
- DJJ定期review
