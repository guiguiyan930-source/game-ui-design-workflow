# 游戏 UI 技能调用指南

本文说明如何在 Cursor 中安装、调用和串联本仓库的五个技能。

## 1. 技能清单

- `game-ui-workflow`：总控技能。适合从需求、规范、页面延展一直做到视觉稿和组件交付。
- `game-ui-specification`：生成或维护 UI 规范与 `style-contract.yaml`。
- `game-ui-extension`：扩展玩家旅程、页面地图与 `screen-contract.yaml`。
- `game-ui-page-generator`：一次生成一个完整页面的方案、提示词和视觉稿。
- `game-ui-component-breakdown`：从已批准页面拆解独立组件素材。

一般项目优先调用 `game-ui-workflow`；只修改某一阶段时调用对应子技能。

## 2. 安装技能

### 安装到当前项目

在目标项目根目录执行：

```bash
mkdir -p .cursor/skills
cp -R /Users/csl/game-ui-design-workflow/skills/* .cursor/skills/
```

这种方式会把技能随项目共享给团队。

### 安装为个人技能

```bash
mkdir -p ~/.cursor/skills
cp -R /Users/csl/game-ui-design-workflow/skills/* ~/.cursor/skills/
```

个人技能可用于本机的其他项目。不要复制到 `~/.cursor/skills-cursor/`，该目录由 Cursor 管理。

安装后新建或继续一个 Agent 对话即可。技能不要求固定斜杠命令；直接在请求中写出技能名最可靠。

## 3. 初始化 UI 项目

在本仓库根目录执行：

```bash
python3 scripts/init_project.py <project-id>
```

`project-id` 只使用小写字母、数字和连字符，例如：

```bash
python3 scripts/init_project.py moon-palace-rpg
```

生成位置：

```text
specs/moon-palace-rpg/
├── spec.md
├── research.md
├── plan.md
├── tasks.md
├── quickstart.md
├── contracts/
├── prompts/
└── assets/
```

如果希望 Agent 自动初始化，可以直接调用总控技能：

```text
使用 game-ui-workflow 新建项目 moon-palace-rpg。
这是一个国风神话卡牌 RPG，手机竖屏 9:16，先完成需求澄清和 UI 规范。
请把所有产物写入 specs/moon-palace-rpg，不要只在对话中回答。
```

## 4. 引用需求和图片

在 Cursor 对话中通过 `@` 引用项目文档、参考图或已有视觉稿：

```text
使用 game-ui-workflow。
读取 @specs/moon-palace-rpg/spec.md 和 @references/home.png，
分析参考图的色彩、材质、光源和布局，但不要复刻其中的商标或角色。
```

推荐至少提供：

- 游戏类型与核心玩法
- 目标平台和比例
- 首个页面
- 视觉关键词或参考图片
- 是否需要实际生图
- 需要拆解的组件范围

信息不足时，技能会使用可调整的默认值；题材、平台、比例或交付范围不明确时会先询问。

## 5. 四步操作指引

推荐按“原型生成视觉 → UI 风格切换 → UI 延展 → UI 组件拆解”推进。每一步都包含开始条件、调用文本、检查点和下一步。

### 第一步：原型生成视觉

目标：先用一个基准页面验证题材、构图和信息层级，不急于生成整套页面。

开始前确认：

- 已创建 `specs/<project-id>/`
- 已明确游戏类型、平台、比例和首个页面
- 有参考图时使用 `@图片路径` 引用
- `style-contract.yaml` 可以处于 `draft`

调用：

```text
使用 game-ui-workflow，当前执行第 1 步“原型生成视觉”。
项目目录是 @specs/moon-palace-rpg。

先读取 spec.md、research.md 和 contracts。
为 screen-id=home 生成一张基准原型视觉：
1. 补全最小可用的视觉约束；
2. 输出页面定位、布局、组件清单、正向提示词和反向限制；
3. 实际调用图片生成工具；
4. 保存提示词到 prompts/pages/home.md；
5. 保存图片到 assets/pages/home-v1.png；
6. 更新 screen-contract.yaml 和 asset-manifest.yaml；
7. 保持 approved=false，等待我验收。

完成后请按“本步产物、检查重点、可选调整、下一步调用文本”给出操作指引。
```

本步产物：

- `prompts/pages/home.md`
- `assets/pages/home-v1.*`，或图片工具不可用时的 `pending-generation`
- `screen-contract.yaml` 中的首页定义
- `asset-manifest.yaml` 中未批准的页面条目

