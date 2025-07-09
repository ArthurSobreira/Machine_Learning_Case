#------------------------------------------------------------------------------#
#                                GENERICS                                      #
#------------------------------------------------------------------------------#

DEFAULT_GOAL: all
.PHONY: build run shell clean re help

#------------------------------------------------------------------------------#
#                                VARIABLES                                     #
#------------------------------------------------------------------------------#

APP_NAME        := case-tractian
SRC_DIR         := src
DOCKERFILE      := Dockerfile
CONTAINER_WORK  := /app

GREEN			= \033[32m
RED				= \033[31m
CYAN			= \033[36m
YELLOW		= \033[33m
RESET			= \033[0m

#------------------------------------------------------------------------------#
#                                  TARGETS                                     #
#------------------------------------------------------------------------------#

all: help build run

help:
	@echo ""
	@echo "$(CYAN)Comandos disponíveis:$(RESET)"
	@echo ""
	@echo "$(YELLOW)make build$(RESET)        - Builda a imagem Docker ($(APP_NAME))"
	@echo "$(YELLOW)make run$(RESET)          - Executa o container junto com a main.py"
	@echo "$(YELLOW)make shell$(RESET)        - Abre um shell interativo dentro do container"
	@echo "$(YELLOW)make re$(RESET)           - Rebuilda a imagem e executa"
	@echo "$(YELLOW)make clean$(RESET)        - Remove a imagem Docker"
	@echo "$(YELLOW)make all/make$(RESET)     - Executa os comandos build e run"
	@echo ""

build:
	@echo "$(GREEN)[+] Buildando imagem Docker: $(APP_NAME)$(RESET)"
	docker build -f $(DOCKERFILE) -t $(APP_NAME) .

# --rm remove the container after it exits (not sure if this is necessary)
# -it allows for interactive terminal
run:
	@echo "$(CYAN)[+] Executando container...$(RESET)"
	docker run --rm -it $(APP_NAME)

shell:
	@echo "$(CYAN)[+] Entrando no container...$(RESET)"
	docker run --rm -it $(APP_NAME) /bin/bash

clean:
	@echo "$(RED)[!] Removendo imagem Docker: $(APP_NAME)$(RESET)"
	docker rmi -f $(APP_NAME) || true

re: clean all
