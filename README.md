# AI Lab 🤖

A Python AI client that connects to the OpenRouter API and uses automatic AI model selection.

## Features

- Connects to OpenRouter
- Automatically selects an available AI model
- Supports multi-turn conversations
- Keeps the API key outside the source code
- Uses a Python virtual environment
- Includes automated tests with pytest
- Uses Ruff for code quality checks
- Version controlled with Git and GitHub

## Project Structure

```text
ai-lab/
├── .venv/                 # Local Python virtual environment
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
## Technologies

- Python
- OpenRouter API
- Requests
- python-dotenv
- pytest
- Ruff
- Git
- GitHub
- VS Code
##Setup

To set up the AI Lab project, clone the repository, navigate into the project directory, and create a Python virtual environment. Activate the virtual environment and install the required dependencies from requirements.txt. Create a local .env file and add your OpenRouter API key as OPENROUTER_API_KEY. The .env file is excluded from Git to protect the API key. Once the setup is complete, run the application using python app.py.
