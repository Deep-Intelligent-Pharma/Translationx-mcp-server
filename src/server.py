import os
from mcp.server import FastMCP

mcp = FastMCP("tx-mcp")
token = os.getenv('token')
host = "https://translation.x-doc.ai"
headers = {"token": token}
