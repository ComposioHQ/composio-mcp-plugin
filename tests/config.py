"""Paths and expected values shared across the test suite."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PLUGIN_ROOT = REPO_ROOT  # root-as-plugin layout

SKILLS_ROOT = PLUGIN_ROOT / "skills"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".cursor-plugin" / "plugin.json"
MCP_CONFIG = PLUGIN_ROOT / "mcp.json"

# Read from the manifest so a rename only needs to change one file.
PLUGIN_NAME = json.loads(PLUGIN_MANIFEST.read_text())["name"]

EXPECTED_SKILLS = ("composio-mcp",)
COMPOSIO_MCP_URL = "https://connect.composio.dev/mcp"
