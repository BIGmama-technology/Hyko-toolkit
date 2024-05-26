from typing import Any, Callable, Coroutine, Optional, Union

from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI
from hyko_sdk.definitions import ToolkitBase
from hyko_sdk.definitions import ToolkitFunction as _ToolkitFunction
from hyko_sdk.definitions import ToolkitIO as _ToolkitIO
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel
from hyko_sdk.definitions import ToolkitUtils as _ToolkitUtils
from hyko_sdk.models import Icon, MetaData

Definition = Union[
    "ToolkitAPI",
    "ToolkitFunction",
    "ToolkitModel",
    "ToolkitUtils",
    "ToolkitIO",
]


class Registry:
    _registry: dict[str, Definition] = {}
    _callbacks_registry: dict[str, Callable[..., Coroutine[Any, Any, MetaData]]] = {}

    @classmethod
    def register(cls, name: str, definition: Definition):
        cls._registry[name] = definition

    @classmethod
    def get_handler(cls, name: str) -> Definition:
        if name not in cls._registry:
            raise ValueError(f"handler '{name}' not found")
        return cls._registry[name]

    @classmethod
    def get_all_metadata(cls):
        return [definition.get_metadata() for definition in cls._registry.values()]

    @classmethod
    def register_callback(
        cls, id: str, callback: Callable[..., Coroutine[Any, Any, MetaData]]
    ):
        cls._callbacks_registry[id] = callback

    @classmethod
    def get_callback(cls, id: str):
        if id not in cls._callbacks_registry:
            raise ValueError(f"callback {id} not found")
        return cls._callbacks_registry[id]


class AllowCallback(ToolkitBase):
    def callback(self, triggers: list[str], id: str):
        for trigger in triggers:
            field = self.params.get(trigger)
            assert field, "trigger field not found in params"
            field.callback_id = id

        def warper(
            callback: Callable[..., Coroutine[Any, Any, MetaData]],
        ):
            Registry.register_callback(id, callback)

        return warper


class AllowCallbackModel(_ToolkitModel):
    def callback(self, triggers: list[str], id: str):
        for trigger in triggers:
            field = self.startup_params.get(trigger) or self.params.get(trigger)
            assert field, "trigger field not found in startup params"
            field.callback_id = id

        def warper(
            callback: Callable[..., Coroutine[Any, Any, MetaData]],
        ):
            Registry.register_callback(id, callback)

        return warper


class ToolkitIO(_ToolkitIO, AllowCallback):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        cost: int = 0,
        icon: Optional[Icon] = "io",
    ):
        super().__init__(
            name=name, task=task, description=description, cost=cost, icon=icon
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitAPI(_ToolkitAPI):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        cost: int,
        icon: Optional[Icon] = "apis",
    ):
        super().__init__(
            name=name, task=task, description=description, cost=cost, icon=icon
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitUtils(_ToolkitUtils):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        cost: int,
        icon: Optional[Icon] = "utils",
    ):
        super().__init__(
            name=name, task=task, description=description, cost=cost, icon=icon
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitFunction(_ToolkitFunction):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        absolute_dockerfile_path: str,
        docker_context: str,
        cost: int,
        icon: Optional[Icon] = "functions",
    ):
        super().__init__(
            name=name,
            task=task,
            cost=cost,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
            icon=icon,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitModel(AllowCallbackModel):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        absolute_dockerfile_path: str,
        docker_context: str,
        cost: int,
        icon: Optional[Icon] = "models",
    ):
        super().__init__(
            name=name,
            task=task,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
            cost=cost,
            icon=icon,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)
