from typing import Union

from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI
from hyko_sdk.definitions import ToolkitFunction as _ToolkitFunction
from hyko_sdk.definitions import ToolkitIO as _ToolkitIO
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel
from hyko_sdk.definitions import ToolkitUtils as _ToolkitUtils

Definition = Union[
    "ToolkitAPI", "ToolkitFunction", "ToolkitModel", "ToolkitUtils", "ToolkitIO"
]


class Registry:
    _registry: dict[str, Definition] = {}

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


class ToolkitIO(_ToolkitIO):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


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
