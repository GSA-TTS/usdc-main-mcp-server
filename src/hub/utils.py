from fastmcp import Client, FastMCP

def mount_servers(mcp, servers_config=None):
    """
    Mount MCP servers from a JSON configuration file.
    
    Args:
        mcp: The MCP instance to mount servers to
        config_path: Path to the JSON configuration file
    
    Returns:
        The mcp instance with mounted servers
    """

    if servers_config is None:
        servers_config = [
            {
                "prefix": "places",
                "url": "https://cdc-places-mcp-server-bright-hartebeest-nc.app.cloud.gov/mcp"
            },
            {
                "prefix": "reporter",
                "url": "https://nih-reporter-mcp-server-relaxed-bilby-co.app.cloud.gov/mcp"
            }
        ]
    
    for server in servers_config:
        proxy = FastMCP.as_proxy(Client(server['url']))
        mcp.mount(proxy, prefix=server['prefix'])
    
    return mcp