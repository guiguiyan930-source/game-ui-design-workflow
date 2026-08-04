# 兼容性说明

## Cursor

本仓库使用标准 Cursor Agent Skill 目录：

```text
skill-name/
└── SKILL.md
```

支持：

- 项目技能：`<project>/.cursor/skills/`
- 个人技能：`~/.cursor/skills/`
- Agent 自动触发或在请求中显式写出技能名

不要安装到 `~/.cursor/skills-cursor/`，该目录由 Cursor 管理。

图片生成取决于当前 Cursor 环境是否提供图片工具。工具不可用时，技能会保留提示词并标记 `pending-generation`。

## Python

- 最低建议版本：Python 3.9
- CI 验证版本：Python 3.11
- 依赖：PyYAML

安装：

```bash
python3 -m pip install -r requirements.txt
```

支持 macOS 和 Linux。Windows 用户可以直接运行 Python 脚本，但 `install.sh` 需要 WSL、Git Bash 或手动复制技能目录。

## 资源格式

验证脚本当前执行真实文件检查：

- PNG：读取实际宽高和 Alpha / `tRNS` 透明信息
- SVG：读取 `width`、`height` 或 `viewBox`

其他格式：

- JPG、WEBP、GIF 等资源路径仍会检查
- 实际尺寸与透明通道暂不检查，会产生警告
- `--strict` 会把该警告视为错误

需要严格交付时，页面优先使用 PNG，透明控件使用 PNG 或 SVG。

## 图片比例

图片工具可能只支持有限比例。必须在 manifest 记录实际尺寸，不能把目标尺寸写成实际尺寸。

处理方式：

1. 选择工具最接近的比例。
2. 记录真实输出尺寸。
3. 重新生成或使用图像工具裁切。
4. 裁切后再次运行严格校验。

## 中文文字

生成模型对中文排版的可靠性不固定：

- 原型阶段可以使用短词验证层级。
- 正式页面建议生成无文字底板，再由设计或客户端排版。
- 出现乱码时不得批准资源。
- 按钮和卡片组件默认不生成文字。

## 契约版本

当前模板使用：

```yaml
schema_version: 1
```

不同 `schema_version` 的项目不应直接混用。升级方法见 [MIGRATION.md](MIGRATION.md)。
