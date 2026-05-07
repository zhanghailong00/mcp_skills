from dotenv import load_dotenv
from openai import OpenAI
import os

# 加载 .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def route(query: str):

    prompt = f"""
你是一个Skill Router。

你需要判断用户问题是否属于：

1. paper_summary_skill
   - 论文
   - 学术
   - 总结
   - 创新点

如果不属于任何Skill，
返回：
default

用户问题：
{query}

只返回Skill名字。
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content