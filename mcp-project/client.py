# %%writefile mcp_project/mcp_chatbot.py
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from typing import List
import asyncio
import nest_asyncio
import os
import json
import getpass

nest_asyncio.apply()
load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
api_key = getpass.getpass("🔐 Enter your GROQ_API_KEY: ")


class MCP_ChatBot:
    def __init__(self):
        self.session: ClientSession = None
        self.available_tools: List[dict] = []
        self.llm = ChatGroq(
            model="llama3-8b-8192",  # or "llama-3-70b-chat"
            api_key = api_key,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,

        )

    async def process_query(self, query):
        # Start conversation
        messages = [HumanMessage(content=query)]
        process_query = True

        while process_query:
            response = self.llm.invoke(messages)
            messages.append(response)

            # Print assistant response
            print(response.content.strip())
            if not hasattr(response, "tool_calls") or not response.tool_calls:
                process_query = False
                break

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = json.loads(tool_call["args"])
                print(f"Calling tool '{tool_name}' with args: {tool_args}")

                try:
                    result = await self.session.call_tool(tool_name, arguments=tool_args)
                except Exception as e:
                    print(f"❌ Tool call failed: {str(e)}")
                    process_query = False
                    break

                # Convert result content to plain string
                if isinstance(result.content, list):
                    content_str = "\n".join(
                        item.text if hasattr(item, "text") else str(item)
                        for item in result.content
                    )
                else:
                    content_str = str(result.content)

                messages.append(ToolMessage(content=content_str, tool_call_id=tool_call["id"]))

    async def chat_loop(self):
        print("\n🤖 LangChain + Groq + MCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                await self.process_query(query)
                print("\n")
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def connect_to_server_and_run(self):
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "server.py"],
            env=None,
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await session.initialize()

                response = await session.list_tools()
                tools = response.tools

                print("\n🛠️ Connected to server with tools:", [tool.name for tool in tools])

                self.available_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema
                        }
                    } for tool in tools
                ]

                await self.chat_loop()


async def main():
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()

if __name__ == "__main__":
    asyncio.run(main())


