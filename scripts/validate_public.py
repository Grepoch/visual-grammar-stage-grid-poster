#!/usr/bin/env python3
"""Validate a released public style-skill package without parent infrastructure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = (
    "SKILL.md", "README.md", "CHANGELOG.md", "LICENSE", "ASSET-LICENSE.md",
    "REFERENCES.md", "release.json", ".gitignore", "scripts/validate_public.py", ".github/workflows/validate.yml", "evals/evals.json", "evals/schema.json",
    "design-system/routing.json", "design-system/compositions.json",
    "design-system/materials.json", "design-system/typography.json",
    "design-system/constraints.json",
)
CATALOGS = (
    "design-system/routing.json",
    "design-system/compositions.json",
    "design-system/materials.json",
    "design-system/typography.json",
    "design-system/constraints.json",
)
PUBLIC_TEXT = ("SKILL.md", "README.md", "CHANGELOG.md", "ASSET-LICENSE.md", "REFERENCES.md")
PUBLIC_REQUIRED_FILES = set(REQUIRED)


def fail(message: str) -> None:
    print(f"public package validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(relative: str) -> dict:
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {relative}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {relative}: {exc}")


for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        fail(f"missing required file {relative}")

release = load("release.json")
if release.get("schema_version") != 1 or release.get("contract_version") != 1 or not SLUG.fullmatch(release.get("slug", "")):
    fail("release manifest has an invalid contract or child slug")
if not re.fullmatch(r"^[0-9]+\.[0-9]+\.[0-9]+$", release.get("version", "")):
    fail("release manifest has an invalid version")
if set(release.get("required_files", [])) != PUBLIC_REQUIRED_FILES:
    fail("release manifest has an incomplete required_files list")
if release.get("status") != "released":
    fail("public package must have released status")
if release.get("public_entry") != "SKILL.md":
    fail("public entry must be SKILL.md")
if release.get("source_material_count", 0) < 3:
    fail("source_material_count must be at least 3")
boundaries = release.get("public_boundaries", {})
if boundaries.get("contains_private_training_notes") is not False or boundaries.get("contains_source_reconstruction") is not False or boundaries.get("attribution_file") != "REFERENCES.md":
    fail("public boundaries are not clean")

for relative in CATALOGS:
    catalog = load(relative)
    if catalog.get("schema_version") != 1 or catalog.get("status") in {"draft", None}:
        fail(f"{relative} is not a validated public catalog")

evals = load("evals/evals.json")
if evals.get("schema_version") != 1 or evals.get("status") in {"draft", None}:
    fail("public evals are not validated")
if not isinstance(evals.get("evals"), list) or len(evals["evals"]) < 3:
    fail("at least three public eval cases are required")

references = (ROOT / "REFERENCES.md").read_text(encoding="utf-8").lower()
if "verified" not in references and "unverified" not in references:
    fail("REFERENCES.md must state provenance status")
for relative in PUBLIC_TEXT:
    text = (ROOT / relative).read_text(encoding="utf-8", errors="ignore").lower()
    if "placeholder" in text:
        fail(f"placeholder remains in {relative}")

examples = ROOT / "examples"
example_files = [p for p in examples.iterdir() if p.is_file() and p.name != "README.md"] if examples.is_dir() else []
if len(example_files) < 3:
    fail("at least three public examples are required")
for path in example_files:
    if path.suffix.lower() in {".md", ".txt", ".json"}:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "placeholder" in text or "draft" in text:
            fail(f"non-public example marker remains in {path.name}")

print(f"Validated public style-skill package {ROOT.name}: {len(example_files)} examples, {len(CATALOGS)} catalogs, {len(evals['evals'])} evals.")
