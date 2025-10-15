# A simple MCP server

Begin by creating a simple MCP service with a single, simple "echo" tool.

## Steps

In a terminal, create a project directory and navigate to it:

```shell
mkdir echo-mcp-server && cd echo-mcp-server
```

Initialize a python project:

```shell
uv init
```

We will use the [fastmcp](https://gofastmcp.com/) framework, so add the dependency:

```shell
uv add fastmcp
```

Review the following simple application that exposes a single "echo" tool:

```python title="main.py"
--8<-- "main.py"
```

!!! note

    - The function produces a string that repeats the given message a given number of times.
    - The MCP service is launched using the `http` transport on port 8000

Copy the above `main.py` script to your project, replacing the stub `main.py` previously produced by `uv init`:

```shell
cp artifacts/main.py echo-mcp-server/
```

## Test it

Launch the application:

```shell
uv run main.py
```

You should see the FastMCP banner come up.

In a separate terminal, launch the MCP Inspector:

```shell
npx @modelcontextprotocol/inspector
```

In the Inspector's browser page, on the left hand side, specify:

1. Transport Type:  `Streamable HTTP`
2. URL: `http://localhost:8000/mcp`

Click _Connect_.

The inspector will switch to the _Connected_ state.

- Select the `tools` tab from the header.
- Click _List Tools_ - the `echo` tool will display.
- Select the `echo` tool.
- Enter a message.
- Click _Run tool_.

Validate the results.
_Disconnect_ the inspector once you are satisfied that the tool is functioning properly and terminate the running MCP server (press _Ctrl+C_ in the terminal).

## Summary

We now have a basic MCP server.
In the next step, we turn our attention to MCP authorization.