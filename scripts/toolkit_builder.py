import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME, ADMIN_PASSWORD = (
    os.getenv("ADMIN_USERNAME"),
    os.getenv("ADMIN_PASSWORD"),
)
assert ADMIN_USERNAME and ADMIN_PASSWORD, "no username and password found in .env"


SKIP_FOLDERS = ["__pycache__", "venv"]

all_built_functions: list[str] = []
failed_functions: list[str] = []


def deploy(path: str, dockerfile_path: str, absolute_dockerfile_path: str, host: str):
    try:
        subprocess.run(
            "poetry run python -c".split(" ")
            + [
                f"""from metadata import func;func.deploy(host="{host}", username="{ADMIN_USERNAME}", password="{ADMIN_PASSWORD}", dockerfile_path="{dockerfile_path}", docker_context="{path}", absolute_dockerfile_path="{absolute_dockerfile_path}")"""
            ],
            cwd=path,
            check=True,
        )
    except subprocess.CalledProcessError:
        failed_functions.append(path)


def walk_directory(path: str, host: str, dockerfile_path: str):
    ls = os.listdir(path)

    if "Dockerfile" in ls:
        dockerfile_path = "Dockerfile"

    if "metadata.py" in ls and ".hykoignore" not in ls:
        all_built_functions.append(path)
        absolute_dockerfile_path = path

        for _ in dockerfile_path.split("../")[:-1]:
            absolute_dockerfile_path = "/".join(
                absolute_dockerfile_path.split("/")[:-1]
            )
        absolute_dockerfile_path = absolute_dockerfile_path + "/Dockerfile"

        deploy(
            path,
            dockerfile_path,
            absolute_dockerfile_path,
            host,
        )

    else:
        dockerfile_path = "../" + dockerfile_path
        for sub_folder in ls:
            sub_folder_path = os.path.join(path, sub_folder)

            if sub_folder in SKIP_FOLDERS:
                continue

            if not os.path.isdir(sub_folder_path):
                continue

            walk_directory(sub_folder_path, host, dockerfile_path)


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
        "--host",
        default="traefik.me",
        help="Set a custom host name",
        type=str,
        choices=["traefik.me", "stage.hyko.ai", "hyko.ai"],
    )
    parser.add_argument(
        "--base",
        default=False,
        help="Build only base images.",
        action="store_true",
    )
    parser.add_argument(
        "--push",
        default=False,
        help="Build only base images.",
        action="store_true",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    directories = args.dir
    host = args.host
    base = args.base
    push = args.push

    dockerfiles = os.listdir("./common_dockerfiles")
    for file in dockerfiles:
        image = file.removesuffix(".Dockerfile")
        subprocess.run(
            f"docker build -t {ADMIN_USERNAME}/{image}:latest -f common_dockerfiles/{file} .".split(
                " "
            ),
            check=True,
        )
        if push:
            subprocess.run(
                f"docker push {ADMIN_USERNAME}/{image}:latest".split(" "),
                check=True,
            )

    if not base:
        for dir in directories:
            walk_directory(dir, host, dockerfile_path=".")

        successful_count = len(all_built_functions) - len(failed_functions)

        print(
            "No functions were built"
            if len(all_built_functions) == 0
            else f"Successfully built: {successful_count} function. Failed to build: {len(failed_functions)} function"
        )
        for path in failed_functions:
            print(f"Error while building: {path}")
