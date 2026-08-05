# 游戏策划方案（GDD）

## 文档状态

- status: approved
- version: 0.1
- owner: factory-v2-shop
- last_updated: 2026-08-05

## 一句话定位

- 项目 ID：`factory-v2-shop`
- 游戏名称：Survivor Shop（案例）
- 品类：2D 欧美卡通生存 Roguelike 商店
- 核心体验：战斗间隙快速筛选商品并完成补给

## 核心循环

```text
战斗结束 → 进入商店 → 筛选购买 → 准备下一轮
```

## 系统清单

| 系统 ID | 名称 | 优先级 | 说明 |
|---|---|---|---|
| shop | 商店 | must-have | Factory v2 主交付页 |

## 与下游文档关系

- `prd.md` / `interaction.md` / Atlas 与引擎 JSON
