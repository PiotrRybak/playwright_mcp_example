# MCP Agent Example Project

This project demonstrates how to use the OpenAI Agents SDK with Model Context Protocol (MCP) servers to create an intelligent agent that can interact with web pages using browser automation.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for AI models to securely access external resources and tools. In this example, we're using an MCP Playwright server that allows our agent to navigate websites, interact with web elements, and extract information from web pages.

## Features

- **Local LLM Integration**: Uses Ollama as the backend LLM server
- **Web Automation**: Agent can navigate websites and extract information using Playwright
- **MCP Protocol**: Demonstrates modern tool integration patterns for web automation
- **Simple Setup**: Easy to run example with minimal configuration

## How It Works

1. The agent connects to a local Ollama server for language model capabilities
2. An MCP Playwright server is created using Node.js tooling
3. The agent can use Playwright tools to navigate websites, interact with elements, and extract data
4. All processing happens locally for privacy and speed

## Prerequisites

- Python 3.8+
- Node.js (for the MCP Playwright server)
- Ollama server running on localhost:11434
- Playwright browser binaries (see installation step below)

## Quick Start

1. Create and activate virtual environment: `python -m venv venv` then `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
2. Install dependencies: `pip install -r requirements.txt`
3. **Install Playwright browsers**: `npx playwright install`
4. Start the Playwright MCP server (SSE): `npx @playwright/mcp@latest --port 8931`
5. Start Ollama server with your preferred model
6. Run the example: `python main.py`

The agent will navigate to Reddit's LocalLLaMA subreddit and extract the title of the newest post! 
