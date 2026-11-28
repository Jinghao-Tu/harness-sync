1. 本仓库是个人所用的 Harness 工具合集远程同步仓库
2. AGENTS.md 是本仓库的描述
3. global/AGENTS.md 是全体 Agent 共用的全局 AGENTS.md, 可同步至各工具全局规则目录(如 ~/.codex/AGENTS.md、~/.gemini/config/GEMINI.md 等)
4. codex/config.toml 是 Codex 使用的全局配置文件, 主要包含配置: 关闭子代理, 开启记忆(但关闭工具记忆), 开启 goal 模式, desktop 配置
   - 运行 `uv run scripts/sync_codex_config.py` 增量同步到 `~/.codex/config.toml`, 可传入目标路径; 缺失项添加, 冲突值以仓库为准, 表递归合并, 数组整体更新, 保留目标独有项。
5. `upstream/` 通过 Git submodule 管理 Superpowers 和 Supervisor，作为上游技能来源，不直接修改其中的源码。
6. `skills/` 保存个人技能，完整技能清单见 [skills/list.md](skills/list.md)。
7. `skills/git-commit/` 保存个人 git-commit 技能，全局安装目录为 `~/.codex/skills/git-commit/`。
8. `skills/codex-worker/` 保存个人 codex-worker 技能，指导主 Agent 通过 Codex CLI 执行子任务，全局安装目录为 `~/.gemini/config/skills/codex-worker/`。
9. 技能的 `short_description` 使用中文，`description`、`default_prompt` 和正文使用英文。
10. Markdown 文档保持简洁, 使用逐项编号、条目下附简短备注的风格, 不增加分类小标题或表格; 不主动扩写为长篇教程或重复已有说明。
11. 修改功能、目录或文件名时, 同步维护相关 Markdown 内容与链接, 确保与实际状态一致; 保留原有文档定位和命名, 除非用户明确要求调整
