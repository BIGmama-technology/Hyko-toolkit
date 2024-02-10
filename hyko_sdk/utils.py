import base64
import json
from typing import Type

from pydantic import BaseModel

from hyko_sdk.metadata import MetaData


def metadata_to_docker_label(metadata: MetaData) -> str:
    return base64.b64encode(
        metadata.model_dump_json(exclude_unset=True, exclude_none=True).encode()
    ).decode()


def docker_label_to_metadata(label: str) -> MetaData:
    return MetaData(**json.loads(base64.b64decode(label.encode()).decode()))


def to_friendly_types(pydantic_model: Type[BaseModel]):
    out: dict[str, str] = {}
    for field_name, field in pydantic_model.model_fields.items():
        annotation = str(field.annotation).lower()
        if "enum" in annotation:
            out[field_name] = "enum"
            continue
        annotation = annotation.lstrip("<").rstrip(">")
        annotation = annotation.replace("class ", "")
        annotation = annotation.replace("hyko_sdk.io.", "")
        annotation = annotation.replace("__main__.", "")
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace(" ", "")
        annotation = annotation.replace("'", "")
        annotation = annotation.replace("str", "text")
        annotation = annotation.replace("int", "whole number")
        annotation = annotation.replace("float", "decimal number")
        out[field_name] = annotation
    return out
