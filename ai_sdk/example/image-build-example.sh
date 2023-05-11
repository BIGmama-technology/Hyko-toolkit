set -x
set -e

# dont use this directly, make sure to change the name and versioning correctly
docker login registry.gitlab.com
docker build -t registry.gitlab.com/big-mama1/big-mama-tech/hyko/backend-services/ai-sdk/add:1.0 .
docker push registry.gitlab.com/big-mama1/big-mama-tech/hyko/backend-services/ai-sdk/add:1.0