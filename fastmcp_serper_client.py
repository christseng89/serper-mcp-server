import os
import asyncio
import traceback
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


class SerperAgent:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.client: MultiServerMCPClient | None = None
        self.agent = None
        self.is_initialized = False

    async def initialize(self) -> None:
        """Initialize MCP client and agent"""
        try:
            # Initialize MCP client for serper-mcp-server
            self.client = MultiServerMCPClient(
                {
                    "serper": {
                        "transport": "stdio",
                        "command": "uvx",
                        "args": ["serper-mcp-server"],
                        "env": {"SERPER_API_KEY": SERPER_API_KEY},
                    }
                }
            )
            tools = await self.client.get_tools()
            self.agent = create_react_agent(self.llm, tools)
            self.is_initialized = True
            print("✅ MCP client initialized with serper-mcp-server.")
        except Exception:
            traceback.print_exc()
            raise

    async def ask(self, messages: list[BaseMessage]) -> str:
        """Ask a question to the agent"""
        try:
            if not self.is_initialized:
                await self.initialize()

            result = await self.agent.ainvoke({"messages": messages})
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage):
                    return msg.content
            return "No valid AI response."
        except Exception as e:
            traceback.print_exc()
            return f"Error: {e}"

    async def close(self):
        """Clean up"""
        # MultiServerMCPClient does not have close(), just clear the client
        self.client = None
        self.agent = None
        self.is_initialized = False
        print("🛑 MCP client closed.")


async def main():
    agent = SerperAgent()

    # Example questions
    questions = [
        "What is the weather in Taipei?",
        "What is the benefit of using FastMCP?"
    ]

    for q in questions:
        messages = [HumanMessage(content=q)]
        response = await agent.ask(messages)
        print(f"💡 Q: {q}\n➡️ A: {response}\n")

    await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
