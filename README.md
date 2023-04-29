# HYKO template of a single function in the AI SDK

clone this repo, create a new branch and make a folder inside of the correct category folder inside functions folders
copy main.py, requirements.txt and Dockerfile to a new folder of the function you want to create and build on top of it following the same structure to make a single function/model/utility in the AI SDK.
merge the branch to main.
create an image, tag it with the correct version and name and add it to gitlab registry of this same repo as shown in image-build-example.sh file (you need to login with your girlab username and personal access token generated with registry read and write access).