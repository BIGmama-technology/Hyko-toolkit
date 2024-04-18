from hyko_sdk.io import Audio, Video
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='video_to_audio', task='converters', description='Convert a video type to audio type (takes only the audio data)', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/converters/video_to_audio/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/converters/video_to_audio')

@func.set_input
class Inputs(CoreModel):
    video: Video = Field(..., description='User input video to be converted to audio')

@func.set_output
class Outputs(CoreModel):
    audio: Audio = Field(..., description='converted audio')
