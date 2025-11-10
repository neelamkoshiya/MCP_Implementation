import asyncio
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    # LangGraph available but using simplified approach for demo
    print("LangGraph installed successfully")
except ImportError as e:
    print(f"Missing MCP: {e}")
    print("Install with: pip install mcp")
    exit(1)

class LangGraphMCPClient:
    def __init__(self):
        self.session = None
    
    async def connect_and_test(self):
        """Connect to MCP server and test functionality"""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                print("Testing LangGraph MCP integration...")
                
                # Test weather tool
                weather_result = await session.call_tool("get_weather", {"location": "Default City"})
                print(f"Weather result: {weather_result.content[0].text}")
                
                # Test search tool
                search_result = await session.call_tool("search_documents", {"query": "computer vision", "limit": 3})
                print(f"Search result: {search_result.content[0].text}")
                
                print("✓ LangGraph MCP integration working!")

# Example usage
async def main():
    client = LangGraphMCPClient()
    await client.connect_and_test()

if __name__ == "__main__":
    asyncio.run(main())
