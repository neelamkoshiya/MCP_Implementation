#!/usr/bin/env python3
"""
FastMCP server implementation with the same tools as the standard MCP server.
"""
try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not installed. Install with: pip install fastmcp")
    exit(1)

# Create FastMCP server
mcp = FastMCP("framework-fastmcp-server")

@mcp.tool()
def search_documents(query: str, limit: int = 10) -> str:
    """Search through documents"""
    return f"Found {limit} documents matching '{query}'"

@mcp.tool()
def get_weather(location: str) -> str:
    """Get weather information"""
    return f"Weather in {location}: 72°F, sunny"

if __name__ == "__main__":
    mcp.run()
