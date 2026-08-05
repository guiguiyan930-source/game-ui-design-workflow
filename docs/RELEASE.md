# 发布与安装

## 从 Release 安装

1. 打开 [Releases](https://github.com/guiguiyan930-source/game-ui-design-workflow/releases)。
2. 下载 `game-ui-design-workflow-vX.Y.Z.zip`。
3. 解压后，使用安装脚本安装到目标项目：

   ```bash
   ./install.sh --project /path/to/project
   ```

   或安装为个人技能：

   ```bash
   ./install.sh --personal
   ```

4. 同名技能默认跳过；升级时确认差异后执行：

   ```bash
   ./install.sh --project /path/to/project --force
   ```

5. 安装校验脚本依赖：

   ```bash
   python3 -m pip install -r requirements.txt
   ```

## 版本策略

- Patch：文档、提示词和兼容性修复，不改变契约含义。
- Minor：新增技能、向后兼容的契约字段或新校验能力。
- Major：不兼容的契约、目录或技能行为变化。

契约不兼容变化必须：

1. 提升对应 `schema_version`。
2. 在 `CHANGELOG.md` 提供迁移说明。
3. 更新模板、示例、校验脚本和测试。

## 发布检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
python3 scripts/validate_project.py examples/guofeng-card-rpg --strict
```

确认：

- 工作区干净，CI 通过。
- README、调用指南和示例与当前行为一致。
- `CHANGELOG.md` 已包含版本和日期。
- Release 压缩包不包含 `.git`、缓存、Token 或临时项目。
- Tag 与 Release 名称使用 `vX.Y.Z`。
