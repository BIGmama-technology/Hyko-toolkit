from typing import Optional

from pydantic import BaseModel, ConfigDict


class Output(BaseModel):
    success: bool = True
    message: Optional[str] = None

    model_config = ConfigDict(extra="allow")
