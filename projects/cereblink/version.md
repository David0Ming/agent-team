# CerebLink v1.3.1

## 当前状态
- 双用户隔离已落地：`zegang` / `dengjingjing`
- 路由已支持：profile → userId；泽钢已配 feishu open_id
- 测试通过：51 passed
- 学习闭环已升级为：learn / review / clarification / cardify / planning_update / profile_update
- 收口资产已接入：session / mastery / review queue / concept card / question card / topic page / today / summary / profile

## 本版新增
- 学习动作路由层：显式产出 `actionType / closureMode / profileUpdate / reason`
- `closureMode` 已开始真正驱动收口行为，而不再只是隐式流程
- `cardify / clarification` 已接入 concept card + question card + topic page
- `planning_update` 已做真分叉：只更新 planning 侧状态，不污染知识学习资产
- `profile_update` 已接入最小可用写入链路
- 强结构 concept card 模板已进入默认收口链

## 当前缺口
- `question_card` 仍是最小实现，问题类型与抽象质量还不够强
- `topic_page` 目前主要是挂接资产，还没维护专题状态
- `profile_update` 还是规则版，不是稳定的结构化抽取版
- 邓菁菁仍缺 feishu open_id 精确路由
- workspace 与 Obsidian live vault 仍需注意同步边界

## 下一步
- 把 `topic_page` 升级成真正的专题状态页
- 提升 `question_card` 的问题抽象质量
- 升级 `profile_update` 为更稳定的结构化更新
- 补邓菁菁 open_id 路由
