from typing import Any, Type, Union, Optional, Tuple, Literal
from enum import Enum
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from .types import PyObjectId, StorageObject, StorageObjectType
from .utils import ObjectStorageConn
import numpy as np
from PIL import Image as PIL_Image
import soundfile # type: ignore
import os
import subprocess
import io
from uuid import UUID
import uuid
import asyncio


class HykoBaseType:

    _obj_id: Optional[UUID] = None
    _obj: Optional[StorageObject] = None
    _sync_conn: Optional[ObjectStorageConn] = None
    _sync_tasks: Optional[list[asyncio.Task[None]]] = None

    @classmethod
    def set_sync(
        cls,
        storage_host: str,
        project_id: PyObjectId,
        blueprint_id: PyObjectId,
        pending_tasks: list[asyncio.Task[None]],
    ):
        cls._sync_conn = ObjectStorageConn(storage_host, project_id, blueprint_id)
        cls._sync_tasks = pending_tasks

    @classmethod
    def clear_sync(cls):
        cls._sync_conn = None
        cls._sync_tasks = None

    def set_obj(self, obj_name: str, obj_type: StorageObjectType, obj_data: bytearray):
        self._obj = StorageObject(name=obj_name, type=obj_type, data=obj_data)

    def set_obj_id(self, obj_id: UUID):
        self._obj_id = obj_id
    
    def sync_storage(self):
        if self._sync_conn is None or self._sync_tasks is None:
            return
        
        if self._obj is None and self._obj_id is not None:
            async def download_task(sync_conn: ObjectStorageConn, id: UUID):
                obj_name, obj_type, obj_data = await sync_conn.download_object(id, show_progress=True)
                self.set_obj(obj_name, obj_type, obj_data)

            self._sync_tasks.append(asyncio.create_task(download_task(self._sync_conn, self._obj_id)))
            return
        
        if self._obj_id is None and self._obj is not None:
            async def upload_task(sync_conn: ObjectStorageConn, obj: StorageObject):
                self.set_obj_id(await sync_conn.upload_object(obj.name, obj.type, obj.data, show_progress=False))

            self._sync_tasks.append(asyncio.create_task(upload_task(self._sync_conn, self._obj)))
            return

        raise Exception("Unexpected sync state")
    
    def get_name(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.name
    
    def get_mime_type(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.type

    def get_data(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.data

class Image(HykoBaseType):

    MimeTypesUnion = Literal["PNG"] | Literal["JPEG"]

    class MimeType(Enum):
        PNG = "PNG"
        JPEG = "JPEG"

    @staticmethod
    def from_ndarray(arr: np.ndarray[Any, Any], filename: str = "image.png", encoding: MimeTypesUnion = "PNG") -> "Image":
        file = io.BytesIO()
        img = PIL_Image.fromarray(arr) # type: ignore
        img.save(file, format="PNG")
        return Image(bytearray(file.getbuffer().tobytes()), filename=filename, mime_type=encoding)

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, 'Image'],
        filename: Optional[str] = None,
        mime_type: Optional[MimeTypesUnion] = None,
    ) -> None:
        
        if isinstance(val, Image):
            self._obj = val._obj
            self._obj_id = val._obj_id
            self.sync_storage()
            # print("Image init from Image")
            return

        if isinstance(val, uuid.UUID):
            self._obj_id = val
            self.sync_storage()
            # print("Image init from UUID")
            return
        
        if isinstance(val, str):
            self._obj_id = UUID(val)
            self.sync_storage()
            # print("Image init from Str")
            return

        if isinstance(val, bytearray): # type: ignore
            if filename is None:
                filename = "test.png"

            if mime_type is None:
                mime_type = "PNG"

            if mime_type == "PNG":
                self.set_obj(filename, StorageObjectType.IMAGE_PNG, val)
            elif mime_type == "JPEG":
                self.set_obj(filename, StorageObjectType.IMAGE_JPEG, val)
            else:
                raise ValueError("Got invalid mime type")
            
            self.sync_storage()
            # print("Image init from Bytearray")
            return
        
        raise ValueError("Got invalid init value")


    def __str__(self) -> str:
        return f"{self._obj_id}"
    
    @staticmethod
    def serialize_id(value: 'Image') -> str:
        # print("Serializing Id")
        return f"{value._obj_id}"
    
    @staticmethod
    def serialize_object(value: 'Image') -> tuple[bytearray, str, str]:
        # print("Serializing StorageObject")
        if value._obj is None:
            raise ValueError("StorageObject serialization error, object not set")
        return (value._obj.data, value._obj.name, value._obj.type)
    
    @staticmethod
    def validate_from_id(value: str | UUID) -> 'Image':
        # print("Validating Id")
        return Image(value)
    
    @staticmethod
    def validate_from_object(value: 'tuple[bytearray, str, str] | Image') -> 'Image':
        # print("Validating StorageObject")
        # print(f"obj type: {type(value)}")
        if isinstance(value, Image):
            return value
        if value[2] == StorageObjectType.IMAGE_PNG:
            obj_type = 'PNG'
        elif value[2] == StorageObjectType.IMAGE_JPEG:
            obj_type = 'JPEG'
        else:
            raise ValueError(f"Invalud StorageObject type, {value[2]}")
        return Image(value[0], value[1], obj_type)
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        assert source is Image

        json_schema = core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(Image.validate_from_id),
                    ]),
                core_schema.chain_schema(
                    [
                        core_schema.uuid_schema(),
                        core_schema.no_info_plain_validator_function(Image.validate_from_id),
                    ]),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Image.serialize_id),
        )

        python_schema = core_schema.union_schema(
            [
                json_schema,
                core_schema.no_info_plain_validator_function(Image.validate_from_object),
                # core_schema.is_instance_schema(Image),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Image.serialize_object)
        )

        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
            # serialization=core_schema.plain_serializer_function_ser_schema(Image.serialize_id),
        )
        
    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ):
        schema = handler(core_schema.str_schema())
        schema["type"] = "image"
        return schema
    

    def to_ndarray(self, keep_alpha_if_png = False) -> np.ndarray:
        if self.get_data():
            img_bytes_io = io.BytesIO(self.get_data())
            img = PIL_Image.open(img_bytes_io)
            img = np.asarray(img)
            if keep_alpha_if_png:
                return img
            return img[...,:3]
        else:
           raise RuntimeError("Image decode error (Imagedata not loaded)")

        
        

