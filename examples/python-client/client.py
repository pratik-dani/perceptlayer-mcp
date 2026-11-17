"""Find an endpoint, read its parameters and call it, with the MCP Python SDK.

    pip install "mcp>=2"
    export PERCEPTLAYER_API_KEY=sk_live_...   # free at https://perceptlayer.com/signup
    python client.py

Searching the catalogue works without a key. Calling an endpoint needs one and
costs the credits the endpoint lists (1 here); a failed call costs nothing.
"""

import asyncio
import json
import os

import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://api.perceptlayer.com/mcp"


def text(result) -> str:
    """The text of a tool result."""
    return "\n".join(block.text for block in result.content if block.type == "text")


async def run(session: ClientSession, has_key: bool) -> None:
    # 1. Search the catalogue for the data you want. Free, no key.
    found = await session.call_tool("search_endpoints", {"query": "google maps places search", "limit": 3})
    print(text(found))

    # 2. Read one endpoint's parameters. Free, no key.
    details = await session.call_tool("get_endpoint", {"endpoint": "google-maps.simple-search"})
    print(text(details))

    if not has_key:
        print("\nSet PERCEPTLAYER_API_KEY to run the call itself.")
        return

    # 3. Call it. The first text block is the endpoint's JSON response.
    called = await session.call_tool(
        "call_endpoint",
        {"endpoint": "google-maps.simple-search", "params": {"query": "coffee shops in austin"}},
    )
    if called.is_error:
        raise SystemExit(text(called))
    places = json.loads(called.content[0].text)
    print(json.dumps(places, indent=2)[:1500])


async def main() -> None:
    key = os.environ.get("PERCEPTLAYER_API_KEY")
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    async with (
        httpx2.AsyncClient(headers=headers, timeout=60) as http,
        streamable_http_client(URL, http_client=http) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        await run(session, bool(key))


asyncio.run(main())
