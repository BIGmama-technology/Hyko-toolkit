from typing import Union

from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI
from hyko_sdk.definitions import ToolkitFunction as _ToolkitFunction
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel

Definition = Union[
    _ToolkitAPI,
    _ToolkitFunction,
    _ToolkitModel,
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
        return [api.get_metadata() for api in cls._registry.values()]


class ToolkitAPI(_ToolkitAPI):
    def __init__(self, name: str, task: str, description: str):
        super().__init__(name=name, task=task, description=description)
        # Automatically register the instance upon creation
        Registry.register(name, self)


class ToolkitUtils(ToolkitAPI):
    pass


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
        Registry.register(name, self)


class ToolkitModel(ToolkitFunction):
    pass
