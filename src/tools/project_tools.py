import uuid
from pydantic import Field
from enum import Enum

from server import mcp, host, headers
from utils import send_request, upload_file
from common import ProjectFileStatusEnum


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
    data = {
        "project_name": project_name,
        "project_no": project_no,
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

@mcp.tool(description="编辑项目信息")
async def edit_project(
    id: str = Field(..., description="项目ID"),
    project_name: str = Field(..., description="项目名称"),
    project_no: str = Field(..., description="项目编号"),
    comment: str = Field('', description="备注")
):
    """
    Name:
        编辑项目信息
    Description:
        编辑项目信息
    Args:
        id: 项目ID
        project_name: 项目名称
        project_no: 项目编号
    """
    url = f"{host}/api/pm/project/edit"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "id": id,
        "project_name": project_name,
        "project_no": project_no,
        "comment": comment
    }
    return await send_request("POST", url, headers, None, data)

@mcp.tool(description="删除项目")
async def delete_project(
    ids: list[str] = Field(..., description="项目ID")
):
    """
    Name:
        删除项目
    Description:
        删除项目
    Args:
        ids: 项目ID列表
    """
    url = f"{host}/api/pm/project/delete"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {"ids": ids}
    return await send_request("POST", url, headers, None, data)



@mcp.tool(description="获取项目文件夹列表")
async def get_project_folder_list(
    id: str = Field(..., description="项目ID"),
    status: list[ProjectFileStatusEnum] = Field(..., description="文件状态"),
    keyword: str = Field('', description="文件名称"),
    page: int = Field(1, description="页数"),
    size: int = Field(10, description="每页数量")
):
    """
    Name:
        获取项目文件夹列表
    Description:
        获取项目文件夹列表
    Args:
        id: 项目ID
        status: 文件状态
        keyword: 文件名称
        page: 页数
        size: 每页数量
    """
    url = f"{host}/api/pm/project/folder/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "id": id,
        "status": status,
        "keyword": keyword,
        "page": page,
        "size": size
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="创建项目文件夹")
async def create_project_folder(
    id: str = Field(..., description="项目ID"),
    name: str = Field(..., description="文件夹名称"),
):
    """
    Name:
        创建项目文件夹
    Description:
        创建项目文件夹
    Args:
        id: 项目ID
        name: 文件夹名称
    """
    url = f"{host}/api/pm/project/folder/add"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "id": id,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="编辑项目文件夹")
async def edit_project_folder(
    id: str = Field(..., description="项目ID"),
    folder_id: int = Field(..., description="文件夹id"),
    name: str = Field(..., description="文件夹名称"),
):
    """
    Name:
        编辑项目文件夹
    Description:
        编辑项目文件夹
    Args:
        id: 项目ID
        folder_id: 文件夹id
        name: 文件夹名称
    """
    url = f"{host}/api/pm/project/folder/edit"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "id": id,
        "folder_id": folder_id,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="删除项目文件夹")
async def delete_project_folder(
    id: int = Field(..., description="项目id"),
    operation_type: int = Field(1, description='操作类型 1 调整首句位置 2 全部解锁'),
    folder_ids: list[int] = Field(..., description="文件夹id")
):
    """
    Name:
        删除项目文件夹
    Description:
        删除项目文件夹
    Args:
        id: 项目id
        operation_type: 操作类型 1 调整首句位置 2 全部解锁
        folder_ids: 文件夹id
    """
    url = f"{host}/api/pm/project/folder/delete"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "id": id,
        "operation_type": operation_type,
        "folder_ids": folder_ids
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="上传项目文件")
async def upload_project_file(
    file_path: str = Field(..., description="文件路径"),
    file_name: str = Field(..., description="文件名"),
    project_id: str = Field(..., description='项目id'),
    folder_id: str = Field(..., description='文件夹id')
):
    """
    Name:
        上传项目文件
    Description:
        上传项目文件
    Args:
        id: 项目ID
        folder_id: 文件夹id
    """
    data = await upload_file(file_path, file_name)
    url = f"{host}/api/pm/project/file/add"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "project_id": project_id,
        "folder_id": folder_id,
        "files": [{
            "filename": file_name,
            "file_path": data.get("file_path"),
            "is_can_edit": data.get("is_can_edit")
        }]
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="删除项目文件")
async def delete_project_file(
    project_id: str = Field(..., description='项目id'),
    operation_type: int = Field(1, description='操作类型 1 调整首句位置 2 全部解锁'),
    ids: list[str] = Field(..., description='文件ID列表')
):
    """
    Name:
        删除项目文件
    Description:
        删除项目文件
    Args:
        project_id: 项目id
        operation_type: 操作类型 1 调整首句位置 2 全部解锁
    """
    url = f"{host}/api/pm/project/file/delete"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "project_id": project_id,
        "operation_type": operation_type,
        "ids": ids
    }
    return await send_request("POST", url, headers, None, data)

if __name__ == "__main__":
    asyncio.run(edit_project(id="1", project_name="test", project_no="test", comment="test"))
