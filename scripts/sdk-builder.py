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

from hyko_sdk.metadata import IOPortType, MetaData, MetaDataBase, Property
from hyko_sdk.utils import metadata_to_docker_label

skip_folders = ["__pycache__", "venv"]
all_built_functions: list[str] = []
threads: list[threading.Thread] = []


class FunctionBuildError(RuntimeError):
    category: str
    function_name: str
    version: str
    reason: str

    def __init__(
        self, category: str, function_name: str, version: str, reason: str
    ) -> None:
        self.category = category
        self.function_name = function_name
        self.version = version
        self.reason = reason
        super().__init__(
            f"Error while building {function_name + ':' + version}. Reason: {reason}"
        )


class NotAllowedTypesError(FunctionBuildError):
    def __init__(
        self,
        category: str,
        function_name: str,
        version: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            category,
            function_name,
            version,
            f"Dictionnary or None types are not allowed: {field_type} name: {field_name}",
        )


class UnionNotAllowedError(FunctionBuildError):
    def __init__(
        self,
        category: str,
        function_name: str,
        version: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            category,
            function_name,
            version,
            f"Union is not allowed in {field_type} ports: {field_type} name: {field_name}",
        )


class EnumNotAllowedError(FunctionBuildError):
    def __init__(
        self,
        category: str,
        function_name: str,
        version: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            category,
            function_name,
            version,
            f"Enum is not allowed in {field_type} ports: {field_type} name: {field_name}",
        )


class UnknownArrayItemsTypeError(FunctionBuildError):
    def __init__(
        self,
        category: str,
        function_name: str,
        version: str,
        field_name: str,
        field_type: Literal["input"] | Literal["output"] | Literal["param"],
    ) -> None:
        super().__init__(
            category,
            function_name,
            version,
            f"list[Unknown] is not allowed. {field_type} name: {field_name}",
        )


failed_functions: list[FunctionBuildError] = []
failed_functions_lock = threading.Lock()


def process_function_dir(path: str, registry_host: str):  # noqa: C901
    """Path has to be a valid path with no spaces in it"""
    path = path.lstrip("./")
    path = path.rstrip("/")

    splitted = path.split("/")
    try:
        if len(splitted) == 2:
            version = splitted[0]
            function_name = splitted[1]
            category = "uncategorized"
        elif len(splitted) > 2:
            version = splitted[-1]
            function_name = splitted[-2]
            category = "/".join(splitted[:-2]).lower()
        else:
            raise FunctionBuildError(
                path,
                "unknown",
                path,
                "Make sure your function follows the correct folder structure: catgeory/fn_name/v1/",
            )

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
                category,
                function_name,
                version,
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

        try:
            metadata = MetaDataBase(**json.loads(metadata))
            metadata = MetaData(
                **metadata.model_dump(
                    exclude_unset=True, exclude_none=True, by_alias=True
                ),
                name=function_name,
                version=version,
                category=category,
            )
        except pydantic.ValidationError as e:
            raise FunctionBuildError(
                category, function_name, version, "Invalid Function MetaData"
            ) from e

        fields: list[str] = []

        def check_property(  # noqa: C901
            field: Property,
            field_name: str,
            field_type: Literal["input", "output", "param"],
            allow_union: bool,
            allow_enum: bool,
        ):
            if field.type == IOPortType.OBJECT or field.type == IOPortType.NULL:
                raise NotAllowedTypesError(
                    category, function_name, version, field_name, field_type
                )

            if not allow_union:
                if field.any_of is not None:
                    if len(field.any_of) == 2 and (
                        field.any_of[0].type is not None
                        and field.any_of[0].type == IOPortType.NULL
                        or field.any_of[1].type is not None
                        and field.any_of[1].type == IOPortType.NULL
                    ):
                        """This is to allow Optional[Type]"""
                        pass
                    else:
                        raise UnionNotAllowedError(
                            category, function_name, version, field_name, field_type
                        )

            if not allow_enum:
                if field.ref is not None:
                    raise EnumNotAllowedError(
                        category, function_name, version, field_name, field_type
                    )

            if field.type == IOPortType.ARRAY:
                if field.items is not None:
                    check_property(
                        field.items, field_name, field_type, allow_union, allow_enum
                    )

                elif field.prefix_items is not None:
                    for item in field.prefix_items:
                        check_property(
                            item, field_name, field_type, allow_union, allow_enum
                        )
                else:
                    raise UnknownArrayItemsTypeError(
                        category, function_name, version, field_name, field_type
                    )

        # INPUTS
        for field_name, field in metadata.inputs.properties.items():
            check_property(
                field, field_name, "input", allow_union=True, allow_enum=False
            )
            fields.append(field_name)

        # PARAMETERS
        for field_name, field in metadata.params.properties.items():
            check_property(
                field, field_name, "param", allow_union=False, allow_enum=True
            )
            fields.append(field_name)

        # OUTPUTS
        for field_name, field in metadata.outputs.properties.items():
            check_property(
                field, field_name, "output", allow_union=False, allow_enum=False
            )
            fields.append(field_name)

        unique_fields = set(fields)
        if len(unique_fields) != len(fields):
            raise FunctionBuildError(
                category,
                function_name,
                version,
                "Port name must be unique within a function (across inputs, params and outputs)",
            )

        print("Building...")
        function_tag = (
            f"{registry_host}/{category.lower()}/{function_name.lower()}:{version}"
        )
        build_cmd = "docker build "
        build_cmd += f"--build-arg CATEGORY={category} "
        build_cmd += f"--build-arg FUNCTION_NAME={function_name} "
        build_cmd += f"-t {function_tag} "
        build_cmd += f"""--label metadata="{metadata_to_docker_label(metadata)}" """
        build_cmd += f"./{path}"
        try:
            subprocess.run(["/bin/sh", "-c", build_cmd], check=True)
        except subprocess.CalledProcessError as e:
            raise FunctionBuildError(
                category,
                function_name,
                version,
                "Failed to build function main docker image",
            ) from e

        print("Pushing...")
        try:
            subprocess.run(f"docker push {function_tag}".split(" "), check=True)
        except subprocess.CalledProcessError as e:
            raise FunctionBuildError(
                category,
                function_name,
                version,
                f"Failed to push to docker registry {registry_host}",
            ) from e

        if registry_host != "registry.traefik.me":
            print("Removing the image")
            try:
                subprocess.run(f"docker rmi {function_tag}".split(" "), check=True)
            except subprocess.CalledProcessError as e:
                raise FunctionBuildError(
                    category,
                    function_name,
                    version,
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
        "--dir", default=["./sdk"], nargs="+", help="A list of function paths", type=str
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
        print(
            f"ERROR WHILE BUILDING: {fn.category}/{fn.function_name}:{fn.version} REASON: {fn.reason}"
        )
