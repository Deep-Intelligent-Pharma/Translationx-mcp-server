from utils import send_request
from pydantic import Field
import uuid
import asyncio
import httpx
host = "https://translation.x-doc.ai"
headers = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTA1LCJlbWFpbCI6Inlhbmdzb25nYmFpQGRpcC1haS5jb20iLCJyb2xlIjoiZnJlZSIsImF1dGhfcHJvdmlkZXIiOiJlbWFpbCIsImV4cCI6MTc0NDk1NTE3NiwibW9kZSI6ImFjY2Vzc190b2tlbiJ9.7ILW5s6lLD9JYPTFaJKzGvIDFxiXfRgqfvjiCSCgfvA"}


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
    headers["Content-Type"] = "application/json"
    data = {
        "id": id,
        "project_name": project_name,
        "project_no": project_no,
        "comment": comment,
        "charge_user_id": "1"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=data)
        result = resp.json()
        code = result.get("code")
        if code != "0":
            error_msg = result.get("message", "unkown error")
            print(result)
            raise Exception(f"API response error: {error_msg}")
        data = result.get("data")
        return data
    # return await send_request("POST", url, headers, None, data)


if __name__ == "__main__":

    asyncio.run(edit_project(id="33", project_name="测试修改", project_no="测试修改", comment="hello world"))