from fastmcp import Client, FastMCP
import json

def mount_servers(mcp, config_path="servers.json"):
    """
    Mount MCP servers from a JSON configuration file.
    
    Args:
        mcp: The MCP instance to mount servers to
        config_path: Path to the JSON configuration file
    
    Returns:
        The mcp instance with mounted servers
    """
    # Load server configuration
    with open(config_path, 'r') as f:
        servers_config = json.load(f)
    
    # Mount each server
    for server in servers_config.get('servers', []):
        proxy = FastMCP.as_proxy(
            Client(server['url'])
        )
        mcp.mount(proxy, prefix=server['prefix'])
    
    return mcp