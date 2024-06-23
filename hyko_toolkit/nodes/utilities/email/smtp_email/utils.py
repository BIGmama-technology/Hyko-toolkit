from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Optional

import aiosmtplib
from pydantic import BaseModel, EmailStr

from hyko_toolkit.exceptions import EmailNotValidError, EmailSendError


class EmailSentSuccessfully(BaseModel):
    success: bool


async def send_smtp_email(
    sender_email: EmailStr,
    recipient_email: EmailStr,
    body_type: str,
    subject: str,
    body: str,
    cc_emails: Optional[list[EmailStr]] = None,
    bcc_emails: Optional[list[EmailStr]] = None,
    attachments: Optional[list[dict[str, Any]]] = None,
) -> EmailSentSuccessfully:
    """Send an email using SMTP."""
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    if cc_emails:
        msg["Cc"] = ", ".join(cc_emails)
    if bcc_emails:
        msg["Bcc"] = ", ".join(bcc_emails)

    if attachments:
        for file in attachments:
            filename = file["name"]
            attachment_content = file["content"]
            part = MIMEApplication(attachment_content)
            part["Content-Disposition"] = f'attachment; filename="{filename}"'
            msg.attach(part)

    msg.attach(MIMEText(body, body_type))

    try:
        smtp = aiosmtplib.SMTP(hostname="mail.big-mama.io", port=465, use_tls=True)
        await smtp.connect()  # type: ignore
        await smtp.login("contact@big-mama.io", "Fqz3!X6rVZyk")

        await smtp.send_message(msg)

        await smtp.quit()
        return EmailSentSuccessfully(success=True)

    except aiosmtplib.SMTPRecipientsRefused as e:
        raise EmailNotValidError from e

    except Exception as e:
        raise EmailSendError from e