用户检查：

- 主操作能否在三秒内识别
- 主视觉是否符合游戏题材
- 顶部资源、中部内容和底部导航是否层级清楚
- 比例、安全区、文字策略是否合理
- 是否存在乱码、商标、按钮变形或元素粘连

如果构图不满意：

```text
保持当前 UI 风格不变，只修正 home-v1 的构图：
【写明问题，例如主按钮不突出、入口太多、角色遮挡】。
生成 home-v2，保留 v1，不要开始风格切换或页面延展。
```

进入下一步的条件：原型构图和功能层级基本成立；页面仍可保持未批准状态。

### 第二步：UI 风格切换

目标：在相同页面结构下比较不同视觉方向，选定后冻结为全项目风格。

不要直接覆盖原型。每个风格方案生成独立版本，并在 manifest 保留来源关系。

调用：

```text
使用 game-ui-workflow，当前执行第 2 步“UI 风格切换”。
读取 @specs/moon-palace-rpg 和现有 home-v1。

保持首页的信息结构、主操作和组件位置不变，
将视觉从【当前风格】切换为【目标风格】：
- 目标关键词：【例如青白玉石、冷月银、轻盈半透明】
- 保留内容：【例如月轮构图、六项底部导航】
- 禁止内容：【例如暖金主色、厚重金属、复杂纹理】

先更新 research.md 中的风格决策，生成候选 style-contract；
再生成 home-v2 作为风格对比稿，不覆盖 home-v1。
完成后列出两个版本在色彩、材质、光源、圆角、图标和可读性上的差异，
等待我选择，不要开始 UI 延展。
```

用户选择风格：

```text
确认采用 home-v2 的视觉方向。
将对应 style-contract.yaml 设为 approved，
将 home-v2 标记为 approved，home-v1 保留为历史方案；
同步更新 research.md、screen-contract.yaml 和 asset-manifest.yaml。
完成后给出第 3 步“UI 延展”的建议页面列表和调用文本。
```

本步检查：

- 风格切换只改变视觉语言，不破坏原型的信息架构
- 色值、材质、光向、圆角、描边和图标视角均进入契约
- 只有被选中的风格和基准页标记为 `approved`
- 未采用版本保留，不伪装成最终资源

进入下一步的条件：`style-contract.yaml` 已批准，至少一个基准页面已批准。

### 第三步：UI 延展

目标：以批准的风格和基准页扩展页面系统，再逐页生成视觉。

先做屏幕地图，不要立即批量生图：

```text
使用 game-ui-workflow，当前执行第 3 步“UI 延展”。
读取 @specs/moon-palace-rpg、已批准的 style-contract 和 home 基准页。

先调用 game-ui-extension：
1. 根据玩家旅程找出首发版本必需页面；
2. 标记 must-have、genre-specific 和 optional；
3. 为每页定义目的、入口、主操作、依赖、组件、状态和边界场景；
4. 更新 plan.md、screen-contract.yaml 和 tasks.md；
5. 按依赖关系给出页面生成批次。

本轮不要生成图片。完成后等待我确认页面范围，
并给出“建议先生成哪一页、原因、下一步调用文本”。
```

确认页面范围后，逐页生成：

```text
页面范围确认。现在只生成 screen-id=formation。
使用 game-ui-page-generator，严格继承已批准的 style-contract 和 home 基准页。
保存 formation-v1、提示词和 manifest 条目，approved=false。
完成后停止，给出本页检查重点和下一页建议。
```

每完成一页，用户需要：

1. 查看视觉稿。
2. 要求修订或明确批准。
3. 批准后再生成下一页。
4. 不满意时生成 `v2`，不要覆盖 `v1`。

本步检查：

- 新页面延续色彩、材质、光向、圆角和导航规则
- 功能重点随页面变化，但不另起视觉系统
- 页面之间入口、返回路径和状态闭合
- 每次只生成一个页面，资源均登记到 manifest

进入下一步的条件：需要拆解的源页面已标记 `approved: true`。

### 第四步：UI 组件拆解

目标：把批准页面拆成可复用、可合成、可开发交付的独立素材。

先确认拆解范围：

- 页面专属：背景、角色底座、主题装饰
- 跨页复用：按钮、卡片、导航、货币栏、图标
- 需要的状态：默认、按下、选中、禁用、锁定、已领取

调用：

