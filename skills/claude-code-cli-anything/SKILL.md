---
name: claude-code-cli-anything
version: 1.0.0
author: DJJ
compatibility: openclaw >= 2026.3.0
description: "Instruct Claude Code to use CLI-Anything for generating CLI interfaces for GUI software. Use when user needs to control GIMP, Blender, LibreOffice, or any software with source code."
tags: [delegation, claude-code, automation]
---

# Claude Code CLI-Anything Integration

This skill teaches OpenClaw how to delegate CLI generation tasks to Claude Code's CLI-Anything plugin.

## When to Use

- User wants to control GUI software (GIMP, Blender, LibreOffice, etc.)
- User asks "can you edit images" or "can you create 3D models"
- User needs to automate desktop applications

## How It Works

OpenClaw doesn't generate CLIs itself. Instead, it instructs Claude Code to do it.

## Usage Pattern

When user requests GUI software control:

1. **Check if CLI-Anything is installed**:
   ```bash
   claude plugin list | grep cli-anything
   ```

2. **If not installed, guide user**:
   ```
   To enable this, run in your terminal:
   claude plugin marketplace add HKUDS/CLI-Anything
   claude plugin install cli-anything
   ```

3. **If installed, delegate to Claude Code**:
   ```bash
   claude /cli-anything generate <software-name>
   ```

## Example Workflow

**User**: "Can you help me edit an image with GIMP?"

**OpenClaw Response**:
```
I can help you control GIMP through Claude Code's CLI-Anything plugin.

Let me check if it's installed:
[run: claude plugin list | grep cli-anything]

[If installed]
I'll generate a GIMP CLI interface:
[run: claude /cli-anything generate gimp]

Once generated, I can help you execute GIMP commands.

[If not installed]
First, install CLI-Anything:
1. claude plugin marketplace add HKUDS/CLI-Anything
2. claude plugin install cli-anything

Then I can generate the GIMP interface for you.
```

## Supported Software

CLI-Anything can generate CLIs for:
- **Image**: GIMP, Inkscape
- **3D**: Blender
- **Audio**: Audacity
- **Video**: Kdenlive, Shotcut, OBS Studio
- **Office**: LibreOffice
- **Any software with available source code**

## Important Notes

- OpenClaw **delegates** to Claude Code, doesn't execute directly
- User must have Claude Code installed
- CLI-Anything plugin must be installed in Claude Code
- Generated CLIs are production-ready and tested

## Troubleshooting

**"claude command not found"**:
- Claude Code is not installed
- Guide user to install: https://docs.anthropic.com/claude-code

**"Plugin not found"**:
- CLI-Anything not installed
- Run installation commands above

**"Software not supported"**:
- Software must have accessible source code
- Check CLI-Anything documentation for supported apps
