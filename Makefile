.PHONY: setup build remove_containers remove_registry_images lint format

dir ?= hyko_toolkit
registry ?= registry.traefik.me

setup:
	./scripts/setup.sh

build:
	python scripts/toolkit_builder.py --dir $(dir) --registry $(registry)

remove_containers:
	docker rm -f $$(docker ps -a | grep hyko_sdk | awk '{print $$1}')

remove_registry_images:
	docker images | grep '^registry' | awk '{print $$3}' | xargs docker rmi -f

lint:
	ruff check .

format:
	ruff format .
