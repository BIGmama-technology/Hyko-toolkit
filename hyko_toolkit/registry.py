from typing import Any, Callable, Coroutine, Union
from uuid import UUID, uuid4

from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI
from hyko_sdk.definitions import ToolkitFunction as _ToolkitFunction
from hyko_sdk.definitions import ToolkitIO as _ToolkitIO
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel
from hyko_sdk.definitions import ToolkitUtils as _ToolkitUtils
from hyko_sdk.models import MetaDataBase

Definition = Union[
    "ToolkitAPI", "ToolkitFunction", "ToolkitModel", "ToolkitUtils", "ToolkitIO"
]


class Registry:
    _registry: dict[str, Definition] = {}
    _callbacks_registry: dict[
        UUID, Callable[..., Coroutine[Any, Any, MetaDataBase]]
    ] = {}

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
        cls, id: UUID, callback: Callable[..., Coroutine[Any, Any, MetaDataBase]]
    ):
        cls._callbacks_registry[id] = callback

    @classmethod
    def get_callback(cls, id: UUID):
        if id not in cls._callbacks_registry:
            raise ValueError(f"callback '{id}' not found")
        return cls._callbacks_registry[id]


class ToolkitIO(_ToolkitIO):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)

    def callback(self, trigger: str, id: UUID = uuid4()):
        field = self.params.get(trigger)

        assert field, "trigger field not found in params"

        field.callback_id = id

        def warper(
            callback: Callable[..., Coroutine[Any, Any, MetaDataBase]],
        ):
            Registry.register_callback(id, callback)

        return warper


class ToolkitAPI(_ToolkitAPI):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitUtils(_ToolkitUtils):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
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
    ):
        super().__init__(
            name=name,
            task=task,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitModel(_ToolkitModel):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        absolute_dockerfile_path: str,
        docker_context: str,
    ):
        super().__init__(
            name=name,
            task=task,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)
