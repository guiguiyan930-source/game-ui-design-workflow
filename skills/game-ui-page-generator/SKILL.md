---
name: game-ui-page-generator
description: Designs and generates one complete game UI page at a time using an approved style and screen contract, producing a page brief, reproducible image prompt, negative constraints, an actual visual asset when image generation is available, and a manifest entry. Use for home, task, ranking, shop, inventory, character, event, reward, settlement, login, onboarding, HUD, or other game screens.
---

# 游戏 UI 单页视觉生成

一次只完成一个页面，继承项目契约，不把连续页面做成互不相关的风格稿。

## 前置条件

读取：

- `spec.md` 与 `research.md`
- `contracts/style-contract.yaml`
- 目标页面在 `contracts/screen-contract.yaml` 中的条目
- 已批准的基准页面及 `asset-manifest.yaml`

若样式契约仍为 `draft`，可以生成探索稿，但资源不得标记为已批准。

## 页面步骤

1. 确认页面 ID、目的、主操作、状态和比例。
2. 建立信息层级：主视觉、主操作、资源状态、导航、次级入口。
3. 具体说明顶部、中部、底部和悬浮区域，不只写通用布局名称。
4. 列出按钮、卡片、图标、角色、状态栏、导航、气泡和装饰。
5. 从样式契约注入色值、材质、光向、圆角、描边和字体策略。
6. 生成完整正向提示词和反向限制。
7. 图片工具可用时实际生图；不可用时保留提示词并降级。
8. 保存提示与图片，更新页面契约和资源清单。

## 提示文件

保存为 `prompts/pages/<screen-id>.md`，结构必须为：

```markdown
# <页面名称>

## 页面定位
## 视觉约束
## 布局与组件
## 状态
## 图像生成提示词
## 反向限制
## 验收记录
```

正向提示词必须包含：

- 页面名称、游戏类型、平台、比例和参考尺寸
- 顶中底及辅助区域的具体内容
- 主角色、场景或核心玩法焦点
- 契约中的色彩、材质、光源、圆角、描边和图标语言
- 可点击质感、信息层级、中文策略、画面质量
- 与已批准基准页保持一致的要求

反向限制至少包含：

- 乱码、错误文字、商标和未经授权角色
- 按钮变形、错误透视、元素粘连、主体遮挡
- 信息层级混乱、过度复杂、低清晰度
- 违反契约的色调、光向、材质或圆角

## 图片生成

图片工具可用时：

1. 使用工具支持的最接近比例。
2. 文件名使用 `<screen-id>-v<数字>.<ext>`。
3. 将结果保存到 `assets/pages/`。
4. 在 manifest 记录真实路径、尺寸、状态和版本来源。
5. 生图中文字不可读时，不通过验收；生成无文字底板或安排后期排字。

图片工具不可用时：

- 不创建假图片
- `status: pending-generation`
- `approved: false`
- 提示词路径必须有效

## 页面批准

只有同时满足以下条件才把 `approved` 设为 `true`：

- 主操作清楚，页面目的成立
- 比例、安全区和导航合理
- 契约中的视觉语言一致
- 关键状态有对应方案
- 文字可读或已明确采用后期排版
- 用户确认或项目验收规则明确通过

## 输出

- 页面说明与提示文件
- 实际视觉稿或明确的待生成状态
- 更新后的 `screen-contract.yaml`
- 更新后的 `asset-manifest.yaml`
- 后续组件拆解建议
