import re

from tests.config import PLUGIN_NAME
from tests.skill import discover_skills


class TestCrossSkillReferences:
    """Validate cross-skill references and link formatting in skill bodies."""

    def setup_method(self):
        self.skills = discover_skills()
        self.skill_names = {skill.metadata.name for skill in self.skills}

    def test_plugin_skill_references_target_real_skills(self):
        pattern = re.compile(rf"`{re.escape(PLUGIN_NAME)}:([a-z0-9-]+)`")
        for skill in self.skills:
            for target in pattern.findall(skill.body):
                assert target in self.skill_names, (
                    f"{skill.path} references unknown skill `{PLUGIN_NAME}:{target}`"
                )

    def test_no_markdown_anchor_links(self):
        for skill in self.skills:
            idx = skill.body.find("](#")
            snippet = skill.body[idx : idx + 30]
            assert idx == -1, f"{skill.path} uses a markdown anchor link near \"{snippet}\""

    def test_no_bare_skill_file_paths(self):
        for skill in self.skills:
            idx = skill.body.find("SKILL.md")
            start = max(0, idx - 30)
            snippet = skill.body[start : idx + 8]
            assert idx == -1, (
                f"{skill.path} references a SKILL.md path near \"{snippet}\"; "
                f"reference skills by the backticked `{PLUGIN_NAME}:skill` form instead"
            )
