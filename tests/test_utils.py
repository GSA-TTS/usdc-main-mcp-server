import json

import pytest

from hub.utils import load_servers_config, mount_servers


class DummyMCP:
    def __init__(self):
        self.mounts = []

    def mount(self, proxy, **kwargs):
        self.mounts.append((kwargs, proxy))


def test_load_servers_config_reads_servers_file(tmp_path):
    config_path = tmp_path / "servers.json"
    config_path.write_text(
        json.dumps(
            {
                "servers": [
                    {"prefix": "places", "url": "https://example.test/mcp"},
                ],
            }
        ),
        encoding="utf-8",
    )

    assert load_servers_config(config_path) == [
        {"prefix": "places", "url": "https://example.test/mcp"},
    ]


def test_load_servers_config_rejects_missing_fields(tmp_path):
    config_path = tmp_path / "servers.json"
    config_path.write_text(
        json.dumps({"servers": [{"prefix": "places"}]}), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="non-empty url"):
        load_servers_config(config_path)


def test_mount_servers_uses_supplied_config(monkeypatch):
    created_proxies = []

    def dummy_create_proxy(url, name):
        created_proxies.append((url, name))
        return f"proxy:{name}"

    monkeypatch.setattr("hub.utils.create_proxy", dummy_create_proxy)

    mcp = mount_servers(
        DummyMCP(),
        servers_config=[
            {"prefix": "places", "url": "https://example.test/places"},
            {"prefix": "reporter", "url": "https://example.test/reporter"},
        ],
    )

    assert created_proxies == [
        ("https://example.test/places", "places"),
        ("https://example.test/reporter", "reporter"),
    ]
    assert mcp.mounts == [
        ({"namespace": "places"}, "proxy:places"),
        ({"namespace": "reporter"}, "proxy:reporter"),
    ]


def test_mount_servers_supports_legacy_fastmcp_proxy(monkeypatch):
    class DummyClient:
        def __init__(self, url):
            self.url = url

    class DummyFastMCP:
        @staticmethod
        def as_proxy(client):
            return f"legacy-proxy:{client.url}"

    monkeypatch.setattr("hub.utils.create_proxy", None)
    monkeypatch.setattr("hub.utils.Client", DummyClient)
    monkeypatch.setattr("hub.utils.FastMCP", DummyFastMCP)

    mcp = mount_servers(
        DummyMCP(),
        servers_config=[{"prefix": "places", "url": "https://example.test/places"}],
    )

    assert mcp.mounts == [
        ({"prefix": "places"}, "legacy-proxy:https://example.test/places"),
    ]
