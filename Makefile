.PHONY: help check install test lint run cluster-up cluster-down

CLUSTER := praktikum

help:            ## Popis naredbi
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

check:           ## Provjeri jesu li svi alati instalirani
	@bash scripts/check-env.sh

install:         ## Napravi .venv i instaliraj ovisnosti (zatim: source .venv/bin/activate)
	python3 -m venv .venv
	.venv/bin/pip install -r app/requirements-dev.txt

lint:            ## Lint Python koda
	ruff check app

test:            ## Pokreni testove
	python -m pytest -q

run:             ## Pokreni API lokalno bez Dockera (http://localhost:8000)
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

cluster-up:      ## Podigni lokalni kind cluster
	kind create cluster --config kind/kind-config.yaml
	kubectl cluster-info --context kind-$(CLUSTER)

cluster-down:    ## Obriši lokalni kind cluster
	kind delete cluster --name $(CLUSTER)
