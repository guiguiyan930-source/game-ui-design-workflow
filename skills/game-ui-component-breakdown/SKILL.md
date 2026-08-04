---
name: game-ui-component-breakdown
description: Breaks an approved game UI page or visual style into reusable, individually generated component assets with clean edges, transparent backgrounds where appropriate, stable naming, states, dimensions, prompts, and traceable manifest records. Use for UI slicing, transparent buttons, icons, cards, modals, navigation, characters, props, frames, labels, effects, or development handoff.
---

# 游戏 UI 组件拆解

输出独立素材或待自动切割的组件雪碧图及其契约，不重新生成完整页面。

## 前置门禁

必须读取：

- `contracts/style-contract.yaml`
- `contracts/screen-contract.yaml`
- `contracts/component-contract.yaml`
- `contracts/asset-manifest.yaml`
- 已批准页面视觉稿

源页面对应 manifest 条目必须为 `approved: true`。若未批准，停止拆解并说明需要先完成页面验收。

## 分类

- `background`：完整场景底图，无文字、按钮、导航或角色遮挡
- `control`：主按钮、次按钮、关闭、返回、领取、导航按钮
- `container`：卡片、文本框、弹窗底板、货币栏、进度条
- `icon`：资源、功能、状态和导航图标
- `character`：角色、NPC、宠物、头像
- `decoration`：边框、角标、光效、底座、丝带和粒子

## 拆解步骤

1. 确定全套拆解或指定范围。
2. 建立组件 ID、分类、用途、复用性、尺寸、状态和源页面关系。
3. 区分页面专属组件与跨页面基础组件。
4. 为每个组件写一份可独立执行的提示文件。
5. 图片工具可用时逐个生成，不把多个组件排成素材板。
6. 检查边缘、透明通道、裁切、光向和比例。
7. 更新组件契约和资源清单。

## 雪碧图模式

当用户后续需要“雪碧图拆分、单元素 PNG、ZIP 打包”时，可以先生成一张组件雪碧图作为中间产物：

- 所有元素完整、互不接触并留有明显间距。
- 使用透明背景或单一纯色背景。
- 不要文字、编号、网格线、水印和说明箭头。
- 阴影与发光不能跨到相邻元素。
- 同一组件的不同状态保持固定顺序和一致轮廓。

雪碧图不是最终切图。生成后必须调用 `game-ui-sprite-sheet-splitter` 导出独立 PNG，并完成人工验收。

最终文件名遵循[组件语义命名规范](references/naming-conventions.md)。`element-001.png` 只允许作为检测中间结果，不能作为批准交付。

## 默认规则

- 除背景外使用透明背景。
- 按钮、卡片、弹窗和标签默认不要文字，保留排版留白。
- 图标保持同一视角、光源、描边和小尺寸识别性。
- 角色完整无遮挡，姿态适合叠放到原布局。
- 装饰可叠加，不带不透明矩形底。
- 保持源页面的视觉权重；不要把次按钮生成得比主按钮更强。
- 按钮、面板、弹窗和进度条填写 `slice` 元数据；9-slice margins 需要人工预览确认。

## 单组件提示文件

保存为 `prompts/components/<component-id>.md`：

```markdown
# <组件名称>

## 来源与用途
## 尺寸和状态
## 必须继承的契约字段
## 图像生成提示词
## 反向限制
## 验收记录
```

提示词必须明确：

- “单独的游戏 UI 组件素材”
- 组件类别、用途、目标尺寸与状态
- 色调、材质、光向、描边、厚度和圆角
- 是否透明、是否无文字、中心构图和安全边距
- 高清、完整轮廓、适合合成和开发
- 不生成完整页面、不粘连其他组件

## 特殊规则

### 背景

无 UI 控件、文字、按钮、导航和前景角色；需要延展时要求边缘自然连续。

### 按钮与容器

空白文字区、完整边框、真实点击质感；为状态生成独立文件，不在一张图中拼版。

### 图标

小尺寸可识别、无文字、统一透视；除非契约要求，不附带底板。

### 角色

完整轮廓、无遮挡、透明背景；不得复刻未经授权的受保护角色。

## 验收

- 文件路径、组件 ID 和源页面可追踪
- 非背景组件透明要求正确
- 没有文字、乱码、脏边、背景残留或意外裁切
- 状态之间轮廓稳定，视觉差异符合契约
- 文件名使用 `<component-id>-<state>-v<数字>.<ext>`
- 每个资源在 manifest 中单独登记

工具不可用时保留提示词，将状态设为 `pending-generation`，不得伪造透明素材。
