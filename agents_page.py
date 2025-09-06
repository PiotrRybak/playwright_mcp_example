import os
import asyncio
import json
import random

os.environ["OPENAI_API_KEY"] = "NO-KEY-REQUIRED"
os.environ["OPENAI_BASE_URL"] = "http://172.25.67.56:8080/"

from agents.models import _openai_shared
from agents import set_tracing_disabled, enable_verbose_stdout_logging, SQLiteSession

enable_verbose_stdout_logging()
set_tracing_disabled(True)
_openai_shared.set_use_responses_by_default(False)

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

from typing_extensions import TypedDict

class AgentRecord(TypedDict):
    name: str
    agency: str
    link: str

@function_tool  # strict mode stays True by default
def append_jsonl(path: str, record: AgentRecord, create_dirs: bool = True) -> str:
    """Append one JSON object as a new line to a .jsonl file."""
    if create_dirs:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    line = json.dumps(record, ensure_ascii=False)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return f"wrote 1 line to {path}"

async def main():
    mcp_playwright = MCPServerSse(
        name="Playwright SSE Server",
        params={
            "url": "http://localhost:8931/sse",
            "sse_read_timeout": None,
        },
        client_session_timeout_seconds=None,
    )

    # Build a single agent
    agent = Agent(
        name="Playwright‑Agent",
        instructions=(
            "You are a web automation agent. Use Playwright MCP tools to navigate websites. "
            "When asked to save or log data, call the 'append_jsonl' tool with a file path and a JSON record. "
            "Return a short final result when done."
        ),
        mcp_servers=[mcp_playwright],
        model="DEFAULT",
        tools=[append_jsonl],
    )

    # Ensure the MCP server is connected and properly cleaned up
    async with mcp_playwright:
        session = SQLiteSession("conversation_" + str(random.randint(100000, 999999)))

        result = await Runner.run(
            agent,
            "Visit https://querytracker.net/agents/. On each page, collect all agent entries. "
            "For every agent, append a JSON object to logs/querytracker_agents.jsonl with keys: "
            "{'name': '<agent name>', 'agency': '<agency name>', 'link': '<agent page URL>'}. "
            "Follow pagination to go through all pages until there are no more, then finish.",
            session=session,
        )

    print("\n\n=== FINAL RESULT ===")
    print(result)

if __name__ == "__main__":
    # Run the async main entrypoint properly
    asyncio.run(main())

