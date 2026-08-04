# Roadmap

以下能力来自 Factory v2 设想，但尚未由仓库内置实现。它们不能在 README、技能或案例中被描述为已完成。

## Vision

- Grounding DINO 组件候选检测
- SAM2 精细分割
- OCR 文字区域检测
- 组件与 component contract 自动语义匹配

## Image repair

- 自动去文字与底板纹理修复
- 阴影分层与可配置移除
- 粘连、遮挡组件的像素恢复

## NinePatch

- 从像素自动识别 corner、border、center
- 自动推荐并预览 9-slice margins
- 多尺寸拉伸回归测试

## Native engine integrations

- Godot `.tres`、`.tscn` 与 Theme 插件
- Unity SpriteAtlas、`.meta` 与 Editor importer
- Cocos plist、meta 与项目导入器

## Dataset

- YOLO bounding-box 导出
- SAM2 mask 数据集
- 标注审核和模型版本追踪

这些能力在实现、测试和示例验证完成前，只作为路线图存在。
