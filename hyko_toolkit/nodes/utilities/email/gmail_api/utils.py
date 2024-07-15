import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Optional

import httpx
from pydantic import EmailStr


async def send_mail(
    access_token: str,
    to_email: EmailStr,
    subject: str,
    html: str,
    cc_emails: Optional[list[EmailStr]] = None,
    bcc_emails: Optional[list[EmailStr]] = None,
) -> dict[Any, Any]:
    """Send an outgoing email via Gmail API."""
    message = MIMEMultipart()
    message["To"] = to_email
    message["Subject"] = subject

    if cc_emails:
        message["Cc"] = ", ".join(cc_emails)
    if bcc_emails:
        message["Bcc"] = ", ".join(bcc_emails)

    message.attach(MIMEText(html, "html"))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"raw": raw_message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
