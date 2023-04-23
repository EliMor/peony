# Variables
APP_NAME=myflaskapp
DOCKER_BUILD_CMD=docker build -t $(APP_NAME) .
DOCKER_RUN_CMD=docker run -d --name $(APP_NAME) -p 5000:5000 $(APP_NAME)
DOCKER_STOP_CMD=docker stop $(APP_NAME)
DOCKER_RM_CMD=docker rm $(APP_NAME)

.PHONY: build up down

build:
	$(DOCKER_BUILD_CMD)

up:
	$(DOCKER_RUN_CMD)

down:
	$(DOCKER_STOP_CMD)
	$(DOCKER_RM_CMD)
