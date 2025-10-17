# Enterprise Single sign-on (SSO)

In enterprises, employees log in to multiple workplace applications with a single set of credentials.

Employees will already bear a JWT token in the requests they make.

For our MCP server to work in that context, we can revise the gateway's configuration to verify the enterprise-issued JWT token.

agentgateway supports [JWT Authentication](https://agentgateway.dev/docs/configuration/security/jwt-authn/), which resembles our previous configuration, in that token verification still involves an issuer, an audience, and a jwks URL.

Let us demonstrate how this works.

## JWT Authentication

Use the [step CLI](https://smallstep.com/docs/step-cli/) to generate a key pair:

```shell
step crypto jwk create pub-key priv-key
```

Press enter when prompted for a password to protect the key.

Next, generate the JSON Web Key:

```shell
cat pub-key | step crypto jwk keyset add jwks-keyset
```

Generate and sign a JWT token, with a specified issuer and audience:

```shell
step crypto jwt sign --key priv-key \
  --iss "acme@example.com" --aud="mcp.example.com" \
  --sub "jsmith" --exp $(date -v+10y +"%s") > jsmith.token
```

Review the following agentgateway configuration, which requires a valid JWT token to access the MCP server:

```yaml title="ag-jwtauth-config.yaml" linenums="1" hl_lines="11-16"
--8<-- "ag-jwtauth-config.yaml"
```

Copy the above `ag-jwtauth-config.yaml` script to your project:

```shell
cp ../artifacts/ag-jwtauth-config.yaml .
```

## Test it

Run the basic MCP server:

```shell
uv run main.py
```

Start the agentgateway:

```shell
./agentgateway -f ag-jwtauth-config.yaml
```

Launch the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

Attempt to connect to the MCP server.
The request will fail.

A line in the `agentgateway` logs will confirm that the request was denied due to the absence of a bearer token:

```shell hl_lines="4"
2025-10-17T18:00:57.855104Z     info    request gateway=bind/9000 listener=listener0 \
  route_rule=route0/default route=route0 src.addr=[::1]:63358 http.method=POST \
  http.host=localhost http.path=/mcp http.version=HTTP/1.1 \
  http.status=403 protocol=http error="authentication failure: no bearer token found" duration=0ms
```

Next, under Authentication -> Custom Headers, click `+ Add`, set the header, as follows:

- Header Name: `Authorization`
- Header Value: `Bearer <paste the contents of the file jsmith.token>`

And click _Connect_.
The connection will succeed, and we can proceed to list tools and run the echo tool.

Disconnect the MCP inspector.

## MCP Authorization

agentgateway supports configuring authorization policy for MCP requests and gives us access to MCP-specific metadata, such as the tool name being invoked.
We also get information from the JWT token, such as claims.

The following gateway configuration adds an MCP authorization policy which requires the user to have administrative privileges (role claim contains "admin") in order to access the `echo` tool:

```yaml title="ag-mcp-authorization.yaml" linenums="1" hl_lines="17-19"
--8<-- "ag-mcp-authorization.yaml"
```

Copy the above `ag-mcp-authorization.yaml` script to your project:

```shell
cp ../artifacts/ag-mcp-authorization.yaml .
```

Restart the agentgateway with the authorization configuration:

```shell
./agentgateway -f ag-mcp-authorization.yaml
```

Attempt to connect again.
The connection is permitted.

However, attempt to List tools (you may need to clear tools first, to clear lingering results), the echo tool is no longer listed.

Generate a second JWT, this time for an admin user:

```shell
echo '{ "roles": ["admin"] }' | \
  step crypto jwt sign --key priv-key \
    --iss "acme@example.com" --aud="mcp.example.com" \
    --sub "pointy-haired-boss" --exp $(date -v+10y +"%s") > boss.token
```

In the MCP inspector, replace the Authorization header with the admin user's JWT token.

- Try to connect again
- List tools

The echo tool will be present this time since this user is allowed to call it.