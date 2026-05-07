from workflows.summary_flow import run_skill


def test_summary():

    text = "MCP is a protocol."

    result = run_skill(text)

    assert "MCP" in result


test_summary()

print("测试通过")