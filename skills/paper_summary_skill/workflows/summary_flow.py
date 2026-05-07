# from pathlib import Path
# from tools.text_tool import clean_text

# # 当前文件目录
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Prompt路径
# SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system.md"
# SUMMARY_PROMPT_PATH = BASE_DIR / "prompts" / "summary.md"

# # 读取 Prompt
# with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
#     SYSTEM_PROMPT = f.read()

# with open(SUMMARY_PROMPT_PATH, "r", encoding="utf-8") as f:
#     SUMMARY_PROMPT = f.read()


# def run_skill(text: str):

#     # Step1 清洗文本
#     text = clean_text(text)

#     # Step2 Prompt拼接
#     final_prompt = (
#         SYSTEM_PROMPT
#         + "\n\n"
#         + SUMMARY_PROMPT.format(text=text)
#     )

#     return final_prompt


# if __name__ == "__main__":

#     paper = """
#     MCP is a protocol for AI-tool communication.
#     It supports tools, prompts and resources.
#     """

#     result = run_skill(paper)

#     print(result)
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

from skills.paper_summary_skill.tools.text_tool import clean_text


# ======================
# 加载环境变量
# ======================
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# ======================
# 项目根目录
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# Prompt路径
# ======================
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system.md"
SUMMARY_PROMPT_PATH = BASE_DIR / "prompts" / "summary.md"

# ======================
# 读取Prompt
# ======================
with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(SUMMARY_PROMPT_PATH, "r", encoding="utf-8") as f:
    SUMMARY_PROMPT = f.read()


def run_skill(text: str):

    # Step1 清洗文本
    text = clean_text(text)

    # Step2 构建Prompt
    user_prompt = SUMMARY_PROMPT.format(text=text)

    # Step3 调用LLM
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    paper = """
    MCP is a protocol for AI-tool communication.
    It supports tools, prompts and resources.
    """

    result = run_skill(paper)

    print(result)