class Audio(HykoBaseType):

    MimeTypesUnion = Literal["MPEG"] | Literal["WEBM"] | Literal["WAV"]

    class MimeType(Enum):
        MPEG = "MPEG"
        WEBM = "WEBM"
        WAV = "WAV"

    @staticmethod
    def from_ndarray(arr: np.ndarray, sampling_rate: int) -> "Audio": # type: ignore
        file = io.BytesIO()
        soundfile.write(file, arr, samplerate=sampling_rate, format="MP3") # type: ignore
        return Audio(bytearray(file.getbuffer().tobytes()), filename="audio.mp3", mime_type="MPEG")
    
    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, 'Audio'],
        filename: Optional[str] = None,
        mime_type: Optional['Audio.MimeTypesUnion'] = None,
    ) -> None:
        
        if isinstance(val, Audio):
            self._obj = val._obj
            self._obj_id = val._obj_id
            self.sync_storage()
            # print("Image init from Audio")
            return

        if isinstance(val, uuid.UUID):
            self._obj_id = val
            self.sync_storage()
            # print("Image init from UUID")
            return
        
        if isinstance(val, str):
            self._obj_id = UUID(val)
            self.sync_storage()
            # print("Image init from Str")
            return

        if isinstance(val, bytearray): # type: ignore
            if filename is None:
                filename = "output.mp3"
                # raise ValueError("Filename should not be None when creating an Image from a bytearray")
            
            if mime_type is None:
                mime_type = 'MPEG'
                # raise ValueError("Mime type should not be None when creating an Image from a bytearray")
            
            if mime_type == 'MPEG':
                self.set_obj(filename, StorageObjectType.AUDIO_MPEG, val)
            elif mime_type == 'WEBM':
                self.set_obj(filename, StorageObjectType.AUDIO_WEBM, val)
            elif mime_type == 'WAV':
                self.set_obj(filename, StorageObjectType.AUDIO_WAV, val)
            else:
                raise ValueError(f"Got invalid mime type, {mime_type}")
            
            self.sync_storage()
            # print("Image init from Bytearray")
            return
        
        raise ValueError(f"Got invalid init value type, {type(val)}")

    def __str__(self) -> str:
        return f"{self._obj_id}"
    
    @staticmethod
    def serialize_id(value: 'Audio') -> str:
        # print("Serializing Id")
        return f"{value._obj_id}"
    
    @staticmethod
    def serialize_object(value: 'Audio') -> tuple[bytearray, str, str]:
        # print("Serializing StorageObject")
        if value._obj is None:
            raise ValueError("StorageObject serialization error, object not set")
        return (value._obj.data, value._obj.name, value._obj.type)
    
    @staticmethod
    def validate_from_id(value: str | UUID) -> 'Audio':
        # print("Validating Id")
        return Audio(value)
    
    @staticmethod
    def validate_from_object(value: 'tuple[bytearray, str, str] | Audio') -> 'Audio':
        # print("Validating StorageObject")
        # print(f"obj type: {type(value)}")
        if isinstance(value, Audio):
            return value
        if value[2] == StorageObjectType.AUDIO_MPEG:
            obj_type = 'MPEG'
        elif value[2] == StorageObjectType.AUDIO_WEBM:
            obj_type = 'WEBM'
        elif value[2] == StorageObjectType.AUDIO_WAV:
            obj_type = 'WAV'
        else:
            raise ValueError(f"Invalud StorageObject type, {value[2]}")
        return Audio(value[0], value[1], obj_type)
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        assert source is Audio

        json_schema = core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(Audio.validate_from_id),
                    ]),
                core_schema.chain_schema(
                    [
                        core_schema.uuid_schema(),
                        core_schema.no_info_plain_validator_function(Audio.validate_from_id),
                    ]),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Audio.serialize_id),
        )

        python_schema = core_schema.union_schema(
            [
                json_schema,
                core_schema.no_info_plain_validator_function(Audio.validate_from_object),
                # core_schema.is_instance_schema(Audio),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Audio.serialize_object)
        )

        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
            # serialization=core_schema.plain_serializer_function_ser_schema(Audio.serialize_id),
        )
        
    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ):
        schema = handler(core_schema.str_schema())
        schema["type"] = "audio"
        return schema
        
        
    _SUBTYPE2DTYPE = {
        "PCM_S8": "int8",
        "PCM_U8": "uint8",
        "PCM_16": "int16",
        "PCM_32": "int32",
        "FLOAT": "float32",
        "DOUBLE": "float64",
    }
    
    def resample(self, sampling_rate: int):
        if self._obj and self._obj.name:
            with open(self._obj.name, "wb") as f:
                f.write(self.get_data())
            out = "audio_resampled.mp3"
            if self._obj.name == out:
                out = "audio_resampled_2.mp3"
                
            subprocess.run(f"ffmpeg -i {self._obj.name} -ac 1 -ar {sampling_rate} {out} -y".split(" "))
            with open(out, "rb") as f:
                self.data = bytearray(f.read())
                
            os.remove(out)
            
    def convert_to(self, new_ext: str):
        if self._obj and self._obj.name:
            
            # user video.{ext} instead of filename directly to avoid errors with names that has space in it
            _, ext = os.path.splitext(self._obj.name)
            with open(f"/app/video.{ext}", "wb") as f:
                f.write(self.data)
                
            out = "media_converted." + new_ext 
            if self._obj.name == out:
                out = "media_converted_2." + new_ext
                
            subprocess.run(f"ffmpeg -i video.{ext} {out} -y".split(" "))
            with open(out, "rb") as f:
                self.data = bytearray(f.read())
                
            os.remove(out)
            
    def to_ndarray( # type: ignore
        self,
        sampling_rate: Optional[int] = None,
        normalize: bool = True,
        frame_offset: int = 0,
        num_frames: int = -1,
    ) -> Tuple[np.ndarray, int]: # type: ignore
        
        if self._obj and self._obj.name:
            if "webm" in self._obj.name:
                self.convert_to("mp3")
                
            if sampling_rate:
                self.resample(sampling_rate)
            
            audio_readable = io.BytesIO(self.get_data())
            with soundfile.SoundFile(audio_readable, "r") as file_:
                if file_.format != "WAV" or normalize:
                    dtype = "float32"
                elif file_.subtype not in Audio._SUBTYPE2DTYPE:
                    raise RuntimeError(f"Unsupported Audio subtype {file_.subtype}")
                else:
                    dtype = Audio._SUBTYPE2DTYPE[file_.subtype]

                frames = file_._prepare_read(frame_offset, None, num_frames) # type: ignore
                waveform: np.ndarray = file_.read(frames, dtype, always_2d=True) # type: ignore
                sample_rate: int = file_.samplerate
                return waveform.reshape((waveform.shape[0])), sample_rate # type: ignore
            
        else:
            raise RuntimeError("Audio decode error (Audio data not loaded)")



