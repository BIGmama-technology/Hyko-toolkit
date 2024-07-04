from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .video_concat.metadata import node as video_concat
from .video_slicer.metadata import node as video_slicer
from .video_subtitle_writer.metadata import node as video_subtitle_writer
from .video_to_audio.metadata import node as video_to_audio

node = NodeGroup(
    name="Video utilities",
    description="perform various video manipulation tasks.",
    icon="video",
    tag=Tag.utilities,
    nodes=[video_slicer, video_subtitle_writer, video_to_audio, video_concat],
)
