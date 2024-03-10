import json
import subprocess
from typing import Any, Callable, Coroutine, Type, TypeVar

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hyko_sdk.models import (
    Category,
    FunctionMetaData,
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
        desc: str,
    ):
        self.category: Category = Category.FUNCTION
        self.desc = desc
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

    def get_base_metadata(self):
        return MetaDataBase(
            category=self.category,
            name=self.name,
            task=self.task,
            description=self.desc,
            inputs=self.inputs,
            params=self.params,
            outputs=self.outputs,
        )

    def dump_metadata(
        self,
    ) -> str:
        metadata = MetaDataBase(
            **self.get_base_metadata().model_dump(exclude_none=True),
        )
        return metadata.model_dump_json(
            exclude_none=True,
            by_alias=True,
        )

    def write(self, host: str, username: str, password: str):
        import httpx

        response = httpx.post(
            f"https://api.{host}/toolkit/write",
            content=self.dump_metadata(),
            auth=httpx.BasicAuth(username, password),
            verify=False if host == "traefik.me" else True,
        )

        if response.status_code != 200:
            raise BaseException(
                f"Failed to write to hyko db. Error code {response.status_code}"
            )

    def deploy(self, host: str, username: str, password: str, **kwargs: Any):
        self.write(host, username, password)


class ToolkitFunction(ToolkitBase, FastAPI):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
    ):
        ToolkitBase.__init__(self, name, task, description)
        FastAPI.__init__(self)
        self.category = Category.FUNCTION

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

    def build(
        self,
        dockerfile_path: str,
    ):
        try:
            subprocess.run(
                f"docker build -t {self.image_name} -f {dockerfile_path} .".split(" "),
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise BaseException(
                "Failed to build function docker image.",
            ) from e

    def push(self):
        try:
            subprocess.run(
                f"docker push {self.image_name}".split(" "),
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise BaseException(
                "Failed to push to docker registry.",
            ) from e

    def deploy(self, host: str, username: str, password: str, **kwargs: Any):
        self.image_name = (
            f"registry.{host}/{self.category.value}/{self.task}/{self.name}:latest"
        )
        dockerfile_path = kwargs.get("dockerfile_path")
        assert dockerfile_path, "docker file path missing"

        self.build(dockerfile_path)
        self.push()
        self.write(host, username, password)

    def dump_metadata(self) -> str:
        base_metadata = self.get_base_metadata()
        metadata = FunctionMetaData(
            **base_metadata.model_dump(exclude_none=True),
            image=self.image_name,
        )
        return metadata.model_dump_json(
            exclude_none=True,
            by_alias=True,
        )


class ToolkitModel(ToolkitFunction):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        self.category = Category.MODEL
        self.started: bool = False
        self.startup_params = None

    def set_startup_params(self, model: T) -> T:
        self.startup_params = HykoJsonSchema(
            **model.model_json_schema(),
            friendly_types=to_friendly_types(model),
        )
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

    def dump_metadata(self) -> str:
        base_metadata = self.get_base_metadata()
        metadata = ModelMetaData(
            **base_metadata.model_dump(exclude_none=True),
            image=self.image_name,
            startup_params=self.startup_params,
        )
        return metadata.model_dump_json(
            exclude_none=True,
            by_alias=True,
        )