class Video(HykoBaseType):

    MimeTypesUnion = Literal["MP4"] | Literal["WEBM"]

    class MimeType(Enum):
        MP4 = "MP4"
        WEBM = "WEBM"

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, 'Video'],
        filename: Optional[str] = None,
        mime_type: Optional['Video.MimeTypesUnion'] = None,
    ) -> None:
        
        if isinstance(val, Video):
            self._obj = val._obj
            self._obj_id = val._obj_id
            self.sync_storage()
            # print("Image init from Video")
            return

        if isinstance(val, uuid.UUID):
            self._obj_id = val
            self.sync_storage()
            # print("Image init from UUID")
            return
        
        if isinstance(val, str):
            self._obj_id = UUID(val)
            self.sync_storage()
            # print("Image init from Str")
            return

        if isinstance(val, bytearray): # type: ignore
            if filename is None:
                filename = "video.mp4"
            
            if mime_type is None:
                mime_type = 'MP4'
            
            if mime_type == 'MP4':
                self.set_obj(filename, StorageObjectType.VIDEO_MP4, val)
            elif mime_type == 'WEBM':
                self.set_obj(filename, StorageObjectType.VIDEO_WEBM, val)
            else:
                raise ValueError(f"Got invalid mime type, {mime_type}")
            
            self.sync_storage()
            # print("Image init from Bytearray")
            return
        
        raise ValueError(f"Got invalid init value type, {type(val)}")
    

    def __str__(self) -> str:
        return f"{self._obj_id}"
    
    @staticmethod
    def serialize_id(value: 'Video') -> str:
        # print("Serializing Id")
        return f"{value._obj_id}"
    
    @staticmethod
    def serialize_object(value: 'Video') -> tuple[bytearray, str, str]:
        # print("Serializing StorageObject")
        if value._obj is None:
            raise ValueError("StorageObject serialization error, object not set")
        return (value._obj.data, value._obj.name, value._obj.type)
    
    @staticmethod
    def validate_from_id(value: str | UUID) -> 'Video':
        # print("Validating Id")
        return Video(value)
    
    @staticmethod
    def validate_from_object(value: 'tuple[bytearray, str, str] | Video') -> 'Video':
        # print("Validating StorageObject")
        # print(f"obj type: {type(value)}")
        if isinstance(value, Video):
            return value
        if value[2] == StorageObjectType.VIDEO_MP4:
            obj_type = 'MP4'
        elif value[2] == StorageObjectType.VIDEO_WEBM:
            obj_type = 'WEBM'
        else:
            raise ValueError(f"Invalid StorageObject type, {value[2]}")
        return Video(value[0], value[1], obj_type)
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        assert source is Video

        json_schema = core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(Video.validate_from_id),
                    ]),
                core_schema.chain_schema(
                    [
                        core_schema.uuid_schema(),
                        core_schema.no_info_plain_validator_function(Video.validate_from_id),
                    ]),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Video.serialize_id),
        )

        python_schema = core_schema.union_schema(
            [
                json_schema,
                core_schema.no_info_plain_validator_function(Video.validate_from_object),
                # core_schema.is_instance_schema(Video),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(Video.serialize_object)
        )

        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
            # serialization=core_schema.plain_serializer_function_ser_schema(Video.serialize_id),
        )
        
    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ):
        schema = handler(core_schema.str_schema())
        schema["type"] = "video"
        return schema


__all__ = ["Image", "Audio", "Video", ]
