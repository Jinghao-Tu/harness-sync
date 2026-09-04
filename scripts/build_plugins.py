#!/usr/bin/env python3
"""Build localized Codex plugins without modifying their upstream submodules."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MARKETPLACE = "harness-sync"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def localize_skill(path, translation):
    """Replace metadata only; retain the complete upstream Markdown body."""
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?=\n|\Z)", text, re.DOTALL)
    if match is None:
        raise ValueError(f"Invalid skill frontmatter: {path / 'SKILL.md'}")
    metadata = yaml.safe_load(match[1])
    metadata["description"] = translation["description"]
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
    (path / "SKILL.md").write_text(
        "---\n" + frontmatter + "---" + text[match.end():], encoding="utf-8"
    )

    interface_path = path / "agents" / "openai.yaml"
    data = yaml.safe_load(interface_path.read_text(encoding="utf-8")) if interface_path.exists() else {}
    # Preserve upstream policy, dependencies, icons, and other interface fields.
    data.setdefault("interface", {}).update(translation["interface"])
    interface_path.parent.mkdir(exist_ok=True)
    interface_path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def build_plugin(name, config):
    source = ROOT / "upstream" / name
    skills = sorted((source / "skills").glob("*/SKILL.md"))
    if not skills:
        raise ValueError(f"No skills in {source}; run git submodule update --init --recursive")
    missing = sorted({skill.parent.name for skill in skills} - config["skills"].keys())
    if missing:
        raise ValueError(f"{name}: missing skill metadata: {', '.join(missing)}")
    for skill in skills:
        translation = config["skills"][skill.parent.name]
        interface = translation["interface"]
        if not re.search(r"[\u4e00-\u9fff]", interface["short_description"]):
            raise ValueError(f"{name}/{skill.parent.name}: short_description must contain Chinese")
        for field, value in (("description", translation["description"]),
                             ("default_prompt", interface["default_prompt"])):
            if not value.strip() or re.search(r"[\u4e00-\u9fff]", value):
                raise ValueError(f"{name}/{skill.parent.name}: {field} must use English")

    manifest = dict(config["manifest"])
    if manifest["name"] != name:
        raise ValueError(f"Plugin name must match config filename: {name}")
    upstream_manifest = source / ".codex-plugin" / "plugin.json"
    if upstream_manifest.exists():
        manifest["version"] = read_json(upstream_manifest)["version"]
    # Codex caches local plugins by version; each build needs a fresh suffix.
    base_version = manifest["version"].split("+", 1)[0]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    manifest["version"] = f"{base_version}+codex.{stamp}"

    destination = DIST / "plugins" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Finish the new package before replacing the previous build.
    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=destination.parent) as temporary:
        package = Path(temporary) / name
        package.mkdir()
        for relative in config["files"]:
            origin = source / relative
            target = package / relative
            if origin.is_dir():
                shutil.copytree(origin, target)
            else:
                shutil.copy2(origin, target)
        for skill in skills:
            target = package / "skills" / skill.parent.name
            shutil.copytree(skill.parent, target)
            localize_skill(target, config["skills"][skill.parent.name])
        write_json(package / ".codex-plugin" / "plugin.json", manifest)
        (package / "LOCALIZATION.md").write_text(
            f"# Localized Codex package\n\nUpstream: {manifest['repository']}\n\n"
            "Packaged by harness-sync. Short UI descriptions use Chinese; descriptions, "
            "default prompts, and other metadata use English. Skill names, Markdown bodies, "
            "and supporting resources are unchanged.\n",
            encoding="utf-8",
        )
        if destination.exists():
            shutil.rmtree(destination)
        package.rename(destination)
    print(f"Built {name}: {len(skills)} skills -> {destination}", flush=True)


def write_marketplace(configs):
    entries = []
    for name, config in configs.items():
        if (DIST / "plugins" / name / ".codex-plugin" / "plugin.json").exists():
            entries.append({
                "name": name,
                "source": {"source": "local", "path": f"./plugins/{name}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": config["manifest"]["interface"]["category"],
            })
    write_json(DIST / ".agents" / "plugins" / "marketplace.json", {
        "name": MARKETPLACE,
        "interface": {"displayName": "Harness Sync"},
        "plugins": entries,
    })


def main():
    configs = {path.stem: read_json(path) for path in sorted((ROOT / "plugins").glob("*.json"))}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugins", nargs="*", help="Plugin names; defaults to all configured plugins")
    parser.add_argument("--install", action="store_true", help="Register the local marketplace and install built plugins")
    args = parser.parse_args()
    names = args.plugins or list(configs)
    unknown = sorted(set(names) - configs.keys())
    if unknown:
        parser.error(f"Unknown plugins: {', '.join(unknown)}; choose from {', '.join(configs)}")
    try:
        for name in names:
            build_plugin(name, configs[name])
        write_marketplace(configs)
        if args.install:
            subprocess.run(["codex", "plugin", "marketplace", "add", str(DIST)], check=True)
            for name in names:
                subprocess.run(["codex", "plugin", "add", f"{name}@{MARKETPLACE}"], check=True)
    except (OSError, ValueError, KeyError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Build/install failed: {error}\n")


if __name__ == "__main__":
    main()
