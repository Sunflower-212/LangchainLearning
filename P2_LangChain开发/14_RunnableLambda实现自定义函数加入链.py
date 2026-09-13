from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()

model = init_chat_model("deepseek:deepseek-flash")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓：{lastname},刚生了{gender},请起名，要求只输出一个名字"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我解析含义。"
)

#函数的入参：AIMessage -> dict({"name":"xxx"})
my_func = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})

chain = first_prompt | model | my_func | second_prompt | model | str_parser

# res:str = chain.invoke({"lastname":"张","gender":"女儿"})
# print(res)

for chunk in chain.stream({"lastname":"张","gender":"女儿"}):
    print(chunk,end="",flush=True)