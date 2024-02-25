import argparse
import json
import os
import random
import string
import subprocess
import sys
from dataclasses import dataclass

from pydantic import ValidationError

from hyko_sdk.metadata import Category, MetaData, MetaDataBase
from hyko_sdk.utils import metadata_to_docker_label

SKIP_FOLDERS = ["__pycache__", "venv"]


@dataclass
class BuildError(BaseException):
    function_name: str
    reason: str


all_built_functions: list[str] = []
failed_functions: list[BuildError] = []


def process_function_dir(path: str, dockerfile_path: str, registry_host: str):
    """Path has to be a valid path with no spaces in it"""
    path = os.path.normpath(path)
    splitted = path.split(os.sep)

    try:
        try:
            function_name = splitted[-1]
            task = splitted[-2]
            category = Category.get_enum_from_string(splitted[1])

        except (IndexError, ValueError) as err:
            raise BuildError(
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
            raise BuildError(
                function_name,
                "Error while extracting metadata",
            ) from e

        splitted = metadata_process.stdout.decode().split(start_token)

        assert (
            len(splitted) == 2
        ), "Probably an error happen in while catching stdout from metadata"
        metadata = splitted[1]

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
        except ValidationError as e:
            raise BuildError(function_name, "Invalid Function MetaData") from e

        print("Building...")
        build_cmd = "docker build "
        build_cmd += f"--build-arg CATEGORY={category} "
        build_cmd += f"--build-arg FUNCTION_NAME={function_name} "
        build_cmd += f"-t {image_name} "
        build_cmd += f"""--label metadata="{metadata_to_docker_label(metadata)}" """
        build_cmd += f"-f ./{dockerfile_path} "
        build_cmd += f"./{path}"
        try:
            subprocess.run(["/bin/sh", "-c", build_cmd], check=True)
        except subprocess.CalledProcessError as e:
            raise BuildError(
                function_name,
                "Failed to build function main docker image",
            ) from e

        print("Pushing...")
        try:
            subprocess.run(f"docker push {image_name}".split(" "), check=True)
        except subprocess.CalledProcessError as e:
            raise BuildError(
                function_name,
                f"Failed to push to docker registry {registry_host}",
            ) from e

        if registry_host != "registry.traefik.me":
            print("Removing the image")
            subprocess.run(f"docker rmi {image_name}".split(" "))

    except BuildError as e:
        failed_functions.append(e)


def walk_directory(path: str, registry_host: str, dockerfile_path: str):
    ls = os.listdir(path)

    if "Dockerfile" in ls:
        dockerfile_full_path = os.path.join(path, "Dockerfile")
        dockerfile_path = dockerfile_full_path

    if all(f in ls for f in ["main.py", "metadata.py"]) and ".hykoignore" not in ls:
        all_built_functions.append(path)
        process_function_dir(path, dockerfile_path, registry_host)

    else:
        for sub_folder in ls:
            sub_folder_path = os.path.join(path, sub_folder)

            if sub_folder in SKIP_FOLDERS:
                continue

            if not os.path.isdir(sub_folder_path):
                continue

            walk_directory(sub_folder_path, registry_host, dockerfile_path)


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
    registry_host = args.registry

    print("build hyko_sdk image")

    subprocess.run(
        "docker build -t hyko-sdk:latest -f common_dockerfiles/hyko-sdk.Dockerfile .".split(
            " "
        ),
        check=True,
    )

    for dir in directories:
        walk_directory(dir, registry_host, dockerfile_path=".")

    successful_count = len(all_built_functions) - len(failed_functions)

    print(
        "no built functions"
        if len(all_built_functions) == 0
        else f"Successfully built: {successful_count} function. Failed to build: {len(failed_functions)} function"
    )
    for fn in failed_functions:
        print(f"ERROR WHILE BUILDING: {fn.function_name} REASON: {fn.reason}")
