from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import resend

load_dotenv()

DEFAULT_MODEL = "nebius/Qwen/Qwen3-30B-A3B"
DEFAULT_API_BASE = "https://api.studio.nebius.ai/v1"


def _split_recipients(to: str) -> list[str]:
    recipients = [recipient.strip() for recipient in to.split(",") if recipient.strip()]
    if not recipients:
        raise ValueError("At least one recipient email address is required.")
    return recipients


def send_email(to: str, subject: str, html: str, from_email: str | None = None) -> dict[str, Any]:
    """Send an HTML email through Resend.

    Args:
        to: Recipient email address, or comma-separated recipient email addresses.
        subject: Email subject line.
        html: HTML content for the email body.
        from_email: Optional sender address. Defaults to RESEND_FROM_EMAIL.

    Returns:
        A dictionary containing send status and the Resend API response.
    """
    resend_api_key = os.getenv("RESEND_API_KEY")
    sender = from_email or os.getenv("RESEND_FROM_EMAIL")

    if not resend_api_key:
        return {
            "status": "error",
            "message": "RESEND_API_KEY is not configured.",
        }

    if not sender:
        return {
            "status": "error",
            "message": "RESEND_FROM_EMAIL is not configured and no from_email was provided.",
        }

    if not subject.strip():
        return {
            "status": "error",
            "message": "Email subject is required.",
        }

    if not html.strip():
        return {
            "status": "error",
            "message": "Email HTML content is required.",
        }

    try:
        recipients = _split_recipients(to)
    except ValueError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    resend.api_key = resend_api_key
    params: resend.Emails.SendParams = {
        "from": sender,
        "to": recipients,
        "subject": subject.strip(),
        "html": html.strip(),
    }

    try:
        response = resend.Emails.send(params)
    except Exception as exc:  # Resend raises provider-specific exceptions.
        return {
            "status": "error",
            "message": f"Resend failed to send the email: {exc}",
        }

    return {
        "status": "success",
        "message": "Email sent successfully.",
        "response": response,
    }


def _build_model() -> LiteLlm:
    api_key = os.getenv("NEBIUS_API_KEY")
    api_base = os.getenv("NEBIUS_API_BASE", DEFAULT_API_BASE)
    model = os.getenv("NEBIUS_MODEL", DEFAULT_MODEL)

    model_kwargs: dict[str, Any] = {
        "model": model,
        "api_base": api_base,
    }

    if api_key:
        model_kwargs["api_key"] = api_key

    return LiteLlm(**model_kwargs)


root_agent = LlmAgent(
    model=_build_model(),
    name="email_agent",
    description="A Google ADK starter agent that sends HTML email through Resend.",
    instruction=(
        "You are EmailAgent, a concise assistant for sending email notifications. "
        "When the user asks you to send an email, collect the recipient, subject, "
        "and HTML body if any are missing. Use the send_email tool only after the "
        "message details are clear. Keep email content professional, readable, "
        "and suitable for the user's requested audience."
    ),
    tools=[send_email],
)
