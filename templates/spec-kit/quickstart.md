# 项目复现与验收

## 项目

- 项目 ID：`{{PROJECT_ID}}`
- 当前可交付版本：

## 输入

- 策划方案：`gdd.md`
- 产品需求：`prd.md`
- 交互逻辑：`interaction.md`
- 需求文件：`spec.md`
- 研究记录：`research.md`
- 视觉契约：`contracts/style-contract.yaml`
- 页面契约：`contracts/screen-contract.yaml`
- 组件契约：`contracts/component-contract.yaml`

## 复现步骤

1. 安装仓库中的技能。
2. 打开本项目目录并让 Agent 读取 `gdd.md`、`prd.md`、`interaction.md`、`spec.md` 与 `contracts/`。
3. 确认策划三文档为 `approved`（或已记录跳过）后再生图。
4. 按 `plan.md` 选择一个页面 ID。
5. 使用页面技能生成视觉稿，保存到 `assets/pages/`。
6. 页面批准后使用组件技能，保存到 `assets/components/`。
7. 组件输出为雪碧图时，使用拆分技能导出单元素 PNG 和 ZIP。
8. 需要开发交付时，审核 9-slice 并生成 Atlas 与引擎 JSON。
9. 更新 sprite、atlas、export contracts 与 `asset-manifest.yaml`。

## 校验

```bash
python3 scripts/validate_project.py specs/{{PROJECT_ID}}
```

## 人工验收

- [ ] 策划方案、PRD、交互逻辑已批准且与页面一致
- [ ] 画面比例与安全区正确
- [ ] 主操作清晰且信息层级稳定
- [ ] 色彩、材质、光源、描边和圆角一致
- [ ] 中文清晰，无乱码和错误商标
- [ ] 组件无粘连、无脏边、无意外裁切
- [ ] 非背景组件满足透明背景要求
- [ ] 雪碧图切片无裁断、粘连或背景残留
- [ ] PNG 压缩包可以解压且包含 manifest
- [ ] Atlas regions、9-slice 和引擎 JSON 一致

## 已知限制

- 
