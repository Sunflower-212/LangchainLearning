import os
from dotenv import load_dotenv
load_dotenv()
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain.embeddings import init_embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
def check_md5(md5_str: str):
    """
    检查传入的md5字符串是否已经被处理过了
    :return False 表示md5未处理过
    """
    if not os.path.exists(config.md5_path):
        # 文件不存在，没处理过md5
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()  # 处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False


def save_md5(md5_str: str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()  # 得到md5对象
    md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()  # 得到md5的十六进制字符串
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        # 如果文件夹不存在则创建，否则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库的表名
            embedding_function=init_embeddings(
                "qwen3.7-text-embedding-flash",
                provider="openai",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                check_embedding_ctx_length=False,  # 绕过 tiktoken
            ),
            persist_directory=config.persist_directory,     # 数据库本地存储文件夹

        )  # 向量存储的实例Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,                #默认采用python自带的len函数做长度统计依据
        )  # 文本分割器的对象

    def upload_by_str(self, data, filename):
        """将传入的字符串进行向量化，存入到向量数据库中"""
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过，内容已经存在知识库中]"

        if len(data) > config.min_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)

        else:
            knowledge_chunks = [data]

        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小王"

        }
        self.chroma.add_texts(          # 内容就能加载到向量库中了
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        # 保存md5
        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"



if __name__ == '__main__':
    service = KnowledgeBaseService()
    res_message = service.upload_by_str("周杰伦","testfile")
    print(res_message)