from typing import Any

import httpx
from fastapi import HTTPException, status
from hyko_sdk.components.components import Search
from hyko_sdk.models import FieldMetadata, MetaDataBase
from pydantic import BaseModel, TypeAdapter

ModelsAdapter = TypeAdapter(list[dict[str, Any]])


class Response(BaseModel):
    success: bool
    body: str


async def huggingface_models_search(
    metadata: MetaDataBase,
    *_: Any,
) -> MetaDataBase:
    """common huggingface search callback.

    `*args` is used here to allow for access_token and refresh token to be passed by the callback route"""
    search = metadata.params["hugging_face_model"].value
    async with httpx.AsyncClient() as client:
        url = "https://huggingface.co/api/models"
        url += f"?pipeline_tag={metadata.name.replace(' ', '-').lower()}"
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
        metadata_dict = metadata.params["hugging_face_model"].model_dump()
        component = metadata.params["hugging_face_model"].component
        if component:
            metadata_dict["component"] = Search(
                **component.model_dump(exclude={"results"}),
                results=model_ids,
            )
            metadata.add_param(FieldMetadata(**metadata_dict))

        return metadata
