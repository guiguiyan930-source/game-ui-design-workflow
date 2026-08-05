---
name: game-ui-workflow
description: Orchestrates an end-to-end game UI workflow from game design (GDD), PRD, and UI interaction logic through design specification, screen-system extension, page image generation, component breakdown, sprite-sheet splitting, PNG ZIP packaging, atlas packing, engine JSON handoff, asset registration, and validation. Use when users ask to build, extend, visualize, split, or deliver a coherent multi-screen game UI project rather than one isolated artifact.
---

# 游戏 UI 总控工作流

把对话需求转换成可复现的 UI 项目。项目事实必须写入 `specs/<project-id>/`；不要仅保留在对话中。

## 快速路由

根据请求选择最小充分路径：

- 游戏策划、PRD、交互逻辑、生图前需求 → `game-ui-product-design`
- 规范、设计系统、统一风格 → `game-ui-specification`
- 页面清单、功能扩展、玩家旅程 → `game-ui-extension`
- 完整单页、原型视觉、页面生图 → `game-ui-page-generator`
- 透明组件、切图、素材拆解 → `game-ui-component-breakdown`
- 雪碧图、单元素 PNG、切片打包 → `game-ui-sprite-sheet-splitter`
- Atlas、9-slice、Godot / Unity / Cocos JSON → `game-ui-asset-pipeline`
- 完整项目或多阶段交付 → 按本工作流依次编排

用户明确要求单阶段时，不强迫执行完整流程；但要读取已有契约。
生图前若 `gdd.md` / `prd.md` / `interaction.md` 缺失或仍为 draft，必须先执行生成第一步：`game-ui-product-design`。

## 分步操作指引

当用户按完整生成链路工作时，**第一步必须是策划与 PRD**，使用以下检查点：

1. **策划与 PRD（生成第一步）**：调用 `game-ui-product-design`，完成并批准 `gdd.md`、`prd.md`、`interaction.md`；未批准前不得进入后续生图步骤。
2. 原型生成视觉：用一个基准页面验证构图和信息层级，保存为未批准版本。
3. UI 风格切换：保持页面结构不变生成风格候选；用户选定后再批准样式契约和基准页。
4. UI 延展：先输出屏幕地图并等待范围确认，再按批次逐页生成。
5. UI 组件拆解：只拆已批准页面，每个组件和状态单独交付。
6. 雪碧图拆分打包：把组件合图切成单元素透明 PNG，生成 manifest 和 ZIP。
7. Atlas 与引擎交付：语义命名、确认 9-slice、打包 Atlas 并生成引擎 JSON。

每一步开始时简要说明：

- 当前步骤和目标
- 将读取的输入
- 将产生或修改的文件
- 本步停止条件

每一步结束时固定输出：

```text
当前步骤：
完成状态：
本步产物：
需要你检查：
可选操作：
进入下一步的条件：
可直接复制的下一步调用文本：
```

存在人工门禁时必须停止，不能把“给出下一步指引”理解为自动执行下一步：

- `gdd.md` / `prd.md` / `interaction.md` 未批准时，不开始页面生图（用户明确要求“跳过策划门禁”除外，并写入 `quickstart.md`）。
- 原型结构未确认时，不开始风格定稿。
- 风格契约和基准页未批准时，不批量延展页面视觉。
- 页面范围未确认时，只完成屏幕地图。
- 源页面未批准时，不拆组件。
- 组件雪碧图不存在时，不伪造单元素 PNG 或 ZIP。
- 语义 mapping 和 9-slice 未审核时，不批准 Atlas 或引擎清单。

## 初始化

1. 生成稳定的 `project-id`，使用小写字母、数字和连字符。
2. 若项目目录不存在，执行：

   ```bash
   python3 scripts/init_project.py <project-id>
   ```

3. 读取 `spec.md`、`research.md`、`plan.md`、`gdd.md`、`prd.md`、`interaction.md` 和 `contracts/` 中全部文件。
4. 将用户提供的参考图路径记入 `spec.md`，分析结论写入 `research.md`。
5. 只询问会改变题材、平台、比例或交付范围的阻断问题；其他信息使用明确标注的默认值。

## 阶段顺序

完整项目启动时，**生成链路从 Product Design 开始**（第一步）。`spec.md` / `research.md` 可在同一步由产品设计回填最小集，或紧随其后补全。

### 1. Product Design（生成第一步）

调用 `game-ui-product-design`：

1. 写入 `gdd.md`：游戏定位、核心循环、系统清单、经济与养成（策划层，不含服务端公式）
2. 写入 `prd.md`：P0/P1 需求、信息架构、页面交付范围、验收标准
3. 写入 `interaction.md`：全局导航、分页面主流程、控件行为、状态机、跨页链路
4. 若 `spec.md` 仍空，同步写入项目定位、平台、比例与范围摘要

三份文档的 `文档状态.status` 均为 `approved` 后，才允许进入原型生图与后续步骤。用户明确跳过时，在 `quickstart.md` 记录跳过原因。

门禁：不得用空模板或仅改标题冒充已批准策划文档；本阶段结束后必须停止等待批准。

