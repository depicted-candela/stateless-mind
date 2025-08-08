# Makefile for managing the Stateless Mind PostgreSQL Environment

# This line ensures the .env file is created with the correct UID/GID if it doesn't exist.
# This must be the first target.
.PHONY: all
all: .env

.env:
	@echo "Creating default .env file..."
	@echo "UID=$$(id -u)" > .env
	@echo "GID=$$(id -g)" >> .env
	@echo "PRIMARY_HOST_PORT=5433" >> .env
	@echo "REPLICA_HOST_PORT=5434" >> .env

# Load environment variables from .env file to make them available to this Makefile
include .env
export PGPASSWORD=password

# Default command
.DEFAULT_GOAL := help

.PHONY: help up down start stop logs psql-primary psql-replica test-lag

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up             Builds and starts all services in detached mode."
	@echo "  down           Stops and removes all containers, networks, and volumes."
	@echo "  start          Starts the services."
	@echo "  stop           Stops the services without removing them."
	@echo "  logs           Follows the logs of all running services."
	@echo "  psql-primary   Connect to the primary PostgreSQL database."
	@echo "  psql-replica   Connect to the replica PostgreSQL database."
	@echo "  test-lag       Run the Python script to check replication lag."

up: .env
	@echo "🚀 Starting up the environment..."
	docker-compose up -d --build

down: .env
	@echo "🔥 Tearing down the environment..."
	docker-compose down -v

start: .env
	@echo "▶️ Starting services..."
	docker-compose start

stop: .env
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
	docker-compose exec pythonClient python /solutions/checkReplicationLag.py