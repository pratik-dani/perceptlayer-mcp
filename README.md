<img src="logo.svg" alt="Perceptlayer" height="32">

# Perceptlayer MCP server

Live web data for AI agents. Google Search, Google Maps, Amazon, Zillow, Airbnb,
Booking.com, Indeed, Walmart, eBay, Tripadvisor, Trustpilot, Glassdoor, Google Flights
and 412 more websites as structured JSON, through one API key and three tools
(480 websites, 2,782 endpoints).

This is a hosted (remote) MCP server. There is nothing to install: point your client
at the URL.

```
https://perceptlayer.com/mcp
```

Transport: Streamable HTTP. Searching the catalogue needs no account. To call an endpoint,
sign in when your client offers it (OAuth, for ChatGPT, Claude and other clients that support
it) or send `Authorization: Bearer sk_live_...`
([get a free key](https://perceptlayer.com/signup), 100 credits on signup, no card).

## Tools

| Tool | What it does | Cost |
| --- | --- | --- |
| `search_endpoints` | Finds endpoints for a site or kind of data, such as "airbnb listing". | Free, no key |
| `get_endpoint` | Lists one endpoint's parameters, with an example and its credit cost. | Free, no key |
| `call_endpoint` | Runs an endpoint and returns its JSON. | The endpoint's credits |

The agent searches the catalogue instead of loading 2,582 tool definitions into its
context.

## Connect a client

**Claude Code**

```bash
claude mcp add --transport http perceptlayer https://perceptlayer.com/mcp \
  --header "Authorization: Bearer $PERCEPTLAYER_API_KEY"
```

**Cursor**: [`examples/cursor-mcp.json`](examples/cursor-mcp.json) in `~/.cursor/mcp.json`.

**VS Code**: [`examples/vscode-mcp.json`](examples/vscode-mcp.json) in `.vscode/mcp.json`.
VS Code asks for the key once and stores it.

**Claude Desktop** and other stdio-only clients: [`examples/claude-desktop.json`](examples/claude-desktop.json),
which bridges through `mcp-remote`.

Any other client that supports remote MCP servers needs the same URL and header.
Browser-based MCP clients aren't supported yet.

## Examples

Runnable code in [`examples/`](examples/): the three tool calls with the MCP Python and
TypeScript SDKs, and an agent built on the Claude Agent SDK that answers a question from
live data.

## What you can get

| Area | Sources |
| --- | --- |
| Real estate | 159 |
| Marketplaces | 69 |
| Social (additional terms) | 40 |
| Cars | 39 |
| Search | 30 |
| Travel | 28 |
| Jobs | 20 |
| Reviews | 15 |
| Apps | 13 |
| Web and SEO | 12 |

Full catalogue: [perceptlayer.com/apis](https://perceptlayer.com/apis).

## Pricing

- 1 credit per successful call. Failed calls (invalid parameters, no data, rate limits,
  source outages) cost nothing.
- Free: 100 credits on signup, 1 request a second.
- Prepaid packs from $15 for 10,000 credits, down to $0.60 per 1,000 calls. No
  subscription; credits last 12 months.

Details: [perceptlayer.com/pricing](https://perceptlayer.com/pricing).

## Limits

- Calls through MCP follow the API's rules: [rate limits](https://docs.perceptlayer.com/rate-limits)
  apply and [restricted endpoints](https://docs.perceptlayer.com/restricted-endpoints) need the terms.
- Responses longer than 100,000 characters are cut short; use an endpoint's paging or
  limit parameters.

## Links

- Docs: [docs.perceptlayer.com/ai-agents](https://docs.perceptlayer.com/ai-agents)
- REST API reference: [docs.perceptlayer.com](https://docs.perceptlayer.com)
- MCP Registry manifest: [`server.json`](server.json)
- Support: support@perceptlayer.com

The server itself is closed source; this repository holds its public listing, client
configs and registry manifest under the MIT license.
