Of course. Based on the corrected and enhanced file system context you provided, here is the updated `README.md`.

This version integrates the improved setup strategy, utilizes the new `Makefile` for a simpler user experience, explains the purpose of the `.env` file to prevent system conflicts, and provides clear, step-by-step instructions for activating, managing, executing, and deactivating the User-Centric Execution Environment (UCEE).

### `README.md`

This directory contains the exercises for **1.1.1 Reliability and Fault Tolerance: Recovery mechanisms**. All exercises run within a self-contained Docker Compose environment designed for robustness and compatibility with rootless Docker on Debian 12.

#### Prerequisites

1.  **Docker and Docker Compose**: Ensure you have Docker and the Docker Compose plugin installed and running.
2.  **Port Configuration**: This project uses an `.env` file to define the host ports for the PostgreSQL primary and replica databases. Before starting, check the `PRIMARY_HOST_PORT` and `REPLICA_HOST_PORT` values in the `.env` file. If ports `5433` or `5434` are already in use on your system, you can change them in this file to avoid conflicts.

#### Environment Lifecycle Management

A `Makefile` is provided to simplify managing the UCEE.

**1. Activate (Build and Start)**

This command builds the necessary Docker images, creates the networks and volumes, and starts all services in the background.

```bash
make up
```

**2. Stop and Start**

You can stop the running services without deleting any resources, and start them again. This is useful for pausing your work.

*   To stop all running containers:
    ```bash
    make stop
    ```
*   To start the previously stopped containers:
    ```bash
    make start
    ```

**3. Deactivate (Teardown and Cleanup)**

This command stops all services and completely removes all containers, networks, and **volumes** associated with the project. This ensures your system is returned to a clean state.

```bash
make down
```

**4. View Logs**

To view the real-time logs from all running services, use:

```bash
make logs
```

#### Executing Exercise Solutions

The exercises in `exercises/recovery-mechanisms.md` will require you to run Python scripts or interact with the databases directly.

**1. Running Python Solution Scripts**

The solution scripts are located in the `solutions/` directory and can be run from within the `pythonClient` service. The `Makefile` provides a shortcut for the replication lag check, and you can use `docker-compose exec` for others.

*   **Example (using Makefile target):**
    ```bash
    make test-lag
    ```
*   **General Purpose (for other scripts):**
    ```bash
    docker-compose exec pythonClient python /solutions/pitrOrchestrator.py
    docker-compose exec pythonClient python /solutions/fullRecoveryOrchestrator.py
    ```

**2. Accessing the Databases**

You can connect to the primary and replica databases directly using `psql` via the `Makefile` targets, which use the ports defined in your `.env` file.

*   **Connect to Primary Database:**
    ```bash
    make psql-primary
    ```
*   **Connect to Replica Database:**
    ```bash
    make psql-replica
    ```

### Configuration Files

<details>
<summary><code>.env</code></summary>

```dotenv
# Environment configuration for Stateless Mind exercises
# Define host ports to avoid conflicts with local services.
# Change these values if ports 5433 or 5434 are in use on your system.
PRIMARY_HOST_PORT=5433
REPLICA_HOST_PORT=5434
```
</details>

<details>
<summary><code>docker-compose.yml</code></summary>

```yaml
version: '3.8'

# This Compose file defines the services, networks, and volumes for the application.

services:
  primary:
    image: postgres:15
    container_name: primary
    volumes:
      - ./primary/init:/docker-entrypoint-initdb.d
      - postgresPrimaryData:/var/lib/postgresql/data
      - walArchive:/archive
    environment:
      POSTGRES_DB: statelessCommerce
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    # CORRECTED: The command now correctly invokes the 'postgres' executable
    # and passes the configuration flags as arguments.
    command: >
      postgres
      -c wal_level=replica
      -c archive_mode=on
      -c archive_command='cp %p /archive/%f'
      -c max_wal_senders=10
      -c hot_standby=on
    ports:
      - "${PRIMARY_HOST_PORT}:5432"
    networks:
      - postgresnet
      - clientnet
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d statelessCommerce"]
      interval: 5s
      timeout: 5s
      retries: 5

  replica:
    build:
      context: ./replica
    container_name: replica
    depends_on:
      primary:
        # Ensures replica setup begins only after the primary is fully healthy.
        condition: service_healthy
    volumes:
      - postgresReplicaData:/var/lib/postgresql/data
      - walArchive:/archive
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "${REPLICA_HOST_PORT}:5432"
    networks:
      - postgresnet

  pythonClient:
    image: python:3.10-slim
    container_name: pythonClient
    working_dir: /app
    volumes:
      - ./solutions:/solutions
    command: tail -f /dev/null # Keep container running
    networks:
      - clientnet
    depends_on:
      - primary
      - replica
    environment:
      PRIMARY_HOST: primary
      REPLICA_HOST: replica
      DB_USER: admin
      DB_PASSWORD: password
      DB_NAME: statelessCommerce

volumes:
  # Named volumes ensure data persistence and are managed by Docker.
  postgresPrimaryData:
    name: statelessCommercePrimaryData
  postgresReplicaData:
    name: statelessCommerceReplicaData
  walArchive:
    name: statelessCommerceWalArchive

networks:
  # Explicit network definitions for better isolation and portability.
  postgresnet:
    driver: bridge
  clientnet:
    driver: bridge
```
</details>

<details>
<summary><code>replica/entrypoint.sh</code></summary>

```bash
#!/bin/bash
set -e

# This script runs as the 'postgres' user inside the container.

# Stop the server that was auto-started by the base image to allow backup.
pg_ctl -D "$PGDATA" -m fast -w stop

# Clean out the existing data directory to ensure a fresh restore.
rm -rf "$PGDATA"/*

echo "Starting base backup from primary..."

# Use a temporary .pgpass file for credentials during backup to avoid interactive prompts.
echo "primary:5432:*:admin:password" > ~/.pgpass
chmod 0600 ~/.pgpass

# Loop until the primary is available and the base backup succeeds.
# --create-slot ensures the primary creates a durable replication slot for this replica.
until pg_basebackup --pgdata="$PGDATA" --host=primary --username=admin -W --wal-method=stream --slot=replica_slot --create-slot
do
  echo "Waiting for primary to connect to create base backup..."
  sleep 1s
done

# Clean up the temporary password file immediately after use.
rm ~/.pgpass

# Set correct permissions for the data directory after backup.
chmod 0700 "$PGDATA"

# Create the standby.signal file to indicate this is a replica.
touch "$PGDATA/standby.signal"

# Create postgresql.auto.conf with connection info and restore command.
cat > "$PGDATA/postgresql.auto.conf" <<EOF
primary_conninfo = 'host=primary port=5432 user=admin password=password'
restore_command = 'cp /archive/%f %p'
primary_slot_name = 'replica_slot'
EOF

echo "Replica setup complete. The container will now start PostgreSQL..."
# The script now finishes, allowing the original Docker entrypoint to start postgres.
```
</details>