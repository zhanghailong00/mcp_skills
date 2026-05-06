import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:")
            print(tools)
            print()

            alerts_result = await session.call_tool(
                "get_alerts",
                {"state": "CA"},
            )
            print("get_alerts(CA):")
            print(alerts_result)
            print()

            forecast_result = await session.call_tool(
                "get_forecast",
                {"latitude": 37.7749, "longitude": -122.4194},
            )
            print("get_forecast(San Francisco):")
            print(forecast_result)


if __name__ == "__main__":
    asyncio.run(main())
