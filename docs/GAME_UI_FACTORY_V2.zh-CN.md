# Game UI Factory v2 架构

Factory v2 把仓库从“页面图片生成”扩展为可验证的 UI 资产交付流水线。

## 流水线

```text
需求与参考图
→ style-contract + design tokens
→ screen / component contracts
→ 页面视觉与无文字组件雪碧图
→ 自动像素分离 + 人工语义 mapping
→ 独立透明 PNG + ZIP
→ 人工审核 9-slice
→ Atlas PNG + JSON
→ Godot / Unity / Cocos JSON handoff
```

## 九层能力映射

1. Design：已有 Spec-Kit 与 `style-contract.yaml`
2. Component：已有组件契约、提示词和无文字素材规则
3. Vision：当前只支持透明/纯色背景连通区域检测
4. Sprite Splitter：已实现 padding、背景移除、透明 PNG 与 ZIP
5. NinePatch：已实现元数据和合法性校验；自动推断未实现
6. Atlas：已实现确定性、不旋转的 PNG + JSON 打包
7. Engine Export：已实现 Godot、Unity、Cocos JSON 清单
8. Dataset：结构化契约可作为数据基础；训练格式导出未实现
9. Design Token：扩展现有 style contract，不建立平行体系

## 单一事实来源

- 全局视觉：`style-contract.yaml`
- 页面结构：`screen-contract.yaml`
- 组件语义与切图方式：`component-contract.yaml`
- 切片坐标与文件：`sprite-contract.yaml`
- Atlas regions：`atlas-contract.yaml`
- 引擎目标：`export-contract.yaml`
- 全局页面、雪碧图与包：`asset-manifest.yaml`

## 为什么不自动语义识别

内置切图脚本只根据 Alpha 或背景色分离像素区域。它不能可靠判断一个区域是“购买按钮”还是“分类标签”。因此通过有序 mapping 将检测结果绑定到已知组件契约，保证结果可复现、可审核。

## 9-slice

当前 margins 由 Agent 或设计师根据组件结构填写，再由校验器确保：

- 四个值非负
- 左右之和小于宽度
- 上下之和小于高度
- Atlas 和引擎 JSON 使用同一组 margins

自动分析 corner、border 和 center 属于路线图。

## 引擎交付边界

内置 exporter 生成 JSON handoff：

- Godot：region 与 patch margins
- Unity：Sprite Multiple rect、pivot 与 border
- Cocos：frame rect 与 cap insets

它不调用引擎 SDK，不创建原生 `.tres`、`.tscn`、`.meta`、SpriteAtlas 或项目场景。文档和契约不得把 JSON handoff 描述为原生导入完成。

完整实例见 [Factory v2 商店案例](../examples/factory-v2-shop/README.md)。