```text
使用 game-ui-workflow，当前执行第 4 步“UI 组件拆解”。
源页面为已批准的 screen-id=home。

调用 game-ui-component-breakdown，拆解：
1. 无 UI 控件和角色的首页背景；
2. 无文字主按钮的默认、按下、禁用状态；
3. 六个底部导航图标；
4. 金币、月玉、体力图标；
5. 页面主题装饰。

要求：
- 除背景外全部透明背景；
- 每个组件单独生成，不要组件拼板；
- 每个组件单独保存提示词和图片；
- 文件名包含 component-id、state 和版本；
- 更新 component-contract.yaml 和 asset-manifest.yaml。

完成后按“已生成、待生成、透明通道检查、尺寸检查、复用建议”给出指引，
最后运行严格校验。
```

本步检查：

- 源页面已批准
- 非背景组件存在透明通道
- 无文字、乱码、脏边、裁切和背景残留
- 同组图标的透视、描边和光源一致
- 主按钮与次按钮视觉权重正确
- 每个状态是独立文件

最终验收：

```text
使用 game-ui-workflow 验收整个项目。
运行 validate_project.py --strict，
检查页面 ID、组件 ID、资源路径、真实尺寸、透明背景和版本来源。
修复全部错误；不能修复的限制写入 quickstart.md。
```

### 每一步完成后的固定汇报格式

要求总控技能在每一步结束时使用：

```text
当前步骤：
完成状态：
本步产物：
需要你检查：
可选操作：
进入下一步的条件：
可直接复制的下一步调用文本：
```

这样用户无需记忆流程，也不会在页面未批准时误入组件拆解。

## 6. 端到端调用

以下提示会依次执行规范、页面延展、单页视觉、组件拆解和校验：

```text
使用 game-ui-workflow，为 moon-palace-rpg 完成一轮端到端 UI 设计。

要求：
1. 读取 specs/moon-palace-rpg 下的现有文档和 contracts。
2. 完成 UI 规范并冻结 style-contract.yaml。
3. 根据玩家旅程延展首页、编队、关卡、战斗 HUD、结算、角色和背包。
4. 先生成首页，实际调用图片生成工具并保存视觉稿。
5. 首页通过验收后，拆解背景、主按钮、底部导航和货币栏。
6. 所有提示词、图片和组件必须登记到 asset-manifest.yaml。
7. 最后运行 validate_project.py，修复全部错误。
```

如果希望在关键阶段人工确认：

```text
使用 game-ui-workflow 分阶段执行。每完成一个阶段先停止并汇报变更：
第一阶段只完成 spec、research 和 style-contract；
我确认后再执行页面延展；
首页视觉必须经我明确批准后才能拆组件。
```

## 7. 单独调用子技能

### 7.1 生成 UI 规范

```text
使用 game-ui-specification，读取 @specs/moon-palace-rpg/spec.md
和 @specs/moon-palace-rpg/research.md。

为手机竖屏国风卡牌 RPG 建立可执行 UI 规范：
- 明确色值、字体层级、安全区、圆角、描边和按钮尺寸；
- 定义默认、按下、选中、禁用、加载和已领取状态；
- 写入 contracts/style-contract.yaml；
- 完成后将 status 设为 approved。
```

主要输出：

- `contracts/style-contract.yaml`
- `research.md` 中的设计决策
- `tasks.md` 中的规范任务状态

### 7.2 延展页面系统

```text
使用 game-ui-extension，读取 @specs/moon-palace-rpg。
基于首页和核心循环扩展首发版本页面，不要无差别加入所有常见系统。

请为每个页面定义目的、入口、1–3 个主操作、依赖、组件、
默认/空/锁定/错误状态、边界场景和数据需求。
更新 plan.md、screen-contract.yaml 和 tasks.md。
```

主要输出：

- `plan.md` 中的页面路线与生成批次
- `contracts/screen-contract.yaml`
- 按优先级拆分的后续任务

### 7.3 生成一个页面

```text
使用 game-ui-page-generator，读取 @specs/moon-palace-rpg。
只生成 screen-id 为 home 的首页。

要求：
- 严格继承 style-contract.yaml；
- 输出具体布局、组件清单、正向提示词和反向限制；
- 实际调用图片生成工具；
- 保存到 assets/pages/home-v1.png；
- 提示词保存到 prompts/pages/home.md；
- 更新 screen-contract.yaml 和 asset-manifest.yaml；
- 未经我确认不要把 approved 设为 true。
```

