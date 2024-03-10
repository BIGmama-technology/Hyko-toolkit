"""
You can deploy this api by running me.
"""
import os

from dotenv import load_dotenv

from hyko_sdk.definitions import ToolkitAPI
from hyko_sdk.models import CoreModel, Method

load_dotenv()

USERNAME, PASSWORD = os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
assert USERNAME and PASSWORD, "no username and password found in .env"

func = ToolkitAPI(
    name="text_completion",
    task="openai",
    description="Use chatgpt openai api for text completion.",
)


@func.set_input
class Inputs(CoreModel):
    prompt: str


@func.set_param
class Params(CoreModel):
    system_prompt: str
    api_key: str


@func.set_output
class Outputs(CoreModel):
    pass


func.on_call(
    method=Method.post,
    url="https://api.openai.com/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Params.api_key}",
    },
    body={
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": Params.system_prompt},
            {"role": "user", "content": Inputs.prompt},
        ],
    },
)

func.deploy(host="traefik.me", username=USERNAME, password=PASSWORD)
