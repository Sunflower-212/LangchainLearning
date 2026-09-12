import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

from dotenv import load_dotenv
load_dotenv()

# 创建模型对象
model = init_chat_model(model="deepseek:deepseek-flash")
# 创建消息列表
message = [
    SystemMessage(content="你是一个翻译专家，精通英汉互译，请将用户的输入进行翻译,回答简洁明了"),
    HumanMessage(content="今天天气真好啊")
]

# 调用流式输出
res = model.stream(message)
for chunk in res:
    print(chunk.content,end="",flush=True)