import asyncio
import json
from typing import Any, Callable, Coroutine, Optional, Type, TypeVar

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hyko_sdk.io import HykoBaseType
from hyko_sdk.metadata import HykoJsonSchemaExt, MetaDataBase
from hyko_sdk.types import PyObjectId
from hyko_sdk.utils import model_to_friendly_property_types

InputsType = TypeVar("InputsType", bound="BaseModel")
ParamsType = TypeVar("ParamsType", bound="BaseModel")
OutputsType = TypeVar("OutputsType", bound="BaseModel")

OnStartupFuncType = Callable[[], Coroutine[Any, Any, None]]
OnShutdownFuncType = Callable[[], Coroutine[Any, Any, None]]
OnExecuteFuncType = Callable[[InputsType, ParamsType], Coroutine[Any, Any, OutputsType]]


class ExecStorageParams(BaseModel):
    host: str
    blueprint_id: PyObjectId


class SDKFunction(FastAPI):
    class InvalidExecSignature(BaseException):
        f_args: list[tuple[str, Type[Any]]]
        f_ret_type: Optional[Type[Any]]

        def __init__(
            self, f_args: list[tuple[str, Type[Any]]], f_ret_type: Optional[Type[Any]]
        ) -> None:
            self.f_args = f_args
            self.f_ret_type = f_ret_type

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
            self.name = name
            self.type = type

    class InvalidExecParamsType(InvalidExecInputsType):
        pass

    class InvalidExecRetType(InvalidExecSignature):
        pass

    __metadata__: MetaDataBase
    startup_tasks: list[asyncio.Task[None]] = []

    def __init__(
        self,
        description: str,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.description = description
        self.inputs: Type[BaseModel]
        self.outputs: Type[BaseModel]
        self.params: Type[BaseModel]

    def set_input(self, cls: Any):
        self.inputs = cls
        return cls

    def set_output(self, cls: Any):
        self.outputs = cls
        return cls

    def set_param(self, cls: Any):
        self.params = cls
        return cls

    def on_startup(self, f: OnStartupFuncType):
        def blocking_exec():
            asyncio.run(f())

        try:
            asyncio.get_running_loop()
            self.startup_tasks.append(
                asyncio.create_task(asyncio.to_thread(blocking_exec))
            )
        except RuntimeError:
            pass

    async def _wait_startup_tasks(self):
        if not len(self.startup_tasks):
            return

        done, _ = await asyncio.wait(
            self.startup_tasks, return_when=asyncio.FIRST_EXCEPTION
        )
        for task in done:
            exc = task.exception()
            if exc is not None:
                raise exc

    def on_shutdown(self, f: OnShutdownFuncType) -> OnShutdownFuncType:
        async def wrapper() -> None:
            await f()

        return self.on_event("shutdown")(wrapper)

    def on_execute(self, f: OnExecuteFuncType[InputsType, ParamsType, OutputsType]):  # noqa: C901
        async def wait_startup_handler():
            try:
                await self._wait_startup_tasks()
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Exception occured during startup:\n{e.__repr__()}",
                ) from e

        self.get("/wait_startup")(wait_startup_handler)

        async def wrapper(  # noqa: C901
            storage_params: ExecStorageParams, inputs: InputsType, params: ParamsType
        ) -> JSONResponse:
            for task in self.startup_tasks:
                if not task.done():
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="SDK Function did not finish startup",
                    )

            pending_download_tasks: list[asyncio.Task[None]] = []
            HykoBaseType.set_sync(
                storage_params.host,
                storage_params.blueprint_id,
                pending_download_tasks,
            )

            inputs = inputs.model_validate_json(inputs.model_dump_json())
            params = params.model_validate_json(params.model_dump_json())
            HykoBaseType.clear_sync()

            if len(pending_download_tasks):
                done, _ = await asyncio.wait(pending_download_tasks)
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc

            try:
                outputs = await f(inputs, params)
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Exception occured during execution:\n{e.__repr__()}",
                ) from e

            pending_upload_tasks: list[asyncio.Task[None]] = []
            HykoBaseType.set_sync(
                storage_params.host,
                storage_params.blueprint_id,
                pending_upload_tasks,
            )

            outputs = outputs.model_validate(outputs.model_dump())
            HykoBaseType.clear_sync()

            if len(pending_upload_tasks):
                done, _ = await asyncio.wait(pending_upload_tasks)
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc

            return JSONResponse(content=json.loads(outputs.model_dump_json()))

        storage_params_annotations = wrapper.__annotations__["storage_params"]
        wrapper.__annotations__ = f.__annotations__
        wrapper.__annotations__["storage_params"] = storage_params_annotations

        return self.post("/execute")(wrapper)

    def get_metadata(self) -> MetaDataBase:
        inputs_json_schema = self.inputs.model_json_schema()
        params_json_schema = self.params.model_json_schema()
        outputs_json_schema = self.outputs.model_json_schema()

        if inputs_json_schema.get("properties"):
            for k, v in inputs_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    all_of = inputs_json_schema["properties"][k].pop("allOf")
                    inputs_json_schema["properties"][k]["$ref"] = all_of[0]["$ref"]

        if params_json_schema.get("properties"):
            for k, v in params_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    all_of = params_json_schema["properties"][k].pop("allOf")
                    params_json_schema["properties"][k]["$ref"] = all_of[0]["$ref"]

        if outputs_json_schema.get("properties"):
            for k, v in outputs_json_schema["properties"].items():
                if v.get("allOf") and len(v["allOf"]) == 1:
                    all_of = outputs_json_schema["properties"][k].pop("allOf")
                    outputs_json_schema["properties"][k]["$ref"] = all_of[0]["$ref"]

        return MetaDataBase(
            description=self.description,
            inputs=HykoJsonSchemaExt(
                **inputs_json_schema,
                friendly_property_types=model_to_friendly_property_types(self.inputs),
            ),
            params=HykoJsonSchemaExt(
                **params_json_schema,
                friendly_property_types=model_to_friendly_property_types(self.params),
            ),
            outputs=HykoJsonSchemaExt(
                **outputs_json_schema,
                friendly_property_types=model_to_friendly_property_types(self.outputs),
            ),
        )

    def dump_metadata(self, indent: Optional[int] = None) -> str:
        return self.get_metadata().model_dump_json(indent=indent)
