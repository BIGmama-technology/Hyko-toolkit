from urllib.parse import parse_qs, urlparse

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from youtube_transcript_api import YouTubeTranscriptApi


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Retrieve the transcript of a YouTube video.

    Args:
    video_id (str): The unique identifier of the YouTube video.

    Returns:
    str: The concatenated transcript text of the video.
         If the video has no transcript available, returns a message indicating so.
    """
    try:
        video_id = parse_qs(urlparse(inputs.video_url).query)["v"][0]
        transcript_result = YouTubeTranscriptApi.get_transcript(
            video_id, languages=[params.language]
        )
        text_result = [segment["text"] for segment in transcript_result]
        video_transcript = " ".join(text_result)
        return Outputs(result=video_transcript)
    except Exception as e:
        language = params.language.name.capitalize()
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving transcript: This video has no {language} transcript available.",
        ) from e
