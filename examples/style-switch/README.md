# 示例：UI 风格切换

目标：把“月宫列传”从深蓝鎏金切换为青白玉石风格，同时保持首页结构、主操作和导航不变。

## 前置条件

- `style-contract.yaml` 已存在
- `home-v1` 已登记但不需要覆盖
- 首页的信息架构已经通过

## 调用

```text
使用 game-ui-workflow，执行“UI 风格切换”。
读取 @examples/moon-palace-rpg 和 home-v1。

保持首页的信息结构、角色占位、主按钮位置和六项底部导航不变，
将视觉切换为“青白玉石、冷月银、轻盈半透明”：
- 主色：青白玉与月银
- 辅色：低饱和湖蓝
- 材质：半透明玉、磨砂玻璃、细银边
- 光源：左上柔和冷光
- 禁止：暖金主色、厚重金属和高密度纹理

先把候选规则写入 research.md，再生成独立 style-contract 候选和 home-v2。
不要覆盖 home-v1，不要开始页面延展。
完成后比较两个版本的色彩、材质、光源、圆角、图标和可读性。
```

## 预期文件变化

```text
research.md                         # 记录候选风格和取舍
contracts/style-contract.yaml       # 选择前保持 draft 或候选状态
prompts/pages/home-v2.md            # 新风格页面提示词
assets/pages/home-v2.*              # 新版本视觉稿
contracts/asset-manifest.yaml       # v1 与 v2 均保留
```

## 人工门禁

检查：

- 信息层级是否与 v1 相同
- 风格变化是否落实到具体契约字段
- 主按钮对比度是否足够
- 中文区域是否保持可读
- v1 是否仍可追踪

选择 v2：

```text
确认采用 home-v2。
将候选 style-contract 设为 approved，将 home-v2 标记为 approved。
home-v1 保留为历史方案，不删除、不覆盖。
同步更新 research.md、screen-contract.yaml 和 asset-manifest.yaml。
```

拒绝 v2：

```text
不采用 home-v2。保留记录但不要批准。
基于以下反馈生成 home-v3：【具体问题】。
不要改变首页结构和已确认的功能层级。
```

## 完成标准

- 只有一个样式契约处于批准状态
- 只有选中基准页标记 `approved: true`
- 所有候选版本有独立路径和来源关系
- 后续页面可以直接引用契约，不再依赖聊天描述
