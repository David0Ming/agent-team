#!/usr/bin/env python3
"""
Cost Tracker - Analyze OpenClaw session costs from JSONL logs
Alternative to model-usage skill (macOS only), works on Linux

Usage:
    cost_tracker.py                    # Show today's cost
    cost_tracker.py --daily            # Daily summary
    cost_tracker.py --weekly           # Weekly summary
    cost_tracker.py --by-model         # Cost breakdown by model
    cost_tracker.py --session <id>     # Specific session cost
    cost_tracker.py --budget 10.00     # Check against daily budget
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def get_sessions_dir() -> Path:
    """Get the sessions directory for the main agent."""
    home = Path.home()
    return home / ".openclaw" / "agents" / "main" / "sessions"


def parse_session_file(filepath: Path) -> List[Dict]:
    """Parse a JSONL session file."""
    messages = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
    return messages


def extract_cost(messages: List[Dict]) -> Tuple[float, Dict[str, float]]:
    """Extract total cost and cost by model from messages."""
    total = 0.0
    by_model: Dict[str, float] = {}
    
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        
        message = msg.get("message", {})
        usage = message.get("usage", {})
        cost = usage.get("cost", {})
        
        msg_cost = cost.get("total", 0) or 0
        total += msg_cost
        
        # Try to get model info
        model = message.get("model", "unknown")
        if model:
            by_model[model] = by_model.get(model, 0) + msg_cost
    
    return total, by_model


def get_session_date(messages: List[Dict]) -> Optional[str]:
    """Get the date of the first message in the session."""
    for msg in messages:
        timestamp = msg.get("timestamp", "")
        if timestamp:
            try:
                # Parse ISO timestamp
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d")
            except:
                pass
    return None


def analyze_all_sessions(sessions_dir: Path) -> Dict:
    """Analyze all session files."""
    daily_costs: Dict[str, float] = {}
    daily_by_model: Dict[str, Dict[str, float]] = {}
    session_data: List[Dict] = []
    
    if not sessions_dir.exists():
        print(f"Error: Sessions directory not found: {sessions_dir}", file=sys.stderr)
        return {}
    
    for filepath in sessions_dir.glob("*.jsonl"):
        # Skip deleted sessions
        if ".deleted." in filepath.name:
            continue
        
        messages = parse_session_file(filepath)
        if not messages:
            continue
        
        cost, by_model = extract_cost(messages)
        date = get_session_date(messages) or "unknown"
        session_id = filepath.stem
        
        # Aggregate by day
        daily_costs[date] = daily_costs.get(date, 0) + cost
        
        if date not in daily_by_model:
            daily_by_model[date] = {}
        for model, model_cost in by_model.items():
            daily_by_model[date][model] = daily_by_model[date].get(model, 0) + model_cost
        
        session_data.append({
            "id": session_id,
            "date": date,
            "cost": cost,
            "by_model": by_model,
            "messages": len(messages)
        })
    
    return {
        "daily_costs": daily_costs,
        "daily_by_model": daily_by_model,
        "sessions": session_data,
        "total_cost": sum(daily_costs.values())
    }


def print_daily_summary(data: Dict, days: int = 7):
    """Print daily cost summary."""
    daily = data.get("daily_costs", {})
    
    print("📊 Daily Cost Summary")
    print("=" * 50)
    
    # Sort by date descending
    sorted_dates = sorted(daily.keys(), reverse=True)[:days]
    
    for date in sorted_dates:
        cost = daily[date]
        print(f"{date}: ${cost:.4f}")
    
    print("-" * 50)
    print(f"Total (last {len(sorted_dates)} days): ${sum(daily[d] for d in sorted_dates):.4f}")


def print_weekly_summary(data: Dict, weeks: int = 4):
    """Print weekly cost summary."""
    daily = data.get("daily_costs", {})
    
    # Aggregate by week
    weekly: Dict[str, float] = {}
    for date_str, cost in daily.items():
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            week_key = dt.strftime("%Y-W%W")
            weekly[week_key] = weekly.get(week_key, 0) + cost
        except:
            continue
    
    print("📅 Weekly Cost Summary")
    print("=" * 50)
    
    sorted_weeks = sorted(weekly.keys(), reverse=True)[:weeks]
    for week in sorted_weeks:
        print(f"{week}: ${weekly[week]:.4f}")
    
    print("-" * 50)
    print(f"Total (last {len(sorted_weeks)} weeks): ${sum(weekly[w] for w in sorted_weeks):.4f}")


def print_by_model(data: Dict):
    """Print cost breakdown by model."""
    daily_by_model = data.get("daily_by_model", {})
    
    # Aggregate all time
    all_models: Dict[str, float] = {}
    for date_models in daily_by_model.values():
        for model, cost in date_models.items():
            all_models[model] = all_models.get(model, 0) + cost
    
    print("🤖 Cost by Model")
    print("=" * 50)
    
    sorted_models = sorted(all_models.items(), key=lambda x: x[1], reverse=True)
    total = sum(all_models.values())
    
    for model, cost in sorted_models:
        pct = (cost / total * 100) if total else 0
        print(f"{model}: ${cost:.4f} ({pct:.1f}%)")
    
    print("-" * 50)
    print(f"Total: ${total:.4f}")


def print_session_cost(data: Dict, session_id: str):
    """Print cost for a specific session."""
    sessions = data.get("sessions", [])
    
    for session in sessions:
        if session_id in session["id"]:
            print(f"📄 Session: {session['id']}")
            print(f"Date: {session['date']}")
            print(f"Cost: ${session['cost']:.4f}")
            print(f"Messages: {session['messages']}")
            
            if session['by_model']:
                print("By model:")
                for model, cost in session['by_model'].items():
                    print(f"  {model}: ${cost:.4f}")
            return
    
    print(f"Session not found: {session_id}")


def check_budget(data: Dict, budget: float):
    """Check today's cost against budget."""
    daily = data.get("daily_costs", {})
    today = datetime.now().strftime("%Y-%m-%d")
    today_cost = daily.get(today, 0)
    
    print(f"💰 Budget Check")
    print("=" * 50)
    print(f"Daily budget: ${budget:.2f}")
    print(f"Today's cost: ${today_cost:.4f}")
    print(f"Remaining: ${budget - today_cost:.4f}")
    
    if today_cost > budget:
        print(f"⚠️  OVER BUDGET by ${today_cost - budget:.4f}")
    elif today_cost > budget * 0.8:
        print(f"⚠️  Approaching budget (80%+)")
    else:
        print(f"✅ Within budget")


