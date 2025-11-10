import asyncio
import os
try:
    from crewai import Agent, Task, Crew, LLM
    from crewai.mcp import MCPServerStdio
    from crewai.mcp.filters import create_static_tool_filter
    print("CrewAI MCP adapter loaded successfully")
except ImportError as e:
    print(f"Missing CrewAI MCP: {e}")
    print("Install with: pip install crewai langchain-aws boto3")
    exit(1)

class CrewAIBedrockMCPClient:
    def __init__(self):
        self.mcp_server = None
        self.crew = None
    
    async def connect_and_test(self):
        """Connect to MCP server using official CrewAI adapter with Bedrock LLM"""
        # Initialize MCP server with stdio transport
        self.mcp_server = MCPServerStdio(
            command="python",
            args=["mcp_server.py"]
        )
        
        # Create tool filter for specific tools
        tool_filter = create_static_tool_filter(["search_documents", "get_weather"])
        
        # Create Bedrock LLM using CrewAI's LLM wrapper
        try:
            bedrock_llm = LLM(
                model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
                aws_region_name="us-east-1"
            )
        except Exception as e:
            print(f"Bedrock LLM setup failed: {e}. Configure AWS credentials.")
            return
        
        # Create agent with MCP tools and Bedrock LLM
        researcher = Agent(
            role="Research Assistant",
            goal="Help with document search and weather information",
            backstory="Expert at finding information using available tools",
            llm=bedrock_llm,
            mcp_servers=[self.mcp_server],
            mcp_tool_filter=tool_filter,
            verbose=True
        )
        
        # Create tasks
        search_task = Task(
            description="Search for documents about 'machine learning' and get weather for San Francisco",
            expected_output="Document search results and weather information",
            agent=researcher
        )
        
        # Create and run crew
        self.crew = Crew(
            agents=[researcher],
            tasks=[search_task],
            verbose=True
        )
        
        print("Testing CrewAI MCP integration with Bedrock...")
        result = await self.crew.kickoff_async()
        print(f"Crew result: {result}")
        print("✓ CrewAI MCP integration with Bedrock working!")

# Example usage
async def main():
    client = CrewAIBedrockMCPClient()
    await client.connect_and_test()

if __name__ == "__main__":
    asyncio.run(main())
