"""Discover and parse plugin skill files."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

from tests.config import SKILLS_ROOT


@dataclasses.dataclass
class Metadata:
    name: str
    description: str
    argument_hint: str | None = None


@dataclasses.dataclass
class Skill:
    metadata: Metadata
    body: str
    path: Path
    content: str

    @classmethod
    def from_path(cls, path: Path) -> "Skill":
        content = path.read_text()
        frontmatter: dict = {}
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
        return cls(
            metadata=Metadata(
                name=frontmatter.get("name", ""),
                description=frontmatter.get("description", ""),
                argument_hint=frontmatter.get("argument-hint"),
            ),
            body=body,
            path=path,
            content=content,
        )


def discover_skills() -> tuple[Skill, ...]:
    skills = []
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            skills.append(Skill.from_path(skill_file))
    return tuple(skills)


def load_skill(skill_name: str) -> Skill:
    skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")
    return Skill.from_path(skill_path)
