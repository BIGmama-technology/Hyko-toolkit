from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IOPortType(str, Enum):
    BOOLEAN = "boolean"
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


class HykoExtraTypes(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"
    CSV = "csv"


class JsonSchemaEnum(BaseModel):
    enum: list[str]
    type: IOPortType


class Property(BaseModel):
    type: Optional[IOPortType | HykoExtraTypes] = None
    anyOf: Optional[List["Property"]] = None  # noqa: N815
    items: Optional["Property"] = None
    prefixItems: Optional[List["Property"]] = None  # noqa: N815
    minItems: Optional[int] = None  # noqa: N815
    maxItems: Optional[int] = None  # noqa: N815
    description: Optional[str] = None
    default: Optional[Any] = None
    ref: Optional[str] = Field(default=None, alias="$ref")
    model_config = ConfigDict(populate_by_name=True)


class HykoJsonSchema(BaseModel):
    properties: Dict[str, Property] = {}
    required: List[str] = []
    defs: Optional[Dict[str, JsonSchemaEnum]] = Field(default=None, alias="$defs")
    model_config = ConfigDict(populate_by_name=True)
    friendly_property_types: Dict[str, str] = {}


class MetaDataBase(BaseModel):
    description: str
    startup_params: HykoJsonSchema
    params: HykoJsonSchema
    inputs: HykoJsonSchema
    outputs: HykoJsonSchema
    model_config = ConfigDict(populate_by_name=True)


class Category(str, Enum):
    MODEL = "models"
    FUNCTION = "functions"

    @classmethod
    def get_enum_from_string(cls, input_string: str):
        for enum_member in cls:
            if input_string == enum_member.value:
                return enum_member
        raise ValueError("String does not match any enum value")


class MetaData(MetaDataBase):
    name: str
    task: str
    image: str
    category: Category


class CoreModel(BaseModel):
    pass
