from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .youtube_downloader.metadata import func as youtube_downloader_node
from .youtube_transcript.metadata import func as youtube_transcript_node

node = NodeGroup(
    name="Youtube reader",
    description="perform various YouTube related tasks.",
    icon="youtube",
    tag=Tag.readers,
    nodes=[youtube_downloader_node, youtube_transcript_node],
)
