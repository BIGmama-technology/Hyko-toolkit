from transformers import pipeline
from fastapi.exceptions import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction

func = SDKFunction(
    description="OPUS French to English Translation specialized model",
    requires_gpu=False,
)

class Inputs(CoreModel):
    french_text: str = Field(..., description="French text")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    english_translated_text: str = Field(..., description="English translated text")


pipe = None

@func.on_startup
async def load():
    global pipe
    if pipe is not None:
        print("Model already loaded")
                  
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", device_map="auto")



@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
     
    if pipe is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    translated = pipe(inputs.french_text, max_length=len(inputs.french_text) * 2)[0]["translation_text"] # type: ignore
    return Outputs(english_translated_text=str(translated))

