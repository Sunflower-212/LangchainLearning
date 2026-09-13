"""
提示词： 用户的提问 + 向量库中检索到的参考资料
"""
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_core.vectorstores import InMemoryVectorStore
from langchain.embeddings import init_embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
embedding_model = init_embeddings(
    "qwen3.7-text-embedding-flash",
    provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False     # 绕过 tiktoken
)

# 构建提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简介和专业的回答用户问题。参考资料：{context}"),
        ("human","用户提问：{input}")
    ]
)

# 创建聊天模型
model = init_chat_model("deepseek:deepseek-flash")

# 内存向量存储
vector_store = InMemoryVectorStore(
    embedding=embedding_model
)

# 创建输出解析器对象
str_parser = StrOutputParser()

# 准备一下资料（向量数据库的数据）
# add_texts 传入一个list[str]
vector_store.add_texts(["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"])

input_text = "怎么减肥？"

# LangChain中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k":2})

"""
retriever:
    - 输入： 用户的提问           str
    - 输出： 向量库的检索结果      list[Document]
    
prompt:
    - 输入： 用户的提问+向量库检索的结果   dict
    - 输出： 完整的提示词                PromptValue   
"""
# 需要将list[Document]转为str
def format_func(docs:list[Document]):
    if not docs:
        return "无相关参考资料"
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str


def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt


# RunnablePassthrough能够拿到整个链条的输入，retriever是链的起始组件，invoke的输入真正提供给retriever，RunnablePassthrough将输入截流copy走了一份
chain = (
    {"input":RunnablePassthrough(),"context": retriever | format_func} | prompt | print_prompt |model | str_parser
)

res = chain.invoke(input_text)
print(res)

