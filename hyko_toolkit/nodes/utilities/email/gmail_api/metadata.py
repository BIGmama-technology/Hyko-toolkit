import logging

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import EmailStr

from hyko_toolkit.exceptions import EmailSendError
from hyko_toolkit.models import Output
from hyko_toolkit.nodes.utilities.email.gmail_api.utils import send_mail

node = ToolkitNode(
    name="Send Email with Gmail",
    description="Send an email using Gmail API.",
    cost=300,
    auth=SupportedProviders.GMAIL,
    icon="gmail",
)


@node.set_input
class Inputs(CoreModel):
    to_email: EmailStr = field(
        description="Recipient's email address",
    )
    subject: str = field(
        description="Email subject",
    )
    cc_emails: list[EmailStr] = field(
        description="CC email addresses",
    )
    bcc_emails: list[EmailStr] = field(
        description="BCC email addresses",
    )
    html_content: str = field(
        description="HTML content of the email",
        component=TextField(placeholder="Your message...", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    access_token: str = field(description="OAuth access token", hidden=True)


@node.on_call
async def on_call(inputs: Inputs, params: Params):
    """On call handler to perform email sending via Gmail API."""
    to_email = inputs.to_email
    subject = inputs.subject
    html_content = inputs.html_content
    cc_emails = inputs.cc_emails or []
    bcc_emails = inputs.bcc_emails or []
    access_token = params.access_token

    try:
        await send_mail(
            access_token, to_email, subject, html_content, cc_emails, bcc_emails
        )
        return Output(message="Email sent successfully!")
    except httpx.HTTPStatusError as exc:
        logging.warning(exc)
        raise EmailSendError from exc
