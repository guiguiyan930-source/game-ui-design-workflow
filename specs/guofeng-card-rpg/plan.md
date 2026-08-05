# UI 实施计划

## 项目概览

- 项目 ID：`guofeng-card-rpg`
- 目标：交付一套深蓝鎏金国风卡牌 RPG UI 的可复现项目
- 当前阶段：主城/编队/背包/战斗已批准；抽卡与商店待批准

## 阶段

0. 策划：批准 `gdd.md` / `prd.md` / `interaction.md`（已完成）
1. 规范：完成 `style-contract.yaml`
2. 延展：完成屏幕地图和 `screen-contract.yaml`
3. 页面：逐页生成、审核并登记视觉稿
4. 拆解：从已批准页面生成独立组件
5. 雪碧图：将组件合图切成单元素 PNG 并打包
6. 资产交付：确认语义命名和 9-slice，生成 Atlas 与引擎 JSON
7. 验收：运行校验并补齐复现说明

## 屏幕路线

| 顺序 | 页面 ID | 页面 | 模块 | 优先级 | 依赖 | 状态 |
|---:|---|---|---|---|---|---|
| 1 | `home` | 主城 | core | must-have | wallet | approved |
| 2 | `formation` | 编队 | core | must-have | roster | approved |
| 3 | `gacha` | 抽卡 | economy | must-have | wallet | generated |
| 4 | `shop` | 商店 | economy | must-have | wallet | generated |
| 5 | `bag` | 背包 | core | must-have | inventory | approved |
| 6 | `battle` | 战斗 HUD | core | must-have | formation | approved |

## 页面生成批次

- 批次 1：主城原型视觉（已批准）
- 批次 2：抽卡、商店探索视觉
- 批次 3：编队、背包、战斗 HUD（已批准）

## 组件拆解范围

- 首个批准页面：`home`
- 复用组件：主按钮、导航图标、货币图标、卡片框
- 页面专属组件：主城背景与角色舞台

## 质量门禁

- [x] `gdd.md` / `prd.md` / `interaction.md` 已批准
- [x] `spec.md` 无阻断性未决事项
- [x] 样式契约字段完整
- [x] 页面 ID 与屏幕契约一致
- [x] 页面批准后才允许拆解（主城已批准）
- [x] 资源均登记到 manifest
- [x] 校验脚本通过
