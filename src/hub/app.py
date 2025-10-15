from fastmcp import FastMCP
from hub.utils import mount_servers
from starlette.responses import JSONResponse

# Initialize FastMCP server
mcp = FastMCP("main")

# Mount servers 
mcp = mount_servers(mcp)

# Health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})

# Create ASGI app for deployment
app = mcp.http_app(stateless_http=True)

# Run the server with stdio transport for local testing
# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='stdio')