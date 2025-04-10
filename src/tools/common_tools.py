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
    headers['x-language'] = 'en-US'
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


if __name__ == '__main__':
    import anyio

    a = anyio.run(get_language_code)
    print(a)
