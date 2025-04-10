import uuid
from pydantic import Field

from server import mcp, host, headers
from utils import send_request


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
