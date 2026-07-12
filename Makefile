# RimaAI developer shortcuts.
.PHONY: help backend-install backend-seed backend-run backend-test backend-lint \
        app-setup app-test docker-up

help:
	@echo "RimaAI make targets:"
	@echo "  backend-install  Create venv and install backend deps"
	@echo "  backend-seed     Seed the demo database"
	@echo "  backend-run      Run the FastAPI dev server (http://localhost:8000/docs)"
	@echo "  backend-test     Run backend pytest suite"
	@echo "  backend-lint     Run ruff on the backend"
	@echo "  app-setup        flutter create + pub get"
	@echo "  app-test         Run Flutter widget tests"
	@echo "  docker-up        Build and run the backend via docker compose"

backend-install:
	cd backend && python -m venv .venv && . .venv/bin/activate && \
		pip install --upgrade pip && pip install -r requirements.txt

backend-seed:
	cd backend && . .venv/bin/activate && python -m app.seed

backend-run:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload

backend-test:
	cd backend && . .venv/bin/activate && pytest

backend-lint:
	cd backend && . .venv/bin/activate && ruff check app tests

app-setup:
	cd app && flutter create . && flutter pub get

app-test:
	cd app && flutter test

docker-up:
	docker compose up --build
