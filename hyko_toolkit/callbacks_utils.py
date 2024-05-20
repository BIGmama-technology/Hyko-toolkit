from typing import Any

import httpx
from fastapi import HTTPException, status
from hyko_sdk.components.components import Search
from hyko_sdk.models import FieldMetadata, ModelMetaData
from pydantic import TypeAdapter

ModelsAdapter = TypeAdapter(list[dict[str, Any]])


async def huggingface_models_search(
    metadata: ModelMetaData,
    *args: Any,
) -> ModelMetaData:
    """common huggingface search callback.

    `*args` is used here to allow for access_token and refresh token to be passed by the callback route"""
    search = metadata.startup_params["hugging_face_model"].value
    async with httpx.AsyncClient() as client:
        url = "https://huggingface.co/api/models"
        url += f"?pipeline_tag={metadata.name}"
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
        metadata_dict = metadata.startup_params["hugging_face_model"].model_dump()
        metadata_dict["component"] = Search(results=model_ids)
        metadata.add_startup_param(FieldMetadata(**metadata_dict))

        return metadata
