# 2026-02-28 - Skill 学习笔记（sag / whisper / nano-pdf）

## sag - ElevenLabs TTS

**用途**: 文本转语音，支持情感标签和多种声音

**关键学习点**:
- 依赖: `ELEVENLABS_API_KEY`
- 安装: `brew install steipete/tap/sag`
- 模型选择:
  - `eleven_v3` (默认) - 表现力最强
  - `eleven_multilingual_v2` - 稳定多语言
  - `eleven_flash_v2_5` - 快速

**情感标签** (v3):
- `[whispers]`, `[shouts]`, `[sings]`
- `[laughs]`, `[sighs]`, `[exhales]`
- `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`
- `[short pause]`, `[long pause]`

**使用场景**:
```bash
# 基础用法
sag "Hello there"

# 指定声音
sag -v Roger "Hello"

# 带情感
sag "[excited] Great news! [short pause] We did it!"

# 生成文件
sag -v Clawd -o /tmp/voice.mp3 "Your message"
```

**评估**: ✅ Linux 可用（Python CLI），需要 API key

---

## openai-whisper-api - 语音转录

**用途**: 音频文件转文字（OpenAI Whisper API）

**关键学习点**:
- 依赖: `OPENAI_API_KEY`（已配置）
- 脚本位置: `{baseDir}/scripts/transcribe.sh`
- 默认模型: `whisper-1`

**使用场景**:
```bash
# 基础转录
./scripts/transcribe.sh /path/to/audio.m4a

# 指定语言
./scripts/transcribe.sh audio.m4a --language zh

# 带提示（人名识别）
./scripts/transcribe.sh audio.m4a --prompt "Speaker: 泽钢, DJJ"

# JSON 输出
./scripts/transcribe.sh audio.m4a --json --out transcript.json
```

**评估**: ✅ Linux 可用，依赖 curl 和 API key

---

## nano-pdf - PDF 编辑

**用途**: 自然语言指令编辑 PDF

**关键学习点**:
- 安装: `uv install nano-pdf`
- 交互方式: 自然语言描述修改

**使用场景**:
```bash
# 编辑第1页标题
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results'"

# 修复拼写错误
nano-pdf edit doc.pdf 3 "Fix typo in paragraph 2"
```

**注意**: 页码可能是 0-based 或 1-based，如果结果不对尝试另一种

**评估**: ✅ Linux 可用，但功能较简单（仅单页编辑）

---

## 学习总结

**所有 Skills 评估**:

| Skill | Linux | 需要配置 | 实用性 |
|-------|-------|---------|--------|
| token-estimator | ✅ | 无 | ⭐⭐⭐⭐⭐ |
| healthcheck | ✅ | 无 | ⭐⭐⭐⭐⭐ |
| session-logs | ✅ | 无 | ⭐⭐⭐⭐⭐ |
| coding-agent | ✅ | 无 | ⭐⭐⭐⭐⭐ |
| summarize | ✅ | summarize CLI | ⭐⭐⭐⭐ |
| sag | ✅ | ElevenLabs API | ⭐⭐⭐⭐ |
| openai-whisper-api | ✅ | OpenAI API | ⭐⭐⭐⭐ |
| nano-pdf | ✅ | nano-pdf CLI | ⭐⭐⭐ |
| skill-creator | ✅ | 无 | ⭐⭐⭐⭐⭐ |

**模型使用成本**（从配置读取）:
- Kimi k2p5: $0（限时免费）
- Fox GPT-5.2: $3/M input, $12/M output
- Anthropic Opus 4.6: $15/M input, $75/M output
- DeepSeek: $0.14/M input, $0.28/M output

**下一步**: 所有核心 skills 已学习完毕。可以开始实际应用或学习其他内容。
