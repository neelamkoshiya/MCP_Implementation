import asyncio
from typing import Dict, Any, List, Optional
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from langchain.tools import BaseTool
    from langchain_openai import ChatOpenAI
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install mcp langchain langchain-openai")
    exit(1)

class MCPLangChainTool(BaseTool):
    def __init__(self, tool_name: str, description: str, session: ClientSession):
        self.tool_name = tool_name
        self.session = session
        super().__init__(
            name=tool_name,
            description=description
        )
    
    def _run(self, **kwargs) -> str:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._async_run(**kwargs))
    
    async def _async_run(self, **kwargs) -> str:
        result = await self.session.call_tool(self.tool_name, kwargs)
        return result.content[0].text if result.content else ""

class LangChainMCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
        self.tools = []
        self.llm = None
    
    async def connect(self):
        server_params = StdioServerParameters(command=self.server_command)
        self.session = await stdio_client(server_params)
        await self.session.initialize()
        
        # Get available tools
        tools_response = await self.session.list_tools()
        
        # Create LangChain tools from MCP tools
        for tool in tools_response.tools:
            lc_tool = MCPLangChainTool(
                tool_name=tool.name,
                description=tool.description,
                session=self.session
            )
            self.tools.append(lc_tool)
        
        # Create LangChain LLM
        try:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        except Exception:
            print("OpenAI API key not set. Set OPENAI_API_KEY environment variable.")
    
    async def invoke(self, message: str) -> str:
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        # Simple tool routing for demo
        if "weather" in message.lower():
            result = await self.session.call_tool("get_weather", {"location": "Paris"})
            return result.content[0].text if result.content else ""
        elif "search" in message.lower() or "document" in message.lower():
            result = await self.session.call_tool("search_documents", {"query": "neural networks", "limit": 4})
            return result.content[0].text if result.content else ""
        
        return f"Processed: {message}"
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = LangChainMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    # Direct tool usage
    docs = await client.search_documents("neural networks", 4)
    print(f"Documents: {docs}")
    
    # Agent execution
    response = await client.invoke("What's the weather like in Paris?")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
