import os
import subprocess

os.chdir("functions")
for category in os.listdir():
    if os.path.isdir(category):
        os.chdir(category)
        for fn in os.listdir():
            if os.path.isdir(fn):
                os.chdir(fn)
                print("building", fn)
                subprocess.run(f"docker build -t registry.gitlab.com/big-mama1/big-mama-tech/hyko/backend-services/ai-sdk/{fn}:1.0 .".split(" "))
                print("pushing", fn)
                subprocess.run(f"docker push registry.gitlab.com/big-mama1/big-mama-tech/hyko/backend-services/ai-sdk/{fn}:1.0".split(" "))
                os.chdir("..")
        os.chdir("..")
        