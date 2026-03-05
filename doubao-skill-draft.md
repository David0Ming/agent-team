# 豆包视频生成 Skill 方案

## 背景
- API: 豆包 Seedance 2 (火山引擎)
- Key: f76f61ca-73e1-4edd-83a7-82100f367b86
- URL: https://ark.cn-beijing.volces.com/api/v3/chat/completions

## 待确认问题（等 Dplan 调研）
1. API 具体参数格式
2. 返回是流式视频还是 URL
3. 认证方式细节
4. 价格和限制

## 初步方案

### Skill 名称
`doubao-video-gen`

### 输入参数
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| prompt | string | 是 | - | 视频描述 |
| width | int | 否 | 1080 | 视频宽度 |
| height | int | 否 | 1920 | 视频高度 |
| duration | int | 否 | 5 | 时长(秒) |
| output | string | 否 | ./output.mp4 | 输出路径 |

### 输出
- 成功: 返回视频文件路径
- 失败: 返回错误信息

### 错误处理
- 网络错误: 重试 3 次
- API 限制: 提示等待
- 参数错误: 立即返回

## 下一步
等 Dplan 调研报告，确认 API 细节后实现。
