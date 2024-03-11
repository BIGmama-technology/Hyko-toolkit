from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Ext(str, Enum):
    TXT = "txt"
    CSV = "csv"
    PDF = "pdf"
    PNG = "png"
    JPEG = "jpeg"
    MPEG = "mpeg"
    WEBM = "webm"
    WAV = "wav"
    MP4 = "mp4"
    MP3 = "mp3"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"
    GIF = "gif"
    JPG = "jpg"
    TIFF = "tiff"
    TIF = "tif"
    BMP = "bmp"
    JP2 = "jp2"
    DIB = "dib"
    PGM = "pgm"
    PPM = "ppm"
    PNM = "pnm"
    RAS = "ras"
    HDR = "hdr"
    WEBP = "webp"


class IOPortType(str, Enum):
    BOOLEAN = "boolean"
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    ARRAY = "array"
    OBJECT = "object"


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
    properties: Dict[str, Property]
    defs: Optional[Dict[str, Property]] = Field(default=None, alias="$defs")
    friendly_types: Dict[str, str]

    model_config = ConfigDict(populate_by_name=True)


class Category(str, Enum):
    MODEL = "models"
    FUNCTION = "functions"
    API = "apis"


class MetaDataBase(BaseModel):
    category: Category = Category.FUNCTION
    name: str
    task: str
    description: str
    params: Optional[HykoJsonSchema] = None
    inputs: Optional[HykoJsonSchema] = None
    outputs: Optional[HykoJsonSchema] = None


class FunctionMetaData(MetaDataBase):
    image: Optional[str] = None


class ModelMetaData(FunctionMetaData):
    startup_params: Optional[HykoJsonSchema] = None


class Method(str, Enum):
    get = "GET"
    post = "POST"
    patch = "PATCH"
    put = "PUT"
    delete = "DELETE"


class APIMetaData(MetaDataBase):
    method: Method
    url: str
    headers: Optional[dict[str, str]] = None
    body: Optional[dict[str, Any]] = None
    response: dict[str, Any]

    @computed_field
    @property
    def image(self) -> str:
        return self.method + self.url


class CoreModel(BaseModel):
    pass
