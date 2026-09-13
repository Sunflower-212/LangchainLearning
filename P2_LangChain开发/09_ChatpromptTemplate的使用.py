from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import init_chat_model
chat_prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","你是一位浪漫主义诗人，热爱生活，热爱自由，喜欢作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首写田园的七言律诗。")
    ]
)

history_data = [
    ("human","你来写一首景秀山川的唐诗。"),
    ("ai","《游仙咏山川》\n碧玉簪峰翠色流，云涛漫卷九霄秋。\n霞铺锦绣三千里，瀑落银河十二楼。\n欲借天风驱白鹿，还斟星斗醉沧洲。\n此身合向蓬山老，骑鹤何年访十洲？"),
    ("human","请再来一首写荷花的七言律诗。"),
    ("ai","《咏荷》\n瑶池仙子降凡尘，翠盖红裳照水滨。\n玉露凝香清入骨，金风弄影醉传神。\n洛妃解佩波心月，湘女遗簪浦口春。\n欲采芳华寄何处，碧云深处有伊人。")
]

# 返回的是一个StringPromptValue对象，需要用to_string()转换为string对象
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
# print(prompt_text)

model = init_chat_model("deepseek:deepseek-flash")


for chunk in model.stream(prompt_text):
    if chunk:
        print(chunk,end="",flush=True)
