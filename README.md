# AI Lab 🤖

A Python AI client that connects to the OpenRouter API and uses automatic AI model selection.

## Features

- Connects to the OpenRouter API
- Automatically selects an available AI model using `openrouter/auto`
- Supports multi-turn conversations
- Handles API and network errors
- Uses a 30-second request timeout
- Keeps the API key outside the source code
- Provides CLI commands for managing conversations
- Includes automated tests with pytest
- Uses Ruff for code quality checks
- Version controlled with Git and GitHub

## CLI Commands

| Command | Description |
|---|---|
| `/help` | Show available commands |
| `/model` | Show the last model selected by OpenRouter |
| `/clear` | Clear the current conversation |
| `/exit` | Exit the application |

## Project Structure

```text
ai-lab/
├── tests/
│   ├── conftest.py
│   └── test_ai_client.py
├── app.py                 # Command-line application
├── ai_client.py           # OpenRouter API client
├── config.py              # Configuration
├── .env                   # Local API key (not committed)
├── .gitignore
├── requirements.txt       # Python dependencies
└── README.md
Technologies
Python
OpenRouter API
Requests
python-dotenv
pytest
Ruff
Git
GitHub
VS Code
Setup

Clone the repository:

git clone git@github.com:milesmorales-cloud/ai-lab.git

Navigate into the project:

cd ai-lab

Create a Python virtual environment:

python -m venv .venv

Activate it:

source .venv/bin/activate

Install the dependencies:

pip install -r requirements.txt

Create a .env file in the project root and add your OpenRouter API key:

OPENROUTER_API_KEY=your_api_key_here

The .env file is excluded from Git to prevent the API key from being committed.

Running the Application

Start the AI client:

python app.py
Testing

Run the automated tests:

pytest

The project currently includes tests for:

Successful API requests
API errors
Network errors
Code Quality

Run Ruff:

ruff check .

Ruff is used to check the project for Python code-quality issues and organize imports.

Security

The OpenRouter API key is stored in a local .env file and is excluded from Git using .gitignore.

Never commit API keys, passwords, tokens, or other secrets to GitHub.