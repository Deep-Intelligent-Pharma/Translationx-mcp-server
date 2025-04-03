import contextvars
import os
from contextlib import asynccontextmanager

import anyio
import httpx
import uvicorn
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from utils import send_request
import uuid

mcp = FastMCP("tx-mcp")
token = os.getenv('token')
host = "https://ai-trans-v2-demo.dip-aitech.com"
headers = {"token": token}


async def get_user_id(token):
    url = f"{host}/api/user/detail"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    response = await send_request("POST", url, headers, None, {})
    return response.get("id")


@mcp.tool(description="获取文件列表")
async def file_list(
        keyword: str = Field("", description="文件名查询"),
        page: int = Field(1, description="页数"),
        size: int = Field(10, description="每页数量")
):
    """
    Name:
        文件列表信息
    Description:
        根据用户提供的文件名称，获取文件的信息
    Args:
        keyword: 用于查询文件的关键字
        page: 页数
        size: 每页的数量
    """
    url = f"{host}/api/trans/file_list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "page": page,
        "size": size,
        "keyword": keyword,
        "order_list": [
            {"column": "create_time", "order_type": "desc"},
            {"column": "id", "order_type": "asc"}
        ]
    }
    return await send_request("POST", url, headers, None, data)

@mcp.tool(description="提交翻译")
async def submit_translation(
        file_ids: list = Field(..., description="文件ID列表"),
        source_language: str = Field(..., description="源语言"),
        target_language: str = Field(..., description="目标语言"),
):
    """
    Name:
        提交翻译
    Description:
        提交翻译
    Args:
        file_ids: 文件ID列表
        source_language: 源语言
        target_language: 目标语言
        operation_content: 操作内容
        trans_scope: 翻译范围
    """
    url = f"{host}api/trans/file_trans"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "file_ids": file_ids,
        "source_language": source_language,
        "target_language": target_language,
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="创建项目")
async def create_project(
        project_name: str = Field(..., description="项目名称"),
        project_no: str = Field(..., description="项目编号"),
        comment: str = Field('', description="备注")
):
    """
    Name:
        创建项目
    Description:
        创建项目
    Args:
        project_name: 项目名称
        project_no: 项目编号
        comment: 备注
    """
    url = f"{host}/api/pm/project/add"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    charge_user_id = await get_user_id(token)
    data = {
        "project_name": project_name,
        "project_no": project_no,
        "charge_user_id": charge_user_id,
        "comment": comment
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="获取项目列表")
async def get_project_list(
        keyword: str = Field('', description="项目名称"),
        page: int = Field(1, description="页数"),
        size: int = Field(10, description="每页数量")
):
    """
    Name:
        获取项目列表
    Description:
        获取项目列表
    Args:
        keyword: 项目名称
        page: 页数
        size: 每页数量
    """
    url = f"{host}/api/pm/project/list"  
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "keyword": keyword,
        "page": page,
        "size": size
    }

    return await send_request("POST", url, headers, None, data)


if __name__ == '__main__':
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
    # anyio.run(run_sse_async)
