# Configure the resource server

The gist of the OAuth flow is that an authorization server issues tokens that give clients access to protected resources for a limited time.

The resource server has the responsibility of enforcing the authorization policy, by:

- Checking that requests are accompanied by a JWT token.
- Verifying the token's authenticity (by checking the signature of the token).
- Verifying the token's expiration timestamp.
- Verifying the token's audience scope matches the intended audience (`echo-mcp-server`).

In this section we begin implementing this enforcement by coding it directly in the application.

## Instructions

Review the following updated application:

```python title="main-with-auth.py" linenums="1" hl_lines="8-16 18"
--8<-- "main-with-auth.py"
```

The main difference from `main.py` is the construction of the FastMCP object with the auth provider `auth_provider`.
Note how the `jwks_uri`, `issuer`, and `audience` match those of the authorization server provisioned in the previous section.

Copy the above `main-with-auth.py` script to your project:

```shell
cp ../artifacts/main-with-auth.py .
```

## Test it

Start the MCP server:

```shell
uv run main-with-auth.py
```

In a separate terminal, attempt to make an HTTP POST request to the `/mcp` endpoint:

```shell
curl -s -v -X POST http://localhost:8000/mcp
```

Here are the salient parts of the captured response:

```shell linenums="1" hl_lines="11 16-18"
* Host localhost:8000 was resolved.
* ...
* Established connection to localhost (127.0.0.1 port 8000) from 127.0.0.1 port 65521
* using HTTP/1.x
> POST /mcp HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.16.0
> Accept: ..
>
* Request completely sent off
< HTTP/1.1 401 Unauthorized
< date: Wed, 15 Oct 2025 18:09:13 GMT
< server: uvicorn
< content-type: application/json
< content-length: 74
< www-authenticate: Bearer error="invalid_token", \
    error_description="Authentication required", \
    resource_metadata="http://localhost:8000/.well-known/oauth-protected-resource"
<
* Connection #0 to host localhost:8000 left intact
{"error": "invalid_token", "error_description": "Authentication required"}
```

Above, note that we were not granted access to the resource, due to the absence of a valid access token in the request.

We get a 401 "Unauthorized" response.
The interesting part is the presence of the response header `www-authenticate`, whose value include the `resource_metadata` attribute which tells the client where to find the authorization server.

If we query that URL ^*^:

```shell
curl -s http://localhost:8000/.well-known/oauth-protected-resource/mcp | jq
```

!!! note "^*^ Above"

    FastMCP appends the suffix `/mcp` to the oauth protected resource.

We are indeed told where to find the authorization server:

```json
{
  "resource": "http://localhost:8000/mcp",
  "authorization_servers": [
    "http://localhost:8080/realms/my-realm"
  ],
  "scopes_supported": [],
  "bearer_methods_supported": [
    "header"
  ]
}
```

!!! note "Above"

    The field `scopes_supported` is empty because we didn't configure a list of valid scopes for the application.


## Test the full OAuth flow

Launch the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

In the form panel on the left:

- Expand _Authentication_.
- Set the _Client ID_ to `mcp-client`.
- Click _Open Auth Settings_ (in the middle of the page).

The _Authentication Settings_ page in the inspector provides a guided OAuth flow.

1. Metadata Discovery:  click the _Continue_ button.
  Expand the _OAuth Metadata Sources_.
  The inspector fetched the discovery endpoint and used it to introspect Keycloak's metadata to discover the endpoints for registration, authorization, and the token endpoint.
2. Client registration:  since we're using a registered client `mcp-client`, no registration takes place.  Click _Continue_
3. Preparing Authorization: This is where the client constructs the authorization URL.
   Follow the URL, and log in to Keycloak using the realm user `eitan` (password `test`).:w
   An authorization code is presented.  Copy it and paste it into the _Authorization Code_ field.
   Click _Continue_
4. Token Request: Click _Continue_.  The inspector will call the token endpoint with the supplied authorization code.
5. Authentication Complete: Expand _Access Tokens_ to revel the access token obtained from the token endpoint.
   Feel free to use sites such as jwt.io to decode the access token and confirm that the audience scope is present in the token.

The full flow functions:  Click _Connect_ and confirm that you can still list tools and call the `echo` tool as before.

## Summary

Congrats!  Basic OAuth authorization is functioning.

But the solution is not ideal, in that the authorization enforcement concern is coupled to the application logic.

A better solution would be to separate those two responsibilities, which can be implemented with the aid of a proxy -- the subject of the next section.