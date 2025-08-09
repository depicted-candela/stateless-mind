# Makefile for managing the Stateless Mind PostgreSQL Environment

# This target automatically creates a .env file with the current user's UID/GID
# if one does not already exist. This is crucial for rootless Docker volume permissions.
.PHONY: all
all: .env

.env:
	@echo "Creating default .env file..."
	@echo "UID=$$(id -u)" > .env
	@echo "GID=$$(id -g)" >> .env
	@echo "PRIMARY_HOST_PORT=5433" >> .env
	@echo "REPLICA_HOST_PORT=5434" >> .env

# Load environment variables from .env file to make them available to this Makefile
# and subsequent shell commands.
include .env
export PGPASSWORD=password

# Default command to show help.
.DEFAULT_GOAL := help

# Define a variable for the command to be passed to psql. Defaults to empty.
CMD ?=

.PHONY: help setup up down clean start stop logs psql-primary psql-replica run-lag-check run-pitr run-full-recovery

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup              Installs host-level Python dependencies required for solution scripts."
	@echo "  up                 Builds and starts all services in detached mode."
	@echo "  down               Stops and removes containers and networks (preserves data volumes)."
	@echo "  clean              DESTRUCTIVE: Stops and removes all containers, networks, AND data volumes."
	@echo "  start              Starts the services."
	@echo "  stop               Stops the services without removing them."
	@echo "  logs               Follows the logs of all running services."
	@echo "  psql-primary       Connect to the primary PostgreSQL database."
	@echo "  psql-replica       Connect to the replica PostgreSQL database."
	@echo "  run-lag-check      Run the Python script to check replication lag."
	@echo "  run-pitr           Run the Point-in-Time Recovery orchestration script."
	@echo "  run-full-recovery  Run the Full Disaster Recovery orchestration script."

setup:
	@echo "🐍 Installing Python dependencies on the host..."
	python3 -m venv .venv
	@. .venv/bin/activate && pip install -r python_client/requirements.txt
	@echo "Setup complete. Activate with 'source .venv/bin/activate'"

up: .env
	@echo "🚀 Starting up the environment..."
	docker-compose up -d --build

down:
	@echo "🔥 Tearing down the environment (preserving data volumes)..."
	docker-compose down

clean:
	@echo "🔥 DESTRUCTIVE: Tearing down the environment AND DELETING ALL DATA..."
	docker-compose down -v

start:
	@echo "▶️ Starting services..."
	docker-compose start

stop:
	@echo "🛑 Stopping services..."
	docker-compose stop

logs:
	@echo "🔎 Tailing logs..."
	docker-compose logs -f

psql-primary:
	@echo "Connecting to primary database on localhost:${PRIMARY_HOST_PORT}..."
	psql "postgresql://admin:password@localhost:${PRIMARY_HOST_PORT}/statelessCommerce" $(CMD)

psql-replica:
	@echo "Connecting to replica database on localhost:${REPLICA_HOST_PORT}..."
	psql "postgresql://admin:password@localhost:${REPLICA_HOST_PORT}/statelessCommerce" $(CMD)

run-lag-check:
	@echo "🐍 Running replication lag check from host..."
	source .venv/bin/activate && python3 solutions/checkReplicationLag.py

run-pitr:
	@echo "🐍 Running PITR orchestrator from host..."
	source .venv/bin/activate && python3 solutions/pitrOrchestrator.py

run-full-recovery:
	@echo "🐍 Running Full Disaster Recovery orchestrator from host..."
	source .venv/bin/activate && python3 solutions/fullRecoveryOrchestrator.py