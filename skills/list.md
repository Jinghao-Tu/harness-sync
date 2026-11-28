# Skill List

1. [Supervisor](https://github.com/HKUSTDial/Supervisor-Skills)

   - 通过 `upstream/supervisor/` Git submodule 管理。
   - 可直接将其中的 `skills/` 用作全局技能，也可按项目选用。

2. [Superpowers](https://github.com/obra/superpowers)

   - 通过 `upstream/superpowers/` Git submodule 管理。
   - 可直接将其中的 `skills/` 用作全局技能，也可按项目选用。

3. [codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill)

   - 作为项目 skill 安装。

4. [image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill)

   - 作为项目 skill 安装，搭配 codex-ppt-skill 使用。
   - 需要飞桨 OCR API key。

5. [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2)

   - 作为项目 skill 安装。

6. [git-commit](git-commit/SKILL.md)

   - 按需创建符合 Conventional Commits 规范的原子提交。
   - 手动同步至 `~/.codex/skills/git-commit/`。

7. [codex-worker](codex-worker/SKILL.md)

   - 指导主 Agent 通过 `codex exec` 调用 Codex CLI（`gpt-6.2-sol` / `gpt-6.2-astra`）作为隔离的子 Agent 执行任务。
   - 手动同步至 `~/.gemini/config/skills/codex-worker/`，面向主 Agent 使用。
