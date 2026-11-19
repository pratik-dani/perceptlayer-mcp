// Find an endpoint, read its parameters and call it, with the MCP TypeScript SDK.
//
//   npm install @modelcontextprotocol/sdk
//   export PERCEPTLAYER_API_KEY=sk_live_...   # free at https://perceptlayer.com/signup
//   node client.mjs
//
// Searching the catalogue works without a key. Calling an endpoint needs one and
// costs the credits the endpoint lists (1 here); a failed call costs nothing.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const URL_ = "https://perceptlayer.com/mcp";
const key = process.env.PERCEPTLAYER_API_KEY;
const text = (result) => result.content.filter((b) => b.type === "text").map((b) => b.text).join("\n");

const transport = new StreamableHTTPClientTransport(new URL(URL_), {
  requestInit: { headers: key ? { Authorization: `Bearer ${key}` } : {} },
});
const client = new Client({ name: "perceptlayer-example", version: "1.0.0" });
await client.connect(transport);

// 1. Search the catalogue for the data you want. Free, no key.
const found = await client.callTool({ name: "search_endpoints", arguments: { query: "google maps places search", limit: 3 } });
console.log(text(found));

// 2. Read one endpoint's parameters. Free, no key.
const details = await client.callTool({ name: "get_endpoint", arguments: { endpoint: "google-maps.simple-search" } });
console.log(text(details));

if (!key) {
  console.log("\nSet PERCEPTLAYER_API_KEY to run the call itself.");
} else {
  // 3. Call it. The first text block is the endpoint's JSON response.
  const called = await client.callTool({
    name: "call_endpoint",
    arguments: { endpoint: "google-maps.simple-search", params: { query: "coffee shops in austin" } },
  });
  if (called.isError) throw new Error(text(called));
  console.log(JSON.stringify(JSON.parse(called.content[0].text), null, 2).slice(0, 1500));
}
await client.close();
