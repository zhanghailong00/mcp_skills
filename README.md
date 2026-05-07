# MCP 与 Skill 学习记录

这个项目记录了我这两天围绕 MCP 和 Skill 的学习、实践与调试过程。

## 这两天我学习了什么

### 1. MCP 的基础概念

我理解了一个 MCP 应用通常包含这几部分：

- MCP Server：负责暴露 tools、prompts、resources
- MCP Client：负责连接 server，并通过 MCP 协议进行通信
- LLM 或上层应用（MCP Host）：负责决定什么时候调用工具、如何使用工具结果

我还理解了两种常见通信方式的区别：

- `stdio` 模式：client 启动 server 子进程，通过标准输入输出通信
- 网络模式：server 作为独立服务运行，供其他机器或其他公司访问

### 2. MCP Server 的基本写法

我编写了一个天气 MCP 服务端：[servers/weather/weather.py](/f:/llm_learn/mcp_skills/servers/weather/weather.py:1)

在这个过程中，我学习并实践了：

- 使用 `FastMCP("weather")` 创建 MCP 服务
- 使用 `@mcp.tool()` 注册工具
- 给工具编写参数说明和函数描述
- 让工具返回可以被 MCP 客户端消费的结果

我实现的工具有：

- `get_alerts(state)`
- `get_forecast(latitude, longitude)`

### 3. MCP Client 与 Server 如何交互

我通过 [servers/weather/test.py](/f:/llm_learn/mcp_skills/servers/weather/test.py:1) 学习了 Python MCP SDK 的基本调用方式，包括：

- 创建 `StdioServerParameters`
- 使用 `stdio_client(...)`
- 创建 `ClientSession`
- 调用 `initialize()`
- 调用 `list_tools()`
- 调用 `call_tool(...)`

我确认了在 `stdio` 模式下：

- 不需要手动先启动服务端
- client 可以自动拉起 server
- client 和 server 的通信走的是 MCP 协议，不是普通 `print()`

### 4. MCP 返回结果的理解

我学习了 MCP 返回结果有两层含义：

- 协议层：`jsonrpc`、`id`、`result`
- SDK 封装层：`content`、`structuredContent`、`isError`、`meta`

我理解了：

- MCP 底层本质上走的是 JSON-RPC 风格消息
- Python SDK 会帮我把这些原始协议消息解析成对象
- 我在 Python 里 `print(result)` 时，看到的通常已经是解析后的 `result` 内容，而不是完整原始报文

### 5. LLM 如何与 MCP 结合

我编写了一个客户端原型：[client/client.py](/f:/llm_learn/mcp_skills/client/client.py:1)

它实现了：

- 连接 MCP Server
- 获取可用 tools
- 把 MCP tools 转成 OpenAI 兼容的 `tools`
- 让模型自主决定是否调用工具
- 把工具结果再回传给模型生成最终回答

通过这个过程，我理解了完整链路：

1. 用户输入自然语言问题
2. 模型看到可用工具
3. 模型决定是否调用某个工具
4. MCP Client 调用 MCP Server 上的 tool
5. Server 执行 tool
6. Tool 结果返回给 Client
7. 模型根据结果生成最终回答

### 6. LLM 如何调用已经写好的 Skill

我还在 [main.py](/f:/llm_learn/mcp_skills/main.py:1) 中实践了“让 LLM 调用已经写好的 skill”这一流程。

当前链路是：

1. 用户输入问题
2. [router/router.py](/f:/llm_learn/mcp_skills/router/router.py:1) 使用 LLM 判断应该选择哪个 skill
3. 如果路由结果是 `paper_summary_skill`
4. 再调用 [skills/paper_summary_skill/workflows/summary_flow.py](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/workflows/summary_flow.py:1) 中的 `run_skill(...)`
5. skill 内部再结合 prompt、tool 和模型生成最终结果

通过这一步，我开始理解：

- MCP 是一种“工具协议”
- Skill 是一种“任务封装方式”
- LLM 既可以调用 MCP tool，也可以通过 router 去选择并调用 skill

### 7. Skill 的目录结构

我创建了一个 Skill 骨架目录：

[skills/paper_summary_skill](/f:/llm_learn/mcp_skills/skills/paper_summary_skill:1)

我学习了一个 skill 可以包含：

- `SKILL.md`
- `manifest.json`
- `prompts/`
- `tools/`
- `workflows/`
- `tests/`
- `README.md`

这让我初步理解了 skill 不只是一个提示词，而是可以把下面这些内容打包在一起：

- 使用说明
- Prompt 模板
- 辅助工具函数
- 工作流逻辑
- 测试文件

