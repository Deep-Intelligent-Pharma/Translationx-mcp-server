from tools.file_tools import *
from tools.project_tools import *
from tools.corpus_tools import *
from server import mcp

if __name__ == '__main__':
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
    # anyio.run(run_sse_async)
