import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.vectorstores import InMemoryVectorStore
from langchain.embeddings import init_embeddings
from langchain_community.document_loaders import CSVLoader

embedding_model = init_embeddings(
    "qwen3.7-text-embedding-flash",
    provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False, # 绕过 tiktoken
)

vector_store = InMemoryVectorStore(
    embedding = embedding_model,
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",
)

# 加载csv文档     list[Document]
docs = loader.load()

# 向量存储的新增、删除、检索
vector_store.add_documents(
    documents=docs,     # 被添加的文档，类型：list[Document]
    ids=["id"+str(i) for i in range(1,len(docs)+1)],# 给添加的文档提供ID（字符串）  list[str]
)

# 删除    传入[id,id...]
vector_store.delete(["id1","id2"])

# 检索 返回类型为list[Document]
result = vector_store.similarity_search(
    "Python是不是简单易学呀",
    3
)
print(result)

