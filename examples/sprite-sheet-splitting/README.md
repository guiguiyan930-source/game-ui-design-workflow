# 示例：雪碧图拆分与 PNG 压缩包

本示例将一张透明组件雪碧图自动拆成 9 个独立 PNG，并生成 ZIP 包。

## 输入

![首页组件雪碧图](../moon-palace-rpg/assets/sprites/home-ui-sheet.png)

雪碧图包含：

- 6 个圆形导航图标
- 3 个横向按钮状态
- 透明背景
- 元素之间的安全间距

## 执行

在仓库根目录运行：

```bash
python3 scripts/split_sprite_sheet.py \
  examples/moon-palace-rpg/assets/sprites/home-ui-sheet.png \
  --output-dir examples/moon-palace-rpg/assets/sprites/home-ui/items \
  --zip examples/moon-palace-rpg/packages/home-ui-png.zip \
  --mode auto \
  --prefix home-ui \
  --min-area 100 \
  --padding 8 \
  --force
```

## 输出

```text
assets/sprites/home-ui/items/
├── home-ui-001.png
├── home-ui-002.png
├── ...
├── home-ui-009.png
└── sprite-manifest.yaml

packages/
└── home-ui-png.zip
```

[下载示例 PNG 包](../moon-palace-rpg/packages/home-ui-png.zip)

ZIP 内部结构：

```text
sprite-manifest.yaml
items/
├── home-ui-001.png
├── ...
└── home-ui-009.png
```

## 检测模式

`--mode auto`：

- 有透明通道时使用 Alpha 检测。
- 完全不透明时采样边缘背景颜色。

显式模式：

```bash
--mode alpha
--mode background
```

## 常见调整

元素被拆碎：

```bash
--connect-gap 6
```

多个元素粘连：

```bash
--connect-gap 0
```

背景残留：

```bash
--background-tolerance 16
```

小图标被过滤：

```bash
--min-area 16
```

发光或阴影被裁断：

```bash
--padding 12
```

## 项目集成

- `component-contract.yaml` 定义雪碧图内应包含的组件。
- `sprite-contract.yaml` 记录检测参数、单元素坐标、路径和审核状态。
- `asset-manifest.yaml` 登记原始雪碧图和最终 ZIP。

自动切图完成后仍需人工确认裁断、粘连、背景残留和半透明边缘，确认后才把 `sprite-contract.yaml` 标记为 `approved`。
