include .env
.PHONY: setup

.PHONY: setup
setup: ## - Setup the repository
	@echo "Setting up the toolkit..."
	@pyenv install || true && \
		poetry install && \
		poetry run pre-commit install --hook-type pre-commit --hook-type pre-push && \
		poetry run gitlint install-hook