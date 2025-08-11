# Makefile for managing the Stateless Mind PostgreSQL Environment

# This target automatically creates a .env file with default ports if one does not exist.
.PHONY: all
all: .env

.env:
	@echo "Creating default .env file..."
	@echo "PRIMARY_HOST_PORT=5433" > .env
	@echo "REPLICA_HOST_PORT=5434" >> .env

# Load environment variables from .env file.
include .env
export PGPASSWORD=password

.DEFAULT_GOAL := help

.PHONY: help up down start stop logs clean psql-primary psql-replica test-lag

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up             Builds and starts all services in detached mode."
	@echo "  down           Stops and removes containers/networks (preserves data)."
	@echo "  clean          Stops and removes everything, INCLUDING ALL DATA VOLUMES."
	@echo "  start          Starts the services."
	@echo "  stop           Stops the services without removing them."
	@echo "  logs           Follows the logs of all running services."
	@echo "  psql-primary   Connect to the primary PostgreSQL database."
	@echo "  psql-replica   Connect to the replica PostgreSQL database."
	@echo "  test-lag       Run the Python script to check replication lag."

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
	psql -h localhost -p ${PRIMARY_HOST_PORT} -U admin -d statelessCommerce

psql-replica:
	@echo "Connecting to replica database on localhost:${REPLICA_HOST_PORT}..."
	psql -h localhost -p ${REPLICA_HOST_PORT} -U admin -d statelessCommerce

test-lag:
	@echo "🐍 Running replication lag check..."
	docker-compose exec python_client python /solutions/checkReplicationLag.py