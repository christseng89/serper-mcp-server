# Addendum

## Install Environment

```cmd
git clone https://github.com/christseng89/serper-mcp-server.git
cd serper-mcp-server
code .
```

```cmd
uv sync
.venv\Scripts\activate
uv sync --upgrade
mcp version
    MCP version 1.12.2

python --version
    Python 3.11.12

npx @modelcontextprotocol/inspector uvx serper-mcp-server
    Add Environment Variables:
        SERPER_API_KEY
        b3cf5....
    Connect => List Tools

uv run -m serper_mcp_server    

```

---

## Docker Build

```cmd
docker build -t serper-mcp-server .
docker run -it --rm -e SERPER_API_KEY=b3cf59ac4... serper-mcp-server
docker run -it -d -e SERPER_API_KEY=b3cf59ac4419d9a8d178413be78c9aefd8d7c6f6 serper-mcp-server
```
