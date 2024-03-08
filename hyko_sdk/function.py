import json
from typing import Any, Callable, Coroutine, Type, TypeVar

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hyko_sdk.metadata import (
    FunctionMetadata,
    HykoJsonSchema,
    MetaDataBase,
    ModelMetaData,
)
from hyko_sdk.utils import to_friendly_types

InputsType = TypeVar("InputsType", bound="BaseModel")
ParamsType = TypeVar("ParamsType", bound="BaseModel")
OutputsType = TypeVar("OutputsType", bound="BaseModel")

OnStartupFuncType = Callable[[ParamsType], Coroutine[Any, Any, None]]
OnShutdownFuncType = Callable[[], Coroutine[Any, Any, None]]
OnExecuteFuncType = Callable[[InputsType, ParamsType], Coroutine[Any, Any, OutputsType]]

T = TypeVar("T", bound=Type[BaseModel])


class ToolkitBase:
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
    ):
        self.description = description
        self.name = name
        self.task = task
        self.inputs = None
        self.outputs = None
        self.params = None

    def set_input(self, model: T) -> T:
        self.inputs = HykoJsonSchema(
            **model.model_json_schema(),
            friendly_types=to_friendly_types(model),
        )
        return model

    def set_output(self, model: T) -> T:
        self.outputs = HykoJsonSchema(
            **model.model_json_schema(),
            friendly_types=to_friendly_types(model),
        )
        return model

    def set_param(self, model: T) -> T:
        self.params = HykoJsonSchema(
            **model.model_json_schema(),
            friendly_types=to_friendly_types(model),
        )
        return model

    def get_base_metadata(self) -> MetaDataBase:
        return MetaDataBase(
            description=self.description,
            name=self.name,
            task=self.task,
            inputs=self.inputs,
            params=self.params,
            outputs=self.outputs,
        )

    def get_metadata(self) -> BaseModel:
        return self.get_base_metadata()

    def dump_metadata(self) -> str:
        return self.get_metadata().model_dump_json(
            exclude_none=True,
            exclude_defaults=True,
            by_alias=True,
        )


class ToolkitFunction(ToolkitBase, FastAPI):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        **kwargs: Any,
    ):
        ToolkitBase.__init__(self, name, task, description)
        FastAPI.__init__(self, **kwargs)

    def on_execute(self, f: OnExecuteFuncType[InputsType, ParamsType, OutputsType]):
        async def wrapper(
            inputs: InputsType,
            params: ParamsType,
        ) -> JSONResponse:
            try:
                outputs = await f(inputs, params)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.__repr__(),
                ) from e

            return JSONResponse(content=json.loads(outputs.model_dump_json()))

        wrapper.__annotations__ = f.__annotations__

        return self.post("/execute")(wrapper)

    def get_metadata(self) -> BaseModel:
        return FunctionMetadata(**self.get_base_metadata().model_dump())


class ToolkitModel(ToolkitFunction):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        self.started: bool = False

    def set_startup_params(self, model: T) -> T:
        self.startup_params = model
        return model

    def on_startup(self, f: OnStartupFuncType[ParamsType]):
        async def wrapper(startup_params: ParamsType):
            if not self.started:
                try:
                    await f(startup_params)
                    self.started = True
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=e.__repr__(),
                    ) from e

        wrapper.__annotations__ = f.__annotations__
        return self.post("/startup")(wrapper)

    def on_shutdown(self, f: OnShutdownFuncType) -> OnShutdownFuncType:
        return self.on_event("shutdown")(f)

    def get_metadata(self) -> ModelMetaData:
        base_metadata = self.get_base_metadata()
        startup_params_json_schema = self.startup_params.model_json_schema()

        return ModelMetaData(
            **base_metadata.model_dump(),
            startup_params=HykoJsonSchema(
                **startup_params_json_schema,
                friendly_types=to_friendly_types(self.startup_params),
            ),
        )
