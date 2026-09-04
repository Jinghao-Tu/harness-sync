1. 本仓库是个人所用的 Harness 工具合集远程同步仓库
2. AGENTS.md 是本仓库的描述
3. codex/AGENTS.md 是 Codex 使用的全局 AGENTS.md, 安装目录是 ~/.codex/AGENTS.md
4. codex/config.toml 是 Codex 使用的全局配置文件, 主要包含配置: 关闭子代理, 开启记忆(但关闭工具记忆), 开启 goal 模式, desktop 配置
5. upstream/ 下是 Superpowers 和 Supervisor 的 Git submodule, 不直接修改其中的源码
6. plugins/*.json 保存插件和 skill 元数据; scripts/build_plugins.py 构建到 dist/, --install 使用 Codex CLI 注册并安装
7. dist/ 是可重新生成的产物, 不提交 Git; 构建和同步步骤见 README.md
8. plugins/git-commit/ 保存独立的个人 git-commit skill; 全局安装目录为 ~/.codex/skills/git-commit/, 不参与插件构建
9. Skill 元数据中只有 short_description 使用中文; SKILL.md 的 description、default_prompt 及其他文本字段使用英文, 且必须准确对应技能正文。插件清单的对应字段遵循同一规则: shortDescription 使用中文, description、longDescription、defaultPrompt 等其他文本字段使用英文。此规则同时适用于 git-commit、Superpowers 和 Supervisor, 不直接修改 upstream/ 源码