## 这两天我完成了什么

### 已完成 1：天气 MCP Server

我成功搭建并跑通了一个天气 MCP 服务端。

已经验证的能力包括：

- server 可以正常启动
- tools 可以正常注册
- `list_tools()` 可以返回工具元数据
- `get_alerts()` 可以被成功调用
- `get_forecast()` 可以被成功调用
- 外部天气 API 可以返回真实天气数据

### 已完成 2：MCP 测试脚本

我完成了一个真实可运行的 MCP 测试脚本：[servers/weather/test.py](/f:/llm_learn/mcp_skills/servers/weather/test.py:1)

它可以：

- 列出可用 tools
- 调用 `get_alerts(CA)`
- 调用 `get_forecast(37.7749, -122.4194)`

这证明了我的 MCP server 和 client 链路已经打通。

### 已完成 3：LLM + MCP 联动

我完成了一个 [client/client.py](/f:/llm_learn/mcp_skills/client/client.py:1) 原型，把 OpenAI 兼容模型与天气 MCP 服务端接在了一起。

我已经成功测试过类似问题：

- `Get the forecast for latitude 37.7749 and longitude -122.4194.`

这说明：

- 模型能看到工具
- 模型能选择合适工具
- MCP Server 能执行工具
- 工具结果能返回给模型
- 模型能基于工具结果生成最终回答

### 已完成 4：论文总结 Skill 骨架

我创建了论文总结 skill 的初始结构，包括：

- [skills/paper_summary_skill/SKILL.md](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/SKILL.md:1)
- [skills/paper_summary_skill/prompts/system.md](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/prompts/system.md:1)
- [skills/paper_summary_skill/prompts/summary.md](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/prompts/summary.md:1)
- [skills/paper_summary_skill/tools/text_tool.py](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/tools/text_tool.py:1)
- [skills/paper_summary_skill/workflows/summary_flow.py](/f:/llm_learn/mcp_skills/skills/paper_summary_skill/workflows/summary_flow.py:1)

这为后续实现一个真正可用的论文总结 skill 打下了基础。

### 已完成 5：LLM 路由并调用 Skill

我在 [main.py](/f:/llm_learn/mcp_skills/main.py:1) 中实现了一个简化版流程：

- 用户输入问题
- router 用 LLM 判断是否命中 `paper_summary_skill`
- 命中后执行 `run_skill(query)`

这意味着我不只是学习了 skill 的目录结构，还开始实践：

- 如何让 LLM 选择 skill
- 如何在主程序中调用 skill workflow
- 如何把 router、skill、prompt、模型串起来

## 这两天我排查并理解了哪些问题

在学习过程中，我遇到并理解了这些典型问题：

- 入口文件并没有真正启动 MCP Server
- 本地目录名 `mcp/` 会和安装的 `mcp` 包冲突
- `pyproject.toml` 中缺少依赖声明
- test 客户端的写法不正确
- `stdio` 模式和常驻网络服务模式容易混淆
- 在 `client` 目录下传错了 `main.py` 路径
- API key 无效或环境变量缺失
- Python 包导入路径写错，例如 `from tools...`
- 普通 `print()` 输出不是合法的 MCP 协议消息

这些调试过程让我对 MCP 的理解比单纯看文档更具体。

## 我当前已经掌握的内容

目前我已经能够解释并实际操作：

- 什么是 MCP Server
- 什么是 MCP Client
- `stdio` 模式如何工作
- 如何列出 tools
- 如何调用 tools
- tool 结果是如何返回的
- LLM 工具调用如何叠加在 MCP 之上
- LLM 如何通过 router 选择并调用 skill
- 一个 skill 目录如何组织

## 当前项目状态

### 已经可以工作的部分

- 天气 MCP Server
- MCP Tool 测试脚本
- LLM + MCP 天气查询流程
- `main.py` 中的 LLM Router + Skill 调用流程
- `paper_summary_skill` 骨架目录

### 还在继续完善的部分

- [router/router.py](/f:/llm_learn/mcp_skills/router/router.py:1) 的路由逻辑
- `paper_summary_skill` 的完整实现
- 包导入路径的统一
- 环境变量组织方式
- 项目结构和文档清晰度

## 下一步学习目标

- 把 `paper_summary_skill` 做成真正可运行的 skill
- 完善 router，让它能在多个 skill 之间做选择
- 学习如何把 MCP Server 提供给外部客户端访问
- 在彻底掌握 `stdio` 后，再继续学习 HTTP/远程模式
- 给 client 和 server 增加更清晰的日志，方便观察每一步发生了什么
