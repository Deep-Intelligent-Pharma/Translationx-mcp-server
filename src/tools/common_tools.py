import uuid
import httpx
from pydantic import Field

from server import mcp, host, headers


@mcp.tool(description="获取语言code信息")
async def get_language_code():
    """
    Name:
        获取枚举信息
    Description:
        获取枚举信息
    """
    url = f"{host}/api/common/enums"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    headers['x-language'] = 'zh-CN'
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.request("GET", url, headers=headers)
            result = resp.json()
            code = result.get("code")
            if code != "0":
                error_msg = result.get("message", "unkown error")
                raise Exception(f"API response error: {error_msg}")
            data = result.get("data")
            language_codes = data.get("languageenum")
            return language_codes
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


@mcp.tool(description="上传文件")
async def upload_file(
    file_path: str = Field(..., description="文件路径"),
    file_name: str = Field(..., description="文件名"),
):
    """
    Name:
        上传文件
    Description:
        上传文件
    """
    url = f"{host}/api/common/upload_big_file"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    headers['x-language'] = 'zh-CN'
    identification = str(uuid.uuid4())
    data = {
        "no": "0",
        "identification": identification,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.request("POST", url, headers=headers, data=data, files={"file": (file_name, open(file_path, "rb"), "application/octet-stream")})
        result = resp.json()
        if resp.status_code != 200 or result.get("code") != "0":
            raise Exception(f"API response error: {result.get('message', 'unkown error')}")

        # 获取上传文件的url
        url = f"{host}/api/common/merge_file"
        headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
        headers['x-language'] = 'zh-CN'
        data = {
            "filename": file_name,
            "identification": identification,
        }
        resp = await client.request("POST", url, headers=headers, data=data)
        result = resp.json()
        if resp.status_code != 200 or result.get("code") != "0":
            raise Exception(f"API response error: {result.get('message', 'unkown error')}")
        data = result.get("data")
        return data



if __name__ == '__main__':
    import anyio

    a = anyio.run(get_language_code)
    print(a)
