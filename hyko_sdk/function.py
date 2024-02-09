import json
from typing import Any, Callable, Coroutine, Optional, Type, TypeVar

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hyko_sdk.metadata import CoreModel, HykoJsonSchema, MetaDataBase
from hyko_sdk.utils import to_friendly_types

InputsType = TypeVar("InputsType", bound="BaseModel")
ParamsType = TypeVar("ParamsType", bound="BaseModel")
OutputsType = TypeVar("OutputsType", bound="BaseModel")

OnStartupFuncType = Callable[[ParamsType], Coroutine[Any, Any, None]]
OnShutdownFuncType = Callable[[], Coroutine[Any, Any, None]]
OnExecuteFuncType = Callable[[InputsType, ParamsType], Coroutine[Any, Any, OutputsType]]


class SDKFunction(FastAPI):
    __metadata__: MetaDataBase

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
        self.startup_params: Type[BaseModel] = CoreModel
        self.started: bool = False

    def set_input(self, cls: Any):
        self.inputs = cls
        return cls

    def set_output(self, cls: Any):
        self.outputs = cls
        return cls

    def set_param(self, cls: Any):
        self.params = cls
        return cls

    def set_startup_params(self, cls: Any):
        self.startup_params = cls
        return cls

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

    def get_metadata(self) -> MetaDataBase:
        startup_params_json_schema = self.startup_params.model_json_schema()
        inputs_json_schema = self.inputs.model_json_schema()
        params_json_schema = self.params.model_json_schema()
        outputs_json_schema = self.outputs.model_json_schema()

        return MetaDataBase(
            description=self.description,
            inputs=HykoJsonSchema(
                **inputs_json_schema,
                friendly_types=to_friendly_types(self.inputs),
            ),
            startup_params=HykoJsonSchema(
                **startup_params_json_schema,
                friendly_types=to_friendly_types(self.startup_params),
            ),
            params=HykoJsonSchema(
                **params_json_schema,
                friendly_types=to_friendly_types(self.params),
            ),
            outputs=HykoJsonSchema(
                **outputs_json_schema,
                friendly_types=to_friendly_types(self.outputs),
            ),
        )

    def dump_metadata(self, indent: Optional[int] = None) -> str:
        return self.get_metadata().model_dump_json(
            indent=indent,
            exclude_none=True,
            exclude_defaults=True,
        )
