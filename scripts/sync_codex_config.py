#!/usr/bin/env python3
"""Merge repository Codex settings into a local config without removing local keys."""

import argparse
from collections.abc import MutableMapping
from pathlib import Path

import tomlkit


SOURCE = Path(__file__).resolve().parents[1] / "codex" / "config.toml"


def merge_config(target, source, prefix=""):
    """Merge tables recursively; replace conflicting values, including whole arrays."""
    changes = []
    target_values = target.unwrap()
    source_values = source.unwrap()
    for key, value in source.items():
        name = f"{prefix}.{key}" if prefix else key
        if key not in target:
            target[key] = value
            changes.append(f"Added {name}")
        elif isinstance(value, MutableMapping) and isinstance(target[key], MutableMapping):
            changes.extend(merge_config(target[key], value, name))
        elif type(target_values[key]) is not type(source_values[key]) or target[key] != value:
            target[key] = value
            changes.append(f"Updated {name}")
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target", nargs="?", type=Path, default=Path.home() / ".codex" / "config.toml",
        help="Target config path (default: ~/.codex/config.toml)",
    )
    target_path = parser.parse_args().target.expanduser()
    source = tomlkit.parse(SOURCE.read_text(encoding="utf-8"))
    target = (
        tomlkit.parse(target_path.read_text(encoding="utf-8"))
        if target_path.exists() else tomlkit.document()
    )
    changes = merge_config(target, source)
    if not changes:
        print(f"Already in sync: {target_path}")
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(tomlkit.dumps(target), encoding="utf-8")
    print("\n".join(changes))
    print(f"Synced: {target_path}")


if __name__ == "__main__":
    main()
