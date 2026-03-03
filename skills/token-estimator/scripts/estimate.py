#!/usr/bin/env python3
"""
Token Estimator - Analyze codebase size and recommend model tier

Usage:
    estimate.py --path ./src
    estimate.py --path ./src --ext .py,.ts,.js
    estimate.py --path ./src --recommend
    estimate.py --path ./src --json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Constants
CHARS_PER_TOKEN = 4  # Conservative estimate
THRESHOLD_LIGHTWEIGHT = 3_000_000  # 3M chars ≈ 750K tokens
THRESHOLD_PREMIUM = 12_000_000     # 12M chars ≈ 3M tokens

# Model recommendations
MODELS = {
    "lightweight": {
        "name": "Opus 4.6 / GPT-Mini",
        "model": "anthropic/claude-opus-4-6",
        "cost_tier": "low",
        "best_for": "Small tasks, quick edits, simple queries"
    },
    "standard": {
        "name": "GPT-5.1 / Kimi",
        "model": "fox/gpt-5.1",
        "cost_tier": "medium",
        "best_for": "Medium projects, standard development work"
    },
    "premium": {
        "name": "GPT-5.2 / Claude Opus",
        "model": "fox/gpt-5.2",
        "cost_tier": "high",
        "best_for": "Large codebases, complex refactoring, deep analysis"
    }
}


def parse_gitignore(path: Path) -> List[str]:
    """Parse .gitignore patterns if present."""
    gitignore = path / ".gitignore"
    if not gitignore.exists():
        return []
    
    patterns = []
    try:
        with open(gitignore, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    except Exception:
        pass
    return patterns


def should_ignore(file_path: Path, patterns: List[str]) -> bool:
    """Check if file should be ignored based on gitignore patterns."""
    path_str = str(file_path)
    name = file_path.name
    
    for pattern in patterns:
        # Simple pattern matching
        if pattern.endswith("/"):
            # Directory pattern
            if pattern.rstrip("/") in path_str:
                return True
        elif pattern.startswith("*"):
            # Extension pattern
            suffix = pattern.lstrip("*")
            if name.endswith(suffix):
                return True
        elif pattern in path_str or pattern == name:
            return True
    
    return False


def get_files_to_analyze(
    path: Path,
    extensions: List[str] = None,
    respect_gitignore: bool = True
) -> List[Path]:
    """Get list of files to analyze."""
    files = []
    gitignore_patterns = parse_gitignore(path) if respect_gitignore else []
    
    # Add common ignore patterns
    default_ignores = [
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", ".nuxt", "coverage", ".coverage",
        "*.min.js", "*.min.css", "*.map", "*.lock"
    ]
    gitignore_patterns.extend(default_ignores)
    
    if path.is_file():
        return [path]
    
    for root, dirs, filenames in os.walk(path):
        root_path = Path(root)
        
        # Filter out ignored directories
        dirs[:] = [
            d for d in dirs 
            if not should_ignore(root_path / d, gitignore_patterns)
        ]
        
        for filename in filenames:
            file_path = root_path / filename
            
            # Check gitignore
            if should_ignore(file_path, gitignore_patterns):
                continue
            
            # Check extensions
            if extensions:
                if not any(str(file_path).endswith(ext) for ext in extensions):
                    continue
            
            files.append(file_path)
    
    return files


def analyze_files(files: List[Path]) -> Tuple[int, int, Dict[str, int]]:
    """Analyze files and return character count, line count, and breakdown by extension."""
    total_chars = 0
    total_lines = 0
    by_extension: Dict[str, int] = {}
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                chars = len(content)
                lines = content.count("\n") + 1
                
                total_chars += chars
                total_lines += lines
                
                # Track by extension
                ext = file_path.suffix.lower() or "(no extension)"
                by_extension[ext] = by_extension.get(ext, 0) + chars
        except Exception:
            # Skip files that can't be read
            pass
    
    return total_chars, total_lines, by_extension


def get_recommendation(total_chars: int) -> Dict:
    """Get model recommendation based on character count."""
    estimated_tokens = total_chars // CHARS_PER_TOKEN
    
    if total_chars < THRESHOLD_LIGHTWEIGHT:
        tier = "lightweight"
        reason = f"Small codebase (~{estimated_tokens:,} tokens). Use cost-effective model."
    elif total_chars < THRESHOLD_PREMIUM:
        tier = "standard"
        reason = f"Medium codebase (~{estimated_tokens:,} tokens). Standard model recommended."
    else:
        tier = "premium"
        reason = f"Large codebase (~{estimated_tokens:,} tokens). Premium model required for sufficient context."
    
    return {
        "tier": tier,
        "model_info": MODELS[tier],
        "estimated_tokens": estimated_tokens,
        "reason": reason
    }


def format_size(num: int) -> str:
    """Format large numbers with commas."""
    return f"{num:,}"


def main():
    parser = argparse.ArgumentParser(
        description="Estimate token costs for codebase analysis"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to analyze (default: current directory)"
    )
    parser.add_argument(
        "--ext",
        type=str,
        help="Comma-separated file extensions to include (e.g., .py,.ts,.js)"
    )
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="Show model recommendation"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Don't respect .gitignore"
    )
    
    args = parser.parse_args()
    
    target_path = Path(args.path).resolve()
    if not target_path.exists():
        print(f"Error: Path not found: {target_path}", file=sys.stderr)
        sys.exit(1)
    
    # Parse extensions
    extensions = None
    if args.ext:
        extensions = [e.strip() for e in args.ext.split(",")]
    
    # Get files
    files = get_files_to_analyze(
        target_path,
        extensions=extensions,
        respect_gitignore=not args.no_gitignore
    )
    
    # Analyze
    total_chars, total_lines, by_extension = analyze_files(files)
    estimated_tokens = total_chars // CHARS_PER_TOKEN
    
    # Get recommendation
    recommendation = get_recommendation(total_chars)
    
    # Output
    if args.json:
        output = {
            "path": str(target_path),
            "files_analyzed": len(files),
            "total_characters": total_chars,
            "total_lines": total_lines,
            "estimated_tokens": estimated_tokens,
            "by_extension": by_extension,
            "recommendation": recommendation if args.recommend else None
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"📊 Token Estimation Report")
        print(f"=" * 50)
        print(f"Path: {target_path}")
        print(f"Files analyzed: {format_size(len(files))}")
        print(f"Total characters: {format_size(total_chars)}")
        print(f"Total lines: {format_size(total_lines)}")
        print(f"Estimated tokens: {format_size(estimated_tokens)}")
        print(f"(Using {CHARS_PER_TOKEN} chars/token ratio)")
        print()
        
        # Show top extensions
        if by_extension:
            print("By file type:")
            sorted_exts = sorted(by_extension.items(), key=lambda x: x[1], reverse=True)[:5]
            for ext, chars in sorted_exts:
                pct = (chars / total_chars * 100) if total_chars else 0
                print(f"  {ext}: {format_size(chars)} chars ({pct:.1f}%)")
            print()
        
        # Show recommendation
        if args.recommend:
            print("🎯 Model Recommendation")
            print("-" * 30)
            print(f"Tier: {recommendation['tier'].upper()}")
            print(f"Model: {recommendation['model_info']['name']}")
            print(f"OpenClaw model: {recommendation['model_info']['model']}")
            print(f"Cost tier: {recommendation['model_info']['cost_tier']}")
            print(f"Best for: {recommendation['model_info']['best_for']}")
            print()
            print(f"Reason: {recommendation['reason']}")
            print()
            print("To apply this recommendation:")
            print(f"  openclaw config set agent.model.primary \"{recommendation['model_info']['model']}\"")


if __name__ == "__main__":
    main()
