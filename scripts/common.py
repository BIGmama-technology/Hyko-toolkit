import subprocess
from hyko_sdk.metadata import MetaData, MetaDataBase, metadata_to_docker_label
import json

registry_host = "registry.localhost"

def process_function_dir(path: str):
    """Path has to be a valid path with no spaces in it """
    if path[:2] == './':
        path = path[2:]
    
    if path[-1] == '/':
        path = path[:-1]
    
    splitted = path.split("/")
    
    if len(splitted) == 2:
        version = splitted[0]
        function_name = splitted[1]
        category = "uncategorized"
    elif len(splitted) > 2:
        version = splitted[-1]
        function_name = splitted[-2]
        category = "/".join(splitted[:-2]).lower()
    else:
        return
    
    print(f"Processing function: {category=} {function_name=} {version=}")


    print("Building metadata...")
    subprocess.run(f"docker build --target metadata -t metadata:latest ./{path}".split(' '))

    metadata_process = subprocess.run(f"docker run -it --rm metadata:latest".split(' '), capture_output=True)
   
    meta_data = metadata_process.stdout.decode()
    meta_data = MetaDataBase(**json.loads(meta_data))
    meta_data = MetaData(**meta_data.model_dump(), name=function_name, version=version, category=category)
    subprocess.run(f"docker rmi -f metadata:latest".split(' '))

    print()
    print("Building...")
    function_tag = f"{registry_host}/{category.lower()}/{function_name.lower()}:{version}"
    build_cmd = f"docker build "
    build_cmd += f"--build-arg CATEGORY={category} "
    build_cmd += f"--build-arg FUNCTION_NAME={function_name} "
    build_cmd += f"--target main "
    build_cmd += f"-t {function_tag} "
    build_cmd += f"""--label metadata="{metadata_to_docker_label(meta_data)}" """
    build_cmd += f"./{path}"

    print("Executing cmd: ", build_cmd.split(' '))

    subprocess.run(["/bin/sh", "-c", build_cmd])


    print()
    print("Pushing...")

    subprocess.run(f"docker push {function_tag}".split(' '))

