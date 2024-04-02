include .env
.PHONY: setup build remove_containers remove_registry_images lint format

dir ?= hyko_toolkit
host ?= traefik.me

.PHONY: setup
setup: ## - Setup the repository
	@echo "Setting up the toolkit..."
	@pyenv install || true && \
		poetry install && \
		poetry run pre-commit install --hook-type pre-commit --hook-type pre-push && \
		poetry run gitlint install-hook

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
	@poetry run ruff check .

format:
	@poetry run ruff format .
