import json
import subprocess
from typing import Any, Callable, Coroutine, Type, TypeVar

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hyko_sdk.exceptions import BuildError, PushError
from hyko_sdk.metadata import (
    Category,
    HykoJsonSchema,
    MetaDataBase,
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

    def get_metadata(self) -> MetaDataBase:
        return self.get_base_metadata()

    def dump_metadata(self, **kwargs: Any) -> str:
        metadata = MetaDataBase(
            **self.get_metadata().model_dump(exclude_none=True),
            **kwargs,
        )
        return metadata.model_dump_json(
            exclude_none=True,
            exclude_defaults=True,
            by_alias=True,
        )

    def write(self, host: str, username: str, password: str, **kwargs: Any):
        import httpx

        response = httpx.post(
            f"https://api.{host}/toolkit/write",
            content=self.dump_metadata(**kwargs),
            auth=httpx.BasicAuth(username, password),
            verify=False if host == "traefik.me" else True,
        )

        if response.status_code != 200:
            raise BaseException("failed to write to hyko db.")

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

    def build(self, dockerfile_path: str, image_name: str):
        try:
            subprocess.run(
                f"docker build -t {image_name} -f {dockerfile_path} .".split(" "),
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise BuildError(
                self.name,
                "Failed to build function docker image.",
            ) from e

    def push(self, image_name: str):
        try:
            subprocess.run(
                f"docker push {image_name}".split(" "),
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise PushError(
                self.name,
                "Failed to push to docker registry.",
            ) from e

    def deploy(self, host: str, username: str, password: str, **kwargs: Any):
        image_name = (
            f"registry.{host}/{self.category.value}/{self.task}/{self.name}:latest"
        )
        dockerfile_path = kwargs.get("dockerfile_path")
        assert dockerfile_path, "docker file path missing"

        self.build(dockerfile_path, image_name)
        self.push(image_name)
        self.write(host, username, password, image=image_name)


class ToolkitModel(ToolkitFunction):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        self.category = Category.MODEL
        self.started: bool = False

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

    def get_metadata(self):
        base_metadata = self.get_base_metadata()

        return MetaDataBase(
            **base_metadata.model_dump(exclude_none=True),
            startup_params=self.startup_params,
        )
