
md5_path = './md5.text'

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"


# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n","。","！","？","!","?"," ",""]
min_split_char_number = 1000        #文本分割的阈值


#
similarity_threshold = 2            # 检索返回匹配的文件数量

embedding_model_name = "qwen3.7-text-embedding-flash"
embedding_model_compatible_type = "openai"
embedding_model_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
embedding_model_api_key_supplier = "DASHSCOPE_API_KEY"
chat_model_name = "deepseek:deepseek-flash"

# session id 配置
session_config = {
    "configurable":{
        "session_id":"user_001",
    }
}