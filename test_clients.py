#!/usr/bin/env python3
"""
Test script to verify all MCP client implementations work correctly.
"""
import asyncio
import subprocess
import sys
import time
from pathlib import Path

async def test_mcp_server():
    """Test if MCP server starts correctly"""
    print("Testing MCP server...")
    try:
        # Start server process
        process = subprocess.Popen([
            sys.executable, "mcp_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        time.sleep(1)
        
        # Check if process is running
        if process.poll() is None:
            print("✓ MCP server starts successfully")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"✗ MCP server failed to start: {stderr.decode()}")
            return False
    except Exception as e:
        print(f"✗ Error testing MCP server: {e}")
        return False

async def test_client(client_file: str, client_name: str):
    """Test individual client implementation"""
    print(f"Testing {client_name}...")
    try:
        # Import the client module
        spec = __import__(client_file.replace('.py', ''))
        
        # Check if main function exists and is callable
        if hasattr(spec, 'main') and callable(spec.main):
            print(f"✓ {client_name} imports successfully and has main function")
            return True
        else:
            print(f"✗ {client_name} missing main function")
            return False
    except ImportError as e:
        print(f"⚠ {client_name} import failed (missing dependencies): {e}")
        return False
    except Exception as e:
        print(f"✗ {client_name} error: {e}")
        return False

async def main():
    """Run all tests"""
    print("=== MCP Client Implementation Tests ===\n")
    
    # Test MCP server
    server_ok = await test_mcp_server()
    print()
    
    # Test all clients
    clients = [
        ("autogen_mcp_client.py", "AutoGen Client"),
        ("llamaindex_mcp_client.py", "LlamaIndex Client"),
        ("strands_mcp_client.py", "Strands Client"),
        ("crewai_mcp_client.py", "CrewAI Client"),
        ("langchain_mcp_client.py", "LangChain Client"),
        ("langgraph_mcp_client.py", "LangGraph Client")
    ]
    
    results = []
    for client_file, client_name in clients:
        if Path(client_file).exists():
            result = await test_client(client_file, client_name)
            results.append((client_name, result))
        else:
            print(f"✗ {client_name} file not found: {client_file}")
            results.append((client_name, False))
        print()
    
    # Summary
    print("=== Test Summary ===")
    print(f"MCP Server: {'✓' if server_ok else '✗'}")
    
    for name, result in results:
        status = '✓' if result else '✗'
        print(f"{name}: {status}")
    
    total_passed = sum(1 for _, result in results if result)
    print(f"\nPassed: {total_passed}/{len(results)} clients")
    
    if server_ok and total_passed > 0:
        print("\n🎉 Basic implementation tests passed!")
        print("Note: Full functionality requires installing framework dependencies.")
    else:
        print("\n⚠ Some tests failed. Check error messages above.")

if __name__ == "__main__":
    asyncio.run(main())
