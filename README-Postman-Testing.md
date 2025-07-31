# Testing Serper MCP Server with Postman

## Overview

The `serper-mcp-server` is an MCP (Model Context Protocol) server that communicates via stdio, not HTTP. To test it with Postman, we need an HTTP wrapper.

## Setup HTTP Wrapper

### 1. Build the HTTP Wrapper Docker Image

```bash
docker build -f Dockerfile.http_wrapper -t serper-http-wrapper .
```

### 2. Run the HTTP Wrapper

```bash
docker run -p 8000:8000 --rm serper-http-wrapper
```

The HTTP wrapper will be available at `http://localhost:8000`

## Postman Testing

### Available Endpoints

#### 1. **GET /** - Health Check
- **URL**: `http://localhost:8000/`
- **Method**: GET
- **Response**: Status and message

#### 2. **GET /tools** - List Available Tools
- **URL**: `http://localhost:8000/tools`
- **Method**: GET
- **Response**: List of available MCP tools

#### 3. **POST /search** - Google Search
- **URL**: `http://localhost:8000/search`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "query": "artificial intelligence",
    "num_results": 5
}
```

#### 4. **POST /search/images** - Image Search
- **URL**: `http://localhost:8000/search/images`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "query": "cute cats",
    "num_results": 3
}
```

#### 5. **POST /search/videos** - Video Search
- **URL**: `http://localhost:8000/search/videos`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "query": "machine learning tutorial",
    "num_results": 5
}
```

#### 6. **POST /scrape** - Webpage Scraping
- **URL**: `http://localhost:8000/scrape`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "url": "https://example.com"
}
```

## Postman Collection

You can import this collection into Postman:

```json
{
    "info": {
        "name": "Serper MCP Server",
        "description": "HTTP wrapper for testing the Serper MCP Server"
    },
    "item": [
        {
            "name": "Health Check",
            "request": {
                "method": "GET",
                "url": "http://localhost:8000/"
            }
        },
        {
            "name": "List Tools",
            "request": {
                "method": "GET",
                "url": "http://localhost:8000/tools"
            }
        },
        {
            "name": "Google Search",
            "request": {
                "method": "POST",
                "url": "http://localhost:8000/search",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"query\": \"artificial intelligence\",\n    \"num_results\": 5\n}"
                }
            }
        },
        {
            "name": "Image Search",
            "request": {
                "method": "POST",
                "url": "http://localhost:8000/search/images",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"query\": \"cute cats\",\n    \"num_results\": 3\n}"
                }
            }
        },
        {
            "name": "Video Search",
            "request": {
                "method": "POST",
                "url": "http://localhost:8000/search/videos",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"query\": \"machine learning tutorial\",\n    \"num_results\": 5\n}"
                }
            }
        },
        {
            "name": "Scrape Webpage",
            "request": {
                "method": "POST",
                "url": "http://localhost:8000/scrape",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"url\": \"https://example.com\"\n}"
                }
            }
        }
    ]
}
```

## Alternative Testing Methods

### 1. **MCP Inspector (Recommended)**
```bash
npx @modelcontextprotocol/inspector docker run -it --rm -e SERPER_API_KEY=your_api_key serper-mcp-server
```

### 2. **Direct MCP Testing**
```bash
# Test the MCP server directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | docker run -i --rm -e SERPER_API_KEY=your_api_key serper-mcp-server
```

## Notes

- The HTTP wrapper creates a new Docker container for each request
- This approach is suitable for testing but not recommended for production
- For production use, consider using MCP clients directly
- The wrapper adds latency due to Docker container startup time 