from config import Inputs, Outputs, Params, Audio
import fastapi
from transformers import pipeline

app = fastapi.FastAPI()

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", device_map="auto")

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    translated = pipe(inputs.french_text, max_length=len(inputs.french_text * 2))[0]["translation_text"]
    return Outputs(english_translated_text=translated)
