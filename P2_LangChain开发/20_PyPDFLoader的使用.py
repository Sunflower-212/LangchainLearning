from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader(
#     file_path="./data/Python教程.pdf",
#     mode="page",            # 默认page模式，每个页面形成一个Document文档对象
#                             # single模式，全部返回一个Document对象
# )

loader = PyPDFLoader(
    file_path="./data/Python教程2.pdf",
    mode="page",            # 默认page模式，每个页面形成一个Document文档对象
                            # single模式，全部返回一个Document对象
    password="123456"       # pdf的密码
)

i=0
for doc in loader.lazy_load():
    i+=1
    print(doc)
    print("="*20,i)
