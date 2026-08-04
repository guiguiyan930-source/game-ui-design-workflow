# 切图方式与 9-slice 规则

## 默认切图方式

- Button、Frame、Popup、Panel、Progress：`9-slice`
- Card、Badge、Character、NPC、Decoration、Background：`full`
- Icon、Currency：`1:1`
- 可重复纹理：`tile`

默认值见仓库 `config/slice-rules.yaml`。

## 9-slice

```yaml
slice:
  type: 9-slice
  margins: [left, right, top, bottom]
```

要求：

- `left + right < width`
- `top + bottom < height`
- 四角和描边不得进入中心拉伸区
- 文字不能烘焙在可拉伸底板中
- margins 必须在实际目标尺寸下人工预览

内置工具只保存并校验 margins，不从像素自动推断拉伸区。自动九宫格分析属于路线图能力。
