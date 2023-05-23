import os
import subprocess
from sdk.common.metadata import MetaData
import json


def metadata_to_labels(meta: MetaData) -> dict[str, str]:
    labels = {}

    labels["HYKO_SDK_NAME"] = meta.name
    labels["HYKO_SDK_DESCRIPTION"] = meta.description
    labels["HYKO_SDK_VERSION"] = meta.version
    labels["HYKO_SDK_CATEGORY"] = meta.category

    i = 0

    for inp in meta.inputs:
        labels[f"HYKO_SDK_INPUT_{i}_NAME"] = inp.name
        labels[f"HYKO_SDK_INPUT_{i}_TYPE"] = inp.type
        i += 1

    i = 0

    for param in meta.params:
        labels[f"HYKO_SDK_PARAM_{i}_NAME"] = param.name
        labels[f"HYKO_SDK_PARAM_{i}_TYPE"] = param.type
        i += 1

    i = 0

    for out in meta.outputs:
        labels[f"HYKO_SDK_OUTPUT_{i}_NAME"] = out.name
        labels[f"HYKO_SDK_OUTPUT_{i}_TYPE"] = out.type
        i += 1

    return labels


registry_host = "registry.localhost"


print(f"categoris: {os.listdir('./sdk')}")

for category in os.listdir("./sdk"):

    if category == "common" or category == "__pycache__":
        continue

    if os.path.isdir("./sdk/" + category):

        for fn in os.listdir("./sdk/" + category):

            if fn == "__pycache__":
                continue

            if os.path.isdir("./sdk/" + category + "/" + fn):

                print()
                print(f"Processing function {category}/{fn}")

                print("Building metadata...")
                subprocess.run(f"docker build --build-arg CATEGORY={category} --build-arg FUNCTION_NAME={fn} --target metadata -t {registry_host}/sdk/{category.lower()}/{fn.lower()}:metadata .".split(' '))

                metadata_process = subprocess.run(f"docker run -it {registry_host}/sdk/{category.lower()}/{fn.lower()}:metadata".split(' '), capture_output=True)
                meta_data = metadata_process.stdout.decode()
                labels = metadata_to_labels(MetaData(**json.loads(meta_data)))
                

                print()
                print("Building...")

                build_cmd = f"docker build "
                build_cmd += f"--build-arg CATEGORY={category} "
                build_cmd += f"--build-arg FUNCTION_NAME={fn} "
                build_cmd += f"--target main "
                build_cmd += f"-t {registry_host}/sdk/{category.lower()}/{fn.lower()}:latest "
                for label_name, label_val in labels.items():
                    build_cmd += f'--label {label_name}="{label_val}" '
                build_cmd += f"."

                print(build_cmd.split(' '))

                subprocess.run(["/bin/sh", "-c", build_cmd])


                print()
                print("Pushing...")

                subprocess.run(f"docker push {registry_host}/sdk/{category.lower()}/{fn.lower()}:latest".split(' '))

