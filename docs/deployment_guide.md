# MCP Server Deployment Guide 

## Initialize your Repository 
To maintain modularity, we recommend creating a new GitHub repository for each MCP server. We like to use uv for Python package management. 

```bash
uv init
uv venv
```

## Structure your MCP Server Repository 

After initializing your repository, set up your folder structure. We recommmend creating a 'src' direcotry and creating a folder named after your server in the src directory (for this server, we chose 'hub'). 

Inside that directory, put all your server code. The first file to create is the file that will run your app (we use 'app.py').

### app.py 

Start with importing your packages:

```python
from fastmcp import FastMCP
from reporter.tools import register_tools 
from reporter.prompts import register_prompts
from starlette.responses import JSONResponse
```

Then initialize your server with the FastMCP SDK, giving it the name you want your server known by: 

```python
mcp = FastMCP("reporter")
```

We then like to register our tools and prompts by calling util functions and passing the just-instantiated mcp object: 

```python 
register_tools(mcp)
register_prompts(mcp)
```

Then add the following so your server generates a health check response: 

```python 
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})
```

And lastly, create an ASGI app for cloud deployment:

```python 
app = mcp.http_app(stateless_http=True)
```

## Other files for deployment 

After developing the server source code and setting up your app.py file, we now need a few other files for deployment. 

### manifest.yml 

The manifest.yml file gives instructions to your cloud hosting on how to build and run your server. 

```bash
applications:
  - name: nih-reporter-mcp-server
    buildpacks:
        - python_buildpack
    command: PYTHONPATH=src uvicorn src.reporter.app:app --host 0.0.0.0 --port $PORT --workers 2
    health-check-type: http
    health-check-http-endpoint: /health
    env:
      PYTHONUNBUFFERED: 1
    random-route: true
    disk_quota: 512M
    memory: 256M
```

Note the line that gives the start command references src.reporter.app:app. This is where you point to your file that launches the ASGI application. For us, that is in the app.py file in the src/reporter directory and the object is named app. 

### Procfile 

The Procfile is a restatement of the launch command. 

```bash 
web: PYTHONPATH=src uvicorn src.reporter.app:app --host 0.0.0.0 --port $PORT --workers 2
```

### requirements.txt 

Depending on your cloud service providers Python build, you may need to export your package requirements to a requirements.txt file. To do that from uv: 

```bash 
uv export --no-dev --no-hashes > requirements.txt
```

