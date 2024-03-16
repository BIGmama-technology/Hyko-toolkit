import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

USERNAME, PASSWORD = os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
assert USERNAME and PASSWORD, "no username and password found in .env"


SKIP_FOLDERS = ["__pycache__", "venv"]

all_built_functions: list[str] = []
failed_functions: list[str] = []


def deploy(path: str, dockerfile_path: str, host: str):
    try:
        subprocess.run(
            "poetry run python -c".split(" ")
            + [
                f"""from metadata import func;func.deploy(host="{host}", username="{USERNAME}", password="{PASSWORD}", dockerfile_path="{dockerfile_path}")"""
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
        deploy(path, dockerfile_path, host)

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
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    directories = args.dir
    host = args.host

    print("login to registry")
    subprocess.run(
        f"docker login registry.{host} -u {USERNAME} -p {PASSWORD}".split(" "),
        check=True,
    )

    dockerfiles = os.listdir("./common_dockerfiles")
    for file in dockerfiles:
        image = file.removesuffix(".Dockerfile")
        subprocess.run(
            f"docker build -t {image}:latest -f common_dockerfiles/{file} .".split(" "),
            check=True,
        )


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
