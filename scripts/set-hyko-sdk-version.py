import os
from typing import List
import sys



def walk_directory(root_path: str, pre_categories: List[str]):

    print(f"Walking {root_path}/{'/'.join(pre_categories)}")

    ls = os.listdir(root_path + '/' + '/'.join(pre_categories))
    if "main.py" in ls and "config.py" in ls and "Dockerfile" in ls:
        output = ""
        with open(root_path + '/' + '/'.join(pre_categories) + '/Dockerfile') as f:
            text = f.readlines()
            if "cuda" in text[0]:
                for line in text:
                    if "RUN pip install uvicorn hyko_sdk==" in line:
                        line = "RUN pip install uvicorn hyko_sdk==" + sys.argv[1] + '\n'
                    output += line
        if output != "":
            with open(root_path + '/' + '/'.join(pre_categories) + '/Dockerfile', 'w') as f:
                f.write(output)
    
    for sub_folder in ls:
        if not os.path.isdir(root_path + '/' + '/'.join(pre_categories) + '/' + sub_folder):
            continue
        
        walk_directory(root_path=root_path, pre_categories=pre_categories + [sub_folder])



if __name__ == "__main__":

    walk_directory("./sdk", [])
    output = ""
    with open("common_dockerfiles/hyko-sdk.Dockerfile") as f:
        text = f.readlines()
        for line in text:
            if "RUN pip install uvicorn hyko_sdk==" in line:
                line = "RUN pip install uvicorn hyko_sdk==" + sys.argv[1] + '\n'
            output += line
    if output != "":
        with open("common_dockerfiles/hyko-sdk.Dockerfile", 'w') as f:
            f.write(output)
            
    output = ""
    with open("setup.cfg") as f:
        text = f.readlines()
        for line in text:
            if "version" in line:
                line = "version = " + sys.argv[1] + '\n'
            output += line
    if output != "":
        with open("setup.cfg", 'w') as f:
            f.write(output)
    # process_function_dir("./sdk", ["utils", "converters", "video-to-audio"])
