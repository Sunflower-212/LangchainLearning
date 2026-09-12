from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chat_models import init_chat_model

# 示例的模板
example_template = PromptTemplate.from_template("单词：{word},反义词：{antonym}")

# 示例的动态数据注入 要求是list内部嵌套字典
examples_data = [
    {"word": "大", "antonym": "小"},
    {"word": "高", "antonym": "矮"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template,                   # 示例数据的模板
    examples=examples_data,                            # 示例的数据（用来注入动态数据）,list内套字典
    prefix="告知我单词的反义词，有如下的示例",               # 示例之前的提示词
    suffix="基于亲们的示例，回答{input_word}的反义词是？",   # 实例之后的提示词
    input_variables=['input_word']                     # 声明在前嘴或后缀中所需要注入的变量名称
)

prompt_text = few_shot_template.invoke({"input_word": "上面"}).to_string()
# print(prompt_text)

model = init_chat_model("deepseek:deepseek-flash")
res = model.invoke(prompt_text)
print(res.content)
