start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker compose -f docker-compose.yml up
	@echo "Containers started - http://localhost:5000"

test: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker compose -f docker-compose-test.yml up
	@echo "Containers started - http://localhost:5000"

test-build: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker compose -f docker-compose-test.yml up --build
	@echo "Containers started - http://localhost:5000"

start-build: ## Rebuild and start the docker containers
	@echo "Re-Building and starting the docker containers"
	@docker compose -f docker-compose.yml up --build
	@echo "Containers started - http://localhost:5000"

stop: ## Stop Containers
	@docker compose down

restart: stop start ## Restart Containers

start-bg:  ## Run containers in the background
	@docker compose -f docker-compose.yml up -d

follow:  ## Follow logs of containers running in the background
	@docker compose logs --follow

build: ## Build Containers
	@docker compose build

ssh: ## SSH into running web container
	docker compose exec web bash

migrations: ## Create DB migrations in the container
	@docker compose exec web flask db init

migrate: ## Run DB migrations in the container
	@docker compose exec web flask db migrate -m "initialise migration"

upgrade-migrate: ## upgrade DB migrations in the container
	@docker compose exec web flask db upgrade

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'