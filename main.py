import contextvars
import os
from contextlib import asynccontextmanager

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

mcp = FastMCP("tx-mcp")
token = os.getenv('BAIDU_MAPS_API_KEY')
host = "https://ai-trans-v2-demo.dip-aitech.com"
current_request = contextvars.ContextVar("token")

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
    token = current_request.get()
    headers["token"] = token
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


def sse_app(mcp_server: FastMCP) -> Starlette:
    """Return an instance of the SSE server app."""
    sse = SseServerTransport(mcp_server.settings.message_path)

    async def handle_sse(request: Request) -> None:
        token = request.headers.get("authorization").replace("Bearer ", "")
        current_request.set(token)
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # type: ignore[reportPrivateUsage]
        ) as streams:
            await mcp_server._mcp_server.run(
                streams[0],
                streams[1],
                mcp_server._mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=True,
        routes=[
            Route(mcp_server.settings.sse_path, endpoint=handle_sse),
            Mount(mcp_server.settings.message_path, app=sse.handle_post_message),
        ],
    )


async def run_sse_async() -> None:
    """Run the server using SSE transport."""
    starlette_app = sse_app(mcp)

    config = uvicorn.Config(
        starlette_app
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    # mcp.run(transport="stdio")
    # mcp.run(transport="sse")
    anyio.run(run_sse_async)
