#!/usr/bin/env python3
"""
嘟嘟巴士先锋引擎 - 主运行脚本
每日10:00自动执行

执行顺序：
1. 搜索昨日热点（web_search + 浏览器）
2. 抓取竞品数据（抖音/小红书）
3. 生成视频提示词（基于热点+竞品洞察）

用法：
  python3 run_daily.py           # 检查时间后执行
  python3 run_daily.py --force  # 强制执行
  python3 run_daily.py --step1  # 仅执行步骤1：热点抓取
  python3 run_daily.py --step2  # 仅执行步骤2：竞品数据
  python3 run_daily.py --step3  # 仅执行步骤3：生成prompt
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
PROJECT_DIR = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_DIR / "config.json"
LOG_DIR = PROJECT_DIR / "logs"
DATA_DIR = PROJECT_DIR / "competitor-data"
PROMPT_DIR = PROJECT_DIR / "prompts"

# 加载配置
def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

# 记录日志
def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] [{level}] {msg}\n")
    print(f"[{timestamp}] [{level}] {msg}")

# 检查时间是否10:00
def is_10am():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    return hour == 10 and minute < 5

# 检查是否已执行
def already_run_today():
    today = datetime.now().strftime("%Y-%m-%d")
    marker = LOG_DIR / f".run_{today}"
    return marker.exists()

def mark_run_today():
    today = datetime.now().strftime("%Y-%m-%d")
    marker = LOG_DIR / f".run_{today}"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(datetime.now().isoformat())

# ========== 步骤1：抓取热点 ==========
def step1_fetch_hotspots():
    """步骤1：搜索昨日热点"""
    log("=" * 50)
    log("【步骤1】搜索昨日热点")
    
    hotspots = []
    
    # 用 web_search 搜热点
    try:
        result = subprocess.run(
            ["codex", "exec", "--", "web_search", "--query", "今日热点 微博 知乎 2026年3月", "--count", "5"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            hotspots.append({"source": "web_search", "content": result.stdout[:1000]})
            log("web_search 热点获取成功")
    except Exception as e:
        log(f"web_search 失败: {e}", "WARNING")
    
    # 如果没有热点，使用备用库
    if not hotspots:
        hotspots = [
            {"source": "backup", "content": "深圳天气：晴转多云，23-28°C"},
            {"source": "backup", "content": "大湾区交通：深中通道相关"},
            {"source": "backup", "content": "职场热点：春季跳槽季"}
        ]
        log("使用备用热点库")
    
    # 保存热点
    today = datetime.now().strftime("%Y-%m-%d")
    hotspot_file = DATA_DIR / today / "hotspots.json"
    hotspot_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hotspot_file, "w", encoding="utf-8") as f:
        json.dump(hotspots, f, ensure_ascii=False, indent=2)
    
    log(f"热点保存到: {hotspot_file}")
    log("【步骤1】完成")
    return {"status": "success", "hotspots": hotspots}

# ========== 步骤2：抓取竞品数据 ==========
def step2_fetch_competitor():
    """步骤2：抓取竞品数据"""
    log("=" * 50)
    log("【步骤2】抓取竞品数据")
    
    # 竞品数据需要通过浏览器抓取，这里标记需要手动/外部触发
    # 实际抓取需要调用浏览器自动化脚本
    
    log("注意：竞品数据需要浏览器登录后抓取")
    log("建议：手动打开浏览器登录后，运行竞品抓取脚本")
    
    # 标记状态
    today = datetime.now().strftime("%Y-%m-%d")
    comp_file = DATA_DIR / today / "competitor_status.json"
    comp_file.parent.mkdir(parents=True, exist_ok=True)
    
    status = {
        "抖音": {"status": "pending", "note": "需要浏览器登录抓取"},
        "小红书": {"status": "pending", "note": "需要浏览器登录抓取"},
        "视频号": {"status": "pending", "note": "需要浏览器登录抓取"}
    }
    
    with open(comp_file, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    
    log("【步骤2】完成（待手动抓取）")
    return {"status": "partial", "note": "竞品数据需要手动抓取"}

# ========== 步骤3：生成Prompt ==========
def step3_generate_prompts():
    """步骤3：基于热点和竞品数据生成Prompt"""
    log("=" * 50)
    log("【步骤3】生成视频提示词")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 读取热点
    hotspot_file = DATA_DIR / today / "hotspots.json"
    hotspots = []
    if hotspot_file.exists():
        with open(hotspot_file, encoding="utf-8") as f:
            hotspots = json.load(f)
    
    # 读取竞品洞察
    insight_file = DATA_DIR / today / "xiaojiang_bus_xiaohongshu.md"
    insights = ""
    if insight_file.exists():
        with open(insight_file, encoding="utf-8") as f:
            insights = f.read()
    
    # 生成Prompt
    prompt_content = f"""# 嘟嘟巴士日报 - 视频提示词
