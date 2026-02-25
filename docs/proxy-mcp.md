# Proxy the MCP Server

In the previous section you configured an authenticated MCP server by using FastMCP's built-in authentication support.

In a production setting, we are much better off separating the concern of implementing the MCP server's functionality from that of configuring authorization (or any other cross-cutting concern beyond security, such as observability, for example).

In this exercise, security policy configuration and enforcement is moved out of the application and into a proxy.

## agentgateway

[agentgateway](https://agentgateway.dev/) is a modern proxy that supports modern AI protocols including [MCP](https://agentgateway.dev/docs/mcp/) and A2A.

### Install agentgateway

[Install](https://agentgateway.dev/docs/quickstart/) the `agentgateway` binary to your project directory:

```shell
USE_SUDO=false AGENTGATEWAY_INSTALL_DIR=. curl https://raw.githubusercontent.com/agentgateway/agentgateway/refs/heads/main/common/scripts/get-agentgateway | bash
```

## Proxy the MCP server

The documentation provides [an example](https://agentgateway.dev/docs/mcp/connect/http/) for configuring and running the gateway to route requests to an MCP backend.

Let's give it a try to understand how this works.

Run the basic MCP server:

```shell
uv run main.py
```

Review the following agentgateway configuration file:

```yaml title="ag-config.yaml" linenums="1" hl_lines="2 12-16"
--8<-- "ag-config.yaml"
```

Above, we configure agentgateway to listen on port 9000, and to route all requests (with a liberal CORS policy) to our MCP backend listening on port 8000.

Copy the above `ag-config.yaml` script to your project:

```shell
cp ../artifacts/ag-config.yaml .
```

### Test it

Start the agentgateway:

```shell
./agentgateway -f ag-config.yaml
```

Launch the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

Point the _URL_ field to the agentgateway proxy running on port 9000:  `http://localhost:9000/mcp`

Click _Connect_ and confirm that everything works, as if we were communicating directly with the MCP server.

Inspect the logs of the agentgateway console to see evidence that requests are indeed routed via the proxy.

Terminate the agentgateway (press `Ctrl+C`).

## Configure authentication

The project documentation provides [an example](https://agentgateway.dev/docs/mcp/mcp-authn/) for configuring MCP authentication directly on the proxy.

Review the updated agentgateway configuration file:

```yaml title="ag-oauth-config.yaml" linenums="1" hl_lines="11-16"
--8<-- "ag-oauth-config.yaml"
```

Above, note that the configuration utilizes the same `issuer`, `jwks.url`, and `audiences` field values for the authorization server.

Copy the above `ag-oauth-config.yaml` script to your project:

```shell
cp ../artifacts/ag-oauth-config.yaml .
```

### Test it

If it's not already running, start the basic, unprotected MCP server:

```shell
uv run main.py
```

Start the agentgateway:

```shell
./agentgateway -f ag-oauth-config.yaml
```

Finally, launch the MCP Inspector.

```shell
npx @modelcontextprotocol/inspector
```

This MCP server should be protected.

Start by walking through the Guided OAuth flow:

- Click _Open Auth Settings_ in the center of the page.
- Click _Guided OAuth Flow_.
- Like before, go through all steps from Metadata Discovery through to Token request.
- When instructed to follow the authorization URL, log in with the user credentials `eitan/test`.
- Copy and paste the authorization code into the corresponding field.

When the authentication completes, we have been issued a token.

Proceed to click _Connect_ on the left hand panel, and to confirm that interaction with the MCP server continues to function as before: Tools -> List Tools -> Echo -> Run Tool.

## Summary

Congratulations!  You now have a flexible configuration: an MCP server fronted by an intelligent proxy where MCP authentication is configured.