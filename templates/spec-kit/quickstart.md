# 项目复现与验收

## 项目

- 项目 ID：`{{PROJECT_ID}}`
- 当前可交付版本：

## 输入

- 需求文件：`spec.md`
- 研究记录：`research.md`
- 视觉契约：`contracts/style-contract.yaml`
- 页面契约：`contracts/screen-contract.yaml`
- 组件契约：`contracts/component-contract.yaml`

## 复现步骤

1. 安装仓库中的五个技能。
2. 打开本项目目录并让 Agent 读取 `spec.md` 与 `contracts/`。
3. 按 `plan.md` 选择一个页面 ID。
4. 使用页面技能生成视觉稿，保存到 `assets/pages/`。
5. 页面批准后使用组件技能，保存到 `assets/components/`。
6. 更新 `contracts/asset-manifest.yaml`。

## 校验

```bash
python3 scripts/validate_project.py specs/{{PROJECT_ID}}
```

## 人工验收

- [ ] 画面比例与安全区正确
- [ ] 主操作清晰且信息层级稳定
- [ ] 色彩、材质、光源、描边和圆角一致
- [ ] 中文清晰，无乱码和错误商标
- [ ] 组件无粘连、无脏边、无意外裁切
- [ ] 非背景组件满足透明背景要求

## 已知限制

- 
