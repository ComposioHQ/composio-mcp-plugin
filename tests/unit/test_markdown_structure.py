import re

from tests.skill import discover_skills


class TestMarkdownStructure:
    def setup_method(self):
        self.skills = discover_skills()

    def test_has_content(self):
        for skill in self.skills:
            assert len(skill.body) > 100, f"{skill.path}: body is suspiciously short"

    def test_has_top_level_heading(self):
        for skill in self.skills:
            assert re.search(r"(?m)^#\s+", skill.body), f"{skill.path}: missing a top-level (#) heading"

    def test_has_section_structure(self):
        for skill in self.skills:
            headings = re.findall(r"^##\s+", skill.body, re.MULTILINE)
            assert len(headings) >= 2, f"{skill.path}: needs at least two (##) sections"
