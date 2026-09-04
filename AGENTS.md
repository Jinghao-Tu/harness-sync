1. 本仓库是个人所用的 Harness 工具合集远程同步仓库
2. AGENTS.md 是本仓库的描述
3. codex/AGENTS.md 是 Codex 使用的全局 AGENTS.md, 安装目录是 ~/.codex/AGENTS.md
4. codex/config.toml 是 Codex 使用的全局配置文件, 主要包含配置: 关闭子代理, 开启记忆(但关闭工具记忆), 开启 goal 模式, desktop 配置
5. upstream/ 下是 Superpowers 和 Supervisor 的 Git submodule, 不直接修改其中的源码
6. plugins/*.json 保存插件和 skill 元数据; scripts/build_plugins.py 构建到 dist/, --install 使用 Codex CLI 注册并安装
7. dist/ 是可重新生成的产物, 不提交 Git; 插件与技能清单见 plugins/list.md
8. plugins/git-commit/ 保存独立的个人 git-commit skill; 全局安装目录为 ~/.codex/skills/git-commit/, 不参与插件构建
9. Skill 元数据中只有 short_description 使用中文; SKILL.md 的 description、default_prompt 及其他文本字段使用英文, 且必须准确对应技能正文。插件清单的对应字段遵循同一规则: shortDescription 使用中文, description、longDescription、defaultPrompt 等其他文本字段使用英文。此规则同时适用于 git-commit、Superpowers 和 Supervisor, 不直接修改 upstream/ 源码
10. Markdown 文档保持简洁, 使用逐项编号、条目下附简短备注的风格, 不增加分类小标题或表格; 不主动扩写为长篇教程或重复已有说明。
11. 修改功能、目录或文件名时, 同步维护相关 Markdown 内容与链接, 确保与实际状态一致; 保留原有文档定位和命名, 除非用户明确要求调整
