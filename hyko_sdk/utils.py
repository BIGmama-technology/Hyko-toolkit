import base64
import json
from typing import AsyncIterator, Callable
from fastapi import HTTPException, status
import httpx
from .metadata import HykoJsonSchemaExt, IOPortType, MetaData, CoreModel, MetaDataBase
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
    return base64.b64encode(metadata.model_dump_json(exclude_unset=True, exclude_none=True).encode()).decode()

    
def docker_label_to_metadata(label: str) -> MetaData:
    return MetaData(**json.loads(base64.b64decode(label.encode()).decode()))


def model_to_friendly_property_types(pydantic_model: CoreModel):
    out: dict[str, str] = {}
    for field_name, field in pydantic_model.model_fields.items():
        annotation = str(field.annotation).lower()
        if "enum" in annotation:
            try:
                out[field_name] = f"enum[{str(pydantic_model.model_json_schema()['$defs'][str(field.annotation)[7:-2]]['type'])}]"
                if "numeric" in out[field_name]:
                    out[field_name] = out[field_name].replace("numeric", "number")
            except KeyError:
                raise RuntimeError(f'Could not find {str(pydantic_model.model_json_schema()["$defs"][str(field.annotation)[7:-2]])} the enums defined in the json schema. Usually happens when you use class(Video, Enum) or similar type')
            continue
        if "<class" in annotation:
            annotation = annotation[8:-2]
        annotation = annotation.replace("hyko_sdk.io.", "")
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace('str', 'string')
        annotation = annotation.replace('int', 'integer')
        annotation = annotation.replace('float', 'number')
        
        out[field_name] = annotation
    return out

def extract_metadata(
    Inputs: CoreModel,
    Params: CoreModel,
    Outputs: CoreModel,
    description: str,
    requires_gpu: bool,
):
    inputs_json_schema = Inputs.model_json_schema()
    if inputs_json_schema.get("$defs"):
        for k,v in inputs_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                inputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER

    params_json_schema = Params.model_json_schema()
    if params_json_schema.get("$defs"):
        for k,v in params_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                params_json_schema["$defs"][k]["type"] = IOPortType.NUMBER
    
    outputs_json_schema = Outputs.model_json_schema()
    if outputs_json_schema.get("$defs"):
        for k,v in outputs_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                outputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER
                            
    __meta_data__ = MetaDataBase(
        description=description,
        inputs=HykoJsonSchemaExt(
            **inputs_json_schema,
            friendly_property_types=
                    model_to_friendly_property_types(Inputs) # type: ignore
        ), 
        
        params=HykoJsonSchemaExt(
            **params_json_schema,
            friendly_property_types=
                    model_to_friendly_property_types(Params) # type: ignore
        ), 
        
        outputs=HykoJsonSchemaExt(
            **outputs_json_schema,
            friendly_property_types=
                    model_to_friendly_property_types(Outputs) # type: ignore
        ), 
        requires_gpu=requires_gpu,
    )
    
    print(__meta_data__.model_dump_json(indent=2, exclude_unset=True))

