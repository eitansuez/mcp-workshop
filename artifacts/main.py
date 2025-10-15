from typing import Annotated
from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("MCP Echo Server")

@mcp.tool
def echo(
        message: Annotated[str, "Message to echo"],
        repeat_count: Annotated[int, Field(description="Number of times to repeat the message", ge=1, le=10)] = 3
    ) -> str:
        """Echo a message a specified number of times."""
        return message * repeat_count

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)