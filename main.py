import os
from doctest import debug

import anyio
import httpx
import uvicorn
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.types import Scope, Receive, Send

mcp = FastMCP("tx-mcp", debug=True)
token = os.getenv('token')

host = "https://ai-trans-v2-demo.dip-aitech.com"

headers = {
    "token": token,
    "x-request-id": "mcp-817a7821cc454ef18c29399a39dadc7c"
}


@mcp.tool(description="获取文件列表")
async def file_list(
        keyword: str = Field("", description="文件名查询")
):
    """
    Name:
        文件列表信息
    Description:
        根据用户提供的文件名称，获取文件的信息
    Args:
        keyword: 用于查询文件的关键字
    """
    url = f"{host}/api/trans/file_list"
    data = {
        "page": 1,
        "size": 10,
        "keyword": keyword,
        "order_list": [
            {"column": "create_time", "order_type": "desc"},
            {"column": "id", "order_type": "asc"}
        ],
        "tag": []
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            result = resp.json()
            code = result.get("code")
            if code != 0:
                error_msg = result.get("message", "unkown error")
                raise Exception(f"API response error: {error_msg}")
            data = result.get("data")
            return data
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
