import os

from langchain.embeddings import init_embeddings
from dotenv import load_dotenv


load_dotenv()


model = init_embeddings(
    "qwen3.7-text-embedding-flash",
    provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False, # 绕过 tiktoken
)

print(model.embed_query("今天天气真好！"))
print(model.embed_documents(["今天天气真不错", "明天天气好像更不错", "明天去哪玩"]))