from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .youtube_downloader.metadata import func as youtube_downloader_node
from .youtube_transcript.metadata import func as youtube_transcript_node

node = ToolkitNode(
    name="youtube_utils",
    description="perform various YouTube related tasks.",
    icon="youtube",
    tag=Tag.readers,
)


class YouTubeUtils(str, Enum):
    youtube_downloader = "youtube_downloader"
    youtube_transcript = "youtube_transcript"


@node.set_param
class Params(CoreModel):
    youtube_util: YouTubeUtils = field(
        description="Type of the YouTube utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="youtube_util", id="change_youtube_util")
async def change_youtube_util_type(metadata: MetaDataBase, *_: Any):
    youtube_util = metadata.params["youtube_util"].value
    metadata.params = {}
    match youtube_util:
        case YouTubeUtils.youtube_downloader.value:
            return youtube_downloader_node.get_metadata()
        case YouTubeUtils.youtube_transcript.value:
            return youtube_transcript_node.get_metadata()
        case _:
            return metadata
