---
name: game-ui-extension
description: Extends a game concept or partial interface into a coherent screen system, player journey, feature flow, prioritized screen inventory, states, edge cases, and implementation-ready screen contracts. Use when users ask to expand an existing game UI, add related pages, audit missing screens, or plan a complete UI ecosystem.
---

# 游戏 UI 延展

从玩法和玩家旅程选择必要页面，不默认堆满所有常见系统。

## 输入

读取 `spec.md`、`research.md`、`contracts/style-contract.yaml`、`plan.md` 和 `contracts/screen-contract.yaml`。若用户只给一张图，先判断它在核心循环中的位置。

需要完整分类审计时读取 [references/screen-taxonomy.md](references/screen-taxonomy.md)；普通延展不必把分类全量载入。

## 玩家旅程

按适用范围检查：

1. 启动与首次进入：启动、登录、公告、选服、创建角色、教程。
2. 核心玩法：大厅、任务、准备、关卡、战斗 HUD、暂停、结算。
3. 成长管理：角色、装备、技能、突破、背包、图鉴、成就。
4. 经济商业：商店、抽卡、通行证、订阅、兑换、广告奖励。
5. 活动回流：签到、日常、活动中心、限时挑战、回归。
6. 社交竞争：好友、公会、聊天、邮件、档案、排行、赛季。
7. 策略表达：编队、卡组、预设、天赋、外观、家园。
8. 支持设置：设置、控制、无障碍、账号、客服、兑换码。

只选择服务题材、平台、核心循环、留存和商业模式的页面。

## 屏幕优先级

- `must-have`：没有它就无法完成核心循环或安全交付。
- `genre-specific`：由玩法决定，例如卡牌编队或射击配装。
- `optional`：增强留存、表达或运营，但不阻断首版。

## 每个页面的契约

写入 `screen-contract.yaml`：

- `id`：稳定的小写连字符 ID
- `purpose`：解决的玩家问题
- `entry_points`：从哪里进入
- `primary_actions`：最重要的 1–3 个动作
- `dependencies`：前置页面或系统
- `layout`：顶部、中部、底部、悬浮区域
- `components`：可复用与页面专属组件
- `states`：默认、加载、空、锁定、可领取、冷却、错误等
- `edge_cases`：背包已满、活动过期、断网、资源不足等
- `data_needs`：货币、计时器、等级、库存、社交状态等

## 延展步骤

1. 写出核心循环和首次进入到日常回流的路径。
2. 将用户已有页面放入旅程，找出真正的断点。
3. 选择页面并标注优先级；合并功能重复的入口。
4. 为每页补齐契约，确保主操作三秒内可识别。
5. 在 `plan.md` 按依赖与价值排序，不按页面名称排序。
6. 规划页面生成批次：先基准页，再复用度高的系统页，最后运营页。

## 设计约束

- 大厅只保留有限高优入口，次级活动进入活动中心。
- 高频动作支持一键领取、批量操作、筛选、预设或跳转来源。
- 商城、抽卡和排行清楚显示价格、概率、结算时间与规则。
- HUD 不遮挡核心玩法区域，并适配输入方式。
- 每页沿用样式契约；延展改变功能重点，不另起视觉系统。

## 输出

- `plan.md` 中的屏幕路线、生成批次和依赖
- 完整 `screen-contract.yaml`
- `tasks.md` 中按 `[extension]`、`[page]` 分仓标记的任务
- 缺口、合并理由和风险摘要

## 检查

- 从首次进入到重复回流路径闭合
- 结算能回到成长或下一局
- 页面没有无入口或无出口的孤岛
- 关键系统含空、锁定、错误和资源不足状态
- 页面数量与项目阶段相称
