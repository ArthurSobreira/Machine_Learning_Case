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
	@echo "$(CYAN)Comandos disponíveis:$(RESET)"
	@echo ""
	@echo "$(YELLOW)make build$(RESET)        - Builda a imagem Docker ($(APP_NAME))"
	@echo "$(YELLOW)make run$(RESET)          - Executa o container junto com a main.py"
	@echo "$(YELLOW)make shell$(RESET)        - Abre um shell interativo dentro do container"
	@echo "$(YELLOW)make re$(RESET)           - Rebuilda a imagem e executa"
	@echo "$(YELLOW)make clean$(RESET)        - Remove a imagem Docker"
	@echo "$(YELLOW)make test$(RESET)         - Executa o projeto fora do container"
	@echo "$(YELLOW)make help$(RESET)         - Exibe esta mensagem de ajuda"
	@echo ""

build:
	@echo "$(GREEN)[+] Buildando imagem Docker: $(APP_NAME)$(RESET)"
	docker build -f $(DOCKERFILE) -t $(APP_NAME) .

run:
	@echo "$(CYAN)[+] Executando container...$(RESET)"
	docker run --rm -it -p 8000:8000 \
		-v "$(PWD)/data:/app/data" --name $(APP_NAME) $(APP_NAME)

shell:
	@echo "$(CYAN)[+] Entrando no container...$(RESET)"
	docker exec -it $(shell docker ps -qf "ancestor=$(APP_NAME)") /bin/bash

test:
	@echo "$(YELLOW)[*] Executando testes...$(RESET)"
	uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload

clean:
	@echo "$(RED)[!] Removendo imagem Docker: $(APP_NAME)$(RESET)"
	docker rmi -f $(APP_NAME) || true
	rm -rf ./data

re: clean all
