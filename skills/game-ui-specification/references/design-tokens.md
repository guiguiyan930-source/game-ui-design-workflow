# 游戏 UI 设计 Token

`style-contract.yaml` 是全局设计 Token 的单一事实来源，不再建立平行设计系统。

## 层级

1. 原始值：`colors`、`typography`、`geometry`、`effects`
2. 语义别名：`tokens.color`、`tokens.spacing`、`tokens.motion`
3. 组件引用：`component-contract.yaml` 中的 `style_dependencies`

示例：

```yaml
colors:
  primary: "#58C36A"
tokens:
  color:
    action-primary: "#58C36A"
  spacing:
    sm: 8
    md: 16
```

规则：

- Token 名使用小写 kebab-case。
- 页面提示词引用语义用途，不只写裸色值。
- 风格切换时先修改全局值和语义别名，再将受影响资源标为 `stale`。
- API token 或访问密钥必须称为“凭据”，避免与设计 Token 混淆。
