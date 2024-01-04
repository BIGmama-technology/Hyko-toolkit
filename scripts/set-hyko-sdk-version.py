import os
import sys
from typing import List


def walk_directory(root_path: str, pre_categories: List[str]):
    print(f"Walking {root_path}/{'/'.join(pre_categories)}")  # noqa: T201

    ls = os.listdir(root_path + "/" + "/".join(pre_categories))
    if "main.py" in ls and "Dockerfile" in ls:
        output = ""
        with open(root_path + "/" + "/".join(pre_categories) + "/Dockerfile") as f:
            text = f.readlines()
            if "cuda" in text[0]:
                for line in text:
                    if "RUN pip install uvicorn hyko_sdk==" in line:
                        line = "RUN pip install uvicorn hyko_sdk==" + sys.argv[1] + "\n"
                    output += line
        if output != "":
            with open(
                root_path + "/" + "/".join(pre_categories) + "/Dockerfile", "w"
            ) as f:
                f.write(output)

    for sub_folder in ls:
        if not os.path.isdir(
            root_path + "/" + "/".join(pre_categories) + "/" + sub_folder
        ):
            continue

        walk_directory(
            root_path=root_path, pre_categories=pre_categories + [sub_folder]
        )


if __name__ == "__main__":
    walk_directory("./sdk", [])
    output = ""
    with open("common_dockerfiles/hyko-sdk.Dockerfile") as f:
        text = f.readlines()
        for line in text:
            if "RUN pip install uvicorn hyko_sdk==" in line:
                line = "RUN pip install uvicorn hyko_sdk==" + sys.argv[1] + "\n"
            output += line
    if output != "":
        with open("common_dockerfiles/hyko-sdk.Dockerfile", "w") as f:
            f.write(output)
