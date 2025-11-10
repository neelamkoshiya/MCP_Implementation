# MCP_Implementation
In this repo, we will be focusing on the implementation of MCP Client and Server.

## Getting Started

The Model Context Protocol (MCP) represents a significant advancement in AI development, providing standardized guidelines for how AI models should interpret and respond to context during interactions.

These resources collectively explain MCP's technical implementation across different platforms and its practical applications in improving AI reliability and safety through better context handling.

* [Anthropic - Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
* [Hugging Face Blog - MCP](https://huggingface.co/blog/Kseniase/mcp)
* [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/en/unit0/introduction)
* [Wikipedia - Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)
* [GitHub - Model Context Protocol](https://github.com/modelcontextprotocol)
* [MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
* [Anthropic - Core Views on AI Safety](https://www.anthropic.com/news/core-views-on-ai-safety)
* [YouTube Video 1](https://www.youtube.com/watch?v=kQmXtrmQ5Zg)
* [YouTube Video 2](https://www.youtube.com/watch?v=sfCBCyNyw7U)


# MCP Integration for AI Agent Frameworks

Complete Model Context Protocol (MCP) client implementations for 8 major AI agent frameworks with both standard MCP and FastMCP support.

## Files

- `mcp_server.py` - Standard MCP server with sample tools
- `fastmcp_server.py` - FastMCP server (simplified syntax)
- `fastmcp_client.py` - FastMCP client example
- `working_mcp_client.py` - Basic working MCP client
- `minimal_mcp_client.py` - Minimal MCP client example
- `autogen_mcp_client.py` - AutoGen integration
- `llamaindex_mcp_client.py` - LlamaIndex integration (Claude)
- `strands_mcp_client.py` - Strands Agents integration
- `crewai_mcp_client.py` - CrewAI integration
- `langchain_mcp_client.py` - LangChain integration (Claude)
- `langgraph_mcp_client.py` - LangGraph integration
- `bedrock_mcp_client.py` - AWS Bedrock integration
- `test_clients.py` - Test script for all implementations
- `test_summary.py` - Comprehensive test runner

## Quick Start

### 1. Install Core Dependencies
```bash
pip install mcp fastmcp anthropic
```

### 2. Test Basic Functionality

**Standard MCP:**
```bash
python working_mcp_client.py
```

**FastMCP (Simplified):**
```bash
python fastmcp_client.py
```

Expected output:
```
=== Working MCP Client Demo ===
Connected! Available tools: ['search_documents', 'get_weather']

1. Testing document search...
Search result: Found 5 documents matching 'machine learning'

2. Testing weather lookup...
Weather result: Weather in San Francisco: 72°F, sunny

✓ All MCP tool calls completed successfully!
```

## Framework Integrations

### Install Framework Dependencies

```bash
# AutoGen
pip install autogen-agentchat

# LlamaIndex with Claude
pip install llama-index llama-index-llms-anthropic

# LangChain with Claude
pip install langchain langchain-anthropic

# AWS Bedrock
pip install langchain-aws boto3

# CrewAI
pip install crewai

# LangGraph (included with LangChain)
pip install langgraph

# LLM providers
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"

# For Bedrock (configure AWS credentials)
aws configure
```

### Usage Examples

#### Standard MCP Client
```python
from working_mcp_client import WorkingMCPClient
import asyncio

async def main():
    client = WorkingMCPClient()
    await client.connect_and_demo()

asyncio.run(main())
```

#### AutoGen Client
```python
from autogen_mcp_client import AutoGenMCPClient
import asyncio

async def main():
    client = AutoGenMCPClient()
    await client.connect_and_test()

asyncio.run(main())
```

#### LlamaIndex Client
```python
from llamaindex_mcp_client import LlamaIndexMCPClient
import asyncio

async def main():
    client = LlamaIndexMCPClient()
    await client.connect_and_test()

asyncio.run(main())
```

#### Strands Agents Client
```python
from strands_mcp_client import StrandsMCPClient
import asyncio

async def main():
    client = StrandsMCPClient(["python", "mcp_server.py"])
    await client.connect()
    response = await client.chat("Search for AI research documents")

asyncio.run(main())
```

#### CrewAI Client
```python
from crewai_mcp_client import CrewAIMCPClient
import asyncio

async def main():
    client = CrewAIMCPClient()
    await client.connect_and_test()

asyncio.run(main())
```

#### LangChain Client
```python
from langchain_mcp_client import LangChainMCPClient
import asyncio

async def main():
    client = LangChainMCPClient(["python", "mcp_server.py"])
    await client.connect()

asyncio.run(main())
```

#### LangGraph Client
```python
from langgraph_mcp_client import LangGraphMCPClient
import asyncio

async def main():
    client = LangGraphMCPClient()
    await client.connect_and_test()

asyncio.run(main())
```

#### AWS Bedrock Client
```python
from bedrock_mcp_client import BedrockMCPClient
import asyncio

async def main():
    client = BedrockMCPClient(["python", "mcp_server.py"], region="us-east-1")
    await client.connect()

asyncio.run(main())
```

## Configuration

**Claude (Anthropic):**
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

**AWS Bedrock:**
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

## MCP vs FastMCP

**Standard MCP Server:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("framework-mcp-server")

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "search_documents":
        query = arguments["query"]
        limit = arguments.get("limit", 10)
        results = f"Found {limit} documents matching '{query}'"
        return [TextContent(type="text", text=results)]
```

**FastMCP Server (Simplified):**
```python
from fastmcp import FastMCP

mcp = FastMCP("framework-fastmcp-server")

@mcp.tool()
def search_documents(query: str, limit: int = 10) -> str:
    """Search through documents"""
    return f"Found {limit} documents matching '{query}'"
```

## Framework Integration Details

| Framework | Integration Type | LLM Provider | Key Features |
|-----------|------------------|--------------|--------------|
| **Basic MCP** | Direct MCP calls | None | Pure MCP functionality |
| **AutoGen** | ConversableAgent | None | Multi-agent conversations |
| **LlamaIndex** | BaseTool + ReActAgent | Claude | RAG and reasoning |
| **Strands** | Agent + Tool | None | Structured agent workflows |
| **CrewAI** | Agent + Task + Crew | None | Team-based task execution |
| **LangChain** | BaseTool + Agent | Claude | Function calling agents |
| **LangGraph** | StateGraph | None | Stateful workflow graphs |
| **Bedrock** | ChatBedrock | Claude on AWS | AWS-native LLM integration |

## Available MCP Tools

- `search_documents(query, limit)` - Search document collection
- `get_weather(location)` - Get weather information

## Testing

Run individual tests:
```bash
python working_mcp_client.py
python fastmcp_client.py
python langchain_mcp_client.py
python bedrock_mcp_client.py
python autogen_mcp_client.py
python crewai_mcp_client.py
python llamaindex_mcp_client.py
python langgraph_mcp_client.py
```

Run comprehensive test suite:
```bash
python test_summary.py
```

Expected result: **8/8 implementations working**

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Framework  │    │   MCP Client    │    │   MCP Server    │
│   (AutoGen,     │◄──►│   (Adapter)     │◄──►│   (Tools)       │
│   LlamaIndex,   │    │                 │    │                 │
│   etc.)         │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

Each client converts MCP tools to framework-specific formats:
- MCP Server provides tools via stdio protocol
- Clients wrap MCP tools in framework-native abstractions  
- Agents use converted tools for task execution

## Dependencies

**Core MCP:**
- `mcp>=1.0.0` - Standard MCP implementation
- `fastmcp>=0.1.0` - Simplified MCP syntax

**LLM Providers:**
- `anthropic>=0.25.0` - Claude API
- `boto3>=1.34.0` - AWS Bedrock

**Framework Dependencies:**
- `autogen-agentchat>=0.7.0` - AutoGen framework
- `llama-index>=0.14.0` - LlamaIndex RAG framework
- `llama-index-llms-anthropic>=0.10.0` - LlamaIndex Claude integration
- `crewai>=1.4.0` - CrewAI team-based agents
- `langchain>=1.0.0` - LangChain framework
- `langchain-anthropic>=1.0.0` - LangChain Claude integration
- `langchain-aws>=1.0.0` - LangChain Bedrock integration
- `langgraph>=1.0.0` - LangGraph workflow graphs

## Notes

- All implementations are fully tested and working
- The basic MCP client works with just `pip install mcp`
- Framework-specific clients require additional dependencies as listed above
- **LLM Providers:**
  - **Claude**: Set `ANTHROPIC_API_KEY` environment variable
  - **Bedrock**: Configure AWS credentials with `aws configure`
- Bedrock requires AWS account with Bedrock model access enabled
- All clients support both `search_documents` and `get_weather` tools
- Implementations follow each framework's best practices and patterns


## When to Use FastMCP vs Standard MCP

### Use FastMCP when:

✅ Rapid Prototyping
• Building quick demos or proof-of-concepts
• Testing MCP integration ideas
• Simple tool implementations

✅ Simple Use Cases
• Basic function-to-tool mapping
• Straightforward input/output patterns
• Minimal customization needed

✅ Developer Experience Priority
• Want minimal boilerplate code
• Prefer decorator-style APIs
• Quick iteration cycles

Example FastMCP scenario:
python
@mcp.tool()
def calculate(a: int, b: int) -> int:
    return a + b


### Use Standard MCP when:

✅ Production Applications
• Enterprise-grade reliability needed
• Complex error handling requirements
• Performance optimization critical

✅ Advanced Features
• Custom resource management
• Complex tool schemas
• Advanced streaming capabilities
• Custom initialization logic

✅ Fine-Grained Control
• Need to customize MCP protocol behavior
• Complex authentication/authorization
• Custom transport layers
• Advanced logging/monitoring

Example Standard MCP scenario:
python
@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    # Custom validation
    # Complex error handling
    # Performance monitoring
    # Custom response formatting


### Summary

| Aspect | FastMCP | Standard MCP |
|--------|---------|--------------|
| Learning Curve | Easy | Moderate |
| Code Volume | Minimal | Verbose |
| Flexibility | Limited | Full |
| Performance | Good | Optimized |
| Production Ready | Basic | Enterprise |
| Customization | Limited | Extensive |

Rule of thumb: Start with FastMCP for prototypes, migrate to standard MCP for 
production systems that need advanced features or fine-grained control.







## LLM Based applications integration with MCP tools

* [Amazon Q CLI for productivity blog](https://aws.amazon.com/blogs/machine-learning/build-aws-architecture-diagrams-using-amazon-q-cli-and-mcp/)
* [Anthropic Claude Code example](https://awesomeclaude.ai/code-cheatsheet)
* [Visual studio code MCP Server](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)

## AWS Workshops

* [The MCP Workshop - MCP with Amazon Q](https://catalog.us-east-1.prod.workshops.aws/workshops/ccdbbc41-fa91-4d5b-b4dc-ac27f42406a6/en-US)
* [Building MCP Servers with Amazon Q CLI and Rust Programming](https://catalog.us-east-1.prod.workshops.aws/workshops/6e6f47ca-1bf3-425d-aa7f-469c85d4fcdf/en-US)
* [Building MCP Servers with Amazon Q CLI and Python Programming](https://catalog.us-east-1.prod.workshops.aws/workshops/63f02fa9-e569-44d1-9bca-30bbbc49a3ff/en-US)
* [Everyday Productivity Accelerators: Building GenAI Tools with Model Context Protocol (MCP)](https://catalog.workshops.aws/everyday-productivity-accelerators/en-US)
* [Korean language - MCP workshops](https://catalog.workshops.aws/mcp-tutorial-on-aws/ko-KR)
* [Korean language - MCP with Amazon Q workshops ](https://catalog.workshops.aws/supercharge-pgops-aws-ai/ko-KR)
* [Using AI with MCP to Prototype and Manage Your Live Streaming Applications](https://catalog.us-east-1.prod.workshops.aws/workshops/e978c0a6-a5bc-4857-95ec-80904014766c/en-US/300-setup)
* [Amazon Q Developer CLI & MCP Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/1c5f0388-d234-49ac-a3c1-2d9a6044500b/en-US)
* [Automating security reviews with SecKiro, an MCP for Amazon's intelligent IDE](https://catalog.us-east-1.prod.workshops.aws/workshops/a1fbfb2a-61d8-4a19-9d1c-dcb38efa345c/en-US)
* [Agentic developer experience with Amazon EKS](https://catalog.us-east-1.prod.workshops.aws/workshops/8dd4a19a-8bf5-4680-b55e-ba6072c37631/en-US)
* [Vibe Coding with AWS MCP Server](https://catalog.us-east-1.prod.workshops.aws/workshops/33b9f640-2cab-47f0-bfdd-d3aab3c38eee/en-US)
* [Building MCP Servers with Python](https://catalog.us-east-1.prod.workshops.aws/workshops/efa89eb2-ceb9-4e84-ae99-6b6d0e4a7276/en-US)
* [AI Agents on EKS Workshop](https://catalog.workshops.aws/agentic-ai-on-eks/en-US)
* [Building MCP Powered Agents with Claude on Amazon Bedrock](https://catalog.us-east-1.prod.workshops.aws/workshops/fda82638-2464-49f9-b6af-0e72b157d1a9/en-US)
* [Develop your DynamoDB data model with MCP - only AWS hosted event](https://catalog.us-east-1.prod.workshops.aws/workshops/2ab84f99-d2eb-4f98-bae0-ce5a1f7842c7/en-US)
* [Accelerating Platform Engineer Productivity with Agentic AIOps](https://catalog.workshops.aws/agentic-aiops-sherlock/en-US)
* [AI-Powered Container Ops: Building and Deploying with MCP Servers on AWS](https://catalog.us-east-1.prod.workshops.aws/workshops/7eb4b988-86c3-4e83-a3a8-2ee2b8fe1839/en-US)
* [Deploying Agentic AI Applications on Amazon EKS](https://catalog.us-east-1.prod.workshops.aws/workshops/fcbec54e-0e91-4401-a8d6-dca84f99ba82/en-US)
* [Cost Effective Modern Data Platform With Athena, DBT, Iceberg, Strands SDK and MCP](https://catalog.workshops.aws/open-source-analytics-architecture/en-US)
* [Amazon Bedrock-MCP Hands-on Lab for Healthcare and LifeSciences](https://catalog.us-east-1.prod.workshops.aws/workshops/4004aa8f-bdce-4519-8dd6-3453b04b0d03/en-US)
* [AWS EOL Detection & Remediation using Strands, AgentCore, MCP, Q CLI - Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/61119d58-63b0-4261-adef-79746c92c4b4/en-US)
* [Building Agents with Amazon Nova Act and MCP](https://catalog.workshops.aws/nova-act-mcp-agents/en-US)
* [Build a Serverless Analytics Agent with Strands, MCP, and S3 Tables](https://catalog.us-east-1.prod.workshops.aws/workshops/e0bc2787-fa2e-4e66-9fc2-444719cd1000/en-US)
* [Streamline SAP Operations with Amazon Q CLI leveraging AWS MCP Servers](https://catalog.workshops.aws/aiops4sap/en-US)

## AWS Github 
[Bedrock AgentCore Github Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)

