#!/usr/bin/env python3
"""
熔断器实现
防止API连续失败导致资源浪费
"""
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None
    
    def call(self, func):
        """执行函数调用，带熔断保护"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("熔断器打开，拒绝请求")
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        """成功时重置"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def on_failure(self):
        """失败时计数"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

if __name__ == "__main__":
    print("熔断器已就绪")
