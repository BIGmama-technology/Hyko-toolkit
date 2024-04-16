from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, StartupParams, func

generator = None


@func.on_startup
async def load(startup_params: StartupParams):
    global generator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    generator = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model,
    )

    if device_map.startswith("cuda"):
        generator.to(device_map)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = generator(
        prompt=inputs.prompt,
        num_inference_steps=params.num_inference_steps,
        image=inputs.image,
        negative_prompt=inputs.negative_prompt,
        strength=params.strength,
        guidance_scale=params.guidance_scale,
    )
    return Outputs(generated_image=await Image.from_pil(res.images[0]))  # type: ignore
