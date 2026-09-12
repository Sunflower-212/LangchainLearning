from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate

"""
PromptTemplate ->StringPromptTemplate ->BasePromptTemplate ->RunnableSerializable ->Runnable
FewShotPromptTemplate ->StringPromptTemplate ->BasePromptTemplate ->RunnableSerializable ->Runnable
ChatPromptTemplate ->BaseChatPromptTemplate ->BasePromptTemplate ->RunnableSerializable ->Runnable
"""
prompt_template = PromptTemplate.from_template("我最喜欢的水果是：{fruit}。")
prompt_text1 = prompt_template.format(fruit="西瓜")
print(prompt_text1,type(prompt_text1)) # 返回字符串提示词

prompt_text2 = prompt_template.invoke({"fruit":"西瓜"}).to_string()
print(prompt_text2,type(prompt_text2)) # 返回StringPromptValue类对象，在构建执行链条更方便，属于Runnable子类对象均可以使用"|"符号来链接

