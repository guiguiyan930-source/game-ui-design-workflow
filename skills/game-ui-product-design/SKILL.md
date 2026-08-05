---
name: game-ui-product-design
description: >-
  Writes and maintains game design docs (GDD), product requirements (PRD), and
  UI interaction logic before any page image generation. Use when users ask for
  游戏策划方案、PRD、产品需求、UI交互逻辑、交互流程、状态机, or say to finish
  planning before generating UI visuals / 生图前先做策划.
---

# 游戏策划 · PRD · UI 交互（生成第一步）

**本技能是完整 UI 生成流程的第一步。** 在调用页面生图、风格切换或批量延展之前，必须先完成本步并请用户批准三份文档。没有批准（且用户未明确跳过）时，不得开始后续视觉生成。

## 输出文件

写入 `specs/<project-id>/`：

| 文件 | 中文名 | 用途 |
|---|---|---|
| `gdd.md` | 游戏策划方案 | 定位、核心循环、系统清单、经济与养成（策划层） |
| `prd.md` | 产品需求文档 | P0/P1 需求、信息架构、交付范围、验收 |
| `interaction.md` | UI 交互逻辑 | 导航、主流程、控件行为、状态机、跨页链路 |

模板来源：仓库 `templates/spec-kit/gdd.md`、`prd.md`、`interaction.md`。项目已初始化则直接编辑现有文件，不要另起平行文档。

## 何时使用

- 任何完整生成流程的**第一步**（默认入口）
- 新建 UI 项目、只有概念尚无视觉
- 用户要求「生成之前加策划 / PRD / 交互」
- 延展或生图前发现三文档缺失、`draft` 或内容空洞
- 玩法或页面范围变更，需要回写需求与交互

## 输入

优先读取：

- `spec.md`、`research.md`、`plan.md`
- 已有的 `gdd.md` / `prd.md` / `interaction.md`
- 若已有：`contracts/screen-contract.yaml`

信息不足时：只询问题材、平台、核心玩法、首发页面范围等阻断问题；其余给可调整默认值并标注。

## 工作流

复制并跟踪：

```text
进度:
- [ ] 1. 确认或初始化项目目录
- [ ] 2. 撰写/更新 gdd.md
- [ ] 3. 撰写/更新 prd.md
- [ ] 4. 撰写/更新 interaction.md
- [ ] 5. 交叉检查三文档一致
- [ ] 6. 停在人工批准门禁
```

### 1. 项目目录

若 `specs/<project-id>/` 不存在：

```bash
python3 scripts/init_project.py <project-id>
```

### 2. `gdd.md`（游戏策划方案）

必须覆盖：

- 一句话定位、目标用户、卖点（≤3）
- 核心循环表（回流 → 准备 → 玩法 → 成长 → 商业）
- 系统清单与优先级（`must-have` / `genre-specific` / `optional`）
- 资源与经济（策划层概述，禁止假装已有服务端公式）
- 养成与进度轴、世界观最小集、风险约束

`文档状态.status` 先保持 `draft`，待用户批准后再改 `approved`。

### 3. `prd.md`（产品需求）

必须覆盖：

- 产品目标与可验证成功指标
- 非目标（明确不做）
- P0 / P1 / P2 需求表（每条对应页面或系统）
- 信息架构与本迭代页面交付范围
- 数据依赖、边界异常、验收清单

每条 P0 必须能被后续某个 `screen-id` 承接。

### 4. `interaction.md`（UI 交互逻辑）

必须覆盖：

- 全局交互原则、全局导航、全局状态
- 每个 must-have 页面：目的、进出、主流程、控件表、状态机
- 跨页链路（至少核心循环相关）
- 「与视觉稿的约束」：首屏必露信息、禁遮挡区、主操作强调

状态名尽量与后续 `screen-contract.yaml` 的 `states` 一致（如 `default` / `loading` / `incomplete` / `low-currency`）。

### 5. 交叉检查

- `gdd` 核心循环中的界面 ⊆ `prd` 页面范围
- `prd` P0 页面 ⊆ `interaction` 分页面章节
- 商业/破坏性操作在 `interaction` 中有确认或失败路径
- 三文档互不矛盾；空洞模板不得标为 approved

### 6. 人工门禁（必须停止）

完成后输出：

```text
当前步骤：第 1 步 · 策划与 PRD / 交互逻辑（生成第一步）
完成状态：draft，等待批准
本步产物：gdd.md、prd.md、interaction.md
需要你检查：定位与循环、P0 范围、分页面主流程与状态
可选操作：修改文案 / 增删系统 / 批准三文档 / 明确跳过门禁
进入下一步的条件：三文档 status 均为 approved，或 quickstart.md 记录跳过原因
可直接复制的下一步调用文本：
批准 @specs/<project-id>/gdd.md、prd.md、interaction.md。
批准后进入第 2 步：使用 game-ui-workflow 生成基准页原型视觉。
```

**禁止**在用户批准前调用 `game-ui-page-generator` 做正式生图。  
用户说「跳过策划门禁」时：在 `quickstart.md` 写明原因，三文档可保持 draft，但不得假装已批准。

## 批准操作

用户批准后：

1. 将三文档 `文档状态.status` 改为 `approved`
2. 更新 `tasks.md` 对应 `[product]` 项
3. 更新 `plan.md` 质量门禁勾选
4. 建议下一步：`game-ui-specification` 或（样式已批准时）`game-ui-extension`

## 与其他技能的关系

```text
第 1 步  game-ui-product-design     ← 生成第一步（必须先做）
第 2 步+ game-ui-specification / 原型生图 / extension / …
         game-ui-page-generator     # 要求第 1 步三文档 approved
```

总控 `game-ui-workflow` 启动完整生成时，**必须先调用本技能作为第 1 步**，不得跳过直接生图。

## 完成定义

- 三文件存在于项目根且无 `{{PROJECT_ID}}` 占位符
- 各含 `status: draft` 或 `approved`
- 内容可支撑屏幕延展与单页生图（非空模板）
- 已停在批准门禁，或已按用户指示完成批准/跳过记录
