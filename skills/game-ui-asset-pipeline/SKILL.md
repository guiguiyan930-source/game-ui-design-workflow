---
name: game-ui-asset-pipeline
description: Packs semantically named transparent game UI PNG files into an atlas, preserves component states and reviewed 9-slice metadata, and exports deterministic JSON handoff manifests for Godot, Unity, Cocos, or generic consumers. Use after sprite-sheet splitting when users ask for atlas packing, nine-patch metadata, engine delivery, Unity sprites, Godot regions, Cocos frames, or a Game UI Factory production handoff.
---

# 游戏 UI Atlas 与引擎交付

把已经批准的语义 PNG 转换成 Atlas 与引擎 JSON。此技能不执行像素识别，不自动猜测语义，也不声称生成原生引擎工程文件。

## 前置条件

- `sprite-contract.yaml` 状态为 `approved`
- 所有 PNG 使用语义名称
- 每个 item 关联 `component_id`、`state` 和 `slice`
- `review.text_free: true`
- 9-slice margins 已人工预览

## 切图方式

- `9-slice`：按钮、面板、弹窗、进度条
- `full`：卡片、角色、徽章、背景
- `1:1`：图标、货币
- `tile`：可重复纹理

9-slice margins 格式：

```yaml
slice:
  type: 9-slice
  margins: [left, right, top, bottom]
```

## Atlas

读取 `contracts/atlas-contract.yaml`，执行：

```bash
python3 scripts/build_sprite_atlas.py specs/<project-id> --force
```

内置打包器：

- 使用透明 PNG
- 不旋转素材
- 可补齐到 2 的幂尺寸
- 保存 region、pivot、state、component ID 和 slice
- 生成 Atlas PNG 与 JSON
- 更新 atlas contract 为 `packed`

打包完成后人工检查，再将状态改为 `approved`。

## 引擎 JSON

读取 `contracts/export-contract.yaml`，执行：

```bash
python3 scripts/export_engine_manifest.py specs/<project-id> --force
```

支持：

- Godot JSON：texture、region、patch margins
- Unity JSON：Sprite Multiple rect、pivot、border、pixels per unit
- Cocos JSON：frame rect、original size、cap insets
- Generic JSON：Atlas 与 sprite metadata

这些文件是确定性交付清单。原生 `.tres`、`.tscn`、Unity SpriteAtlas 和 Cocos 工程导入器不在内置实现范围内。

## 人工验收

- Atlas 无重叠、裁断和透明污染
- region 与源 PNG 尺寸一致
- 9-slice 留有可拉伸中心
- 所有语义名称唯一
- 引擎 JSON 引用同一 Atlas
- 禁止把 native project files 标记为已生成

## 完成定义

- `atlas-contract.yaml` 状态为 `approved`
- Atlas PNG 与 JSON 存在
- `export-contract.yaml` 状态为 `approved`
- 每个目标引擎 JSON 存在并可解析
- 项目严格校验通过
