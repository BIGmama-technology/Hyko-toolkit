from typing import Type

from pydantic import BaseModel


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
