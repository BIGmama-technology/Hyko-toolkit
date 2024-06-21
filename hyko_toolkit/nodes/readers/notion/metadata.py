from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .read_database_item.metadata import node as read_database_item

node = NodeGroup(
    name="Notion reader",
    description="perform various notion operations.",
    icon="notion",
    tag=Tag.readers,
    nodes=[read_database_item],
)
