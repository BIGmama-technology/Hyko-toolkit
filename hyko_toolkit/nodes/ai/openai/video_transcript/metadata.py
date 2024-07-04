import asyncio
import tempfile
from datetime import timedelta
from typing import Any

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from pydub import AudioSegment

node = ToolkitNode(
    name="Openai video transcript",
    description="Use openai api to extract transcription from a video.",
    cost=6000,
    icon="openai",
)


@node.set_input
class Inputs(CoreModel):
    audio: Audio = field(description="Audio to convert to text.")


@node.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )


@node.set_output
class Outputs(CoreModel):
    text: str = field(description="The extracted transcript.")


class Response(CoreModel):
    text: str


async def format_timestamp(seconds: int):
    td = timedelta(seconds=seconds)
    milliseconds = int((td.microseconds / 1000) % 1000)
    return f"{td.seconds // 3600:02d}:{(td.seconds // 60) % 60:02d}:{td.seconds % 60:02d},{milliseconds:03d}"


def split_audio(file_path: str, chunk_length: int = 25000) -> list[AudioSegment]:
    audio = AudioSegment.from_file(file_path)  # type: ignore
    chunks = [audio[i : i + chunk_length] for i in range(0, len(audio), chunk_length)]  # type: ignore
    return chunks  # type: ignore


def save_chunks(chunks: list[AudioSegment], base_name: str) -> list[str]:
    filenames: list[str] = []
    for i, chunk in enumerate(chunks):
        filename = f"{base_name}_chunk{i}.wav"
        chunk.export(filename, format="wav")  # type: ignore
        filenames.append(filename)
    return filenames


async def transcribe_chunk(
    client: httpx.AsyncClient, file_path: str, api_key: str
) -> dict[str, Any]:
    with open(file_path, "rb") as f:
        res = await client.post(
            url="https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            files={
                "file": (file_path, f, None),
            },
            data={
                "model": "whisper-1",
                "response_format": "verbose_json",
            },
        )

        if res.is_success:
            return res.json()
        else:
            return {}


def combine_transcripts(transcripts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    combined: list[dict[Any, Any]] = []
    timestamp_offset = 0
    for transcript in transcripts:
        for segment in transcript["segments"]:
            segment["start"] += timestamp_offset
            segment["end"] += timestamp_offset
            combined.append(segment)
        timestamp_offset += transcript["segments"][-1]["end"] - timestamp_offset
    return combined


@node.on_call
async def call(inputs: Inputs, params: Params):
    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    temp_input_file.write(await inputs.audio.get_data())
    temp_input_file.flush()

    chunks = split_audio(temp_input_file.name)
    chunk_files = save_chunks(chunks, "temp_audio_chunk")

    transcripts: list[dict[Any, Any]] = []
    # try:
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [
            transcribe_chunk(
                client=client, file_path=chunk_file, api_key=params.api_key
            )
            for chunk_file in chunk_files
        ]
        transcripts = await asyncio.gather(*tasks)

    combined_transcript = combine_transcripts(transcripts)

    transcript_with_timestamps: str = ""

    counter = 1
    for segment in combined_transcript:
        start_time = await format_timestamp(segment["start"])
        end_time = await format_timestamp(segment["end"])
        text = segment["text"]
        transcript_with_timestamps += f"""
{counter}
{start_time} --> {end_time}
{text}.
"""
        counter += 1

    return Outputs(text=transcript_with_timestamps)
    # except Exception as e:
    #     raise VideoSlicingError from e
