# 项目复现与验收

## 项目

- 项目 ID：`factory-v2-shop`
- 当前可交付版本：Factory v2 shop case v1

## 输入

- 需求文件：`spec.md`
- 研究记录：`research.md`
- 视觉契约：`contracts/style-contract.yaml`
- 页面契约：`contracts/screen-contract.yaml`
- 组件契约：`contracts/component-contract.yaml`

## 复现步骤

1. 安装仓库中的全部技能。
2. 打开本项目目录并让 Agent 读取 `spec.md` 与 `contracts/`。
3. 按 `plan.md` 选择一个页面 ID。
4. 使用页面技能生成视觉稿，保存到 `assets/pages/`。
5. 页面批准后生成无文字组件雪碧图。
6. 使用 `--mapping mappings/shop-components.yaml` 导出语义 PNG 和 ZIP。
7. 运行 `build_sprite_atlas.py` 生成 Atlas。
8. 运行 `export_engine_manifest.py` 生成三种引擎 JSON。
9. 重新检查生成结果后批准 atlas 和 export contracts。

## 校验

```bash
python3 scripts/validate_project.py examples/factory-v2-shop --strict
```

## 人工验收

- [x] 画面比例与安全区正确
- [x] 主操作清晰且信息层级稳定
- [x] 色彩、材质、光源、描边和圆角一致
- [x] 页面文字可读，组件素材无文字
- [x] 组件无粘连、无脏边、无意外裁切
- [x] 非背景组件满足透明背景要求
- [x] 雪碧图切片无裁断、粘连或背景残留
- [x] PNG 压缩包可以解压且包含 manifest
- [x] Atlas regions 与三种引擎 JSON 一致

## 已知限制

- 公开分享不嵌入上传图片；用户后续提供的三张案例图片保存在 `references/`，页面视觉仍为独立重构。
- 自动组件检测、自动去字修复、自动九宫格推断和原生引擎工程文件未实现。
