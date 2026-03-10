#!/usr/bin/env python3
"""
容错处理器
实现重试、降级、隔离策略
"""
import time

def retry_with_backoff(func, max_retries=3):
    """重试策略（指数退避）"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise e
            time.sleep(2 ** i)  # 指数退避

def with_fallback(primary_func, fallback_func):
    """降级策略"""
    try:
        return primary_func()
    except Exception:
        return fallback_func()

if __name__ == "__main__":
    print("容错处理器已就绪")
