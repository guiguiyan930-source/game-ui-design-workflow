# Game UI Design Workflow

一个面向 Cursor Agent 的游戏 UI 设计技能仓库。它用 Spec-Kit 风格的项目文档串联四项能力：

1. UI 规范：建立视觉语言、设计令牌、布局和交互规则。
2. UI 延展：从玩法与玩家旅程扩展完整屏幕地图。
3. 页面生成：逐页生成方案、提示词与视觉稿。
4. 组件拆解：把已批准页面拆成可复用、可交付的独立素材。

`game-ui-workflow` 是总控技能；四个阶段技能也可独立调用。项目事实保存在 `specs/<project>/`，避免只依赖对话上下文。

## 目录

```text
skills/
  game-ui-workflow/
  game-ui-specification/
  game-ui-extension/
  game-ui-page-generator/
  game-ui-component-breakdown/
templates/
  spec-kit/
  contracts/
scripts/
  init_project.py
  validate_project.py
specs/
examples/
```

## 安装

将仓库中的技能目录复制或链接到项目技能目录：

```bash
mkdir -p .cursor/skills
cp -R skills/* .cursor/skills/
```

如果希望跨项目使用，可复制到 `~/.cursor/skills/`。不要安装到 Cursor 内置的 `~/.cursor/skills-cursor/`。

完整的安装、显式调用、分阶段确认、页面批准和组件拆解示例见
[游戏 UI 技能调用指南](docs/SKILL_USAGE.zh-CN.md)。

完整交付示例见 [月宫列传：从首页原型到组件拆解](examples/moon-palace-rpg/README.md)。

## 快速开始

```bash
python3 scripts/init_project.py moon-palace-rpg
python3 scripts/validate_project.py specs/moon-palace-rpg
```

然后在 Cursor 中提出：

```text
使用 game-ui-workflow，根据参考图为一款国风卡牌 RPG 建立完整 UI 项目，
先完成规范和屏幕地图，再生成首页视觉，批准后拆解首页组件。
```

端到端流程：

```text
spec.md
  → research.md
  → contracts/style-contract.yaml
  → plan.md + contracts/screen-contract.yaml
  → assets/pages/ + asset-manifest.yaml
  → contracts/component-contract.yaml + assets/components/
  → tasks.md + quickstart.md + validation
```

## 阶段调用

- “建立这个游戏的 UI 规范” → `game-ui-specification`
- “基于现有首页延展完整页面” → `game-ui-extension`
- “生成商城页视觉并保存图片” → `game-ui-page-generator`
- “把这个页面拆成透明背景组件” → `game-ui-component-breakdown`
- “从需求一直做到组件交付” → `game-ui-workflow`

图片生成工具可用时，技能应实际生成并保存图片；不可用时保留完整提示词，将资源状态标为 `pending-generation`，不能伪造文件。

## 项目约束

- `spec.md` 是需求与验收标准的唯一来源。
- `contracts/` 是跨阶段视觉一致性的唯一来源；后续阶段不得静默改写。
- 页面生成一次只处理一个页面，批准后才进入组件拆解。
- 所有资源必须登记到 `contracts/asset-manifest.yaml`。
- 修改项目后运行校验脚本；失败项修复前不得宣称交付完成。

## 来源

本仓库对以下公开技能的职责进行重新组织与结构化重写：

- [Game-UI-Extension](https://github.com/guiguiyan930-source/Game-UI-Extension)
- [game-ui-page-generator](https://github.com/guiguiyan930-source/game-ui-page-generator)
- [game-ui-specification](https://github.com/guiguiyan930-source/game-ui-specification)
- [game-ui-component-breakdown](https://github.com/guiguiyan930-source/game-ui-component-breakdown)

详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
