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

from load_openapi.https_tools import create_mcp_tools_from_openapi

mcp = FastMCP("tx-mcp")

@mcp.tool(description="获取文件列表")
async def get_file_list(
        keyword: str = Field("", description="文件名查询")
):
    """
    获取文件列表
    :param keyword:
    :return:
    """
    url = f"{host}/api/trans/file_list"
    data = {"page": 1, "size": 10, "keyword": keyword,
            "order_list": [{"column": "create_time", "order_type": "desc"}, {"column": "id", "order_type": "asc"}],
            "tag": []}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()


def sse_app(mcp_server: FastMCP) -> Starlette:
    """Return an instance of the SSE server app."""
    sse = SseServerTransport(mcp_server.settings.message_path)

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # type: ignore[reportPrivateUsage]
        ) as streams:
            query_string = request.scope.get("query_string").decode()
            query_params = {param.split("=")[0]:param.split("=")[1] for param in query_string.split("&")}
            print(query_params)
            await mcp_server._mcp_server.run(
                streams[0],
                streams[1],
                mcp_server._mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=mcp_server.settings.debug,
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
