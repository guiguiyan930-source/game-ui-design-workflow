# UI 交互逻辑

## 文档状态

- status: approved
- version: 0.1
- owner: factory-v2-shop
- last_updated: 2026-08-05

## 全局交互原则

- 分类筛选优先；价格与库存同屏可读
- 购买为主操作；货币不足有明确反馈

## 分页面交互

### `shop`（商店）

- 目的：战斗后补给
- 主流程：进入 → 切分类 → 选商品 → 购买确认 → 库存/货币更新
- 控件：分类 Tab、商品卡、购买按钮、货币栏
- 状态：default / sold-out / low-currency
