from typing import Any, List, Optional, Union, Dict
from .io import BaseModel
from pprint import pprint
from enum import Enum

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
    items: Optional['Property' | List['Property']] = None
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
