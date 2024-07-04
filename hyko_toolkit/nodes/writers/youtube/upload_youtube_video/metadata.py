import logging

import httpx
from hyko_sdk.components.components import Select, SelectChoice
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel, SupportedProviders
from hyko_sdk.utils import field

node = ToolkitNode(
    name="YouTube Video Uploader",
    cost=0,
    description="Upload a video to YouTube",
    auth=SupportedProviders.YOUTUBE,
    icon="youtube",
)


@node.set_input
class Inputs(CoreModel):
    video: Video = field(description="Input video to upload")
    title: str = field(description="Title of the video")
    description: str = field(description="Description of the video")


@node.set_param
class Params(CoreModel):
    access_token: str = field(description="YouTube API Bearer Token", hidden=True)
    privacy_status: str = field(
        description="Choose the video privacy status",
        component=Select(
            choices=[
                SelectChoice(label="Private", value="private"),
                SelectChoice(label="Public", value="unlisted"),
                SelectChoice(label="Unlisted", value="public"),
            ]
        ),
    )


@node.set_output
class Outputs(CoreModel):
    video_url: str = field(description="URL of the uploaded YouTube video")


async def upload_video(
    client: httpx.AsyncClient,
    access_token: str,
    video_data: bytes,
    title: str,
    description: str,
    privacy: str,
) -> str:
    """Upload a video to YouTube."""
    # Start the resumable upload session
    session_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/*",
        "X-Upload-Content-Length": str(len(video_data)),
    }
    body = {
        "snippet": {
            "title": title,
            "description": description,
        },
        "status": {"privacyStatus": privacy},
    }
    response = await client.post(session_url, headers=headers, json=body)
    response.raise_for_status()
    upload_url = response.headers["Location"]

    # Upload the video data
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.put(upload_url, headers=headers, content=video_data)
    response.raise_for_status()

    video_id = response.json()["id"]
    return f"https://www.youtube.com/watch?v={video_id}"


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    """Uploads a video to YouTube and returns the video URL."""

    async with httpx.AsyncClient() as client:
        try:
            # Get video data
            video_data: bytes = await inputs.video.get_data()

            # Upload video
            video_url = await upload_video(
                client,
                params.access_token,
                video_data,
                inputs.title,
                inputs.description,
                params.privacy_status,
            )

            return Outputs(video_url=video_url)

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise
