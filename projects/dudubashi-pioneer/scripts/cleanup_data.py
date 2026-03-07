#!/usr/bin/env python3
"""
数据自动清理脚本
保留最近30天的数据，超过30天的临时文件列出待删除
删除前需用户确认
"""

import argparse
import os
from datetime import datetime

# 配置清理规则
RETENTION_DAYS = 30  # 数据保留30天

# 需要清理的目录
CLEANUP_DIRS = [
    "/tmp/competitor_*.json",
    "/tmp/*prompt*.json",
    "/tmp/*crawl*.json",
]

def should_cleanup(file_path: str) -> tuple[bool, str]:
    """判断文件是否应该被清理，返回(是否应清理, 原因)"""
    try:
        # 获取文件修改时间
        mtime = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(mtime)

        # 计算天数差
        age = datetime.now() - file_date
        if age.days > RETENTION_DAYS:
            return True, f"已保存{age.days}天"
        return False, f"还有{RETENTION_DAYS - age.days}天"
    except Exception as e:
        return False, f"检查失败: {e}"

def cleanup_files(confirm: bool = False) -> list[dict]:
    """执行清理 - 确认模式才真正删除"""
    files_to_delete = []

    for pattern in CLEANUP_DIRS:
        # 使用glob匹配
        import glob
        files = glob.glob(pattern)

        for file_path in files:
            should_clean, reason = should_cleanup(file_path)
            if should_clean:
                file_size = os.path.getsize(file_path) / 1024  # KB
                files_to_delete.append({
                    "path": file_path,
                    "reason": reason,
                    "size_kb": round(file_size, 1)
                })

    # 如果确认删除，执行删除
    if confirm and files_to_delete:
        for f in files_to_delete:
            try:
                os.remove(f["path"])
                print(f"🗑️  已删除: {f['path']}")
            except Exception as e:
                print(f"❌ 删除失败 {f['path']}: {e}")

    return files_to_delete

def main():
    parser = argparse.ArgumentParser(description="数据清理脚本")
    parser.add_argument("--confirm", action="store_true", help="确认删除（不加此参数只列出待删除文件）")
    args = parser.parse_args()

    print("🧹 数据清理脚本启动")
    print(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ 保留最近 {RETENTION_DAYS} 天的数据")
    print("-" * 40)

    files = cleanup_files(confirm=args.confirm)

    print("-" * 40)
    if not files:
        print("✅ 没有需要清理的数据")
        return

    if args.confirm:
        print(f"✅ 清理完成，共删除 {len(files)} 个文件")
    else:
        # 输出待删除文件列表（供用户确认）
        print(f"📋 待清理文件 ({len(files)}个)：\n")
        for f in files:
            print(f"  🗑️  {f['path']}")
            print(f"     大小: {f['size_kb']}KB | {f['reason']}")

        print("\n" + "=" * 40)
        print("⚠️  删除前需确认泽钢")
        print("运行以下命令确认删除:")
        print("  python scripts/cleanup_data.py --confirm")
        print("=" * 40)

if __name__ == "__main__":
    main()
