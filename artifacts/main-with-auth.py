from typing import Annotated

from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import AnyHttpUrl, Field

auth_provider = RemoteAuthProvider(
    token_verifier=JWTVerifier(
        jwks_uri="http://localhost:8080/realms/my-realm/protocol/openid-connect/certs",
        issuer="http://localhost:8080/realms/my-realm",
        audience="echo-mcp-server"
    ),
    authorization_servers=[AnyHttpUrl("http://localhost:8080/realms/my-realm")],
    base_url="http://localhost:8000"
)

mcp = FastMCP("MCP Echo Server", auth=auth_provider)

@mcp.tool
def echo(
        message: Annotated[str, "Message to echo"],
        repeat_count: Annotated[int, Field(description="Number of times to repeat the message", ge=1, le=10)] = 3
    ) -> str:
        """Echo a message a specified number of times."""
        return message * repeat_count

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)