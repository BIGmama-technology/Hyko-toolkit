# This script counts the number of "main.py" files in the "sdk" directory and the number of models in the "huggingface" directory.
# It also provides the total number of models in the "huggingface" directory.
# The "-v" option can be used to display the number of models for each subdirectory in the "huggingface" directory.
#!/bin/bash

verbose=0
if [ "$1" == "-v" ]; then
    verbose=1
fi

cd ./sdk
tree | grep -o 'main.py' | wc -l | xargs echo "Number of sdk nodes:"

cd ./huggingface
total=0
for subdir in $(ls -d */); do
    for model in $(ls -d ${subdir}/*); do
        model=$(basename ${model})

        endpoint_url="https://api.traefik.me/huggingface/models?pipeline_tag=${model}&sort=downloads&direction=-1&limit=1"
        response=$(curl -k -s "${endpoint_url}")

        length=$(jq -r '.total_count' <<< "${response}")

        if [ $verbose -eq 1 ]; then
            echo "number of ${model} models: ${length}"
        fi

        total=$((total + length))
    done
done

echo "total number of huggingface models ${total}"
