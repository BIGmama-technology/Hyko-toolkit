from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .upload_youtube_video.metadata import node as upload_video_node

node = NodeGroup(
    name="Twitter Writer",
    description="Preform sevral actions with twitter account",
    icon="x",
    tag=Tag.writers,
    nodes=[upload_video_node],
)
