---
name: agent-browser
skill_version: 1.0.0
description: Browser automation for AI agents. Navigate, snapshot, interact with web pages using CLI commands. Supports authentication, session persistence, screenshots, PDF generation, mobile testing, and security features.
---

# agent-browser

Browser automation skill for AI agents by Vercel Labs.

## Installation

```bash
npm install -g agent-browser
```

## Core Workflow

```
open → snapshot -i → interact → re-snapshot
```

## Essential Commands

### Navigation
```bash
agent-browser open <url>          # Navigate to URL
agent-browser close               # Close browser
```

### Snapshot (Get element refs @e1, @e2...)
```bash
agent-browser snapshot -i         # Interactive elements with refs
agent-browser snapshot -i -C      # Include cursor-interactive elements
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interaction (use refs from snapshot)
```bash
agent-browser click @e1           # Click element
agent-browser click @e1 --new-tab # Open in new tab
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser select @e3 "option" # Select dropdown
agent-browser check @e1           # Check checkbox
agent-browser press Enter         # Press key
agent-browser scroll down 500     # Scroll page
```

### Get Information
```bash
agent-browser get text @e1        # Get element text
agent-browser get url             # Get current URL
agent-browser get title           # Get page title
```

### Wait
```bash
agent-browser wait @e1            # Wait for element
agent-browser wait --load networkidle  # Wait for network idle
agent-browser wait --url "**/dashboard" # Wait for URL pattern
agent-browser wait 2000           # Wait milliseconds
```

### Capture
```bash
agent-browser screenshot          # Screenshot
agent-browser screenshot --full   # Full page
agent-browser screenshot --annotate  # With element labels
agent-browser pdf output.pdf      # Save as PDF
```

## Common Patterns

### Form Submission
```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
```

### Authentication with Auth Vault
```bash
# Save credentials (encrypted)
echo "pass" | agent-browser auth save github --url https://github.com/login --username user --password-stdin

# Login using saved profile
agent-browser auth login github
```

### Session Persistence
```bash
# Login and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Reuse in future
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Command Chaining
```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

## Security Features

```bash
# Content boundaries (mark untrusted page content)
export AGENT_BROWSER_CONTENT_BOUNDARIES=1

# Domain allowlist
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"

# Action policy
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

## Mobile Testing (iOS)

```bash
# List devices
agent-browser device list

# Launch on iPhone
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios swipe up
```

## Important Rules

1. **Refs are invalidated when page changes** - always re-snapshot after navigation
2. **Use `--stdin` or `-b` for complex JavaScript** - avoids shell escaping issues
3. **Close sessions when done** - `agent-browser close`
4. **Use named sessions for concurrent agents** - `--session agent1`

## Resources

- GitHub: https://github.com/vercel-labs/agent-browser
- Full docs: https://skills.sh/vercel-labs/agent-browser/agent-browser