# 生成日期: {today}

## 热点来源
{json.dumps(hotspots, ensure_ascii=False, indent=2)}

## 竞品洞察
{insights}

---
## 视频提示词 1

## 视频主题
[基于热点：{hotspots[0]['source'] if hotspots else '备用'}]

## 司机开场白（45字，语速快）
"..."

## 画面描述（英文，10-15秒分镜）
**00:00-00:03** 【Hook】
**00:03-00:08** 【展开】
**00:08-00:15** 【反转/收尾】

## BGM建议

---
## 视频提示词 2
...

---
## 视频提示词 3
...
"""
    
    # 保存Prompt
    prompt_file = PROMPT_DIR / today / "morning_prompt_v1.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt_content)
    
    log(f"Prompt保存到: {prompt_file}")
    log("【步骤3】完成")
    return {"status": "success", "file": str(prompt_file)}

# ========== 主流程 ==========
def run_full_pipeline():
    """完整流程：步骤1 → 步骤2 → 步骤3"""
    results = {}
    
    # 步骤1：热点
    try:
        results["step1"] = step1_fetch_hotspots()
    except Exception as e:
        log(f"步骤1失败: {e}", "ERROR")
        results["step1"] = {"status": "failed", "error": str(e)}
    
    # 步骤2：竞品
    try:
        results["step2"] = step2_fetch_competitor()
    except Exception as e:
        log(f"步骤2失败: {e}", "ERROR")
        results["step2"] = {"status": "failed", "error": str(e)}
    
    # 步骤3：生成Prompt（依赖步骤1）
    try:
        results["step3"] = step3_generate_prompts()
    except Exception as e:
        log(f"步骤3失败: {e}", "ERROR")
        results["step3"] = {"status": "failed", "error": str(e)}
    
    return results

# 反思环节
def reflect(results):
    log("=" * 50)
    log("执行复盘")
    
    issues = []
    if results.get("step1", {}).get("status") != "success":
        issues.append("步骤1：热点抓取失败")
    if results.get("step2", {}).get("status") != "success":
        issues.append("步骤2：竞品数据待手动抓取")
    if results.get("step3", {}).get("status") != "success":
        issues.append("步骤3：Prompt生成失败")
    
    for issue in issues:
        log(f"  - {issue}")
    
    log("=" * 50)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="强制执行")
    parser.add_argument("--step1", action="store_true", help="仅执行步骤1：热点")
    parser.add_argument("--step2", action="store_true", help="仅执行步骤2：竞品")
    parser.add_argument("--step3", action="store_true", help="仅执行步骤3：生成Prompt")
    args = parser.parse_args()
    
    config = load_config()
    log("=" * 50)
    log("嘟嘟巴士先锋引擎启动")
    
    # 时间检查（除非强制执行）
    if not args.force:
        if not is_10am():
            log("非10:00，跳过执行")
            return
        log("时间检查通过：10:00")
    
    # 检查是否已执行（完整流程）
    if already_run_today() and not args.force and not any([args.step1, args.step2, args.step3]):
        log("今日已执行完整流程")
    
    # 执行选定的步骤
    if args.step1:
        step1_fetch_hotspots()
    elif args.step2:
        step2_fetch_competitor()
    elif args.step3:
        step3_generate_prompts()
    else:
        # 完整流程
        results = run_full_pipeline()
        reflect(results)
        mark_run_today()
    
    log("执行完成")

if __name__ == "__main__":
    main()
