from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

parser = StrOutputParser()
model = init_chat_model("deepseek:deepseek-flash")
prompt = PromptTemplate.from_template(
    "我的邻居姓：{lastname},刚生了{gender},请起名，仅告知我名字无需其他内容"
)

chain = prompt | model | parser | model # 需要直接输出string最后再加上一个输出解析器就行

res:AIMessage = chain.invoke({"lastname":"王","gender":"女儿"})
print(res.content)
print(type(res))
