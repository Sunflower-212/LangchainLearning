from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

@tool(description="传入股票名称，获取股价")
def get_price(name:str)->str:
    return f"pirce{name}的价格是20$"

@tool(description="传入股票名称，获取股票信息")
def get_info(name:str)->str:
    return f"股票{name}，是一家A股上市公司，专注于IT职业教育"
agent = create_agent(
    model=init_chat_model("deepseek:deepseek-flash"),
    tools=[get_price,get_info],
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"
)

for chunk in agent.stream(
    {
        "messages":[{"role":"user","content":"小汪教育股价是多少，并介绍一下"}]
    },
    stream_mode="values"
):
    latest_message = chunk["messages"][-1]
    # print(latest_message)
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f'工具调用：{[tc["name"] for tc in latest_message.tool_calls]}')
    except AttributeError as e:
        pass

