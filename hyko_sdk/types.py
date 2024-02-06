from enum import Enum
from typing import Any, Callable

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @staticmethod
    def validate(val: "str | bytes | PyObjectId | ObjectId") -> ObjectId:
        try:
            return ObjectId(val)
        except InvalidId as e:
            raise ValueError("Invalid ObjectId") from e

    @staticmethod
    def serialize(obj: "PyObjectId") -> str:
        return f"{obj}"

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_before_validator_function(
            PyObjectId.validate,
            schema=core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.is_subclass_schema(ObjectId),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=PyObjectId.serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
                when_used="json",
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(_core_schema)


class MimeType(str, Enum):
    TXT = "txt"
    CSV = "csv"
    PDF = "pdf"
    PNG = "png"
    JPEG = "jpeg"
    MPEG = "mpeg"
    WEBM = "webm"
    WAV = "wav"
    MP4 = "mp4"
