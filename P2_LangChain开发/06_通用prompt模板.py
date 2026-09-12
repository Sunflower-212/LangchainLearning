from dotenv import load_dotenv
load_dotenv()


from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastName}，刚生了一个{gender}，你帮我起个名字，简单回答。"
)
model = init_chat_model("deepseek:deepseek-flash")
#调用format方法注入信息
# prompt_text = prompt_template.format(lastName="张", gender="女儿")
#
# res = model.invoke(prompt_text)
# print(res.content)

# 构建执行链条
chain = prompt_template | model
res = chain.invoke({"lastName":"张","gender":"女儿"})
print(res.content)


