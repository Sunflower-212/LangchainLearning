from email import message

from dotenv import load_dotenv
# 加载.env中的环境变量
load_dotenv()

from langchain_deepseek import ChatDeepSeek
# 还可以设置temperature、max_tokens、timeout、max_retries
model = ChatDeepSeek(model="deepseek-flash")
message = [
    ("system","你是代码编程助手，辅导用户一步一步的完成编程任务，并会发现和描述编码过程中的难点，通过注释将其中的原理讲解清楚"),
    ("human","我想要使用python语言解决汉诺塔问题，该如何做？"),
]
# 非流式输出
# res = model.invoke(message)
# print(res.content)

# 流式输出
for chunk in model.stream(message):
    print(chunk.text,end="",flush=True)