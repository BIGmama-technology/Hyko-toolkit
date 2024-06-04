import os
from enum import Enum

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Image converter",
    task="Image utils",
    category=Category.UTILS,
    cost=0,
    description="Convert an input image to a specified target image type.",
    icon="image",
)


class SupportedTypes(Enum):
    png = Ext.PNG
    jpeg = Ext.JPEG
    bmp = Ext.BMP
    webp = Ext.WEBP


@func.set_input
class Inputs(CoreModel):
    original_image: Image = field(
        description="The original image.",
    )


@func.set_param
class Params(CoreModel):
    target_type: SupportedTypes = field(
        description="The Target Type.",
    )


@func.set_output
class Outputs(CoreModel):
    output: Image = field(
        description="Converted image.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    img = await inputs.original_image.to_pil()
    img.save(f"converted-image.{params.target_type.name}")
    with open(f"converted-image.{params.target_type.name}", "rb") as file:
        val = file.read()
    os.remove(f"converted-image.{params.target_type.name}")
    return Outputs(
        output=await Image(
            obj_ext=params.target_type.value,
        ).init_from_val(
            val=val,
        )
    )
