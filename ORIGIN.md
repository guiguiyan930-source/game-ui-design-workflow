# 项目来源与演进说明

Game UI Design Workflow 由作者此前创建并维护的四个游戏 UI 技能仓库整合演进而来：

- [Game-UI-Extension](https://github.com/guiguiyan930-source/Game-UI-Extension)：游戏 UI 屏幕系统、玩家旅程和页面延展。
- [game-ui-page-generator](https://github.com/guiguiyan930-source/game-ui-page-generator)：单页游戏 UI 方案、提示词和视觉生成。
- [game-ui-specification](https://github.com/guiguiyan930-source/game-ui-specification)：色彩、字体、布局、组件和交互规范。
- [game-ui-component-breakdown](https://github.com/guiguiyan930-source/game-ui-component-breakdown)：页面组件拆解、透明素材和开发交付。

这些仓库均属于同一作者的早期实践，不是本项目引入的第三方技能。

## 为什么整合

早期仓库分别解决单一阶段问题，但跨阶段使用时仍需要人工传递视觉规则、页面状态和资源信息。本项目将它们统一为一条可复现工作流：

```text
原型生成视觉
  → UI 风格切换与批准
  → UI 页面延展与逐页生成
  → UI 组件拆解与雪碧图生成
  → 单元素 PNG 拆分、ZIP 打包与严格校验
  → 语义命名、9-slice、Atlas 与引擎 JSON
```

## 本项目新增能力

- `game-ui-workflow` 总控技能和阶段路由
- Spec-Kit 风格的需求、研究、计划、任务与复现文档
- 样式、页面、组件和资源四类核心契约，以及可选雪碧图拆分契约
- 页面批准、版本保留和资源失效门禁
- 雪碧图自动检测、单元素透明 PNG 导出和 ZIP 打包
- 设计 Token、语义 mapping、Atlas 与多引擎 JSON handoff
- 实际图片尺寸、PNG Alpha 通道和 SVG 尺寸校验
- 项目初始化、一键安装、自动化测试和 GitHub Actions
- 完整项目、风格切换、页面延展与组件包示例

## 后续维护

统一仓库是后续功能、规范和发布的主要维护入口。早期仓库可继续作为单项能力的历史记录和轻量入口；涉及跨阶段契约、自动化校验和完整交付时，以本仓库为准。

本统一仓库中的原创整合内容按根目录 [MIT License](LICENSE) 发布。
