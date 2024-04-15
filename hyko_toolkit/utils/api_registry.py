from hyko_sdk.definitions import ToolkitUtils as _ToolkitUtils


class UtilsRegistry:
    _registry: dict[str, _ToolkitUtils] = {}

    @classmethod
    def register(cls, name: str, api: _ToolkitUtils):
        cls._registry[name] = api

    @classmethod
    def get_handler(cls, name: str) -> _ToolkitUtils:
        if name not in cls._registry:
            raise ValueError(f"Utils handler '{name}' not found")
        return cls._registry[name]


class ToolkitUtils(_ToolkitUtils):
    def __init__(self, name: str, task: str, description: str):
        # Automatically register the instance upon creation
        super().__init__(name=name, task=task, description=description)
        UtilsRegistry.register(name, self)
