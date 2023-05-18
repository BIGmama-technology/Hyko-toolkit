from enum import Enum
from pydantic import BaseModel


# Keep the same
class IOType(str, Enum):
    FLOAT = "FLOAT"
    STRING = "STR"

class IOPort(BaseModel):
    name: str
    type: IOType
