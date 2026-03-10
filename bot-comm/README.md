# Bot通讯目录

## 目录结构
- `local-to-mac/` - local发给mac的消息
- `mac-to-local/` - mac发给local的消息  
- `shared/` - 共享文档

## 通讯协议
1. 发送消息：在对应目录创建 `YYYY-MM-DD-HHmmss-{topic}.md`
2. 读取消息：定期扫描对应目录
3. 已读标记：读取后重命名为 `*.read.md`

## 当前任务
- local → mac: 升级指导方案
