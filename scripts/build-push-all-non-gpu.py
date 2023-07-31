import os
import subprocess
import sys

from common import process_function_dir

skip_folders = ["common", "__pycache__", "venv", "math"]


def walk_directory(path: str):

    print("Walking:", path)
    
    ls = os.listdir(path)
    if "main.py" in ls and "config.py" in ls and "Dockerfile" in ls:
        with open(path + '/Dockerfile') as f:
            dockerfile = f.read()
            if 'cuda' in dockerfile:
                return
        process_function_dir(path)
        # import threading
        # threading.Thread(target=process_function_dir, args=[root_path, pre_categories]).start()

    for sub_folder in ls:

        if sub_folder in skip_folders:
            continue
        
        if not os.path.isdir(path + '/' + sub_folder):
            continue
        
        walk_directory(path + '/' + sub_folder)



if __name__ == "__main__":

    # subprocess.run(f"docker build -t torch-cuda:latest -f common_dockerfiles/torch-cuda.Dockerfile .".split(" "))
    subprocess.run(f"docker build -t hyko-sdk:latest -f common_dockerfiles/hyko-sdk.Dockerfile .".split(" "))
    if len(sys.argv) >= 2:
        walk_directory(sys.argv[1])
    else:
        walk_directory("./sdk")
        
        