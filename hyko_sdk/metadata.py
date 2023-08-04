from typing import Any, List, Optional, Union, Dict
from .io import BaseModel
from enum import Enum
import json

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
    
class Property(BaseModel):
    type: Optional[IOPortType] = None
    subtype: Optional[HykoExtraTypes] = None
    anyOf: Optional [List['Property']] = None
    items: Optional[Union['Property', List['Property']]] = None
    prefixItems: Optional[List['Property']] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    description: Optional[str] = None
    default: Optional[Any] = None

class HykoJsonSchema(BaseModel):
    properties: Dict[str, Property] = {}
    required: List[str] = []
    
class MetaDataBase(BaseModel):
    description: str
    inputs: HykoJsonSchema
    outputs: HykoJsonSchema
    params: HykoJsonSchema
    requires_gpu: bool

class MetaData(MetaDataBase):
    version: str
    name: str
    category: str


def metadata_to_docker_label(metadata: MetaData) -> str:
    return metadata.model_dump_json(exclude_unset=True, exclude_none=True).replace('"', "'")

    
def docker_label_to_metadata(label: str) -> MetaData:
    return MetaData(**json.loads(label.replace("'", '"')))


