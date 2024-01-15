import base64
import json
from io import BytesIO
from typing import Type
from uuid import UUID

import httpx
from fastapi import HTTPException, status
from httpx import Timeout
from pydantic import BaseModel

from hyko_sdk.metadata import MetaData
from hyko_sdk.types import PyObjectId, StorageObjectType


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
        blueprint_id: PyObjectId,
    ) -> None:
        self.blueprint_id = blueprint_id
        self._conn = httpx.AsyncClient(
            base_url=f"https://{host}/blueprints/{blueprint_id}",
            http2=True,
            verify=False,
            timeout=Timeout(timeout=120),
        )
        pass

    async def download_object(
        self,
        id: UUID,
        expected_object_types: list[StorageObjectType],
    ):
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
                    detail=f"Could not read HEAD object info, status: {head_res.status_code}.",
                )

        head_headers = head_res.headers
        object_name = head_headers.get("X-Hyko-Storage-Name")

        if object_name is None:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing object name header, url: {head_res.url}",
            )

        object_type = head_headers.get("X-Hyko-Storage-Type")

        if object_type is None:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing object type header, url: {head_res.url}",
            )

        if object_type not in expected_object_types:
            raise ObjectStorageConn.DownloadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Expected object types {expected_object_types}, but got {object_type}",
            )

        res = await self._conn.get(f"/storage/{id}")
        # This should never happen but you never know...
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


def docker_label_to_metadata(label: str) -> MetaData:
    return MetaData(**json.loads(base64.b64decode(label.encode()).decode()))


def model_to_friendly_property_types(pydantic_model: Type[BaseModel]):
    out: dict[str, str] = {}
    for field_name, field in pydantic_model.model_fields.items():
        annotation = str(field.annotation).lower()
        if "enum" in annotation:
            out[field_name] = "enum"
            continue
        annotation = annotation.lstrip("<").rstrip(">")
        annotation = annotation.replace("class ", "")
        annotation = annotation.replace("hyko_sdk.io.", "")
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace("str", "string")
        annotation = annotation.replace("int", "integer")
        annotation = annotation.replace("float", "number")
        annotation = annotation.replace(" ", "")
        annotation = annotation.replace("'", "")
        out[field_name] = annotation
    return out
