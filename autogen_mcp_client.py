import asyncio
import json
from typing import Dict, Any, List
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    import autogen
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install mcp autogen-agentchat")
    exit(1)

class MCPAgent(autogen.ConversableAgent):
    def __init__(self, name: str, server_command: List[str], **kwargs):
        super().__init__(name, **kwargs)
        self.server_command = server_command
        self.session = None
        
    async def _connect_mcp(self):
        if not self.session:
            server_params = StdioServerParameters(command=self.server_command)
            self.session = await stdio_client(server_params)
            await self.session.initialize()
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        await self._connect_mcp()
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text if result.content else ""

class AutoGenMCPClient:
    def __init__(self):
        self.mcp_agent = MCPAgent(
            name="mcp_agent",
            server_command=["python", "mcp_server.py"],
            system_message="You are an agent with access to MCP tools."
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config=False
        )
    
    async def search_documents(self, query: str, limit: int = 10) -> str:
        return await self.mcp_agent.call_mcp_tool("search_documents", {
            "query": query, 
            "limit": limit
        })
    
    async def get_weather(self, location: str) -> str:
        return await self.mcp_agent.call_mcp_tool("get_weather", {
            "location": location
        })
    
    def chat(self, message: str):
        return self.user_proxy.initiate_chat(
            self.mcp_agent,
            message=message
        )

# Example usage
async def main():
    client = AutoGenMCPClient()
    
    # Use MCP tools
    weather = await client.get_weather("New York")
    print(f"Weather: {weather}")
    
    docs = await client.search_documents("machine learning", 5)
    print(f"Documents: {docs}")

if __name__ == "__main__":
    asyncio.run(main())
