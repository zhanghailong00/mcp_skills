from pathlib import Path
from tools.text_tool import clean_text

# 当前文件目录
BASE_DIR = Path(__file__).resolve().parent.parent

# Prompt路径
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system.md"
SUMMARY_PROMPT_PATH = BASE_DIR / "prompts" / "summary.md"

# 读取 Prompt
with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(SUMMARY_PROMPT_PATH, "r", encoding="utf-8") as f:
    SUMMARY_PROMPT = f.read()


def run_skill(text: str):

    # Step1 清洗文本
    text = clean_text(text)

    # Step2 Prompt拼接
    final_prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + SUMMARY_PROMPT.format(text=text)
    )

    return final_prompt


if __name__ == "__main__":

    paper = """
    MCP is a protocol for AI-tool communication.
    It supports tools, prompts and resources.
    """

    result = run_skill(paper)

    print(result)