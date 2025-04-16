import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from app.graph import LLMNodeGraph
from langchain.schema.messages import AIMessageChunk


memory = False
streaming = False

class MCPClient:
    def __init__(self) -> None:
        
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.graph = None
    

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        print("Connect to an MCP server / loading....")
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"

        # extending mcp.json
        # replace mcp configuration, https://mcp.so/
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        
        # mcp tools to langchain tools
        tools = await load_mcp_tools(self.session)

        llm_node_graph = LLMNodeGraph(memory=memory)
        self.graph = llm_node_graph.chatbot_tools(tools, async_invoke = True)
        print("\nConnected to server with tools:", [tool.name for tool in tools])


    async def stream_graph_updates(self, user_input: str, memory: bool = False, streaming: bool = False):

        config = {"configurable": {"thread_id": "5"}} if memory else {}
        stream_mode = 'messages' if streaming else 'values'

        async for event in self.graph.astream(
            {"messages": [
                # {"role": "system", "content": '你是一位资深的沟通专家，精通心理学相关的知识与实战经验。'},
                {"role": "user", "content": user_input}]
            },
            config,
            stream_mode=stream_mode     
            ):

            if streaming:
                if isinstance(event[0], AIMessageChunk):
                    print(event[0].content, end="", flush=True)
            else: 
                if "messages" in event:
                    event["messages"][-1].pretty_print()



    async def chat_loop(self):
        while True:
            try:
                user_input = input("\nUser(quit、exit、q): ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                await self.stream_graph_updates(user_input, memory=memory, streaming=streaming)
            except Exception as e:
                print(e)
                print("Exit goodbye!")
                break


    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    print('MCP => START')
    asyncio.run(main())