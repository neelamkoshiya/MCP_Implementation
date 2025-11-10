#!/usr/bin/env python3
"""
Minimal working MCP client that demonstrates basic functionality
without external framework dependencies.
"""
import asyncio
import json
from typing import Dict, Any, List

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("MCP not installed. Install with: pip install mcp")
    exit(1)

class MinimalMCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
        self.available_tools = []
    
    async def connect(self):
        """Connect to MCP server and get available tools"""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        
        # Use async context manager properly
        session_context = stdio_client(server_params)
        self.session = await session_context.__aenter__()
        await self.session.initialize()
        
        # Get available tools
        tools_response = await self.session.list_tools()
        self.available_tools = [tool.name for tool in tools_response.tools]
        print(f"Connected to MCP server. Available tools: {self.available_tools}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a specific MCP tool"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available. Available: {self.available_tools}")
        
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text if result.content else ""
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        """Search documents using MCP tool"""
        return await self.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
    
    async def get_weather(self, location: str) -> str:
        """Get weather using MCP tool"""
        return await self.call_tool("get_weather", {
            "location": location
        })
    
    async def interactive_demo(self):
        """Interactive demonstration of MCP capabilities"""
        print("\n=== MCP Client Demo ===")
        
        # Test search_documents
        print("\n1. Testing document search...")
        docs_result = await self.search_documents("machine learning", 5)
        print(f"Search result: {docs_result}")
        
        # Test get_weather
        print("\n2. Testing weather lookup...")
        weather_result = await self.get_weather("San Francisco")
        print(f"Weather result: {weather_result}")
        
        # Test with different parameters
        print("\n3. Testing with different parameters...")
        docs_result2 = await self.search_documents("artificial intelligence", 3)
        print(f"AI search result: {docs_result2}")
        
        weather_result2 = await self.get_weather("Tokyo")
        print(f"Tokyo weather: {weather_result2}")
        
        print("\n✓ All MCP tool calls completed successfully!")

async def main():
    """Main demonstration function"""
    print("Starting MCP Client Demo...")
    
    # Create client
    client = MinimalMCPClient("python mcp_server.py")
    
    try:
        # Connect to server
        await client.connect()
        
        # Run interactive demo
        await client.interactive_demo()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure mcp_server.py is in the same directory and MCP is installed.")

if __name__ == "__main__":
    asyncio.run(main())
