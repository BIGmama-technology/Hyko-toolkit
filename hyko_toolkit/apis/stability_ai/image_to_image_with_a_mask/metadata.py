import base64
from enum import Enum

import httpx
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, Ext, Method
from pydantic import Field

from hyko_toolkit.apis.api_registry import ToolkitAPI
from hyko_toolkit.exceptions import APICallError

func = ToolkitAPI(
    name="image_to_image_with_a_mask",
    task="stability_ai",
    description="Selectively modify portions of an image using a mask Using Stability.ai API .",
)


class ArtStyle(Enum):
    THREE_D_MODEL = "3d-model"
    ANALOG_FILM = "analog-film"
    ANIME = "anime"
    CINEMATIC = "cinematic"
    COMIC_BOOK = "comic-book"
    DIGITAL_ART = "digital-art"
    ENHANCE = "enhance"
    FANTASY_ART = "fantasy-art"
    ISOMETRIC = "isometric"
    LINE_ART = "line-art"
    LOW_POLY = "low-poly"
    MODELING_COMPOUND = "modeling-compound"
    NEON_PUNK = "neon-punk"
    ORIGAMI = "origami"
    PHOTOGRAPHIC = "photographic"
    PIXEL_ART = "pixel-art"
    TILE_TEXTURE = "tile-texture"


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="What you wish to see in the output image.")
    init_image: Image = Field(
        ...,
        description="Image used to initialize the diffusion process, in lieu of random noise.",
    )
    mask_image: Image = Field(
        ...,
        description="Image used to mask the diffusion process.",
    )


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    image_strength: float = Field(
        default=0.35,
        description="How much influence the init_image has on the diffusion process.",
    )
    style_preset: ArtStyle = Field(
        default=ArtStyle.CINEMATIC,
        description="Style preset to use for the image generation (default : cinematic).",
    )
    steps: int = Field(
        default=30,
        description="Number of steps to run the diffusion process for (max : 50)",
    )


@func.set_output
class Outputs(CoreModel):
    result: Image = Field(..., description="Generated Image.")


class Artifact(CoreModel):
    base64: str


class Response(CoreModel):
    artifacts: list[Artifact]


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image/masking",
            headers={"authorization": f"Bearer {params.api_key}", "accept": "image/*"},
            files={
                "image": inputs.init_image.get_data(),
                "mask_image": inputs.mask_image.get_data(),
            },
            data={
                "image_strength": params.image_strength,
                "text_prompts[0][text]": inputs.prompt,
                "style_preset": params.style_preset.value,
                "steps": params.steps,
                "clip_guidance_preset": "SIMPLE",
                "mask_source": "MASK_IMAGE_WHITE",
                "cfg_scale": 7,
                "samples": 1,
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Response(**res.json())
        decoded_images = [
            base64.b64decode(image.base64) for image in response.artifacts
        ]
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(result=Image(val=decoded_images[0], obj_ext=Ext.PNG))
