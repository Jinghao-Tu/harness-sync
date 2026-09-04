# Plugin List

1. [Supervisor](https://github.com/HKUSTDial/Supervisor-Skills)

   - 通过 `upstream/supervisor/` submodule 管理，配置见 [supervisor.json](supervisor.json)。
   - 作为全局插件构建安装，也可按需选取 skill 用于单个项目。

2. [Superpowers](https://github.com/obra/superpowers)

   - 通过 `upstream/superpowers/` submodule 管理，配置见 [superpowers.json](superpowers.json)。
   - 作为全局插件构建安装，也可按需选取 skill 用于单个项目。

3. [codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill)

   - 作为项目 skill 安装。

4. [image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill)

   - 作为项目 skill 安装，搭配 codex-ppt-skill 使用。
   - 需要飞桨 OCR API key。

5. [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2)

   - 作为项目 skill 安装。

6. [git-commit](git-commit/SKILL.md)

   - 按需创建符合 Conventional Commits 规范的原子提交。
   - 手动同步至 `~/.codex/skills/git-commit/`，不参与插件构建。
