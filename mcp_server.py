#!/usr/bin/env python3
import asyncio
import json
from typing import Any, Dict, List
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP not installed. Install with: pip install mcp")
    exit(1)

app = Server("framework-mcp-server")

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="search_documents",
            description="Search through documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_weather",
            description="Get weather information",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Location name"}
                },
                "required": ["location"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "search_documents":
        query = arguments["query"]
        limit = arguments.get("limit", 10)
        results = f"Found {limit} documents matching '{query}'"
        return [TextContent(type="text", text=results)]
    
    elif name == "get_weather":
        location = arguments["location"]
        weather = f"Weather in {location}: 72°F, sunny"
        return [TextContent(type="text", text=weather)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
