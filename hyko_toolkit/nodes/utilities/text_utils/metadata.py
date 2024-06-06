from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .concat.metadata import node as concat_node
from .count.metadata import node as count_node
from .index_mapping.metadata import node as index_mapping_node
from .join.metadata import node as join_node
from .length.metadata import node as length_node
from .lowercase.metadata import node as lowercase_node
from .padding.metadata import node as padding_node
from .replace.metadata import node as replace_node
from .reverse.metadata import node as reverse_node
from .slice.metadata import node as slice_node
from .split.metadata import node as split_node
from .uppercase.metadata import node as uppercase_node

node = NodeGroup(
    name="Text utilities",
    description="perform various text processing tasks.",
    icon="text",
    tag=Tag.utilities,
    nodes=[
        concat_node,
        count_node,
        index_mapping_node,
        join_node,
        length_node,
        lowercase_node,
        padding_node,
        replace_node,
        reverse_node,
        slice_node,
        split_node,
        uppercase_node,
    ],
)
