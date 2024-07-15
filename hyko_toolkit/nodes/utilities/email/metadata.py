from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .gmail_api.metadata import node as gmail_api_node
from .smtp_email.metadata import node as smtp_email_node

node = NodeGroup(
    name="Email Sending",
    description="Perform various email sending operations.",
    icon="email",
    tag=Tag.utilities,
    nodes=[smtp_email_node, gmail_api_node],
)
