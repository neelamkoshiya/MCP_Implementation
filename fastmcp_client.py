#!/usr/bin/env python3
"""
FastMCP client example that works with the FastMCP server.
"""
import asyncio
from typing import Dict, Any

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("MCP not installed. Install with: pip install mcp")
    exit(1)

class FastMCPClient:
    def __init__(self):
        self.session = None
        self.available_tools = []
    
    async def connect_and_demo(self):
        """Connect to FastMCP server and run demo"""
        server_params = StdioServerParameters(
            command="python",
            args=["fastmcp_server.py"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                self.available_tools = [tool.name for tool in tools_response.tools]
                print(f"Connected to FastMCP server! Available tools: {self.available_tools}")
                
                # Test search_documents
                print("\n1. Testing document search...")
                search_result = await session.call_tool("search_documents", {
                    "query": "machine learning",
                    "limit": 5
                })
                print(f"Search result: {search_result.content[0].text}")
                
                # Test get_weather
                print("\n2. Testing weather lookup...")
                weather_result = await session.call_tool("get_weather", {
                    "location": "New York"
                })
                print(f"Weather result: {weather_result.content[0].text}")
                
                print("\n✓ FastMCP server integration working!")

async def main():
    """Main function"""
    print("=== FastMCP Client Demo ===")
    
    try:
        client = FastMCPClient()
        await client.connect_and_demo()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure fastmcp_server.py is available and FastMCP is installed.")

if __name__ == "__main__":
    asyncio.run(main())
