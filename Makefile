# my-claude-agent — Docker shortcuts
#
#   make build   build the container image
#   make run     run the built image locally, mounting $PWD into /work
#
# All values are overridable on the command line, e.g.:
#   make run PORT=8090 ANTHROPIC_BASE_URL=http://127.0.0.1:11434
#
# The container exposes the HTTP API on 9999 (CONTAINER_PORT) and reaches Ollama
# on the host via host.docker.internal:11434. Override IMAGE / TAG / PORT as needed.

IMAGE ?= my-claude-agent
TAG   ?= $(IMAGE):latest
CONTAINER_PORT ?= 9999
HOST_PORT  ?= 9999

.DEFAULT_GOAL := build

.PHONY: build run

# Build the container image.
build:
	docker build -t $(TAG) .

# Run the built image, mounting the repo into /work where the harness lives.
run:
	docker run --rm -p $(HOST_PORT):$(CONTAINER_PORT) -v "$$PWD:/work" $(TAG)
