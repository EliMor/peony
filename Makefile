APP_NAME=peony
COMPOSE_FILE=docker-compose.yml

.PHONY: build
build:
	docker-compose -f $(COMPOSE_FILE) build

.PHONY: up
up:
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "Go to http://localhost:50000/"

.PHONY: down
down:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(APP_NAME)

.PHONY: shell
shell:
	docker exec -it peony-box bash