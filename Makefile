# One command per job (Ch. 4.1): the same commands for you, for agents, and for CI.
# The production repo's Makefile is much bigger (stamped commits, scoped gates,
# worktrees): see reference/Makefile.production and docs/WHY.md.

MODULES := services/notification-service shared/infra
COMPOSE := docker compose --env-file .env -f infrastructure/docker-compose.yml

.PHONY: help setup certs up down logs fmt vet build test check scan

help:            ## List the commands
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'

setup:           ## First run: create .env from the example and local certs
	@test -f .env || cp .env.example .env
	@$(MAKE) certs

certs:           ## Generate throwaway local mTLS certificates
	bash infrastructure/certs/generate-certs.sh

up:              ## Start MongoDB, Redis and notification-service
	$(COMPOSE) up -d --build

down:            ## Stop the stack
	$(COMPOSE) down

logs:            ## Follow the service logs
	$(COMPOSE) logs -f notification-service

fmt:             ## Format all Go code
	gofmt -w services shared

vet:             ## go vet every module
	@for m in $(MODULES); do echo "== vet $$m"; (cd $$m && go vet ./...) || exit 1; done

build:           ## go build every module
	@for m in $(MODULES); do echo "== build $$m"; (cd $$m && go build ./...) || exit 1; done

test:            ## Run every module's tests (Mongo/Redis tests skip if not reachable)
	@for m in $(MODULES); do echo "== test $$m"; (cd $$m && go test ./... -count=1) || exit 1; done

check:           ## The gate to run before every commit: format, vet, build, test, secret scan
	@test -z "$$(gofmt -l services shared)" || { echo "gofmt needed:"; gofmt -l services shared; exit 1; }
	@$(MAKE) --no-print-directory vet build test scan

scan:            ## Secret scan of the working tree (needs gitleaks installed)
	@command -v gitleaks >/dev/null || { echo "install gitleaks: https://github.com/gitleaks/gitleaks"; exit 1; }
	gitleaks dir . --config .gitleaks.toml --redact --no-banner
