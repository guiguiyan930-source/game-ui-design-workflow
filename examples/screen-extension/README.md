# 示例：UI 页面延展

目标：从已批准首页扩展首发版本页面，先建立屏幕地图，再按依赖逐页生成。

## 第一步：建立屏幕地图

```text
使用 game-ui-extension，读取 @examples/moon-palace-rpg、
已批准的 style-contract 和 home 基准页。

根据“进入首页 → 调整编队 → 选择关卡 → 战斗 → 结算 → 成长 → 回到首页”
建立首发屏幕地图。

要求：
- 页面分为 must-have、genre-specific、optional；
- 每页定义目的、入口、1–3 个主操作、依赖、组件、状态、边界和数据；
- 合并重复入口，不把所有活动堆在首页；
- 更新 plan.md、screen-contract.yaml 和 tasks.md；
- 只规划，不生成图片。
```

## 建议首发路线

```text
登录
  → 首页
  → 编队
  → 关卡选择
  → 战斗 HUD
  → 结算
  → 角色成长 / 背包
  → 首页
```

运营与商业页面作为第二批：

```text
首页 → 召唤 / 商城 / 活动中心 / 每日任务
```

## 第二步：确认页面范围

用户需要检查：

- 核心循环是否闭合
- 每个页面是否有入口和出口
- 结算是否连接下一局或成长
- 是否包含加载、空、锁定、错误和资源不足状态
- 首发页面数量是否可控

确认调用：

```text
确认首发范围。按以下批次执行：
批次 1：编队、关卡选择；
批次 2：战斗 HUD、结算；
批次 3：角色、背包。
每次只生成一个页面，批准后再继续。
```

## 第三步：逐页生成

```text
使用 game-ui-page-generator，只生成 screen-id=formation。
继承已批准的 style-contract 和 home 基准页。

保存 formation-v1、页面提示词和 manifest 条目；
approved=false，完成后停止并给出检查项。
```

修订使用新版本：

```text
formation-v1 的英雄列表过密，保留整体风格，
减少首屏卡片数量并强化编队槽位，生成 formation-v2。
不要覆盖 v1。
```

## 完成标准

- `plan.md` 的顺序与页面依赖一致
- `screen-contract.yaml` 的 ID 唯一且可追踪
- 新页面延续批准的视觉契约
- 每次只处理一个页面
- 未确认页面保持 `approved: false`
