"""An agent that answers a question with live web data, built on the Claude Agent SDK.

    pip install claude-agent-sdk
    export PERCEPTLAYER_API_KEY=sk_live_...   # free at https://perceptlayer.com/signup
    python agent.py "Find three well-rated coffee shops in Austin, with rating and address."

The agent searches the catalogue for an endpoint, reads its parameters and calls it,
then answers from the JSON it got back. Each successful call spends the credits the
endpoint lists (usually 1); failed calls cost nothing.

Claude itself runs through your Claude Code sign-in or ANTHROPIC_API_KEY.
"""

import asyncio
import os
import sys

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, SystemMessage, query

URL = "https://perceptlayer.com/mcp"
QUESTION = "Find three well-rated coffee shops in Austin, with rating and address."


async def main() -> None:
    options = ClaudeAgentOptions(
        mcp_servers={
            "perceptlayer": {
                "type": "http",
                "url": URL,
                "headers": {"Authorization": f"Bearer {os.environ['PERCEPTLAYER_API_KEY']}"},
            }
        },
        # Only this server's three tools are approved: search_endpoints, get_endpoint, call_endpoint.
        allowed_tools=["mcp__perceptlayer__*"],
    )

    prompt = sys.argv[1] if len(sys.argv) > 1 else QUESTION
    async for message in query(prompt=f"Use the perceptlayer tools to answer: {prompt}", options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            # Without the server the agent has nothing to answer from: say so, don't let it guess.
            for server in message.data.get("mcp_servers", []):
                if server.get("name") == "perceptlayer" and server.get("status") in ("failed", "needs-auth"):
                    print(f"perceptlayer MCP server: {server['status']}. Check PERCEPTLAYER_API_KEY.", file=sys.stderr)
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if getattr(block, "name", "").startswith("mcp__"):
                    print(f"-> {block.name} {block.input}", file=sys.stderr)
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
