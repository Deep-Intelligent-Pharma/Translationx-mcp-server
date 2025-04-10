import uuid
from pydantic import Field

from server import mcp, host, headers
from utils import send_request


# 获取记忆库列表
@mcp.tool(description="获取记忆库列表")
async def get_memory_lib_list(
        size: int = Field(10, description="每页数量"),
        page: int = Field(1, description="页数"),
        name: str = Field('', description="记忆库名称")
):
    """
    Name:
        获取记忆库列表
    Description:
        获取记忆库列表
    """
    url = f"{host}/api/master_lib/memory/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)


# 获取术语库列表
@mcp.tool(description="获取术语库列表")
async def get_term_lib_list(
        size: int = Field(10, description="每页数量"),
        page: int = Field(1, description="页数"),
        name: str = Field('', description="术语库名称")
):
    """
    Name:
        获取术语库列表
    Description:
        获取术语库列表
    """
    url = f"{host}/api/master_lib/term/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)
