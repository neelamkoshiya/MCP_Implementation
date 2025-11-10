import asyncio
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError as e:
    print(f"Missing MCP: {e}")
    print("Install with: pip install mcp")
    exit(1)

# Simplified LangGraph-style implementation
class GraphState:
    def __init__(self):
        self.messages = []
        self.tool_results = {}

class LangGraphNode:
    def __init__(self, tools: Dict[str, Any]):
        self.tools = tools
    
    async def process(self, state: GraphState, message: str) -> GraphState:
        state.messages.append(message)
        
        # Simple routing logic
        if "weather" in message.lower():
            result = await self.tools["get_weather"].execute(location="Default City")
            state.tool_results["weather"] = result
        elif "search" in message.lower() or "document" in message.lower():
            result = await self.tools["search_documents"].execute(query="computer vision", limit=3)
            state.tool_results["search"] = result
        
        return state

class LangGraphTool:
    def __init__(self, name: str, description: str, session: ClientSession):
        self.name = name
        self.description = description
        self.session = session
    
    async def execute(self, **kwargs) -> str:
        result = await self.session.call_tool(self.name, kwargs)
        return result.content[0].text if result.content else ""

class LangGraphMCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
        self.tools = {}
        self.graph_node = None
    
    async def connect(self):
        server_params = StdioServerParameters(command=self.server_command)
        self.session = await stdio_client(server_params)
        await self.session.initialize()
        
        # Get available tools
        tools_response = await self.session.list_tools()
        
        # Create LangGraph tools from MCP tools
        for tool in tools_response.tools:
            lg_tool = LangGraphTool(
                name=tool.name,
                description=tool.description,
                session=self.session
            )
            self.tools[tool.name] = lg_tool
        
        # Create LangGraph node
        self.graph_node = LangGraphNode(self.tools)
    
    async def invoke(self, message: str) -> Dict[str, Any]:
        if not self.graph_node:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        initial_state = GraphState()
        result_state = await self.graph_node.process(initial_state, message)
        return result_state.tool_results
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        result = await self.session.call_tool("search_documents", {
            "query": query,
            "limit": limit
        })
        return result.content[0].text if result.content else ""

# Example usage
async def main():
    client = LangGraphMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    # Direct tool usage
    docs = await client.search_documents("computer vision", 3)
    print(f"Documents: {docs}")
    
    # Graph execution
    result = await client.invoke("Search for documents about AI")
    print(f"Graph result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
