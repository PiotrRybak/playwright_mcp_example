# Setup Instructions for MCP Agent Example

## Prerequisites

Before running this example, you need to have the following installed:

### 1. Python 3.8+
Make sure you have Python 3.8 or later installed on your system.

### 2. Node.js
The MCP filesystem server requires Node.js. Install it from [nodejs.org](https://nodejs.org/) if you haven't already.

### 3. Ollama Server
This example uses Ollama as the local LLM server. 

#### Installing Ollama:
1. Download and install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull a model (e.g., `ollama pull llama2` or `ollama pull llama3.2`)
3. Start the Ollama server (it usually runs automatically after installation)

#### Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

## Installation Steps

### 1. Clone/Download the Project
Make sure you have all the project files in your directory:
- `main.py`
- `requirements.txt`
- `README.md`
- `SETUP.md`

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Node.js is Available
The MCP filesystem server uses npx to run a Node.js package. Verify it's available:
```bash
npx --version
```

## Running the Example

### 1. Activate Virtual Environment (if not already active)
```bash
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Start Ollama (if not already running)
```bash
ollama serve
```

### 3. Run the Example
```bash
python main.py
```

**Alternative**: Use the provided run script that checks for virtual environment activation:
```bash
python run.py
```

## What the Example Does

1. **Sets up environment variables** to point to your local Ollama server
2. **Creates an MCP filesystem server** using the `@modelcontextprotocol/server-filesystem` package
3. **Builds an agent** that can use the filesystem server to read files
4. **Runs a task** asking the agent to read README.md and summarize the first 100 words

## Troubleshooting

### Common Issues:

1. **"Connection refused" errors**: Make sure Ollama is running on localhost:11434
2. **"npx command not found"**: Install Node.js
3. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
4. **No model available**: Pull a model with `ollama pull llama2` or similar

### Testing Your Setup:

1. Test Ollama: `curl http://localhost:11434/api/tags`
2. Test Node.js: `npx --version`
3. Test Python packages: `python -c "import agents; print('OK')"`

## Customizing the Example

You can modify the example to:

1. **Use different models**: Change the Ollama model or use other OpenAI-compatible servers
2. **Different tasks**: Modify the task string in `Runner.run_sync()`
3. **Add more MCP servers**: Add additional MCP servers to the agent's configuration
4. **Change filesystem scope**: Modify the MCP server path to access different directories

## Security Note

The filesystem MCP server gives the agent access to read files in the current directory and subdirectories. Make sure you're comfortable with this access level before running the example. 