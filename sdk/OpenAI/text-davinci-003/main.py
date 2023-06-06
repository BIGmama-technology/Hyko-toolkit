import fastapi
from fastapi.responses import JSONResponse
from .config import Inputs, Params, Outputs
import httpx

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url="https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {inputs.api_key}",
            },
            json={
                "model": "text-davinci-003",
                "prompt": inputs.prompt,
                "max_tokens": int(inputs.max_tokens),
                "temperature": inputs.temperature,
                "top_p": int(inputs.top_p),
            }
        )

        if res.is_success:
            try:
                generated_text = res.json()["choices"][0]["text"]
                return Outputs(generated_text=generated_text)
            except:
                return JSONResponse(
                    status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content="Error while decoding OpenAi API response",
                )
            
        return JSONResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"OpenAi API error ({res.status_code}): {res.text}",
        )


##############################################################################################################

