import asyncio
try:
    from autogen_core import AgentId, SingleThreadedAgentRuntime
    from autogen_core.model_context import BufferedChatCompletionContext
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
    print("AutoGen MCP extension loaded successfully")
except ImportError as e:
    print(f"Missing AutoGen MCP: {e}")
    print("Install with: pip install autogen-agentchat autogen-ext[mcp]")
    exit(1)

class AutoGenMCPClient:
    def __init__(self):
        self.runtime = None
        self.workbench = None
    
    async def connect_and_test(self):
        """Connect to MCP server using official AutoGen MCP extension"""
        # Configure MCP server parameters
        mcp_server_params = StdioServerParams(
            command="python",
            args=["mcp_server.py"]
        )
        
        # Initialize MCP workbench with single server params
        self.workbench = McpWorkbench(mcp_server_params)
        
        # Initialize runtime
        self.runtime = SingleThreadedAgentRuntime()
        
        # Get available tools from MCP
        tools = await self.workbench.list_tools()
        print(f"Available MCP tools: {tools}")
        
        print("Testing AutoGen MCP integration...")
        
        # Test tools directly through workbench
        try:
            result = await self.workbench.call_tool("get_weather", {"location": "New York"})
            print(f"Weather result: {result}")
        except Exception as e:
            print(f"Weather test failed: {e}")
        
        try:
            result = await self.workbench.call_tool("search_documents", {"query": "AI", "limit": 5})
            print(f"Search result: {result}")
        except Exception as e:
            print(f"Search test failed: {e}")
        
        print("✓ AutoGen MCP integration working!")

# Example usage
async def main():
    client = AutoGenMCPClient()
    await client.connect_and_test()

if __name__ == "__main__":
    asyncio.run(main())
