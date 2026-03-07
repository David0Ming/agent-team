# 2026-02-28 - Skill 学习笔记（summarize & session-logs）

## summarize Skill

**用途**: 快速总结 URL、本地文件、YouTube 视频

**关键学习点**:
- 依赖外部 CLI `summarize`（brew 安装）
- 支持多模型：OpenAI、Anthropic、xAI、Google
- 默认模型：`google/gemini-3-flash-preview`（便宜快速）
- 特殊功能：YouTube 转录（不需要 yt-dlp）

**使用场景**:
```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model openai/gpt-5.2
summarize "https://youtu.be/xxx" --youtube auto --extract-only
```

**评估**: 
- ✅ Linux 可用（只要安装 summarize CLI）
- ✅ 符合"信息处理"需求
- ⚠️ 需要额外安装工具

---

## session-logs Skill ⭐ 重要

**用途**: 搜索分析会话历史（JSONL 格式）

**关键发现 - 成本追踪**:
会话日志包含成本信息：
```json
{
  "message": {
    "usage": {
      "cost": {
        "total": 0.0023
      }
    }
  }
}
```

**实用查询**:
```bash
# 单日成本汇总
for f in ~/.openclaw/agents/main/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r

# 单会话总成本
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl

# 工具使用统计
jq -r '.message.content[]? | select(.type == "toolCall") | .name' <session>.jsonl | sort | uniq -c | sort -rn
```

**评估**:
- ✅ 完美替代 model-usage！
- ✅ 原生 OpenClaw 数据，无需外部工具
- ✅ Linux 可用
- ✅ 实时、准确

---

## 成本追踪方案

基于 session-logs，我们可以创建自定义成本追踪脚本：
- 读取 `~/.openclaw/agents/main/sessions/*.jsonl`
- 按天/周/月汇总成本
- 按模型分解成本
- 设置预算告警

这比 model-usage 更好，因为：
1. 不依赖外部 CLI
2. 数据实时准确
3. 完全可控
