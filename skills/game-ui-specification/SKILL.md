---
name: game-ui-specification
description: Creates and maintains production-oriented game UI specifications and shared visual contracts covering color, typography, layout, geometry, components, interaction states, adaptation, and image-generation constraints. Use when users ask for a game UI design system, visual rules, standardization, or consistent downstream page and asset generation.
---

# 游戏 UI 规范

输出能被页面延展、生图、组件拆解和开发共同读取的规则，不只描述“高级、统一、美观”。

## 输入

优先读取：

- `spec.md`：玩法、平台、比例、范围和验收标准
- `research.md`：参考图抽象与版权约束
- `contracts/style-contract.yaml`：现有契约

独立调用且没有项目目录时，在回答中使用相同字段结构，并建议用户创建项目。

## 工作流

1. 明确玩法中的高频操作和信息优先级。
2. 从参考图提取风格语言，不复刻具体角色、商标或完整页面。
3. 选择适配目标平台的参考尺寸、安全区和密度。
4. 定义颜色、字体、几何、材质、光源、图标视角和状态。
5. 更新 `style-contract.yaml`；未知值不得用“待定”掩盖，应给出可调整的默认值。
6. 检查每条规则能否被页面和组件提示词引用。

全局值与语义别名按[设计 Token 规范](references/design-tokens.md)维护；`style-contract.yaml` 是单一事实来源，不另建冲突的平行 Token 文件。

## 必需规范

### 平台与布局

- 目标平台、方向、比例、参考尺寸
- 顶、右、底、左安全区
- 顶部状态区、中间内容区、底部导航和悬浮入口
- 刘海屏、长文本、横竖屏或宽屏策略

### 视觉语言

- 主题、情绪、复杂度、材质
- 主光方向、阴影软硬和高光语言
- 主色、辅色、强调、背景、警告、奖励、禁用色
- 对比度、饱和度和稀有度颜色规则

### 字体

- 标题、模块标题、正文、数字、按钮的尺寸与字重
- 中文可读性、描边、投影和小尺寸限制
- 生图文字不可靠时的后期排版策略

### 几何与组件

- 小组件、卡片和弹窗圆角
- 描边等级、按钮高度、图标尺寸
- 按钮、图标、卡片、弹窗、进度条、导航、奖励框、货币栏
- 默认、按下、选中、禁用、加载、锁定、已领取状态

### 交互

- 点击、切页、弹窗、奖励、任务、排行和购买确认反馈
- 动效持续时间建议与减少动态效果选项
- 网络错误、资源不足、冷却和过期状态

## 契约规则

- 使用明确色值或色相范围；颜色字段不能只写“高级金色”。
- 同一组件状态只能有一套定义。
- 所有页面共享光向、材质词汇、圆角等级和图标视角。
- 若修改已批准契约，将依赖资源标记为 `stale`，不要静默覆盖。
- 完成评审后把 `status` 设为 `approved`。

## 输出

1. 一段说明玩法如何决定视觉规则。
2. 更新后的 `contracts/style-contract.yaml`。
3. 关键决策与风险写入 `research.md`。
4. 受影响的任务写入 `tasks.md`。

## 检查

- 数值、范围、状态和适用场景明确
- 规则适合目标平台与触控热区
- 主操作对比强于次操作
- 文字和数字在复杂背景上可读
- 页面和组件提示词可以直接引用契约字段
