from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI
from hyko_sdk.definitions import ToolkitFunction as _ToolkitFunction
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel


class APIRegistry:
    _registry: dict[str, _ToolkitAPI] = {}

    @classmethod
    def register(cls, name: str, api: _ToolkitAPI):
        cls._registry[name] = api

    @classmethod
    def get_handler(cls, name: str) -> _ToolkitAPI:
        if name not in cls._registry:
            raise ValueError(f"API handler '{name}' not found")
        return cls._registry[name]

    @classmethod
    def get_apis(cls):
        return [api.get_metadata() for api in cls._registry.values()]


class ToolkitAPI(_ToolkitAPI):
    def __init__(self, name: str, task: str, description: str):
        # Automatically register the instance upon creation
        super().__init__(name=name, task=task, description=description)
        APIRegistry.register(name, self)


#############################################
class ModelRegistry:
    _registry: dict[str, _ToolkitModel] = {}

    @classmethod
    def register(cls, name: str, api: _ToolkitModel):
        cls._registry[name] = api

    @classmethod
    def get_models(cls):
        return [model.get_metadata() for model in cls._registry.values()]


class ToolkitModel(_ToolkitModel):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        absolute_dockerfile_path: str,
        docker_context: str,
    ):
        # Automatically register the instance upon creation
        super().__init__(
            name=name,
            task=task,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
        )
        ModelRegistry.register(name, self)


##################################


class FunctionRegistry:
    _registry: dict[str, _ToolkitFunction] = {}

    @classmethod
    def register(cls, name: str, api: _ToolkitFunction):
        cls._registry[name] = api

    @classmethod
    def get_functions(cls):
        return [function.get_metadata() for function in cls._registry.values()]


class ToolkitFunction(_ToolkitFunction):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        absolute_dockerfile_path: str,
        docker_context: str,
    ):
        # Automatically register the instance upon creation
        super().__init__(
            name=name,
            task=task,
            description=description,
            docker_context=docker_context,
            absolute_dockerfile_path=absolute_dockerfile_path,
        )
        FunctionRegistry.register(name, self)
