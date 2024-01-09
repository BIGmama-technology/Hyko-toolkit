.PHONY: setup build_sdk build_threaded build_dir override_registry remove_containers remove_registry_images count_models lint format

dir ?= sdk
registry ?= registry.treafik.me

setup:
	./scripts/setup-env.sh

build_sdk:
	python scripts/sdk-builder.py

build_threaded:
	python scripts/sdk-builder.py --threaded

build_dir:
	python scripts/sdk-builder.py --dir $(dir)

override_registry:
	python scripts/sdk-builder.py --dir $(dir) --registry $(registry)

remove_containers:
	docker rm -f $$(docker ps -a | grep hyko_sdk | awk '{print $$1;}')

remove_registry_images:
	docker images | grep '^registry' | awk '{print $3}' | xargs docker rmi -f

lint:
	ruff check .

format:
	ruff format .
