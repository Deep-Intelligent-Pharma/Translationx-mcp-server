import httpx


def send_request(method, url, headers, params, data):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.request(method, url, headers=headers, params=params, json=data)
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

