.PHONY: up down reset migrate logs shell test help

DC = docker compose

# ── Bootstrap ─────────────────────────────────────────────────────────────────

up: ## Build images, start all services, and run migrations
	$(DC) up --build --wait -d
	$(DC) exec api alembic upgrade head

down: ## Stop and remove containers
	$(DC) down

reset: ## Full teardown (including volumes) then bootstrap from zero
	$(DC) down -v
	$(DC) up --build --wait -d
	$(DC) exec api alembic upgrade head

# ── Database ──────────────────────────────────────────────────────────────────

migrate: ## Run pending migrations
	$(DC) exec api alembic upgrade head

migration: ## Generate a new migration (usage: make migration msg="add users table")
	$(DC) exec api alembic revision --autogenerate -m "$(msg)"

# ── Tests ─────────────────────────────────────────────────────────────────────

test: ## Run the test suite
	.venv/bin/pytest $(ARGS)

# ── Observability ─────────────────────────────────────────────────────────────

logs: ## Tail logs for all services
	$(DC) logs -f

logs-api: ## Tail API logs only
	$(DC) logs -f api

logs-worker: ## Tail worker logs only
	$(DC) logs -f worker

# ── Shells ────────────────────────────────────────────────────────────────────

shell: ## Open a shell in the api container
	$(DC) exec api bash

db-shell: ## Open psql in the db container
	$(DC) exec db psql -U trails trails

# ── Help ──────────────────────────────────────────────────────────────────────

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
