# Makefile for managing the Stateless Mind PostgreSQL Environment

# Load environment variables from .env file to make them available to this Makefile
include .env
export

# Default command
.DEFAULT_GOAL := help

.PHONY: help up down logs psql-primary psql-replica test-lag

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up             Builds and starts all services in detached mode."
	@echo "  down           Stops and removes all containers, networks, and volumes."
	@echo "  logs           Follows the logs of all running services."
	@echo "  psql-primary   Connect to the primary PostgreSQL database."
	@echo "  psql-replica   Connect to the replica PostgreSQL database."
	@echo "  test-lag       Run the Python script to check replication lag."

up:
	@echo "🚀 Starting up the environment..."
	docker-compose up -d --build

down:
	@echo "🔥 Tearing down the environment..."
	docker-compose down -v

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