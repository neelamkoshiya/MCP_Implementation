import asyncio
from typing import Dict, Any, List, Optional
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from llama_index.core.tools import BaseTool, ToolMetadata
    from llama_index.core.agent import ReActAgent
    from llama_index.llms.openai import OpenAI
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install mcp llama-index llama-index-llms-openai")
    exit(1)

class MCPTool(BaseTool):
    def __init__(self, tool_name: str, description: str, session: ClientSession):
        self.tool_name = tool_name
        self.session = session
        metadata = ToolMetadata(
            name=tool_name,
            description=description
        )
        super().__init__(metadata=metadata)
    
    def call(self, **kwargs) -> str:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._async_call(**kwargs))
    
    async def _async_call(self, **kwargs) -> str:
        result = await self.session.call_tool(self.tool_name, kwargs)
        return result.content[0].text if result.content else ""

class LlamaIndexMCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
        self.tools = []
        self.agent = None
    
    async def connect(self):
        server_params = StdioServerParameters(command=self.server_command)
        self.session = await stdio_client(server_params)
        await self.session.initialize()
        
        # Get available tools
        tools_response = await self.session.list_tools()
        
        # Create LlamaIndex tools from MCP tools
        for tool in tools_response.tools:
            mcp_tool = MCPTool(
                tool_name=tool.name,
                description=tool.description,
                session=self.session
            )
            self.tools.append(mcp_tool)
        
        # Create ReAct agent with tools
        llm = OpenAI(model="gpt-3.5-turbo")
        self.agent = ReActAgent.from_tools(
            tools=self.tools,
            llm=llm,
            verbose=True
        )
    
    def chat(self, message: str) -> str:
        if not self.agent:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        response = self.agent.chat(message)
        return str(response)
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""
    
    async def get_weather(self, location: str) -> str:
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        result = await self.session.call_tool("get_weather", {
            "location": location
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = LlamaIndexMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    # Direct tool usage
    weather = await client.get_weather("San Francisco")
    print(f"Weather: {weather}")
    
    # Agent-based chat
    response = client.chat("What's the weather like in Boston?")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
