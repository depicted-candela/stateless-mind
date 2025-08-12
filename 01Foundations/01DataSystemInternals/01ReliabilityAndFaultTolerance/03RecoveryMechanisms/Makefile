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

.PHONY: help up down start stop logs psql-primary psql-replica test-lag clean promote-replica

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up                Builds and starts all services in detached mode."
	@echo "  down              Stops and removes all containers, networks (preserves data)."
	@echo "  clean             DESTRUCTIVE: Stops and removes everything, including data volumes."
	@echo "  start             Starts the services."
	@echo "  stop              Stops the services without removing them."
	@echo "  logs              Follows the logs of all running services."
	@echo "  psql-primary      Connect to the primary PostgreSQL database."
	@echo "  psql-replica      Connect to the replica PostgreSQL database."
	@echo "  test-lag          Run the Python script to check replication lag."
	@echo "  promote-replica   Promotes the replica to a primary server (for failover tests)."

up: .env
	@echo "🚀 Starting up the environment..."
	docker-compose up -d --build

down:
	@echo "🔥 Tearing down the environment (preserving data volumes)..."
	docker-compose down

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

# SOLUTION: Add a dedicated target for promoting the replica as the correct user.
promote-replica:
	@echo "🚀 Promoting replica to primary..."
	docker-compose exec --user postgres replica pg_ctl promote

clean:
	@echo "🔥 DESTRUCTIVE: Tearing down the environment AND DELETING ALL DATA..."
	docker-compose down -v