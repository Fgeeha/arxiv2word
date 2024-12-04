DC=docker compose
D=docker
APP_CONTAINER=arxiv-downloader


ifeq ($(OS),Windows_NT)
    # Windows
    CUR_DIR := $(shell cd)
    VOLUME_PATH := $(CUR_DIR)/output
else
    # Linux, macOS
    CUR_DIR := $(shell pwd)
    VOLUME_PATH := $(CUR_DIR)/output
endif


.PHONY: build run

build:
	${D} build -t ${APP_CONTAINER} .

run:
	${D} run -it --rm -v $(VOLUME_PATH):/app/output ${APP_CONTAINER}




