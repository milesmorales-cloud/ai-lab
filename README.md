# AI Lab 🤖

A Python terminal AI client. It primarily uses the **Gemini** API and
automatically **falls back to OpenRouter** when Gemini is unavailable, with
automatic model selection so you can start chatting right away.

## Features

- Primary provider: **Gemini** (Google Generative Language API)
- Automatic fallback to **OpenRouter** when Gemini fails or is not configured
- Automatic selection of an available AI model
- Interactive terminal UI with a clean `›` prompt, loading indicator, colored
  messages, separators, and wrapped long responses
- Multi-turn conversations
- Conversation history with titles, **selection**, **resume**, and **deletion**
- Handles API and network errors gracefully
- Uses a 30-second request timeout
- Keeps API keys out of source code
- Automated tests with pytest
- Code quality checks with Ruff
- Version controlled with Git and GitHub

## CLI Commands

Commands are secondary — just start typing to chat.

| Command | Description |
| --- | --- |
| `/help` | Show available commands |
| `/model` | Show the last model used |
| `/history` | Show numbered list of saved conversation titles |
| `/clear` | Clear the current conversation (saved history is kept) |
| `/select` | Resume a conversation by number |
| `D<n>` | Delete conversation number `n` (with confirmation) |
| `/exit` | Exit the application |

## Project Structure

```text
ai-lab/
├── tests/
│   ├── conftest.py
│   ├── test_ai_client.py
│   ├── test_conversation.py
│   └── test_app.py
├── app.py                  # Command-line application and command dispatch
├── ui.py                   # Terminal UI: styling, spinner, layout helpers
├── provider_client.py      # Provider abstraction: Gemini with OpenRouter fallback
├── gemini_client.py        # Gemini API client
├── ai_client.py            # OpenRouter API client
├── conversation.py         # Conversation storage and title generation
├── config.py               # Configuration and API keys
├── .env                    # Local API keys (not committed)
├── .gitignore
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup

Clone the repository:

```bash
git clone git@github.com:milesmorales-cloud/ai-lab.git
cd ai-lab
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with your API keys:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

The `.env` file is excluded from Git to prevent secrets from being committed.

## Running the Application

Start the AI client:

```bash
python app.py
```

## Testing

Run the automated tests:

```bash
pytest
```

Tests cover successful API requests, API errors, network errors, conversation
storage, and CLI command behavior.

## Code Quality

Run Ruff to check the project for Python code-quality issues and organize
imports:

```bash
ruff check .
```

## Security

API keys are stored in a local `.env` file and excluded from Git via
`.gitignore`. Never commit API keys, passwords, tokens, or other secrets.
