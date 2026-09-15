from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
import os
from vector_stores import VectorStores
import config_data as config
from langchain.embeddings import init_embeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from file_history_store import get_history
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt


class RagService:
    def __init__(self):
        self.vector_service = VectorStores(
            embedding = init_embeddings(
                model=config.embedding_model_name,
                provider=config.embedding_model_compatible_type,
                api_key=os.getenv(config.embedding_model_api_key_supplier),
                base_url=config.embedding_model_base_url,
                check_embedding_ctx_length=False
            )
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的参考资料为主，简介专业的回答用户问题。参开资料：{context}"),
                ("system","并且用户的对话历史记录如下："),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问：{input}")
            ]
        )
        self.chat_model = init_chat_model(config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        """ 获取最终的执行链 """

        retriever = self.vector_service.get_retriever()


        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def format_for_retriever(val:dict)->str:# 输入是一个{'input': '*****', 'history': []}的字典，但是retriever需要的是input对应的str
            return val["input"]
        def format_for_prompt_template(val:dict)->dict:
            #{input, context, history}
            new_value = {
                "input": val["input"]["input"],
                "context": val["context"],
                "history": val["input"]["history"]
            }
            return new_value
        chain = (
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever) | retriever | format_document
            }| RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt |self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == '__main__':
    # session id 配置
    session_config = {
        "configurable":{
            "session_id":"user_001",
        }
    }
    res = RagService().chain.invoke({"input":"刺客的技能介绍"},session_config)
    print(res)
