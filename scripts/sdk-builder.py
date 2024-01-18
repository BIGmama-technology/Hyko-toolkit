import argparse
import json
import os
import random
import string
import subprocess
import sys
import threading
from typing import Literal

import pydantic

from hyko_sdk.metadata import Category, IOPortType, MetaData, MetaDataBase, Property
from hyko_sdk.utils import metadata_to_docker_label

skip_folders = ["__pycache__", "venv"]
all_built_functions: list[str] = []
threads: list[threading.Thread] = []


class FunctionBuildError(RuntimeError):
    function_name: str
    reason: str

    def __init__(self, function_name: str, reason: str) -> None:
        self.function_name = function_name
        self.reason = reason
        super().__init__(f"Error while building {function_name}, reason: {reason}")


class NotAllowedTypesError(FunctionBuildError):
    def __init__(
        self,
        function_name: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            function_name,
            f"Dictionnary or None types are not allowed: {field_type} name: {field_name}",
        )


class UnionNotAllowedError(FunctionBuildError):
    def __init__(
        self,
        function_name: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            function_name,
            f"Union is not allowed in {field_type} ports: {field_type} name: {field_name}",
        )


class EnumNotAllowedError(FunctionBuildError):
    def __init__(
        self,
        function_name: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            function_name,
            f"Enum is not allowed in {field_type} ports: {field_type} name: {field_name}",
        )


class UnknownArrayItemsTypeError(FunctionBuildError):
    def __init__(
        self,
        function_name: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            function_name,
            f"list[Unknown] is not allowed. {field_type} name: {field_name}",
        )


failed_functions: list[FunctionBuildError] = []
failed_functions_lock = threading.Lock()


def check_property(  # noqa: C901
    function_name: str,
    field: Property,
    field_name: str,
    field_type: Literal["input", "output", "param"],
    allow_union: bool,
    allow_enum: bool,
):
    if field.type == IOPortType.OBJECT or field.type == IOPortType.NULL:
        raise NotAllowedTypesError(function_name, field_name, field_type)

    if not allow_union:
        if field.anyOf is not None:
            if len(field.anyOf) == 2 and (
                field.anyOf[0].type is not None
                and field.anyOf[0].type == IOPortType.NULL
                or field.anyOf[1].type is not None
                and field.anyOf[1].type == IOPortType.NULL
            ):
                """This is to allow Optional[Type]"""
                pass
            else:
                raise UnionNotAllowedError(function_name, field_name, field_type)

    if not allow_enum:
        if field.ref is not None:
            raise EnumNotAllowedError(function_name, field_name, field_type)

    if field.type == IOPortType.ARRAY:
        if field.items is not None:
            check_property(
                function_name,
                field.items,
                field_name,
                field_type,
                allow_union,
                allow_enum,
            )

        elif field.prefixItems is not None:
            for item in field.prefixItems:
                check_property(
                    function_name, item, field_name, field_type, allow_union, allow_enum
                )
        else:
            raise UnknownArrayItemsTypeError(function_name, field_name, field_type)


