import contextvars
import os
from contextlib import asynccontextmanager
import anyio
import httpx
import uvicorn
from pydantic import Field, BaseModel
from mcp.server.fastmcp import FastMCP
from utils import send_request
import uuid

from server import mcp, host, headers


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
        "keyword": keyword
    }
    return await send_request("POST", url, headers, None, data)


class MasterMemoryLib(BaseModel):
    memory_lib_id: int = Field(..., description="主记忆库ID")
    threshold: float = Field(..., description="阈值")


@mcp.tool(description="提交翻译")
async def submit_translation(
        file_ids: list = Field(..., description="文件ID列表"),
        source_language: str = Field(..., description="源语言"),
        target_language: str = Field(..., description="目标语言"),
        master_memory_libs: list[MasterMemoryLib] = Field(None, description="记忆库"),
        master_term_lib_ids: list[int] = Field(None, description="术语库ID列表"),
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
        master_memory_libs: 记忆库
        master_term_lib_ids: 术语库ID列表
    """
    url = f"{host}api/trans/file_trans"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "file_ids": file_ids,
        "source_language": source_language,
        "target_language": target_language,
        "master_memory_libs": master_memory_libs or [],
        "master_term_lib_ids": master_term_lib_ids or [],
    }
    return await send_request("POST", url, headers, None, data)
