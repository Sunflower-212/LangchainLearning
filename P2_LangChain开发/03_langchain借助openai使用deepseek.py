import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    # 抛出异常
    raise ValueError("DEEPSEEK_API_KEY not set")

# 创建模型对象
model = ChatOpenAI(model="deepseek-flash",temperature=0.7,api_key=API_KEY,base_url="https://api.deepseek.com/v1")
# 创建消息列表
message = [
    SystemMessage(content="你是一个翻译专家，精通英汉互译，请将用户的输入进行翻译,回答简洁明了"),
    HumanMessage(content="今天天气真好啊")
]

# 调用流式输出
res = model.stream(message)
for chunk in res:
    print(chunk.content,end="",flush=True)