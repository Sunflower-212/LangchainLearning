

from langchain_chroma import Chroma
import config_data as config

class VectorStores(object):
    def __init__(self,embedding):
        """

        :param embedding:  嵌入模型的传入
        """
        self.embedding = embedding
        self.vectors_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """ 返回向量检索器，方便加入chain """
        return self.vectors_store.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    from langchain.embeddings import  init_embeddings
    embedding_model = init_embeddings(
        "qwen3.7-text-embedding-flash",
        provider="openai",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        check_embedding_ctx_length=False,  # 绕过 tiktoken
    )
    retriever =  VectorStores(embedding_model).get_retriever()

    res = retriever.invoke("鹅鸭杀有哪些角色？")
    print(res)
