from hyko_sdk.components.components import (
    Select,
    SelectChoice,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from pydantic import EmailStr

from .utils import send_smtp_email

node = ToolkitNode(
    name="Send SMTP Email",
    description="Send an email using SMTP protocol.",
    cost=300,
    icon="gmail",
)


@node.set_input
class Inputs(CoreModel):
    sender_email: EmailStr = field(
        description="Sender's email address",
    )
    recipient_email: EmailStr = field(
        description="Recipient's email address",
    )
    subject: str = field(
        description="Email subject",
    )
    cc_emails: list[EmailStr] = field(
        description="List of cc emails",
    )
    bcc_emails: list[EmailStr] = field(
        description="List of bcc emails",
    )
    message: str = field(
        description="Email message",
    )


@node.set_param
class Params(CoreModel):
    body_type: str = field(
        description="Body type",
        component=Select(
            choices=[
                SelectChoice(label="HTML", value="html"),
                SelectChoice(label="Text", value="plain"),
            ]
        ),
    )


@node.on_call
async def send_email(inputs: Inputs, params: Params):
    return await send_smtp_email(
        sender_email=inputs.sender_email,
        recipient_email=inputs.recipient_email,
        cc_emails=inputs.cc_emails,
        bcc_emails=inputs.bcc_emails,
        subject=inputs.subject,
        body=inputs.message,
        body_type=params.body_type,
    )
