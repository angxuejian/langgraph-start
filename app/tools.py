from langchain_community.tools.tavily_search import TavilySearchResults
from datetime import datetime, timedelta
from langchain_core.tools import tool
from config.config import web


# 联网搜索
search_results = TavilySearchResults(max_results=2,tavily_api_key=web.get("tavily_api_key"))


@tool
def get_current_time(days: int):
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


TOOLS = [search_results, get_current_time]