import json
from pathlib import Path

try:
    from fastmcp.server import create_proxy
except ImportError:
    create_proxy = None

from fastmcp import Client, FastMCP

DEFAULT_SERVERS_CONFIG = Path(__file__).with_name("servers.json")


def load_servers_config(config_path=DEFAULT_SERVERS_CONFIG):
    """Load mounted MCP server definitions from a JSON config file."""
    with Path(config_path).open(encoding="utf-8") as config_file:
        config = json.load(config_file)

    servers = config.get("servers") if isinstance(config, dict) else config
    if not isinstance(servers, list):
        raise ValueError("server configuration must contain a list of servers")

    for index, server in enumerate(servers):
        if not isinstance(server, dict):
            raise ValueError(f"server entry {index} must be an object")

        prefix = server.get("prefix")
        url = server.get("url")
        if not isinstance(prefix, str) or not prefix:
            raise ValueError(f"server entry {index} must define a non-empty prefix")
        if not isinstance(url, str) or not url:
            raise ValueError(f"server entry {index} must define a non-empty url")

    return servers


def create_mounted_proxy(server):
    """Create a proxy server across supported FastMCP versions."""
    if create_proxy is not None:
        return create_proxy(server["url"], name=server["prefix"])

    return FastMCP.as_proxy(Client(server["url"]))


def mount_servers(mcp, servers_config=None):
    """
    Mount MCP servers from a JSON configuration file.

    Args:
        mcp: The MCP instance to mount servers to
        servers_config: Optional list of server dictionaries. Defaults to
            servers.json next to this module.

    Returns:
        The mcp instance with mounted servers
    """

    if servers_config is None:
        servers_config = load_servers_config()

    for server in servers_config:
        proxy = create_mounted_proxy(server)
        if create_proxy is not None:
            mcp.mount(proxy, namespace=server["prefix"])
        else:
            mcp.mount(proxy, prefix=server["prefix"])

    return mcp
