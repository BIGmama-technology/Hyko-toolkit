import io

import openai
from fastapi import HTTPException, status
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    file = io.BytesIO(inputs.audio.get_data())
    file.name = inputs.audio.get_name()

    res = await openai.Audio.atranscribe(
        model="whisper-1",
        file=file,
        api_key=params.api_key,
        prompt=params.prompt,
        language=params.language,
        temperature=params.temperature,
    )

    transcription = res.get("text")  # type: ignore

    if transcription is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error occured {res}",
        )

    return Outputs(transcribed_text=transcription)
