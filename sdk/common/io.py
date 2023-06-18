from enum import Enum
from typing import Optional
from pydantic import BaseModel

from typing import Any, Callable, Dict, Generator, Optional

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydantic import BaseModel


class Number(float):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "number"

class Integer(int):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "integer"

class String(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"


class Image(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return value

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["format"] = "image"


class Audio(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return value

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["format"] = "audio"


# Keep the same
class IOPortType(str, Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    IMAGE = "image"
    AUDIO = "audio"

class IOPort(BaseModel):
    name: str
    description: Optional[str]
    type: IOPortType
    required: bool
    default: Optional[float | int | str]
