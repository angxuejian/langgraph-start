from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta


mcp = FastMCP('tools-server')

@mcp.tool()
async def get_current_time_mcpfunction(days: int):
    """
    获取当前/过去/未来的日期和时间，并格式化为字符串。
    
    参数：
        days(int): 当天时间为0; 未来时间为正数,例如"1" 或 "2"; 过去的时间为负数,例如"-1" 或 "-2"

    返回值:
        str: 格式为 "年-月-日 时:分" 的当前时间字符串，例如 "2025-03-31 14:30"。
    """
    now = datetime.now()

    formatted = (now + timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
    return formatted


if __name__ == "__main__":
    # Initialize and run the server
    print('mcp-server => start')
    mcp.run(transport='stdio')

