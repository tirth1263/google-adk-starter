from email_adk_agent.agent import send_email


def test_send_email_requires_resend_api_key(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    monkeypatch.setenv("RESEND_FROM_EMAIL", "Demo <demo@example.com>")

    result = send_email(
        to="recipient@example.com",
        subject="Hello",
        html="<p>Hello</p>",
    )

    assert result["status"] == "error"
    assert "RESEND_API_KEY" in result["message"]


def test_send_email_sends_with_expected_payload(monkeypatch):
    captured = {}

    def fake_send(params):
        captured.update(params)
        return {"id": "email_123"}

    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("RESEND_FROM_EMAIL", "Demo <demo@example.com>")
    monkeypatch.setattr("resend.Emails.send", fake_send)

    result = send_email(
        to="one@example.com, two@example.com",
        subject="  Hello team  ",
        html="  <p>Welcome</p>  ",
    )

    assert result["status"] == "success"
    assert captured == {
        "from": "Demo <demo@example.com>",
        "to": ["one@example.com", "two@example.com"],
        "subject": "Hello team",
        "html": "<p>Welcome</p>",
    }
    assert result["response"] == {"id": "email_123"}


def test_send_email_rejects_empty_recipients(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("RESEND_FROM_EMAIL", "Demo <demo@example.com>")

    result = send_email(to=" , ", subject="Hello", html="<p>Hello</p>")

    assert result["status"] == "error"
    assert "recipient" in result["message"].lower()
