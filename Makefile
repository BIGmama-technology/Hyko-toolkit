.PHONY: build_sdk build_sdk_cuda build_threaded override_registry skip_push remove_containers

dir ?= sdk
registry ?= registry.treafik.me

build_sdk:
	python scripts/sdk-builder.py

build_sdk_cuda:
	python scripts/sdk-builder.py --cuda

build_threaded:
	python scripts/sdk-builder.py --threaded

build_dir:
	python scripts/sdk-builder.py --dir $(dir) --cuda

override_registry:
	python scripts/sdk-builder.py --registry $(registry)

skip_push:
	python scripts/sdk-builder.py --no-push

remove_containers:
	docker rm -f $$(docker ps -a | grep hyko_sdk | awk '{print $$1;}')
