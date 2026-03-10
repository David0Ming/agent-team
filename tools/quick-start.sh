#!/bin/bash
# 快速启动脚本 - 常用命令集合

echo "🚀 OpenClaw 快速启动菜单"
echo ""
echo "1. 查看系统状态"
echo "2. 检查Agent健康"
echo "3. 知识库维护"
echo "4. 生成每日报告"
echo "5. 查看性能监控"
echo "6. 运行嘟嘟巴士任务"
echo "0. 退出"
echo ""
read -p "请选择操作 (0-6): " choice

case $choice in
    1)
        echo "📊 系统状态..."
        openclaw status
        ;;
    2)
        echo "🏥 Agent健康检查..."
        bash ~/.openclaw/workspace/tools/agent-health-check.sh
        ;;
    3)
        echo "📚 知识库维护..."
        python3 ~/.openclaw/workspace/tools/knowledge-maintenance.py
        ;;
    4)
        echo "📝 生成每日报告..."
        python3 ~/.openclaw/workspace/tools/daily-report.py
        ;;
    5)
        echo "📈 性能监控..."
        python3 ~/.openclaw/workspace/tools/agent-monitor.py
        ;;
    6)
        echo "🚌 运行嘟嘟巴士任务..."
        python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/run_daily.py
        ;;
    0)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
