# Parity AI

Parity AI is a small stack that connects a LangGraph ReAct agent to Slack and Gmail through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io). A FastAPI service exposes the agent, and a Streamlit app provides a simple UI for natural-language queries across both sources.

**Repository:** [https://github.com/Aditii2112/Parity_AI](https://github.com/Aditii2112/Parity_AI)

## Why "Parity"?

*Parity* refers to the state of being equal. The agent is meant to help keep **Slack** and **Gmail** at parity: a single place to reason across both so email and chat are not stuck in separate silos.

## What it does

- **Backend** (`main.py`, `backend_core.py`): On startup, spawns MCP servers for Slack and Gmail (via `npx`), loads their tools into a single agent backed by Google Gemini, and serves HTTP endpoints.
- **Frontend** (`frontend.py`): Streamlit client that posts user questions to the API and displays the agent reply.
- **OAuth helper** (`get_gmail_token.py`): One-off script to complete the Google OAuth flow locally and print values you can place in your environment for the Gmail MCP server.

## Prerequisites

- Python 3.11 or newer (3.14 may show third-party warnings; a 3.11 or 3.12 venv is recommended for fewer compatibility surprises).
- Node.js and npm (for `npx` to run MCP server packages).
- A [Google AI Studio](https://aistudio.google.com/) or Google Cloud API key for Gemini (`GOOGLE_API_KEY`).
- A Slack app with a bot token and workspace (team) ID for the official Slack MCP server.
- A Google Cloud OAuth **Desktop** client and Gmail API enabled, plus a refresh token for the Google Workspace MCP package used in code (`mcp-server-google-workspace`).

## Security

Do **not** commit real secrets. This repository expects:

- `.env` for API keys and tokens (gitignored).
- `credentials.json` only on your machine for the OAuth helper (gitignored).

Copy `.env.example` to `.env` and fill in values locally. Never push `.env`, `credentials.json`, or token files.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Aditii2112/Parity_AI.git
   cd Parity_AI
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy environment template and edit `.env`:

   ```bash
   cp .env.example .env
   ```

4. For Gmail OAuth, download your OAuth client JSON from Google Cloud Console as `credentials.json` in the project root (this file is gitignored). Then run:

   ```bash
   python get_gmail_token.py
   ```

   Add the printed `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REFRESH_TOKEN` to `.env`.

## Running

1. Start the API (from the project root, with the venv active):

   ```bash
   python main.py
   ```

   Default bind: `http://0.0.0.0:8000`.

2. In another terminal, start the UI:

   ```bash
   streamlit run frontend.py
   ```

3. Open the Streamlit URL shown in the terminal. Submit a query; the app sends it to `POST http://localhost:8000/ask` with JSON `{"text": "<your question>"}`.

### API

- `GET /` — Health-style JSON with status and version.
- `POST /ask` — Body: `{"text": "..."}`. Response: `{"answer": "..."}`.

## Project layout

| File | Role |
|------|------|
| `main.py` | FastAPI app and lifespan hook to initialize the MCP-backed agent |
| `backend_core.py` | MCP client configuration, model, and agent query logic |
| `frontend.py` | Streamlit UI |
| `get_gmail_token.py` | Local OAuth flow for Gmail read scope |

## Future expansion

Planned directions include wiring the same agent pattern to **Jira** (issues, sprints, and project context) and **GitHub** (repositories, pull requests, and development activity), so Parity can eventually align engineering and communication sources alongside Slack and Gmail.

## License

Add a license file if you intend to open-source under specific terms; none is included by default.
