import asyncio
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    import boto3
    from langchain_aws import ChatBedrock
    from langchain.tools import BaseTool
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install mcp langchain langchain-aws boto3")
    exit(1)

class MCPBedrockTool(BaseTool):
    name: str
    description: str
    
    def __init__(self, tool_name: str, description: str, session):
        super().__init__(name=tool_name, description=description)
        self._tool_name = tool_name
        self._session = session
    
    def _run(self, **kwargs) -> str:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._async_run(**kwargs))
    
    async def _async_run(self, **kwargs) -> str:
        result = await self._session.call_tool(self._tool_name, kwargs)
        return result.content[0].text if result.content else ""

class BedrockMCPClient:
    def __init__(self, server_command: List[str], region: str = "us-east-1"):
        self.server_command = server_command
        self.region = region
        self.session = None
        self.tools = []
        self.llm = None
    
    async def connect(self):
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                
                # Create Bedrock tools from MCP tools
                for tool in tools_response.tools:
                    bedrock_tool = MCPBedrockTool(
                        tool_name=tool.name,
                        description=tool.description,
                        session=session
                    )
                    self.tools.append(bedrock_tool)
                
                # Create Bedrock LLM
                try:
                    self.llm = ChatBedrock(
                        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                        region_name=self.region
                    )
                    print("Bedrock LLM initialized successfully")
                except Exception as e:
                    print(f"Bedrock setup failed: {e}")
                    print("Ensure AWS credentials are configured and Bedrock access is enabled.")
                
                # Test direct tool usage
                print("Testing Bedrock MCP integration...")
                
                # Test weather tool
                weather_result = await session.call_tool("get_weather", {"location": "Seattle"})
                print(f"Weather result: {weather_result.content[0].text}")
                
                # Test search tool
                search_result = await session.call_tool("search_documents", {"query": "AWS", "limit": 5})
                print(f"Search result: {search_result.content[0].text}")
                
                print("✓ Bedrock MCP integration working!")
    
    async def invoke(self, message: str) -> str:
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        # Simple tool routing for demo
        if "weather" in message.lower():
            result = await self.session.call_tool("get_weather", {"location": "Seattle"})
            return result.content[0].text if result.content else ""
        elif "search" in message.lower() or "document" in message.lower():
            result = await self.session.call_tool("search_documents", {"query": "AWS", "limit": 5})
            return result.content[0].text if result.content else ""
        
        return f"Processed with Bedrock: {message}"
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = BedrockMCPClient(["python", "mcp_server.py"])
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
