# UI 交互逻辑

## 文档状态

- status: approved
- version: 0.1
- owner: moon-palace-rpg
- last_updated: 2026-08-05

## 全局交互原则

- 主 CTA 高对比；活动过期不遮挡主线
- 底栏导航高亮当前页

## 全局导航

| 入口 | 目标页 | 高亮规则 |
|---|---|---|
| 首页 | home | 在首页时高亮 |
| 编队 | formation | 在编队时高亮 |

## 分页面交互

### `home`（首页）

- 目的：回流枢纽
- 主流程：进入 → 识别资源与主线 CTA → 进入主线或编队
- 状态：default / loading；活动过期态不挡主 CTA

### `formation`（编队）

- 目的：配置出战阵容
- 主流程：进入 → 调整槽位 → 保存 → 可进战斗入口
- 状态：default / incomplete
