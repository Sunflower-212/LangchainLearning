from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# 创建解析器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = init_chat_model("deepseek:deepseek-flash")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓：{lastname},刚生了{gender},请起名，并以JSON的格式返回，"
    "要求key是name,value是起的名字。严格遵循格式要求"
)


second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我解析含义。"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

res:str = chain.invoke({"lastname":"张","gender":"女儿"})
print(res)
print(type(res))

# 流式输出
for chunk in chain.stream({"lastname":"张","gender":"女儿"}):
    print(chunk,end="",flush=True)