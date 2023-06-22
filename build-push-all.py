import os
import subprocess
from hyko_sdk.metadata import MetaData
import json


def metadata_to_labels(meta: MetaData) -> dict[str, float | int | str | bool]:
    labels = {}

    labels["HYKO_SDK_NAME"] = meta.name
    labels["HYKO_SDK_DESCRIPTION"] = meta.description
    labels["HYKO_SDK_VERSION"] = meta.version
    # labels["HYKO_SDK_CATEGORY"] = meta.category

    i = 0

    for inp in meta.inputs:
        labels[f"HYKO_SDK_INPUT_{i}_NAME"] = inp.name
        if inp.description is not None:
            labels[f"HYKO_SDK_INPUT_{i}_DESCRIPTION"] = inp.description
        labels[f"HYKO_SDK_INPUT_{i}_TYPE"] = inp.type
        labels[f"HYKO_SDK_INPUT_{i}_REQUIRED"] = inp.required
        if inp.default is not None:
            labels[f"HYKO_SDK_INPUT_{i}_DEFAULT"] = inp.default
        i += 1

    i = 0

    for param in meta.params:
        labels[f"HYKO_SDK_PARAM_{i}_NAME"] = param.name
        if param.description is not None:
            labels[f"HYKO_SDK_PARAM_{i}_DESCRIPTION"] = param.description
        labels[f"HYKO_SDK_PARAM_{i}_TYPE"] = param.type
        labels[f"HYKO_SDK_PARAM_{i}_REQUIRED"] = param.required
        if param.default is not None:
            labels[f"HYKO_SDK_PARAM_{i}_DEFAULT"] = param.default
        i += 1

    i = 0

    for out in meta.outputs:
        labels[f"HYKO_SDK_OUTPUT_{i}_NAME"] = out.name
        if out.description is not None:
            labels[f"HYKO_SDK_OUTPUT_{i}_DESCRIPTION"] = out.description
        labels[f"HYKO_SDK_OUTPUT_{i}_TYPE"] = out.type
        labels[f"HYKO_SDK_OUTPUT_{i}_REQUIRED"] = out.required
        if out.default is not None:
            labels[f"HYKO_SDK_OUTPUT_{i}_DEFAULT"] = out.default
        i += 1

    return labels


registry_host = "registry.localhost"


def process_function_dir(root_path: str, pre_categories: list[str]):
    
    if len(pre_categories) < 2:
        return
    
    categories_prefix = '/'.join(pre_categories[:-1])
    function_name = pre_categories[-1]
    
    print()
    print(f"Processing function: {root_path=}, {categories_prefix=} {function_name=}")


    print("Building metadata...")
    subprocess.run(f"docker build --target metadata -t {registry_host}/sdk/{categories_prefix.lower()}/{function_name.lower()}:metadata ./sdk/{categories_prefix}/{function_name}".split(' '))

    metadata_process = subprocess.run(f"docker run -it {registry_host}/sdk/{categories_prefix.lower()}/{function_name.lower()}:metadata".split(' '), capture_output=True)
    meta_data = metadata_process.stdout.decode()
    print(meta_data)
    labels = metadata_to_labels(MetaData(**json.loads(meta_data)))
    labels["HYKO_SDK_CATEGORY"] = categories_prefix

    print()
    print("Building...")

    build_cmd = f"docker build "
    build_cmd += f"--build-arg CATEGORY={categories_prefix} "
    build_cmd += f"--build-arg FUNCTION_NAME={function_name} "
    build_cmd += f"--target main "
    build_cmd += f"-t {registry_host}/sdk/{categories_prefix.lower()}/{function_name.lower()}:latest "
    for label_name, label_val in labels.items():
        build_cmd += f'--label {label_name}="{label_val}" '
    build_cmd += f"./sdk/{categories_prefix}/{function_name}"

    print(build_cmd.split(' '))

    subprocess.run(["/bin/sh", "-c", build_cmd])


    print()
    print("Pushing...")

    subprocess.run(f"docker push {registry_host}/sdk/{categories_prefix.lower()}/{function_name.lower()}:latest".split(' '))



skip_folders = ["common", "__pycache__", "venv", "math"]


def walk_directory(root_path: str, pre_categories: list[str]):

    print(f"Walking {root_path}/{'/'.join(pre_categories)}")

    ls = os.listdir(root_path + '/' + '/'.join(pre_categories))

    if "main.py" in ls and "config.py" in ls:
        process_function_dir(root_path=root_path, pre_categories=pre_categories)

    for sub_folder in ls:

        if sub_folder in skip_folders:
            continue
        
        if not os.path.isdir(root_path + '/' + '/'.join(pre_categories) + '/' + sub_folder):
            continue
        
        walk_directory(root_path=root_path, pre_categories=pre_categories + [sub_folder])



if __name__ == "__main__":

    subprocess.run(f"docker build -t hyko-sdk:latest -f common_dockerfiles/hyko-sdk.Dockerfile .".split(" "))
    subprocess.run(f"docker build -t torch-cuda:latest -f common_dockerfiles/torch-cuda.Dockerfile .".split(" "))

    walk_directory("./sdk", [])
