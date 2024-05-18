from typing import Any

import httpx
from fastapi import HTTPException, status
from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, FieldMetadata, MetaData
from hyko_sdk.utils import field
from pydantic import Field, TypeAdapter

from hyko_toolkit.registry import ToolkitModel

ModelsAdapter = TypeAdapter(list[dict[str, Any]])

func = ToolkitModel(
    name="depth_estimation",
    task="computer_vision",
    description="HuggingFace depth estimation",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/depth_estimation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


@func.set_output
class Outputs(CoreModel):
    depth_map: Image = Field(..., description="Output depth map")


@func.set_param
class Param(CoreModel):
    search: str = field(
        description="The search query",
        component=Search(),
    )


@func.callback(triggers=["search"], id="depth_estimation_search")
async def add_search_results(
    metadata: MetaData, access_token: str, refresh_token: str
) -> MetaData:
    search = metadata.params["search"].value

    async with httpx.AsyncClient() as client:
        url = "https://huggingface.co/api/models"
        url += "?pipeline_tag=depth-estimation"
        url += f"&search={search}"
        url += "&sort=downloads"
        url += "&direction=-1"
        url += "&limit=10"
        url += "&filter=endpoints_compatible"

        res = await client.get(url=url)

        if not res.is_success:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=res.text,
            )

        results = ModelsAdapter.validate_json(res.text)
        model_ids = [item["modelId"] for item in results]
        metadata_dict = metadata.params["search"].model_dump()
        metadata_dict["component"] = Search(placeholder=str(search), results=model_ids)
        metadata.add_param(FieldMetadata(**metadata_dict))

        return metadata
