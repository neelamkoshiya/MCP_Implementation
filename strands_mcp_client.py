import asyncio
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError as e:
    print(f"Missing MCP: {e}")
    print("Install with: pip install mcp")
    exit(1)

# Simplified Strands-style implementation
class StrandsAgent:
    def __init__(self, name: str, tools: List, instructions: str):
        self.name = name
        self.tools = {tool.name: tool for tool in tools}
        self.instructions = instructions
    
    async def run(self, message: str) -> str:
        # Simple tool routing
        if "weather" in message.lower():
            return await self.tools["get_weather"].execute(location="Default City")
        elif "search" in message.lower() or "document" in message.lower():
            return await self.tools["search_documents"].execute(query="AI", limit=5)
        return f"Processed: {message}"

class StrandsTool:
    def __init__(self, name: str, description: str, session: ClientSession):
        self.name = name
        self.description = description
        self.session = session
    
    async def execute(self, **kwargs) -> str:
        result = await self.session.call_tool(self.name, kwargs)
        return result.content[0].text if result.content else ""

class StrandsMCPClient:
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
        
        # Create Strands tools from MCP tools
        for tool in tools_response.tools:
            strands_tool = StrandsTool(
                name=tool.name,
                description=tool.description,
                session=self.session
            )
            self.tools.append(strands_tool)
        
        # Create Strands agent with tools
        self.agent = StrandsAgent(
            name="mcp_agent",
            tools=self.tools,
            instructions="You are an agent with access to MCP tools."
        )
    
    async def chat(self, message: str) -> str:
        if not self.agent:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        response = await self.agent.run(message)
        return response
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = StrandsMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    # Direct tool usage
    docs = await client.search_documents("AI research", 5)
    print(f"Documents: {docs}")
    
    # Agent chat
    response = await client.chat("Search for machine learning documents")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
