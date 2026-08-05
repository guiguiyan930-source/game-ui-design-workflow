# 项目复现与验收

## 项目

- 项目 ID：`guofeng-card-rpg`
- 当前可交付版本：主城/编队/背包/战斗已批准；home-ui Atlas 与三引擎 JSON 已导出

## 输入

- 策划方案：`gdd.md`（approved）
- 产品需求：`prd.md`（approved）
- 交互逻辑：`interaction.md`（approved）
- 需求文件：`spec.md`
- 研究记录：`research.md`
- 视觉契约：`contracts/style-contract.yaml`
- 页面契约：`contracts/screen-contract.yaml`
- 组件 / 雪碧图 / Atlas / 导出契约：`contracts/`

## 复现步骤

1. 安装仓库技能并读取 `examples/guofeng-card-rpg`（含策划三文档）。
2. 主城基准页已批准：`assets/pages/home-v1.png`。
3. 编队、背包、战斗 HUD 视觉已批准（`formation-v1` / `bag-v1` / `battle-v1`）。
4. 语义 PNG 包：`packages/home-ui-png.zip`。
5. Atlas：`assets/atlases/home-ui.png` + `home-ui.json`。
6. 引擎 JSON：`exports/godot|unity|cocos/home-ui.json`。

## 校验

```bash
python3 scripts/validate_project.py examples/guofeng-card-rpg --strict
```

## 人工验收

- [x] 策划方案、PRD、交互逻辑已批准
- [x] 主城已批准为风格基准
- [x] 编队 / 背包 / 战斗已批准
- [x] 组件无文字、透明 PNG 与 ZIP 完整
- [x] Atlas regions、9-slice 与三引擎 JSON 一致
- [ ] 生产前将页面重生或裁切为精确 1080×1920
- [ ] 抽卡与商店仍待逐页批准

## 已知限制

- 生图实际尺寸为 1024×1536（约 2:3），不是精确 9:16 契约尺寸。
- 引擎导出为 JSON handoff，不是原生 `.tres` / SpriteAtlas / Cocos 工程文件。
- 抽卡与商店仍为探索稿，尚未逐页批准。
