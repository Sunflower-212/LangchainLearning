import os
from operator import truediv

from openai import OpenAI
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

# 获取环境变量中的API_KEY
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 1.获取client对象
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=API_KEY
)
model_name:str = "deepseek-flash"
# 2.调用模型
response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role":"system","content":"你是一个代码编辑助手，仅为用户解决遇到的代码编程问题，回答问题简洁精炼！用户的询问不属于代码问题时，请拒绝回答！"},
        {"role":"user","content":"你是谁？"}
    ],
    stream=True # 流式输出
)
# 非流式输出
# print(response.choices[0].message.content)

for chunk in response:
    if chunk.choices[0].delta.content:  # 如果不写非空判断的话，会打印很多None，因为前面响应的chunk块有角色声明和思考过程，content为空
        print(chunk.choices[0].delta.content,end="",flush=True)
#     print(chunk.model_dump_json(indent=2)) # 查看每个chunk完整的结构信息




