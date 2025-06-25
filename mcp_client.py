from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

async def main():
    client = MultiServerMCPClient(
        {
            "math": { 
                "command": "python",
                "args": ["./mcp_server.py"], # 서버에서 가지고 옴
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    # response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    response = await agent.ainvoke({"messages": "5000만원 연봉을 받는 직장인의 소득세는?"})
    print(response)
    
    # final_message = response["messages"][-1]
    # print(final_message.content)
    
if __name__ == "__main__":
    asyncio.run(main())