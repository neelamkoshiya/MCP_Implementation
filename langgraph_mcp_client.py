import asyncio
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from langchain_anthropic import ChatAnthropic
    from typing import Annotated, TypedDict
    print("LangGraph MCP adapter loaded successfully")
except ImportError as e:
    print(f"Missing LangGraph MCP: {e}")
    print("Install with: pip install langgraph langchain-mcp-adapters langchain-anthropic")
    exit(1)

class State(TypedDict):
    messages: Annotated[list, add_messages]

class LangGraphMCPClient:
    def __init__(self):
        self.mcp_client = None
        self.graph = None
    
    async def connect_and_test(self):
        """Connect to MCP server using official LangGraph MCP integration"""
        # Create MCP client
        self.mcp_client = MultiServerMCPClient({
            "server1": {
                "transport": "stdio",
                "command": "python",
                "args": ["mcp_server.py"]
            }
        })
        
        # Get MCP tools
        tools = await self.mcp_client.get_tools()
        
        # Create LLM with tools
        try:
            llm = ChatAnthropic(model="claude-3-sonnet-20240229").bind_tools(tools)
            
            # Create LangGraph workflow
            workflow = StateGraph(State)
            
            def call_model(state: State):
                response = llm.invoke(state["messages"])
                return {"messages": [response]}
            
            workflow.add_node("model", call_model)
            workflow.set_entry_point("model")
            workflow.add_edge("model", END)
            
            self.graph = workflow.compile()
            
            # Test the workflow
            result = await self.graph.ainvoke({
                "messages": [("human", "Search for AI documents and get weather for Tokyo")]
            })
            
            print(f"LangGraph result: {result['messages'][-1].content}")
            
        except Exception as e:
            print(f"LLM setup failed: {e}. Set ANTHROPIC_API_KEY environment variable.")
            print("Testing MCP tools directly...")
            
            # Test tools directly without LLM
            for tool in tools:
                if hasattr(tool, 'name'):
                    if tool.name == "get_weather":
                        result = await tool.ainvoke({"location": "Tokyo"})
                        print(f"Weather result: {result}")
                    elif tool.name == "search_documents":
                        result = await tool.ainvoke({"query": "AI", "limit": 3})
                        print(f"Search result: {result}")
        
        print("✓ LangGraph MCP integration working!")

# Example usage
async def main():
    client = LangGraphMCPClient()
    await client.connect_and_test()

if __name__ == "__main__":
    asyncio.run(main())
