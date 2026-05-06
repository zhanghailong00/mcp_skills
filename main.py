from servers.weather.weather import mcp


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
