# Introduction

In this workshop you will learn to build MCP servers and secure them with OAuth2.

An important focus is building and deploying production-ready MCP services, ones that can be maintained, upgraded, consumed by multiple agents, and secured with authentication and authorization policies.

The activities in this workshop were inspired by the work of Christian Posta and Lin Sun.

One influence is Christian's four-part series "Understanding MCP Authorization, Step by Step" ([GitHub Repository](https://github.com/christian-posta/mcp-auth-step-by-step)):

- [Part 1: An MCP server](https://blog.christianposta.com/understanding-mcp-authorization-step-by-step/)
- [Part 2: Hand-rolled OAuth](https://blog.christianposta.com/understanding-mcp-authorization-step-by-step-part-two/)
- [Part 3: Keycloak](https://blog.christianposta.com/understanding-mcp-authorization-step-by-step-part-three/)
- [Part 4: DCR](https://blog.christianposta.com/understanding-mcp-authorization-with-dynamic-client-registration/)

Another is Christian Posta and Lin Sun's upcoming ebook "AI Agents in Kubernetes."

You will:

1. Build an MCP server & test it with MCP inspector
2. Provision Keycloak and configure it as the Identity Provider (IdP).
3. Configure the MCP server with OAuth2 and demonstrate authentication flow.
4. Introduce agentgateway as a passthrough proxy.
5. Shift the authentication & authorization configuration from the MCP server to the gateway

We then shift focus to deploying the solution on Kubernetes.

In the second part of this workshop, you will:

1. Deploy MCP servers to Kubernetes.
2. Build an agent (with kagent) that utilizes the tools exposed by the MCP server.
3. See the tool server work in an end-to-end scenario with an agent.
