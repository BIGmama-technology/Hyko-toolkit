from enum import Enum
from typing import Dict, List, Optional

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


class Property(BaseModel):
    type: Optional[IOPortType | HykoExtraTypes] = None
    description: Optional[str] = None
    all_of: Optional[list[dict[str, str]]] = Field(default=None, alias="allOf")
    ref: Optional[str] = Field(default=None, alias="$ref")

    enum: Optional[list[str]] = None
    any_of: Optional[List["Property"]] = Field(default=None, alias="anyOf")

    items: Optional["Property"] = None

    model_config = ConfigDict(populate_by_name=True)


class HykoJsonSchema(BaseModel):
    properties: Dict[str, Property] = {}
    defs: Optional[Dict[str, Property]] = Field(default=None, alias="$defs")
    friendly_types: Dict[str, str] = {}

    model_config = ConfigDict(populate_by_name=True)


class MetaDataBase(BaseModel):
    description: str
    startup_params: HykoJsonSchema
    params: HykoJsonSchema
    inputs: HykoJsonSchema
    outputs: HykoJsonSchema


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
