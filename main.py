# from servers.weather.weather import mcp


# def main():
#     mcp.run(transport="stdio")


# if __name__ == "__main__":
#     main()
from router.router import route
from skills.paper_summary_skill.workflows.summary_flow import run_skill


query = input("请输入问题：")

# Step1 Router
skill = route(query)

print("Router选择：", skill)

# Step2 执行Skill
if skill == "paper_summary_skill":

    result = run_skill(query)

    print("\nSkill执行结果：\n")

    print(result)