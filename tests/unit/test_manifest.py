"""Check that the plugin manifest and MCP config are valid and consistent."""
import json
import re

from tests.config import (
    COMPOSIO_MCP_URL,
    MCP_CONFIG,
    PLUGIN_MANIFEST,
    PLUGIN_NAME,
    PLUGIN_ROOT,
)

KEBAB = re.compile(r"^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$")


def _load(path):
    return json.loads(path.read_text())


class TestPluginManifest:
    def setup_method(self):
        self.manifest = _load(PLUGIN_MANIFEST)

    def test_name_is_kebab_case(self):
        assert KEBAB.match(self.manifest["name"]), f"plugin name '{self.manifest['name']}' not kebab-case"

    def test_skills_dir_is_discoverable(self):
        assert (PLUGIN_ROOT / "skills").is_dir(), "skills/ directory must exist for auto-discovery"

    def test_mcp_json_is_discoverable(self):
        assert (PLUGIN_ROOT / "mcp.json").exists(), "mcp.json must exist at plugin root for auto-discovery"

    def test_logo_path_exists(self):
        logo = self.manifest.get("logo")
        assert logo, "plugin.json must declare a logo"
        assert not logo.startswith(("/", "..")), f"logo path '{logo}' must be relative"
        assert (PLUGIN_ROOT / logo).exists(), f"logo path '{logo}' does not exist"


class TestMcpConfig:
    def setup_method(self):
        self.mcp = _load(MCP_CONFIG)

    def test_composio_server_points_at_connect_url(self):
        servers = self.mcp.get("mcpServers", {})
        assert "composio" in servers, "mcp.json must define a `composio` server"
        assert servers["composio"].get("url") == COMPOSIO_MCP_URL, (
            f"composio MCP url must be {COMPOSIO_MCP_URL}"
        )


class TestPluginName:
    def test_manifest_name_matches_expected(self):
        assert _load(PLUGIN_MANIFEST)["name"] == PLUGIN_NAME
