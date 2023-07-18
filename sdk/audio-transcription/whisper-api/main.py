from config import Inputs, Params, Outputs
from fastapi import FastAPI, HTTPException, status
import openai
import io

app = FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):

    print(f"key: {params.api_key}")

    await inputs.audio.wait_data()

    if inputs.audio.data is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Received empty audio object",
        )
    
    file = io.BytesIO(inputs.audio.data)
    file.name = inputs.audio.filename

    res = await openai.Audio.atranscribe(
        model="whisper-1",
        file=file,
        api_key=params.api_key,
        prompt=params.prompt,
        language=params.language,
        temperature=params.temperature,
    )

    transcription = res.get("text") # type: ignore

    if transcription is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error occured {res}",
        )
    
    return Outputs(transcribed_text=transcription)


##############################################################################################################

