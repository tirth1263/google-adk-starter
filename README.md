# Google ADK Starter Agent

A focused starter project for building an email-enabled AI agent with Google's Agent Development Kit (ADK), Nebius AI Studio, and Resend.

This repository is designed for developers who want a practical first ADK project: one agent, one useful external API integration, and a clear path from local testing to production-ready notification workflows.

**Live website:** [https://tirth1263.github.io/google-adk-starter/](https://tirth1263.github.io/google-adk-starter/)

## Why this project is useful

Most starter agents stop at "hello world." This one demonstrates a real integration pattern:

- Use Google ADK to define a tool-using agent.
- Use Nebius AI Studio as the LLM inference provider through ADK's LiteLLM wrapper.
- Use Resend to send structured HTML emails.
- Keep configuration in environment variables.
- Return clear tool results that are easy to debug and extend.

The result is a small but realistic foundation for notification bots, onboarding assistants, operations alerts, lead follow-up tools, and internal workflow agents.

## What the agent can do

The `email_adk_agent` package exposes a single ADK `root_agent` named `email_agent`.

When a user asks the agent to send an email, the agent can call the `send_email` tool with:

- recipient email address or comma-separated recipients
- subject line
- HTML email body
- optional sender override

The tool validates required inputs, reads the Resend API key from the environment, sends the message through Resend, and returns the provider response.

## Project structure

```text
google-adk-starter/
├── email_adk_agent/
│   ├── __init__.py
│   └── agent.py
├── tests/
│   └── test_email_tool.py
├── website/
│   ├── assets/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Required API keys

You need two services:

1. **Nebius AI Studio** for model inference  
   Get started at [Nebius AI Studio](https://dub.sh/AIStudio).

2. **Resend** for email delivery  
   Get started at [Resend](https://resend.com/).

For production email delivery, verify your sending domain in Resend and use a sender address from that domain.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/tirth1263/google-adk-starter.git
cd google-adk-starter
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv, if installed
uv sync
```

### 4. Verify ADK installation

```bash
adk --version
```

## Environment setup

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` with your keys:

```env
NEBIUS_API_KEY="your_nebius_api_key_here"
NEBIUS_API_BASE="https://api.studio.nebius.ai/v1"
NEBIUS_MODEL="nebius/Qwen/Qwen3-30B-A3B"

RESEND_API_KEY="your_resend_api_key_here"
RESEND_FROM_EMAIL="Your Name <your@verified-domain.com>"
```

> Note: Nebius API examples may also show `https://api.studio.nebius.com/v1/`. Use the base URL shown in your Nebius dashboard if it differs.

## Usage

Run the agent with the ADK CLI:

```bash
# Terminal chat
adk run email_adk_agent

# ADK development UI
adk web
```

When using `adk web`, run the command from the repository root so ADK can discover the `email_adk_agent` package.

Example prompt:

```text
Send a short welcome email to alex@example.com with the subject "Welcome to the demo" and a friendly HTML message.
```

The agent will decide when to call the `send_email` tool and will return the Resend response after sending.

## Customizing the email tool

To customize the delivery behavior, edit `send_email` in `email_adk_agent/agent.py`.

Example payload sent to Resend:

```python
params = {
    "from": "Your Name <your@verified-domain.com>",
    "to": ["recipient@example.com"],
    "subject": "Custom Email Subject",
    "html": "<p>Your custom email content here</p>",
}
```

You can extend the tool with:

- `reply_to`
- tags or metadata
- template selection
- audit logging
- idempotency keys
- database-backed delivery history

## Running tests

```bash
pytest
```

The tests mock the Resend SDK so you can validate tool behavior without sending real email.

## Deployment ideas

This repository includes a static website in `website/` for showcasing the project publicly. A GitHub Pages workflow is included at `.github/workflows/deploy-website.yml`, so pushes to `main` can publish the site automatically.

For the agent itself, typical deployment options include:

- running ADK behind an API service
- deploying to Google Cloud Run
- deploying to Vertex AI Agent Engine
- connecting the tool to an internal workflow system

Keep API keys in your deployment platform's secret manager, never in source control.

## Security notes

- Do not commit `.env`.
- Use a verified Resend domain for production.
- Restrict API keys where your provider supports it.
- Validate recipients before using the tool in automated workflows.
- Consider approval steps before sending external emails from autonomous agents.

## Tech stack

- Google Agent Development Kit (ADK)
- LiteLLM
- Nebius AI Studio
- Resend Python SDK
- Python dotenv
- Pytest

## License

MIT License. Use it, modify it, and build something useful.
