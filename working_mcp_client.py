#!/usr/bin/env python3
"""
Working MCP client example that demonstrates basic functionality.
"""
import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("MCP not installed. Install with: pip install mcp")
    exit(1)

class WorkingMCPClient:
    def __init__(self):
        self.session = None
        self.available_tools = []
    
    async def connect_and_demo(self):
        """Connect to MCP server and run demo"""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        
        # Use proper async context manager
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                self.available_tools = [tool.name for tool in tools_response.tools]
                print(f"Connected! Available tools: {self.available_tools}")
                
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
                    "location": "San Francisco"
                })
                print(f"Weather result: {weather_result.content[0].text}")
                
                # Test with different parameters
                print("\n3. Testing different parameters...")
                ai_search = await session.call_tool("search_documents", {
                    "query": "artificial intelligence",
                    "limit": 3
                })
                print(f"AI search: {ai_search.content[0].text}")
                
                tokyo_weather = await session.call_tool("get_weather", {
                    "location": "Tokyo"
                })
                print(f"Tokyo weather: {tokyo_weather.content[0].text}")
                
                print("\n✓ All MCP tool calls completed successfully!")

async def main():
    """Main function"""
    print("=== Working MCP Client Demo ===")
    
    try:
        client = WorkingMCPClient()
        await client.connect_and_demo()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure mcp_server.py is in the same directory.")

if __name__ == "__main__":
    asyncio.run(main())
