#!/bin/bash
# 修复OpenClaw麦克风权限
# 允许Web Speech API访问麦克风

OPENCLAW_DIR="/home/mzg/.npm-global/lib/node_modules/openclaw/dist"

echo "🎤 修复麦克风权限..."

# 备份
for file in "$OPENCLAW_DIR"/gateway-cli-*.js; do
    if [ -f "$file" ]; then
        cp "$file" "$file.bak.$(date +%Y%m%d)"
        echo "  备份: $(basename $file)"
    fi
done

# 修改权限策略
sed -i 's/microphone=()/microphone=(self)/g' "$OPENCLAW_DIR"/gateway-cli-*.js

# 验证
if grep -q 'microphone=(self)' "$OPENCLAW_DIR"/gateway-cli-*.js; then
    echo "✅ 麦克风权限修复成功"
    exit 0
else
    echo "❌ 修复失败"
    exit 1
fi
