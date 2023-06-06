from enum import Enum
from typing import Optional
from pydantic import BaseModel


# Keep the same
class IOPortType(str, Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"

class IOPort(BaseModel):
    name: str
    description: Optional[str]
    type: IOPortType
    required: bool
    default: Optional[float | int | str]