### 2. Specify

补全 `spec.md`（若第一步未写全）：

- 项目定位、核心玩法、目标平台、画面比例和语言
- 用户故事、范围、首个页面和交付物
- 可验证的视觉、功能和版权验收标准

门禁：存在阻断性未决事项时不得冻结契约。

### 3. Research

把参考图抽象成可复用语言，不复制受保护角色、商标或完整构图：

- 色彩、材质、光源、圆角、描边、密度
- 导航、卡片、按钮、图标和反馈模式
- 玩家旅程、核心循环、平台限制与风险

### 4. Specification

调用 `game-ui-specification`，写入 `contracts/style-contract.yaml`。将状态从 `draft` 改为 `approved` 前，确认色彩、文字、几何、效果和一致性规则均可执行。

门禁：页面技能不得静默引入契约外的主色、材质、光向或圆角体系。

### 5. Extension

调用 `game-ui-extension`：

- 以 `gdd.md` / `prd.md` / `interaction.md` 为输入
- 在 `plan.md` 建立按玩家旅程排序的屏幕路线
- 在 `contracts/screen-contract.yaml` 记录页面目的、入口、主操作、组件、状态、边界和数据
- 只选择服务玩法与商业模式的页面，标注 `must-have`、`genre-specific` 或 `optional`

### 6. Page generation

调用 `game-ui-page-generator`，一次处理一个页面：

1. 确认生成第一步（策划三文档）已批准（或已记录跳过）。
2. 读取样式、页面契约与 `interaction.md` 中该页主流程/状态。
3. 保存页面说明与最终提示词到 `prompts/pages/<screen-id>.md`。
4. 图片工具可用时实际生成图片，保存到 `assets/pages/<screen-id>.<ext>`。
5. 更新 `asset-manifest.yaml`；等待用户或明确验收规则批准。

不要因为工具不可用而虚构图片。此时资源状态使用 `pending-generation`，并保留可直接执行的提示词。

### 7. Component breakdown

仅对 `approved: true` 的页面调用 `game-ui-component-breakdown`：

- 先更新 `component-contract.yaml`
- 每个组件单独提示、单独文件、单独 manifest 条目
- 除背景外默认透明；默认不生成文字
- 组件状态、尺寸、命名和源页面可追踪

### 8. Sprite-sheet splitting

组件拆解输出为整张雪碧图时，调用 `game-ui-sprite-sheet-splitter`：

1. 读取实际雪碧图和组件契约。
2. 检查并去掉标题、按钮文案、数字标签、水印和文字残影。
3. 使用 Alpha 或纯色背景检测独立元素。
4. 导出单元素透明 PNG。
5. 生成坐标、尺寸和路径 manifest。
6. 将 PNG 与 manifest 打包成 ZIP。
7. 人工检查文字、裁断、粘连、阴影和透明边缘。

自动检测不可靠时调整阈值或重新生成留有间距的雪碧图，不得把错误切片标记为批准。

### 9. Atlas and engine handoff

需要开发交付时调用 `game-ui-asset-pipeline`：

1. 将检测序号映射为稳定语义名称。
2. 为组件登记 `full`、`1:1`、`tile` 或人工审核的 `9-slice`。
3. 生成不旋转的 Atlas PNG 与 JSON。
4. 生成 Godot、Unity、Cocos 或通用 JSON 清单。
5. 明确区分 JSON handoff 与原生引擎工程文件。

### 10. Validate

执行：

```bash
python3 scripts/validate_project.py specs/<project-id>
```

修复全部错误。警告必须在 `quickstart.md` 解释或解决。

## 视觉生成规则

图片生成工具可用时：

1. 页面图使用契约的画面比例。
2. 工具不支持精确尺寸时选择最接近比例，并在 manifest 记录实际尺寸。
3. 对中文文字生成不可靠时，优先生成无文字底板并注明后期排版区域；不得声称乱码可直接交付。
4. 组件生图逐个执行，不把多个组件粘在同一张图中。
5. 工具返回的文件移动或复制到项目资源目录，再更新真实路径。

## 变更控制

- 用户修改视觉方向时，先更新 `spec.md` 和 `style-contract.yaml`，再标记受影响页面与组件为 `stale`。
- 页面结构变化时，更新 `screen-contract.yaml` 后再生图。
- 页面未批准时，不得开始组件拆解。
- 不覆盖已批准资源；生成新版本并在 manifest 中保留来源关系。

## 完成定义

- 六类 Spec-Kit 产物完整，并含已批准（或已记录跳过）的 `gdd.md` / `prd.md` / `interaction.md`
- 四类核心契约之间的 ID 和路径一致；使用雪碧图时附加拆分契约
- 页面及组件图片存在，或明确标记待生成
- 视觉稿与组件均有提示词可复现
- 使用雪碧图时，单元素 PNG、拆分 manifest 和 ZIP 包可追踪
- 使用开发交付时，Atlas regions、9-slice 与引擎 JSON 一致
- `tasks.md` 反映真实状态
- 校验脚本无错误
