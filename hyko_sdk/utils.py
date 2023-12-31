import base64
import json
from io import BytesIO
from typing import Type
from uuid import UUID

import httpx
from fastapi import HTTPException, status
from httpx import Timeout
from pydantic import BaseModel

from .metadata import HykoJsonSchemaExt, IOPortType, MetaData, MetaDataBase
from .types import PyObjectId


class ObjectStorageConn:
    class DownloadError(HTTPException):
        """Raised when an error occurs on file download"""

        pass

    class UploadError(HTTPException):
        """Raised when an error occurs on file upload"""

        pass

    def __init__(
        self,
        host: str,
        project_id: PyObjectId,
        blueprint_id: PyObjectId,
    ) -> None:
        self.project_id = project_id
        self.blueprint_id = blueprint_id
        self._conn = httpx.AsyncClient(
            base_url=f"https://{host}/projects/{project_id}/blueprints/{blueprint_id}",
            http2=True,
            verify=False,
            timeout=Timeout(timeout=120),
        )
        pass

    async def download_object(self, id: UUID):
        head_res = await self._conn.head(f"/storage/{id}")

        if not head_res.is_success:
            if head_res.status_code == status.HTTP_404_NOT_FOUND:
                raise ObjectStorageConn.DownloadError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Object not found, url: {head_res.url}",
                )
            else:
                raise ObjectStorageConn.DownloadError(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Could not read HEAD object info, status: {head_res.status_code}, res: {head_res.text}",
                )

        object_name = head_res.headers.get("X-Hyko-Storage-Name")

        if object_name is None:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing object name header, url: {head_res.url}",
            )

        object_type = head_res.headers.get("X-Hyko-Storage-Type")

        if object_type is None:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing object type header, url: {head_res.url}",
            )

        object_size = head_res.headers.get("Content-Length")

        if object_size is None:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing object content length header, url: {head_res.url}",
            )

        res = await self._conn.get(f"/storage/{id}")
        if not res.is_success:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not get object content, status: {res.status_code}, res: {res.text}",
            )
        object_data = bytearray(res.content)

        return (object_name, object_type, object_data)

    async def upload_object(self, filename: str, content_type: str, data: bytearray):
        res = await self._conn.post(
            url="/storage",
            files={"file": (filename, BytesIO(data), content_type)},
        )
        if not res.is_success:
            raise ObjectStorageConn.UploadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload error, status: {res.status_code}, res: {res.text}",
            )
        obj_id = UUID(res.text[1:-1])

        return obj_id


def metadata_to_docker_label(metadata: MetaData) -> str:
    return base64.b64encode(
        metadata.model_dump_json(exclude_unset=True, exclude_none=True).encode()
    ).decode()


def docker_label_to_metadata(label: str) -> MetaData:  # used in backend
    return MetaData(**json.loads(base64.b64decode(label.encode()).decode()))


def model_to_friendly_property_types(pydantic_model: Type[BaseModel]):
    out: dict[str, str] = {}
    for field_name, field in pydantic_model.model_fields.items():
        annotation = str(field.annotation).lower()
        if "enum" in annotation:
            try:
                out[
                    field_name
                ] = f"enum[{str(pydantic_model.model_json_schema()['$defs'][str(field.annotation)[7:-2]]['type'])}]"
                if "numeric" in out[field_name]:
                    out[field_name] = out[field_name].replace("numeric", "number")
            except KeyError as e:
                raise RuntimeError(
                    f'Could not find {str(pydantic_model.model_json_schema()["$defs"][str(field.annotation)[7:-2]])} the enums defined in the json schema. Usually happens when you use class(Video, Enum) or similar type'
                ) from e
            continue
        if "<class" in annotation:
            annotation = annotation[8:-2]
        annotation = annotation.replace("hyko_sdk.io.", "")
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace("str", "string")
        annotation = annotation.replace("int", "integer")
        annotation = annotation.replace("float", "number")

        out[field_name] = annotation
    return out


def extract_metadata(
    inputs: BaseModel,
    params: BaseModel,
    outputs: BaseModel,
    description: str,
    requires_gpu: bool,
):
    inputs_json_schema = inputs.model_json_schema()
    if inputs_json_schema.get("$defs"):
        for k, v in inputs_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                inputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER

    params_json_schema = params.model_json_schema()
    if params_json_schema.get("$defs"):
        for k, v in params_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                params_json_schema["$defs"][k]["type"] = IOPortType.NUMBER

    outputs_json_schema = outputs.model_json_schema()
    if outputs_json_schema.get("$defs"):
        for k, v in outputs_json_schema["$defs"].items():
            if v.get("type") and v["type"] == "numeric":
                outputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER

    __meta_data__ = MetaDataBase(
        description=description,
        inputs=HykoJsonSchemaExt(
            **inputs_json_schema,
            friendly_property_types=model_to_friendly_property_types(inputs),  # type: ignore
        ),
        params=HykoJsonSchemaExt(
            **params_json_schema,
            friendly_property_types=model_to_friendly_property_types(params),  # type: ignore
        ),
        outputs=HykoJsonSchemaExt(
            **outputs_json_schema,
            friendly_property_types=model_to_friendly_property_types(outputs),  # type: ignore
        ),
        requires_gpu=requires_gpu,
    )

    print(__meta_data__.model_dump_json(indent=2, exclude_unset=True))  # noqa: T201
