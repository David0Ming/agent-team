---
name: browser-auto
description: Browser automation for AI agents. Use when: (1) User asks to open/fetch/screenshot a website, (2) Need to browse the web, (3) Need to interact with web pages. Trigger: phrases like "打开浏览器", "访问", "浏览", "browser", "open website", "read article".
---

# Browser Auto

## Quick Start

### Check Browser Status
```bash
openclaw browser --profile chrome status
```

### Open Browser (if closed)
```bash
openclaw browser --profile chrome start
```

### List Tabs
```bash
openclaw browser --profile chrome tabs
```

### Navigate to URL
```bash
openclaw browser --profile chrome navigate <url>
```

### Get Page Content
```bash
openclaw browser --profile chrome snapshot
```

## Workflow

1. **Check if browser is running**: `browser(action="status")`
2. **Start if needed**: `browser(action="start", profile="chrome")`
3. **Navigate**: `browser(action="navigate", profile="chrome", targetUrl="...")`
4. **Read content**: `browser(action="snapshot", profile="chrome")`

## Common Issues

- **"No tabs"**: Browser started but no page open → use navigate
- **"Chrome extension relay not connected"**: User needs to click OpenClaw extension icon in Chrome
- **"Captcha/验证"**: WeChat articles often need manual verification → suggest alternative sources

## Profiles

- `chrome`: Use existing Chrome with OpenClaw extension (requires user to click extension icon)
- `openclaw`: Launch isolated Chrome browser (no extension needed)

## Example Usage

User: "帮我打开百度"
→ Use browser to navigate to baidu.com and snapshot the result
