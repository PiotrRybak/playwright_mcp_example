# --- Standard library imports ---
import os
import asyncio
import random

# ---------------------------------------------------------------------------
# 1. Configure environment BEFORE importing the Agents SDK or OpenAI client
# ---------------------------------------------------------------------------

# Local servers ignore the key but the OpenAI client expects one to exist.
os.environ["OPENAI_API_KEY"] = "NO-KEY-REQUIRED"

# Point the SDK at our local OpenAI-compatible endpoint (Ollama / llama.cpp / LM Studio)
#os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:5001/v1/"
os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:11434/v1/"

# ---------------------------------------------------------------------------
# 2. Now that env vars are in place, import the Agents SDK and disable tracing
# ---------------------------------------------------------------------------

from agents import set_tracing_disabled, SQLiteSession
from agents.models import _openai_shared  # Add this import to control OpenAI provider behavior

# Disable tracing to avoid attempts to upload runs to api.openai.com
set_tracing_disabled(True)

# Disable the Responses API (use Chat Completions) because local endpoints don't implement /responses
_openai_shared.set_use_responses_by_default(False)

# ---------------------------------------------------------------------------
# 3. Remaining imports that rely on the configured environment
# ---------------------------------------------------------------------------

from agents import Agent, Runner
from agents.mcp import MCPServerSse  # Connect via SSE to running Playwright MCP server
from litellm import completion

# 2. Describe your MCP server (here: playwright server for web automation)
mcp_playwright = MCPServerSse(
    name="Playwright SSE Server",
    params={
        "url": "http://localhost:8931/sse",
        # Disable the SSE read timeout to keep the connection open indefinitely
        "sse_read_timeout": None,
    },
    client_session_timeout_seconds=None,
)

# 3. Build a single agent
agent = Agent(
    name="Playwright‑Agent",
    instructions="You are a web automation agent. Use Playwright MCP tools to navigate websites, interact with elements, and extract information. When asked to get content from a webpage, use the appropriate Playwright tools to navigate to the page and extract the requested information. Use Playwright tool calls always when navigating, reading, or interacting with the page. Look carefully at the page and use the tools to navigate to the page and extract the requested information. Return short final result when you are done. You can use the same tool multiple times.",
    mcp_servers=[mcp_playwright],
    model="qwen3:14blong"
)

# Connect to the SSE server before running the agent
asyncio.get_event_loop().run_until_complete(mcp_playwright.connect())

# 4. Run

session = SQLiteSession("conversation_" + str(random.randint(100000, 999999)))

result = Runner.run_sync(agent, "Go to https://jp.indeed.com/, and then open the login screen.", session=session)

print(result.final_output)
print(result.tool_calls_executed)

# Cleanup the server connection
asyncio.get_event_loop().run_until_complete(mcp_playwright.cleanup()) 