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
        transcript_result = YouTubeTranscriptApi.get_transcript(
            inputs.video_id, languages=[params.language]
        )
        text_result = [segment["text"] for segment in transcript_result]
        video_transcript = " ".join(text_result)
        return Outputs(result=video_transcript)
    except:  # noqa: E722
        return Outputs(result="This video has no transcript available.")
