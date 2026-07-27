# AI Agent

A minimal, from-scratch AI coding agent written in Python. It talks to an LLM (via [OpenRouter](https://openrouter.ai/)) and lets the model autonomously explore, read, execute, and modify code inside a sandboxed working directory by calling a small set of tools.

The project ships with an example **calculator** app so you can immediately see the agent read files, run scripts, fix bugs, and write patches on a real (tiny) codebase.

---

## Features

- **Tool-using LLM loop** &mdash; the model plans, calls a function, receives the result, and keeps iterating until it can answer (up to 20 turns).
- **Four built-in tools** the agent can invoke:
  - `get_files_info` &mdash; list files and directories with sizes.
  - `get_file_content` &mdash; read a file (capped at `MAX_CHARS = 10,000` characters, truncated safely).
  - `run_python_file` &mdash; execute a Python file with optional arguments and capture stdout/stderr.
  - `write_file` &mdash; create or overwrite a file.
- **Path-traversal sandbox** &mdash; every tool resolves paths with `os.path.abspath` + `os.path.commonpath` and refuses any operation that escapes the working directory. The working directory is injected server-side, so the model never sets it.
- **Verbose mode** (`--verbose`) that prints token usage, each function call with its arguments, and each tool result.
- **Bring-your-own model** &mdash; any OpenRouter-compatible chat model works; just change the model string in `main.py`.

---

## Project Structure

```
aiagent/
├── main.py                 # Entry point: CLI + agent loop
├── call_function.py        # Dispatches tool calls, injects working directory
├── prompts.py              # System prompt shown to the model
├── config.py               # MAX_CHARS cap for file reads
├── functions/              # The tools exposed to the LLM
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/             # Sandboxed target app the agent operates on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── test_get_files_info.py  # Manual sanity checks for each tool
├── test_get_file_content.py
├── test_run_python_file.py
├── test_write_file.py
├── pyproject.toml
└── uv.lock
```

---

## Requirements

- Python **3.13+**
- An [OpenRouter](https://openrouter.ai/) API key
- [`uv`](https://github.com/astral-sh/uv) (recommended) or plain `pip`

Dependencies:

- `openai==2.44.0`
- `python-dotenv==1.1.0`

---

## Installation

```bash
# clone
git clone https://github.com/tgybyrl/aiagent.git
cd aiagent

# install dependencies (uv)
uv sync

# ...or with pip
python -m venv .venv
source .venv/bin/activate
pip install "openai==2.44.0" "python-dotenv==1.1.0"
```

Create a `.env` file at the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

## Usage

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see token counts and every tool call the agent makes:

```bash
uv run main.py "your prompt here" --verbose
```

### Examples

Ask the agent about the sandboxed project:

```bash
uv run main.py "what files are in the project?"
```

Have it read code:

```bash
uv run main.py "explain how pkg/calculator.py evaluates an expression"
```

Have it run the app:

```bash
uv run main.py "run main.py with the expression 3 + 5 and tell me the output"
```

Have it modify code:

```bash
uv run main.py "there is a bug in the operator precedence, find it and fix it"
```

---

## How It Works

`main.py` builds a message list starting with the system prompt, then enters a bounded loop (max 20 iterations):

1. Send the conversation to the model together with the tool schemas from `available_functions`.
2. If the response contains `tool_calls`, hand each one to `call_function` in `call_function.py`.
3. `call_function` decodes the arguments, injects the sandboxed `working_directory` (`./calculator` by default), invokes the matching Python function, and returns a `role: "tool"` message.
4. The tool result is appended to the conversation and the loop continues.
5. When the model finally responds without tool calls, that text is printed and the loop exits.

The system prompt (`prompts.py`) tells the model it can list files, read files, run Python files, and write files, and that all paths are relative to a working directory that is injected automatically.

---

## Security Notes

- The working directory is set in `call_function.py` (currently `./calculator`) and **is not exposed to the model**. This is what keeps the agent from touching arbitrary parts of your filesystem.
- Every tool validates that the resolved absolute path stays under the working directory using `os.path.commonpath`.
- `run_python_file` runs subprocesses with a **30-second timeout** and only allows `.py` files inside the sandbox.
- `get_file_content` truncates output at `MAX_CHARS` (10,000) to prevent runaway context usage.

Even with these guards, remember that you are letting an LLM execute code on your machine. Only point the agent at directories you are comfortable letting it modify, and review changes it makes.

---

## Configuration

- **Change the sandbox directory** &mdash; edit the line `function_args["working_directory"] = "./calculator"` in `call_function.py`.
- **Change the model** &mdash; edit the `model=` argument in `main.py` (`client.chat.completions.create(...)`).
- **Change the file-read cap** &mdash; edit `MAX_CHARS` in `config.py`.
- **Change the iteration limit** &mdash; edit the `range(20)` in `main.py`.

---

## Manual Tests

Each tool has a small standalone script that exercises it against the `calculator/` sandbox:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py
```

These are handy for verifying the sandbox rejects out-of-bounds paths.

---

## Roadmap Ideas

- Interactive/REPL mode instead of one-shot prompts
- Persistent conversation history across runs
- More tools (delete file, move file, shell command, git operations)
- Configurable working directory via CLI flag
- Streaming responses

---

## Acknowledgments

Built while working through the ["Build an AI Agent" course on boot.dev](https://www.boot.dev/). The overall structure of the project (tool loop, sandboxed working directory, calculator target app) follows the course; the implementation is my own.

---

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and redistribute this project as long as the copyright notice is preserved.
