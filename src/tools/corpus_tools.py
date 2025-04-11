import uuid
from pydantic import Field

from server import mcp, host, headers
from utils import send_request


@mcp.tool(description="记忆库列表")
async def get_memory_lib_list(
        size: int = 10,
        page: int = 1,
        name: str = ""
):
    """
    Name:
        记忆库列表
    Description:
        记忆库列表
    Args:
        size: 每页数量
        page: 页数
        name: 记忆库名称
    """
    url = f"{host}/api/master_lib/memory/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="术语库列表")
async def get_term_lib_list(
        size: int = 10,
        page: int = 1,
        name: str = ""
):
    """
    Name:
        术语库列表
    Description:
        术语库列表
    Args:
        size: 每页数量
        page: 页数
        name: 记忆库名称
    """
    url = f"{host}/api/master_lib/term/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data=data)
