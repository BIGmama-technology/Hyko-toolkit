import json
from typing import AsyncIterator, Callable
from fastapi import HTTPException, status
import httpx
from .metadata import MetaData, CoreModel
import tqdm

async def download_file(url: str) -> bytearray:
    async with httpx.AsyncClient(verify=False, http2=True) as client:

        # Get file size
        head_res = await client.head(url=url)
        if not head_res.is_success:
            if head_res.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Object not found, url: '{url}'",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Could not read HEAD Object info, status: {head_res.status_code}, res: {head_res.text}",
                )
        
        file_size = int(head_res.headers["Content-Length"])

        async with client.stream("GET", url) as response:
            with tqdm.tqdm(total=file_size, unit_scale=True, unit_divisor=1024, unit="B", desc=f"Downloading {url}") as progress:
                data = bytearray()
                async for chunk in response.aiter_bytes():
                    data += chunk
                    progress.update(len(chunk))
                return data

async def bytearray_aiter(data: bytearray, update_progress: Callable[[float | None], bool | None]) -> AsyncIterator[bytearray]:
    step_size = int(len(data) / 100)
    if not step_size: step_size = 1
    for start in range(0, len(data), step_size):
        end = start + step_size
        if end > len(data):
            end = len(data)
        yield data[start:end]
        update_progress(end-start)

async def upload_file(url: str, data: bytearray) -> None:
    async with httpx.AsyncClient(verify=False, http2=True) as client:
        file_size = len(data)
        with tqdm.tqdm(total=file_size, unit_scale=True, unit_divisor=1024, unit="B", desc=f"Uploading {url}") as progress:
            res = await client.put(
                url=url,
                headers={"Content-Length": str(file_size)},
                content=bytearray_aiter(data=data, update_progress=progress.update),
            )
            if not res.is_success:
                raise Exception(f"Error while uploading, {res.text}")

def metadata_to_docker_label(metadata: MetaData) -> str:
    return metadata.model_dump_json(exclude_unset=True, exclude_none=True).replace('"', "'")

    
def docker_label_to_metadata(label: str) -> MetaData:
    return MetaData(**json.loads(label.replace("'", '"')))


def model_to_friendly_property_types(pydantic_model: CoreModel):
    out: dict[str, str] = {}
    for field_name, field in pydantic_model.model_fields.items():
        annotation = str(field.annotation).lower()
        if "<class" in annotation:
            annotation = annotation[8:-2]

        annotation = annotation.replace("hyko_sdk.io.", "")
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace('str', 'string')
        annotation = annotation.replace('int', 'integer')
        annotation = annotation.replace('float', 'number')
        
        out[field_name] = annotation
    return out