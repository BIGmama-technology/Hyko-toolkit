from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .append_text.metadata import node as append_text_node
from .create_doc.metadata import node as create_doc_node

node = NodeGroup(
    name="Docs writer",
    description="Perform various docs operations.",
    icon="docs",
    tag=Tag.writers,
    nodes=[append_text_node, create_doc_node],
)
