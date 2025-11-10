import asyncio
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError as e:
    print(f"Missing MCP: {e}")
    print("Install with: pip install mcp")
    exit(1)

# Simplified CrewAI-style implementation
class CrewAgent:
    def __init__(self, role: str, goal: str, backstory: str, tools: List):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = {tool.name: tool for tool in tools}
    
    async def execute_task(self, description: str) -> str:
        # Simple task routing
        if "weather" in description.lower():
            return await self.tools["get_weather"].execute(location="Tokyo")
        elif "search" in description.lower() or "document" in description.lower():
            return await self.tools["search_documents"].execute(query="deep learning", limit=3)
        return f"Task completed: {description}"

class CrewTool:
    def __init__(self, name: str, description: str, session: ClientSession):
        self.name = name
        self.description = description
        self.session = session
    
    async def execute(self, **kwargs) -> str:
        result = await self.session.call_tool(self.name, kwargs)
        return result.content[0].text if result.content else ""

class CrewAIMCPClient:
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
        
        # Create CrewAI tools from MCP tools
        for tool in tools_response.tools:
            crew_tool = CrewTool(
                name=tool.name,
                description=tool.description,
                session=self.session
            )
            self.tools.append(crew_tool)
        
        # Create CrewAI agent with tools
        self.agent = CrewAgent(
            role="MCP Assistant",
            goal="Help users with MCP tool capabilities",
            backstory="An AI agent with access to MCP tools for various tasks",
            tools=self.tools
        )
    
    async def execute_task(self, description: str) -> str:
        if not self.agent:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        result = await self.agent.execute_task(description)
        return result
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = CrewAIMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    # Direct tool usage
    docs = await client.search_documents("deep learning", 3)
    print(f"Documents: {docs}")
    
    # Task execution
    result = await client.execute_task("Search for weather information in Tokyo")
    print(f"Task result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
