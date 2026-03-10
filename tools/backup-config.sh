#!/bin/bash
# 配置备份工具
# 备份关键配置文件

BACKUP_DIR=~/.openclaw/workspace/backups
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p $BACKUP_DIR

echo "📦 开始备份..."
tar -czf $BACKUP_DIR/config-$DATE.tar.gz \
    ~/.openclaw/workspace/SOUL.md \
    ~/.openclaw/workspace/HEARTBEAT.md \
    ~/.openclaw/workspace/tools/ \
    2>/dev/null

echo "✅ 备份完成: config-$DATE.tar.gz"