def process_function_dir(path: str, registry_host: str):  # noqa: C901
    """Path has to be a valid path with no spaces in it"""
    path = path.lstrip("./")
    path = path.rstrip("/")

    splitted = path.split("/")
    try:
        try:
            function_name = splitted[-1]
            task = splitted[-2]
            category = Category.get_enum_from_string(splitted[1])

        except (IndexError, ValueError) as err:
            raise FunctionBuildError(
                path,
                f"""Make sure your function follows the correct folder structure:
                hyko_toolkit/category/../../task/fn_name/ current allowed categories {[c.value for c in Category]}""",
            ) from err

        start_token = "START_TOKEN" + "".join(
            random.choice(string.ascii_letters) for _ in range(16)
        )

        try:
            metadata_process = subprocess.run(
                "poetry run python -c".split(" ")
                + [
                    f"from metadata import func;print('{start_token}');print(func.dump_metadata())"
                ],
                cwd=path,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(e.stdout.decode())
            raise FunctionBuildError(
                function_name,
                "Error while extracting metadata",
            ) from e

        splitted = metadata_process.stdout.decode().split(start_token)

        if len(splitted) == 2:
            metadata = splitted[1]
        elif len(splitted) == 1:
            metadata = splitted[0]
        else:
            print("Probably an error happen in while catching stdout from metadata")
            return

        image_name = f"{registry_host}/{category.lower()}/{task.lower()}/{function_name.lower()}:latest"
        try:
            metadata = MetaDataBase(**json.loads(metadata))
            metadata = MetaData(
                **metadata.model_dump(
                    exclude_unset=True, exclude_none=True, by_alias=True
                ),
                image=image_name,
                name=function_name,
                category=category,
                task=task,
            )
        except pydantic.ValidationError as e:
            raise FunctionBuildError(function_name, "Invalid Function MetaData") from e

        fields: list[str] = []

        # INPUTS
        for field_name, field in metadata.inputs.properties.items():
            check_property(
                function_name,
                field,
                field_name,
                "input",
                allow_union=True,
                allow_enum=False,
            )
            fields.append(field_name)

        # PARAMETERS
        for field_name, field in metadata.params.properties.items():
            check_property(
                function_name,
                field,
                field_name,
                "param",
                allow_union=False,
                allow_enum=True,
            )
            fields.append(field_name)

        # OUTPUTS
        for field_name, field in metadata.outputs.properties.items():
            check_property(
                function_name,
                field,
                field_name,
                "output",
                allow_union=False,
                allow_enum=False,
            )
            fields.append(field_name)

        unique_fields = set(fields)
        if len(unique_fields) != len(fields):
            raise FunctionBuildError(
                function_name,
                "Port name must be unique within a function (across inputs, params and outputs)",
            )

        print("Building...")
        build_cmd = "docker build "
        build_cmd += f"--build-arg CATEGORY={category} "
        build_cmd += f"--build-arg FUNCTION_NAME={function_name} "
        build_cmd += f"-t {image_name} "
        build_cmd += f"""--label metadata="{metadata_to_docker_label(metadata)}" """
        build_cmd += f"./{path}"
        try:
            subprocess.run(["/bin/sh", "-c", build_cmd], check=True)
        except subprocess.CalledProcessError as e:
            raise FunctionBuildError(
                function_name,
                "Failed to build function main docker image",
            ) from e

        print("Pushing...")
        try:
            subprocess.run(f"docker push {image_name}".split(" "), check=True)
        except subprocess.CalledProcessError as e:
            raise FunctionBuildError(
                function_name,
                f"Failed to push to docker registry {registry_host}",
            ) from e

        if registry_host != "registry.traefik.me":
            print("Removing the image")
            try:
                subprocess.run(f"docker rmi {image_name}".split(" "), check=True)
            except subprocess.CalledProcessError as e:
                raise FunctionBuildError(
                    function_name,
                    "Failed to remove built image from host",
                ) from e

    except FunctionBuildError as e:
        failed_functions_lock.acquire()
        failed_functions.append(e)
        failed_functions_lock.release()


def walk_directory(
    path: str, threaded: bool, registry_host: str, enable_cuda: bool = False
):
    ls = os.listdir(path)

    if (
        all(f in ls for f in ["main.py", "metadata.py", "Dockerfile"])
        and ".hykoignore" not in ls
    ):
        if not enable_cuda:
            with open(path + "/Dockerfile") as f:
                dockerfile = f.read()
                if "cuda" in dockerfile:
                    return

        all_built_functions.append(path)

        if threaded:
            thread = threading.Thread(
                target=process_function_dir, args=[path, registry_host]
            )
            thread.start()
            threads.append(thread)
        else:
            process_function_dir(path, registry_host)

    else:
        for sub_folder in ls:
            if sub_folder in skip_folders:
                continue

            if not os.path.isdir(path + "/" + sub_folder):
                continue

            walk_directory(
                path + "/" + sub_folder, threaded, registry_host, enable_cuda
            )


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This script will build an image of your functions and push them to Hyko registry"
    )
    parser.add_argument(
        "--dir",
        default=["./hyko_toolkit"],
        nargs="+",
        help="A list of functions or models paths",
        type=str,
    )
    parser.add_argument("--threaded", action="store_true", help="Enable threaded mode")
    parser.add_argument("--cuda", action="store_true", help="Re-build torch-cuda image")
    parser.add_argument(
        "--registry",
        default="registry.traefik.me",
        help="Set a custom registry host",
        type=str,
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    directories = args.dir
    threaded = args.threaded
    registry_host = args.registry
    enable_cuda = args.cuda

    subprocess.run(
        "docker build -t hyko-sdk:latest -f common_dockerfiles/hyko-sdk.Dockerfile .".split(
            " "
        )
    )
    if enable_cuda:
        subprocess.run(
            "docker build -t torch-cuda:latest -f common_dockerfiles/torch-cuda.Dockerfile .".split(
                " "
            )
        )

    for dir in directories:
        dir = dir.rstrip("/")
        walk_directory(dir, threaded, registry_host, enable_cuda)

    if threaded:
        for thread in threads:
            thread.join()

    successful_count = len(all_built_functions) - len(failed_functions)
    print(
        f"Successfully built: {successful_count} function. Failed to build: {len(failed_functions)} function"
    )
    for fn in failed_functions:
        print(f"ERROR WHILE BUILDING: {fn.function_name} REASON: {fn.reason}")
