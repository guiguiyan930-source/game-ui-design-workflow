# 组件语义命名规范

仓库统一使用小写 kebab-case，不使用 `button1.png` 或无语义序号作为最终交付名。

## 格式

```text
<scope>-<component>-<variant>-<state>.png
```

示例：

```text
shop-buy-button-normal.png
shop-buy-button-hover.png
shop-buy-button-pressed.png
shop-category-tab-active.png
shop-currency-coin-default.png
shop-sale-badge-default.png
```

## 规则

- `scope`：页面或系统，如 `shop`、`battle`、`inventory`。
- `component`：组件职责，如 `buy-button`、`product-card`。
- `variant`：材质、层级或语义变体；没有时可省略。
- `state`：`default`、`normal`、`hover`、`pressed`、`disabled`、`active` 等。
- 同一组件的所有状态必须共享 `component_id`。
- 雪碧图自动检测序号只用于中间结果；通过 mapping 转成语义名称后才可批准。

命名不采用下划线，以保持与项目 ID 和契约 ID 的 kebab-case 规则一致。
