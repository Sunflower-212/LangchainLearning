from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

@tool(description="获取体重，返回值是int类型，单位kg")
def get_weight()->int:
    return 75
@tool(description="获取身高，返回值是int类型，单位cm")
def get_height()->int:
    return 175

agent = create_agent(
    model=init_chat_model("deepseek:deepseek-flash"),
    tools=[get_weight,get_height],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按照[思考-行动-观察-在思考]的流程结局问题,
    且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
    并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我。"""
)

for chunk in agent.stream(
        {
            "messages": [{"role":"user","content":"计算我的BMI"}]
        },
    stream_mode="values",
):
    last_message = chunk["messages"][-1]
    if last_message.content:
        print(last_message.content.strip())
    try:
        if last_message.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in last_message.tool_calls]}")
    except AttributeError as e:
        pass
