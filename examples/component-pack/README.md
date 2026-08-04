# 示例：UI 组件包拆解

目标：从已批准首页生成可复用的背景、控件、导航和资源图标组件包。

## 前置门禁

- 页面资源在 manifest 中为 `approved: true`
- `style-contract.yaml` 已批准
- `component-contract.yaml` 指向正确源页面
- 用户已确认拆解范围和组件状态

页面未批准时，组件技能应停止。

## 拆解调用

```text
使用 game-ui-component-breakdown。
读取 @examples/moon-palace-rpg 的已批准 home 页面和全部 contracts。

拆解以下组件：
1. 首页背景：无角色、按钮、文字、导航和 UI 控件；
2. 主按钮：默认、按下、禁用，空白文字区；
3. 底部导航：首页、编队、角色、背包、召唤、活动；
4. 资源图标：金币、月玉、体力；
5. 装饰：月牙选中光效、红点和卡片金边。

要求：
- 除背景外全部透明背景；
- 每个组件和状态独立生成；
- 不要组件拼板，不要文字；
- 文件名包含 component-id、state、version；
- 每项保存独立提示词并登记 manifest。
```

## 推荐命名

```text
home-background-default-v1.png
primary-button-default-v1.png
primary-button-pressed-v1.png
primary-button-disabled-v1.png
nav-home-default-v1.png
nav-home-selected-v1.png
currency-gold-default-v1.png
effect-nav-crescent-selected-v1.png
```

## 检查顺序

1. 源页面与组件 ID 是否可追踪。
2. PNG 实际尺寸是否等于 manifest。
3. 非背景 PNG 是否真的包含 Alpha 通道。
4. 边缘是否有脏边、背景残留或意外裁切。
5. 同组图标是否使用同一透视、光向和描边。
6. 默认、按下和禁用状态是否保持轮廓稳定。
7. 主按钮是否比次按钮具有更高视觉权重。

## 工具不支持透明背景

```text
当前图片工具不能可靠输出透明 PNG。
保留完整提示词，将状态标为 pending-generation。
可确定性绘制的简单控件允许使用透明 SVG 降级，
但必须在 manifest notes 中说明，不能伪造透明 PNG。
```

## 验收

```bash
python3 scripts/validate_project.py examples/moon-palace-rpg --strict
```

校验脚本会读取 PNG 与 SVG 的真实尺寸，并检查要求透明的 PNG 是否具有 Alpha 通道。

如果组件以雪碧图形式生成，继续执行
[雪碧图拆分与 PNG 打包](../sprite-sheet-splitting/README.md)，不能把组件合图直接当作最终切图。

## 完成标准

- 每个组件有独立契约、提示词和资源条目
- 文件真实尺寸与 manifest 一致
- 透明背景要求已通过文件级检查
- 页面专属与跨页复用组件分类清楚
- 未生成资源明确标记 `pending-generation`