页面技能一次只处理一个 `screen-id`。继续生成其他页面时，应明确继承已批准基准页：

```text
使用 game-ui-page-generator 继续生成 formation 页面。
继承已批准的 home 页面以及全部视觉契约，只改变页面功能重点。
```

### 7.4 批准页面

确认视觉稿符合要求后调用：

```text
检查 @specs/moon-palace-rpg/assets/pages/home-v1.png。
如果它满足比例、安全区、主操作、视觉契约和文字策略，
将对应 manifest 条目改为 approved，并同步 screen-contract.yaml；
如果不满足，列出问题并生成 v2，不要覆盖 v1。
```

只有页面 manifest 条目为 `approved: true`，组件技能才会继续。

### 7.5 拆解组件

```text
使用 game-ui-component-breakdown，读取已批准的 home 页面和全部 contracts。

拆解：
- 无 UI 控件的首页背景；
- 无文字主按钮的默认、按下、禁用状态；
- 六个底部导航图标；
- 金币、月玉和体力图标。

除背景外全部要求透明背景。每个组件单独生成、单独保存、
单独写提示词并登记 manifest，不要生成组件拼板。
```

主要输出：

- `contracts/component-contract.yaml`
- `prompts/components/<component-id>.md`
- `assets/components/`
- `contracts/asset-manifest.yaml`

## 8. 修改已有项目

### 修改整体风格

```text
使用 game-ui-specification，把整体视觉从深蓝鎏金调整为青白玉石。
先更新 spec.md 和 style-contract.yaml，
再将受影响的已生成页面和组件标记为 stale。
不要直接覆盖已批准资源。
```

### 增加新页面

```text
使用 game-ui-extension，为当前项目增加公会系统。
先补充公会大厅、成员、活动和管理页面契约，
说明它们与首页、聊天和活动中心的入口关系，不要立即生图。
```

### 重新生成页面版本

```text
使用 game-ui-page-generator，修正 home-v1 中主按钮不突出的问题。
保持其他契约不变，生成 home-v2，并在 manifest 中保留 v1 的来源关系。
```

## 9. 校验交付物

普通校验：

```bash
python3 scripts/validate_project.py specs/moon-palace-rpg
```

严格校验：

```bash
python3 scripts/validate_project.py specs/moon-palace-rpg --strict
```

也可以让总控技能执行：

```text
使用 game-ui-workflow 验收 @specs/moon-palace-rpg。
运行严格校验，修复合同 ID、资源路径、尺寸、透明背景和 manifest 引用错误。
不要跳过警告；无法修复的限制写入 quickstart.md。
```

## 10. 图片工具不可用时

技能必须安全降级：

- 保存完整正向提示词和反向限制
- 不创建虚假图片
- manifest 使用 `status: pending-generation`
- 设置 `approved: false`
- 图片工具恢复后根据提示词继续生成

调用示例：

```text
使用 game-ui-page-generator 生成 home 页面。
如果当前无法调用图片工具，只保存可直接执行的提示词，
并在 manifest 标记 pending-generation，不要伪造图片路径。
```

## 11. 推荐调用顺序

新项目：

```text
game-ui-workflow
→ game-ui-specification
→ game-ui-extension
→ game-ui-page-generator
→ 页面批准
→ game-ui-component-breakdown
→ validate_project.py
```

已有规范、只做单页：

```text
game-ui-page-generator
→ 页面批准
→ game-ui-component-breakdown（可选）
```

只有参考图、需要扩展整套页面：

```text
game-ui-workflow
→ 参考图研究
→ game-ui-specification
→ game-ui-extension
```

## 12. 常见问题

### 技能没有自动触发

在请求第一句明确写：

```text
使用 game-ui-workflow。
```

并确认技能已安装到当前项目 `.cursor/skills/` 或个人 `~/.cursor/skills/`。

### 连续页面风格不一致

要求页面技能读取已批准页面、`style-contract.yaml` 和 `asset-manifest.yaml`，不要只引用聊天中的风格描述。

### 组件仍带背景或文字

明确指定“除背景外透明背景、不要文字、每个组件单独生成”，并检查 `component-contract.yaml` 中的 `transparent_background` 和 `text_policy`。

### 页面还没确认就开始拆组件

先批准页面并更新 manifest。组件拆解技能应在 `approved: true` 之前停止。

### 图片比例与契约不一致

在 manifest 记录工具返回的真实尺寸，不要伪造目标尺寸；随后重新生成或裁切为契约比例。
