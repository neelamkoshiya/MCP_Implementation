import asyncio
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain.agents import create_agent
    from langchain_anthropic import ChatAnthropic
    print("LangChain MCP adapter loaded successfully")
except ImportError as e:
    print(f"Missing LangChain MCP: {e}")
    print("Install with: pip install langchain langchain-mcp-adapters langchain-anthropic")
    exit(1)

class LangChainMCPClient:
    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self.mcp_client = None
        self.agent = None
    
    async def connect(self):
        """Connect to MCP server using official LangChain MCP adapter"""
        # Create MCP client
        self.mcp_client = MultiServerMCPClient({
            "server1": {
                "transport": "stdio",
                "command": self.server_command[0],
                "args": self.server_command[1:]
            }
        })
        
        # Get MCP tools
        tools = await self.mcp_client.get_tools()
        
        # Create LangChain agent with MCP tools
        try:
            llm = ChatAnthropic(model="claude-3-sonnet-20240229")
            self.agent = create_agent(llm, tools)
        except Exception as e:
            print(f"LLM setup failed: {e}. Set ANTHROPIC_API_KEY environment variable.")
        
        print("LangChain MCP integration initialized")
    
    async def invoke(self, message: str) -> str:
        """Invoke the agent with MCP tools"""
        if not self.agent:
            return f"Processed: {message} (no LLM configured)"
        
        result = await self.agent.ainvoke({"input": message})
        return result["output"]

# Example usage
async def main():
    client = LangChainMCPClient(["python", "mcp_server.py"])
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
