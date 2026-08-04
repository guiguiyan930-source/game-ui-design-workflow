# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/)。

## [0.3.0] - 2026-08-05

### Added

- Game UI Factory v2 欧美卡通生存商店完整案例。
- 语义 mapping，将自动切片序号转换为稳定组件名称。
- 组件切图方式与人工审核 9-slice 元数据。
- 确定性 Atlas PNG + JSON 打包脚本。
- Godot、Unity、Cocos JSON handoff 导出脚本。
- `game-ui-asset-pipeline` 技能、设计 Token 和语义命名规范。
- Atlas / export 可选契约、JSON Schema、配置与路线图说明。

### Changed

- 总控流程从六类视觉产物扩展到开发资产交付。
- 严格校验覆盖语义切片、9-slice、Atlas 与引擎 JSON。

## [0.2.1] - 2026-08-04

- 强制雪碧图元素去掉标题、按钮文案、数字标签、水印和文字残影；批准包必须通过 `review.text_free` 人工验收。

## [0.2.0] - 2026-08-04

### Added

- README 中独立的使用场景、30 秒使用方法和文档快速入口。
- UI 风格切换前后视觉对比与完整效果演示。
- Cursor、Python、资源格式和中文文字兼容性说明。
- 隐私、版权、生成图片审查和 GitHub 协作安全指南。
- 契约字段、Schema 版本和已批准资源的迁移指南。
- 支持项目级、个人级、强制更新和预览模式的一键安装脚本。
- 5 个安装脚本自动化测试。
- 将第三方声明替换为同一作者早期技能仓库的项目来源与演进说明。
- 新增 `game-ui-sprite-sheet-splitter`，支持透明或纯色背景雪碧图自动检测、单元素透明 PNG 导出、坐标 manifest 和 ZIP 打包。
- 新增可选 `sprite-contract.yaml`、雪碧图项目校验、完整示例和 4 个拆分测试。

## [0.1.0] - 2026-08-04

首个公开版本。

### Added

- `game-ui-workflow` 总控技能，提供原型视觉、风格切换、页面延展和组件拆解的分步指引与人工门禁。
- UI 规范、UI 延展、单页生成、组件拆解四个独立技能。
- Spec-Kit 风格项目文档和样式、页面、组件、资源四类 YAML 契约。
- 项目初始化、项目校验和技能格式校验脚本。
- PNG 实际尺寸、PNG Alpha 通道和 SVG 尺寸检查。
- 8 个初始化与验证单元测试。
- GitHub Actions 自动运行测试、技能校验和完整示例严格校验。
- “月宫列传”完整项目，以及风格切换、页面延展和组件包拆解操作示例。
- 中文技能调用指南、贡献指南、Issue 模板和 PR 模板。

[0.3.0]: https://github.com/guiguiyan930-source/game-ui-design-workflow/releases/tag/v0.3.0
[0.2.1]: https://github.com/guiguiyan930-source/game-ui-design-workflow/releases/tag/v0.2.1
[0.2.0]: https://github.com/guiguiyan930-source/game-ui-design-workflow/releases/tag/v0.2.0
[0.1.0]: https://github.com/guiguiyan930-source/game-ui-design-workflow/releases/tag/v0.1.0
