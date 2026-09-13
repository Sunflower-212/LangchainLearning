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

# 检索向量库
result = vector_store.similarity_search(input_text,2)
# print(result) 输出的是Document对象列表
reference_text = "["
for doc in result:
    reference_text += doc.page_content
reference_text += "]"
# print(reference_text)  输出的是字符串

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

# chain 搭建链
chain = prompt | print_prompt |model | str_parser


res = chain.invoke({"input":input_text,"context":reference_text})
print(res)

