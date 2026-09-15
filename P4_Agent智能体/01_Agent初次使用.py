from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

@tool(description="查询天气")
def get_weather()->str:
    return "晴天"

agent = create_agent(
    model=init_chat_model("deepseek:deepseek-flash"),
    tools=[get_weather],
    system_prompt="你是一个智能体，能够调用工具为用户解决问题"
)

res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"明天武汉的天气如何？"}
        ]
    }
)

for msg in res["messages"]:
    print(type(msg).__name__,msg.content)


