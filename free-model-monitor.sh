#!/bin/bash
# 每10分钟寻找免费模型并自动配置

LOG_FILE="/home/mzg/.openclaw/workspace/memory/free-models.log"
CONFIG_FILE="/home/mzg/.openclaw/openclaw.json"

echo "[$(date)] 开始搜索免费模型..." >> "$LOG_FILE"

# 1. 检查当前可用模型状态
echo "=== 当前模型状态 ===" >> "$LOG_FILE"
openclaw status 2>&1 | grep -A5 "Models:" >> "$LOG_FILE"

# 2. 搜索免费模型资源
echo "=== 搜索免费模型 ===" >> "$LOG_FILE"

# 检查 DeepSeek 状态
curl -s https://api.deepseek.com/v1/models -H "Authorization: Bearer sk-5cb8ca39c0f64ba6bd0c61ddfd5063c8" 2>&1 | head -3 >> "$LOG_FILE"

# 检查 Kimi 状态（等待限速解除）
curl -s https://api.kimi.com/coding/v1/models 2>&1 | head -3 >> "$LOG_FILE"

# 3. 检查其他免费模型
# Qwen (阿里云)
echo "检查 Qwen..." >> "$LOG_FILE"
curl -s https://dashscope.aliyuncs.com/compatible-mode/v1/models 2>&1 | head -3 >> "$LOG_FILE"

# 4. 记录发现
echo "[$(date)] 搜索完成" >> "$LOG_FILE"
echo "=========================" >> "$LOG_FILE"
