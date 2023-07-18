from config import Inputs, Outputs, Params
import fastapi
from transformers import pipeline
from fastapi import HTTPException

app = fastapi.FastAPI()

pipe = None

@app.post("/load", response_model=None)
def load():
    global pipe
    if pipe is not None:
        print("Model already loaded")
        return
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", device_map="auto")

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if pipe is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    translated = pipe(inputs.french_text, max_length=len(inputs.french_text) * 2)[0]["translation_text"]
    return Outputs(english_translated_text=translated)
