#!/bin/bash
# Switch main agent to Fox GPT-5.2
# To be executed at 09:51 (7 hours from 02:51)

echo "🔄 Switching main agent model to Fox GPT-5.2..."
echo "Time: $(date)"

# Switch model
openclaw config set agents.list[0].model.primary "fox/gpt-5.2"

# Verify
echo "✅ Model switched. Current config:"
openclaw config get agents.list[0].model

# Restart session to apply changes
echo "🔄 Restarting main session..."
openclaw session restart agent:main:main

echo "🎉 Done! Model should now be Fox GPT-5.2"