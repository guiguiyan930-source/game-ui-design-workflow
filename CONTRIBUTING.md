# 贡献指南

感谢改进 Game UI Design Workflow。

## 开发环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
python scripts/validate_project.py examples/guofeng-card-rpg --strict
python scripts/validate_project.py examples/moon-palace-rpg --strict
```

提交前确保四条命令全部通过。

## 修改技能

- 技能目录名与 `SKILL.md` 的 `name` 必须一致。
- `name` 只使用小写字母、数字和连字符。
- `description` 同时说明“做什么”和“何时使用”。
- 主 `SKILL.md` 保持在 500 行以内。
- 详细分类、示例和模板放到同级 `references/`，引用只深入一层。
- 不要把对话限定的临时信息写成永久规则。

新增技能时，同时更新根 README、调用指南和技能校验测试。

## 修改契约

- 契约字段变化需要更新 `schema_version` 或保持向后兼容。
- 同步修改 `templates/contracts/`、完整示例和验证脚本。
- 新字段必须说明来源、用途、允许值和缺省行为。
- 不得静默改变已批准资源的含义。

## 修改资源校验

- 对 manifest 中声明的尺寸和透明背景进行真实文件检查。
- 新增图片格式时补充正常、尺寸错误和透明通道错误测试。
- 未支持的格式应产生明确警告，不能假装已检查。

## 新增示例

示例至少包含：

- 需求、研究、计划、任务和复现文档
- 四类核心契约，以及按交付范围使用的 sprite、atlas、export 可选契约
- 页面或组件提示词
- manifest 中可追踪的资源条目
- `README.md` 说明调用步骤与限制
- 严格校验通过，或清楚解释故意保留的限制

不得提交未经授权的商标、受保护角色或来源不明素材。

## 提交和拉取请求

- 每个提交只解决一个清晰问题。
- 提交信息说明改动目的，例如 `feat: validate PNG alpha channels`。
- PR 描述包含摘要、测试方法、视觉资源来源和兼容性影响。
- 改变视觉输出时附前后对比图；改变契约时附迁移说明。

## 报告问题

Issue 应包含：

- 使用的技能和调用文本
- 项目目录结构或最小复现
- 预期结果与实际结果
- 校验脚本输出
- 可公开的参考图或生成资源

请删除账号、Token、商业项目素材等敏感信息。