def print_today_summary(data: Dict):
    """Print today's cost summary."""
    daily = data.get("daily_costs", {})
    today = datetime.now().strftime("%Y-%m-%d")
    today_cost = daily.get(today, 0)
    
    # Get today's model breakdown
    daily_by_model = data.get("daily_by_model", {})
    today_models = daily_by_model.get(today, {})
    
    print(f"📊 Today ({today})")
    print("=" * 50)
    
    if today_cost == 0:
        print("Total cost: $0.00 (using free/cached models)")
    else:
        print(f"Total cost: ${today_cost:.4f}")
    
    if today_models:
        print("\nBy model:")
        for model, cost in sorted(today_models.items(), key=lambda x: x[1], reverse=True):
            if cost == 0:
                print(f"  {model}: $0.00 (free/cached)")
            else:
                print(f"  {model}: ${cost:.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Track OpenClaw session costs from JSONL logs"
    )
    parser.add_argument(
        "--daily",
        action="store_true",
        help="Show daily summary"
    )
    parser.add_argument(
        "--weekly",
        action="store_true",
        help="Show weekly summary"
    )
    parser.add_argument(
        "--by-model",
        action="store_true",
        help="Show cost breakdown by model"
    )
    parser.add_argument(
        "--session",
        type=str,
        help="Show specific session cost"
    )
    parser.add_argument(
        "--budget",
        type=float,
        help="Check against daily budget"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days for daily summary (default: 7)"
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=4,
        help="Number of weeks for weekly summary (default: 4)"
    )
    
    args = parser.parse_args()
    
    # Get data
    sessions_dir = get_sessions_dir()
    data = analyze_all_sessions(sessions_dir)
    
    if not data:
        sys.exit(1)
    
    # Output based on args
    if args.session:
        print_session_cost(data, args.session)
    elif args.budget:
        check_budget(data, args.budget)
    elif args.by_model:
        print_by_model(data)
    elif args.weekly:
        print_weekly_summary(data, args.weeks)
    elif args.daily:
        print_daily_summary(data, args.days)
    else:
        print_today_summary(data)


if __name__ == "__main__":
    main()
