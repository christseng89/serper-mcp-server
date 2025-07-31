import os
import asyncio
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


async def main():
    client = MultiServerMCPClient(
        {
            "serper": {
                "transport": "stdio",
                "command": "docker",
                "args": ["run", "-i", "--rm", "-e", f"SERPER_API_KEY={SERPER_API_KEY}", "serper-mcp-server"]
            }
        }
    )

    tools = await client.get_tools()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools)

    query = "Search the latest news about FastMCP"
    messages = [HumanMessage(content=query)]
    result = await agent.ainvoke({"messages": messages})

    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
