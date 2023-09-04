from typing import Optional, Callable, Any, Coroutine, TypeVar, Type
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import inspect
import asyncio
from .types import PyObjectId
from .io import HykoBaseType
from .metadata import MetaDataBase, HykoJsonSchemaExt, IOPortType
from .utils import model_to_friendly_property_types
import json
import os
import signal

InputsType = TypeVar("InputsType", bound="BaseModel")
ParamsType = TypeVar("ParamsType", bound="BaseModel")
OutputsType = TypeVar("OutputsType", bound="BaseModel")

OnStartupFuncType = Callable[[], Coroutine[Any, Any, None]]
OnShutdownFuncType = Callable[[], Coroutine[Any, Any, None]]
OnExecuteFuncType = Callable[[InputsType, ParamsType], Coroutine[Any, Any, OutputsType]]


class ExecStorageParams(BaseModel):
    host: str
    project_id: PyObjectId
    blueprint_id: PyObjectId


class SDKFunction(FastAPI):


    class InvalidExecSignature(BaseException):
        f_args: list[tuple[str, Type[Any]]]
        f_ret_type: Optional[Type[Any]]

        def __init__(self, f_args: list[tuple[str, Type[Any]]], f_ret_type: Optional[Type[Any]]) -> None:
            self.f_args=f_args
            self.f_ret_type=f_ret_type

        def __str__(self) -> str:
            return f"args: {self.f_args}, ret_type: {self.f_ret_type}"


    class InvalidExecParamsCount(InvalidExecSignature):
        pass


    class InvalidExecInputsType(InvalidExecSignature):
        name: str
        type: Type[Any]

        def __init__(
            self,
            f_args: list[tuple[str, Type[Any]]],
            f_ret_type: Optional[Type[Any]],
            name: str,
            type: Type[Any],
        ) -> None:
            super().__init__(f_args, f_ret_type)
            self.name=name
            self.type=type

    class InvalidExecParamsType(InvalidExecInputsType):
        pass

    class InvalidExecRetType(InvalidExecSignature):
        pass

    
    __metadata__: MetaDataBase
    startup_tasks: list[asyncio.Task[None]] = []


    def __init__(
        self,
        description: str,
        requires_gpu: bool,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._status = asyncio.Future[bool]()
        self.description = description
        self.requires_gpu = requires_gpu


    def on_startup(self, f: OnStartupFuncType):
        def blocking_exec():
            asyncio.run(f())
        try:
            asyncio.get_running_loop()
            self.startup_tasks.append(asyncio.create_task(asyncio.to_thread(blocking_exec)))
        except RuntimeError:
            pass

    async def _wait_startup_tasks(self):
        if not len(self.startup_tasks):
                return
        done, _ = await asyncio.wait(self.startup_tasks, return_when=asyncio.FIRST_EXCEPTION)
        for task in done:
            exc = task.exception()
            if exc is not None:
                raise exc


    def on_shutdown(self, f: OnShutdownFuncType) -> OnShutdownFuncType:
        async def wrapper() -> None:
            await f()
        return self.on_event("shutdown")(wrapper)


    def on_execute(self, f: OnExecuteFuncType[InputsType, ParamsType, OutputsType]):

        async def wait_startup_handler():
            try:
                await self._wait_startup_tasks()
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Exception occured during startup: {exc}",
                )
            return

        self.get("/wait_startup")(wait_startup_handler)
        
        async def wait_startup_exit_handler():
            try:
                await self._wait_startup_tasks()
            except:
                os.kill(os.getpid(), signal.SIGINT)
        
        try:
            asyncio.get_running_loop()
            self.startup_task = asyncio.create_task(wait_startup_exit_handler())
        except RuntimeError:
            pass
        
        f_args = [(param.name, param.annotation) for param in inspect.signature(f).parameters.values()]
        f_ret_type = inspect.signature(f).return_annotation

        if len(f_args) < 2:
            raise SDKFunction.InvalidExecParamsCount(
                f_args=f_args,
                f_ret_type=f_ret_type,
            )
        
        f_inputs_name, f_inputs_type = f_args[0]
        f_params_name, f_params_type = f_args[1]


        if not issubclass(f_inputs_type, BaseModel):
            raise SDKFunction.InvalidExecInputsType(
                f_args=f_args,
                f_ret_type=f_ret_type,
                name=f_inputs_name,
                type=f_inputs_type,
            )
        
        if not issubclass(f_params_type, BaseModel):
            raise SDKFunction.InvalidExecInputsType(
                f_args=f_args,
                f_ret_type=f_ret_type,
                name=f_params_name,
                type=f_params_type,
            )
        
        if not issubclass(f_ret_type, BaseModel) or isinstance(f_ret_type, inspect.Parameter.empty):
            raise SDKFunction.InvalidExecRetType(
                f_args=f_args,
                f_ret_type=f_ret_type,
            )

        inputs_json_schema = f_inputs_type.model_json_schema()
        if inputs_json_schema.get("$defs"):
            for k,v in inputs_json_schema["$defs"].items():
                if v.get("type") and v["type"] == "numeric":
                    inputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER
        
        if inputs_json_schema.get("properties"):
            for k,v in inputs_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    allOf = inputs_json_schema["properties"][k].pop("allOf")
                    inputs_json_schema["properties"][k]["$ref"] = allOf[0]["$ref"]

        params_json_schema = f_params_type.model_json_schema()
        if params_json_schema.get("$defs"):
            for k,v in params_json_schema["$defs"].items():
                if v.get("type") and v["type"] == "numeric":
                    params_json_schema["$defs"][k]["type"] = IOPortType.NUMBER

        if params_json_schema.get("properties"):
            for k,v in params_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    allOf = params_json_schema["properties"][k].pop("allOf")
                    params_json_schema["properties"][k]["$ref"] = allOf[0]["$ref"]

        outputs_json_schema = f_ret_type.model_json_schema()
        if outputs_json_schema.get("$defs"):
            for k,v in outputs_json_schema["$defs"].items():
                if v.get("type") and v["type"] == "numeric":
                    outputs_json_schema["$defs"][k]["type"] = IOPortType.NUMBER
        
        if outputs_json_schema.get("properties"):
            for k,v in outputs_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    allOf = outputs_json_schema["properties"][k].pop("allOf")
                    outputs_json_schema["properties"][k]["$ref"] = allOf[0]["$ref"]
         
        self.__metadata__ = MetaDataBase(
            description=self.description,
            inputs=HykoJsonSchemaExt(
                **inputs_json_schema,
                friendly_property_types=
                    model_to_friendly_property_types(f_inputs_type)
            ), 
            
            params=HykoJsonSchemaExt(
                **params_json_schema,
                friendly_property_types=
                    model_to_friendly_property_types(f_params_type)
            ), 
            
            outputs=HykoJsonSchemaExt(
                **outputs_json_schema,
                friendly_property_types=
                    model_to_friendly_property_types(f_ret_type)
            ), 
            requires_gpu=self.requires_gpu,
        )

        async def wrapper(storage_params: ExecStorageParams, inputs: InputsType, params: ParamsType) -> OutputsType:
            if not self.startup_task.done():
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="SDK Function did not finish startup",
                )
            pending_download_tasks: list[asyncio.Task[None]] = []
            HykoBaseType.set_sync(
                storage_params.host,
                storage_params.project_id,
                storage_params.blueprint_id,
                pending_download_tasks,
            )
            # print("Rebuilding inputs")
            inputs = inputs.model_validate_json(inputs.model_dump_json())
            params = params.model_validate_json(params.model_dump_json())
            HykoBaseType.clear_sync()
            # print("waiting for inputs")
            if len(pending_download_tasks):
                done, _ = await asyncio.wait(pending_download_tasks)
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc
            # print("Inputs done")
            outputs = await f(inputs, params)

            pending_upload_tasks: list[asyncio.Task[None]] = []
            HykoBaseType.set_sync(
                storage_params.host,
                storage_params.project_id,
                storage_params.blueprint_id,
                pending_upload_tasks,
            )
            # print("Rebuilding outputs")
            outputs = outputs.model_validate(outputs.model_dump())
            HykoBaseType.clear_sync()
            # print("waiting for inputs")
            if len(pending_upload_tasks):
                done, _ = await asyncio.wait(pending_upload_tasks)
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc
            # print("Inputs done")
            
            return JSONResponse(content=json.loads(outputs.model_dump_json())) # type: ignore
        
        storage_params_annotations = wrapper.__annotations__["storage_params"]
        wrapper.__annotations__ = f.__annotations__
        wrapper.__annotations__["storage_params"] = storage_params_annotations
        return self.post("/execute")(wrapper)

    def get_metadata(self) -> MetaDataBase:
        return self.__metadata__
    
    def dump_metadata(self, indent: Optional[int] = None) -> str:
        return self.get_metadata().model_dump_json(indent=indent)


__all__ = ["SDKFunction", ]
