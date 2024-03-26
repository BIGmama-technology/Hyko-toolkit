include .env
.PHONY: setup build remove_containers remove_registry_images lint format

dir ?= hyko_toolkit
host ?= traefik.me

setup:
	@./scripts/setup.sh

build:
	@python scripts/toolkit_builder.py --dir $(dir) --host $(host)

build-push-base:
	@python scripts/toolkit_builder.py --base
	@docker login -u $$ADMIN_USERNAME -p $$ADMIN_PASSWORD
	@python scripts/toolkit_builder.py --base --push 


remove_toolkit_containers:
	@docker rm -f $$(docker ps -a | grep hyko_toolkit | awk '{print $$1}')

remove_toolkit_images:
	@docker images | grep '^functions' | awk '{print $$3}' | xargs docker rmi -f
	@docker images | grep '^models' | awk '{print $$3}' | xargs docker rmi -f

lint:
	@ruff check .

format:
	@ruff format .
