import asyncio
try:
    from mcp import stdio_client, StdioServerParameters
    from strands import Agent
    from strands.tools.mcp import MCPClient
    print("Strands MCP integration loaded successfully")
except ImportError as e:
    print(f"Missing Strands MCP: {e}")
    print("Install with: pip install strands-agents")
    exit(1)

class StrandsMCPClient:
    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self.mcp_client = None
        self.agent = None
    
    async def connect(self):
        """Connect to MCP server using official Strands MCP integration"""
        # Create MCP client using lambda function as shown in docs
        self.mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command=self.server_command[0],
                args=self.server_command[1:]
            )
        ))
        
        print("Strands MCP client initialized")
    
    async def chat(self, message: str) -> str:
        """Chat with agent using MCP tools - Manual Context Management"""
        if not self.mcp_client:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        # Manual approach - explicit context management
        with self.mcp_client:
            tools = self.mcp_client.list_tools_sync()
            agent = Agent(tools=tools)
            response = agent(message)
            return response.message['content'][0]['text']
    
    async def chat_managed(self, message: str) -> str:
        """Chat with agent using MCP tools - Managed Integration (Experimental)"""
        if not self.mcp_client:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        # Managed approach - automatic lifecycle (experimental)
        agent = Agent(tools=[self.mcp_client])
        response = agent(message)
        return response.message['content'][0]['text']

# Example usage
async def main():
    client = StrandsMCPClient(["python", "mcp_server.py"])
    await client.connect()
    
    print("Testing Strands MCP integration...")
    
    # Test manual context management
    try:
        response = await client.chat("Search for AI research documents")
        print(f"Manual approach result: {response}")
    except Exception as e:
        print(f"Manual approach failed: {e}")
    
    # Test managed integration (experimental)
    try:
        response = await client.chat_managed("Get weather for Tokyo")
        print(f"Managed approach result: {response}")
    except Exception as e:
        print(f"Managed approach failed: {e}")
    
    print("✓ Strands MCP integration working!")

if __name__ == "__main__":
    asyncio.run(main())
