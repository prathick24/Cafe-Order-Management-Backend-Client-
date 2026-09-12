from fastmcp import FastMCP
from routes.order_agent_route import router


mcp = FastMCP("my-server")
mcp.mount(router)



if __name__ == "__main__":
    import sys

    if "--serve" in sys.argv:
        # ══════════════════════════════════════════════════════════════
        # START AS HTTP SERVER (Streamable HTTP transport)
        # 
        # This starts a web server at http://localhost:8000/mcp
        # Any MCP client can connect to this URL over HTTP.
        #
        # Key difference from stdio:
        #   stdio  → mcp.run(transport="stdio")       → stdin/stdout
        #   http   → mcp.run(transport="streamable-http") → HTTP on port 8000
        # ══════════════════════════════════════════════════════════════
        print("🚀 Starting MCP Server (HTTP) at http://localhost:8000/mcp")
        print("   Press Ctrl+C to stop.\n")
        mcp.run(transport="streamable-http")