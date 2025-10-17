# Targeting Kubernetes

Activities so far have run MCP servers on a local machine.
This is useful when developing.

In this final activity, you will learn about [kmcp](https://kagent.dev/docs/kmcp), (a part of the [kagent project](https://kagent.dev/)) a tool designed specifically to aid with the end-to-end process, from scaffolding a new project, to building a Docker image, to deploying the MCP server to Kubernetes.

install the kmcp CLI

```shell
curl -fsSL https://raw.githubusercontent.com/kagent-dev/kmcp/refs/heads/main/scripts/get-kmcp.sh | bash
```

A Kubernetes cluster is running.

Deploy the kmcp CRDs:

```shell
helm install kmcp-crds oci://ghcr.io/kagent-dev/kmcp/helm/kmcp-crds \
  --namespace kmcp-system \
  --create-namespace
```

Run `kmcp install` to deploy the Kubernetes controller:

```shell
kmcp install
```

## Scaffolding

kmcp supports multiple target frameworks: go, python, java, and typescript.

```shell
kmcp init --help
```

Start a new python project:

```shell
kmcp init python my-mcp-server --description "My first mcp server" --non-interactive \
  && cd my-mcp-server
```

Inspect the project directory structure:

```shell
tree .
```

An example `echo` tool is present by default.
It's easy to add more tools by adding more `.py` files to the `tools/` subdirectory.

## Test the MCP Server

The kmcp CLI provides a convenient `run` command:

```shell
kmcp run
```

It launches the MCP server, and the MCP inspector, allowing us to test connecting to the server, listing tools, and running them.

## Build and Package

The kmcp `build` command simplifies building and packaging the MCP server:

```shell
kmcp build --help
```

Building the MCP server produces a Docker image:

```shell
kmcp build --tag my-mcp-server:latest
```

Next, we can publish the container image to a registry.

Here let's simply upload the image to the cluster:

```shell
k3d image import my-mcp-server --cluster my-k8s-cluster
```

## Deploy

Finally, deploy the MCP server to the cluster:

```shell
kmcp deploy --file kmcp.yaml --image my-mcp-server:latest
```

Deployment generates and applies an MCPServer resource to the cluster:

```shell
kubectl get mcpserver my-mcp-server -o yaml
```

The kmcp controller watches for MCPServer resources and creates (and applies) the deployment manifest for us:

```shell
kubectl get pod
```

The above deploy command also launches an MCP inspector allowing us to test the deployed MCP server.

## Summary

Congratulations!  Your MCP server is now running on Kubernetes.

The story does not end here.

Agentgateway is [supported in Kubernetes](https://agentgateway.dev/docs/kubernetes/) by the kgateway project, a control plane that can dynamically program agentgateway using cloud-native APIs such as the Kubernetes Gateway API and AI extensions.

With kgateway, we can deploy an agentgateway proxy for our MCP server and configure it to route requests to the MCP server, with MCP authorization and other policies.
See Christian Posta and Lin Sun's upcoming ebook _AI Agents in Kubernetes_ for more information.