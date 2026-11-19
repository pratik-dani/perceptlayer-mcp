# Examples

Each example does the same three things an agent does with this server: search the
catalogue, read an endpoint's parameters, call it.

| Example | What it is | Needs |
| --- | --- | --- |
| [`python-client/`](python-client/client.py) | The three tool calls with the MCP Python SDK, no model involved | Python 3.10+, `pip install "mcp>=2"` |
| [`node-client/`](node-client/client.mjs) | The same with the MCP TypeScript SDK | Node 18+, `npm install @modelcontextprotocol/sdk` |
| [`claude-agent-sdk/`](claude-agent-sdk/agent.py) | An agent that answers a question from live data, choosing the endpoints itself | `pip install claude-agent-sdk`, and Claude Code signed in or `ANTHROPIC_API_KEY` |
| [`claude-desktop.json`](claude-desktop.json), [`cursor-mcp.json`](cursor-mcp.json), [`vscode-mcp.json`](vscode-mcp.json) | Client configuration files | |

Searching the catalogue is free and needs no key, so the two client examples print
their first two steps as they are. For the call itself, set a key
([free, 100 credits on signup](https://perceptlayer.com/signup)):

```bash
export PERCEPTLAYER_API_KEY=sk_live_...
python python-client/client.py
node node-client/client.mjs
python claude-agent-sdk/agent.py "Find three well-rated coffee shops in Austin, with rating and address."
```

A successful call spends the credits the endpoint lists, usually 1. A failed call costs nothing.

Clients with a person at the keyboard (ChatGPT, Claude, Claude Code) don't need a key:
add `https://perceptlayer.com/mcp` and sign in when the client asks.
