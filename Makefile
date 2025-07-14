#------------------------------------------------------------------------------#
#                                GENERICS                                      #
#------------------------------------------------------------------------------#

DEFAULT_GOAL: help
.PHONY: help build run shell test clean re

#------------------------------------------------------------------------------#
#                                VARIABLES                                     #
#------------------------------------------------------------------------------#

APP_NAME        := case-tractian
SRC_DIR         := src
DOCKERFILE      := Dockerfile
CONTAINER_WORK  := /app
PWD             := $(shell pwd)

GREEN     = \033[32m
RED       = \033[31m
CYAN      = \033[36m
YELLOW    = \033[33m
RESET     = \033[0m

#------------------------------------------------------------------------------#
#                                  TARGETS                                     #
#------------------------------------------------------------------------------#

help:
	@echo ""
	@echo "$(CYAN)Available Commands:$(RESET)"
	@echo ""
	@echo "$(YELLOW)make build$(RESET)        - Build the Docker image for the project"
	@echo "$(YELLOW)make run$(RESET)          - Execute the Docker container with the project"
	@echo "$(YELLOW)make shell$(RESET)        - Open a shell in the running container"
	@echo "$(YELLOW)make re$(RESET)           - Remove the Docker image and rebuild it"
	@echo "$(YELLOW)make clean$(RESET)        - Remove the Docker image and data directory"
	@echo "$(YELLOW)make help$(RESET)         - Display this help message"
	@echo ""

build:
	@echo "$(GREEN)[+] Building Docker image: $(APP_NAME)$(RESET)"
	docker build -f $(DOCKERFILE) -t $(APP_NAME) .

run:
	@echo "$(CYAN)[+] Executing container: $(APP_NAME)$(RESET)"
	docker run --rm -it -p 8000:8000 \
		-v "$(PWD)/data:/app/data" --name $(APP_NAME) $(APP_NAME)

shell:
	@echo "$(CYAN)[+] Opening shell in container: $(APP_NAME)$(RESET)"
	docker exec -it $(shell docker ps -qf "ancestor=$(APP_NAME)") /bin/bash

test:
	@echo "$(YELLOW)[*] Running test server: $(APP_NAME)$(RESET)"
	uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload

clean:
	@echo "$(RED)[!] Cleaning up Docker image and data directory$(RESET)"
	docker rmi -f $(APP_NAME) || true
	rm -rf ./data

re: clean all
