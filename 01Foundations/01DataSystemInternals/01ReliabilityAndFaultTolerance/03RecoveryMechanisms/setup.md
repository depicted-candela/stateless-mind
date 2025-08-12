This directory contains the exercises for **1.1.1 Reliability and Fault Tolerance: Recovery mechanisms**. All exercises run within a self-contained Docker Compose environment designed for robustness and compatibility with rootless Docker on Debian 12.

#### Prerequisites

1. **Docker and Docker Compose**: Ensure you have Docker and the Docker Compose plugin installed and running.
2. **make**: The `make` utility must be installed (`sudo apt-get install build-essential`).

#### Environment Lifecycle Management

A `Makefile` is provided to simplify managing the User-Centric Execution Environment (UCEE). It will automatically generate a `.env` file on its first run with your user's permissions and default ports to ensure a conflict-free setup.

**1. Activate (Build and Start)**

This command prepares and launches the entire environment.

```bash
make up
```

**2. Stop and Start**

You can stop the running services without losing their state, and start them again later. This is useful for pausing your work.

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
make clean
```

**4. View Logs**

To view the real-time logs from all running services, use:

```bash
make logs
```

### Executing Exercise Solutions

The exercises in `exercises/recovery-mechanisms.md` will require you to run Python scripts or interact with the databases directly.

**1. Running Python Solution Scripts**

The solution scripts are located in the `solutions/` directory and can be run from within the `python_client` service. The `Makefile` provides a shortcut for the replication lag check.

- **Example (using Makefile target):**
  
    ```bash
    make test-lag
    ```
  
- **General Purpose (for other scripts):**
  
    ```bash
    docker-compose exec python_client python /solutions/pitrOrchestrator.py
    docker-compose exec python_client python /solutions/fullRecoveryOrchestrator.py
    ```
  

**2. Accessing the Databases**

You can connect to the primary and replica databases directly using `psql` via the `Makefile` targets.

- **Connect to Primary Database:**
  
    ```bash
    make psql-primary
    ```
  
- **Connect to Replica Database:**
  
    ```bash
    make psql-replica
    ```
  

### Architecture and Configuration Explained

This environment is designed to be robust, especially for rootless Docker setups. Here are the key design choices:

- **Internal WAL Archiving**: The `primary` database archives its WAL files to a subdirectory *within its own data volume* (`/var/lib/postgresql/data/wal-archive`). This avoids the "Permission denied" errors that occur when a rootless container tries to write to a host-mounted volume it doesn't own.
- **Read-Only Volume Sharing**: The `replica` service gains access to the WAL files by mounting the `primary`'s data volume in read-only mode (`:ro`). This is a secure and efficient way to share the necessary recovery data.
- **Automated and Idempotent Setup**: The entrypoint scripts for both `primary` and `replica` are designed to be robust. The replica's script waits in a loop for the primary to be fully ready for replication, solving the startup race condition. It also uses replication slots to ensure the primary doesn't delete WAL files before the replica has consumed them.

<br>

### Configuration Files

<details>
<summary><code>Makefile</code></summary>

```makefile
# Makefile for managing the Stateless Mind PostgreSQL Environment

# This target automatically creates a .env file with the current user's UID/GID
# if one does not already exist. This is crucial for rootless Docker volume permissions.
.PHONY: all
all: .env

.env:
    @echo "Creating default .env file..."
    # Use $$ to escape the $ for `make`, so the shell executes the command substitution.
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

promote-replica:
    @echo "🚀 Promoting replica to primary..."
    docker-compose exec --user postgres replica pg_ctl promote

clean:
    @echo "🔥 DESTRUCTIVE: Tearing down the environment AND DELETING ALL DATA..."
    docker-compose down -v
```

</details>

<details>
<summary><code>docker-compose.yml</code></summary>

```yaml
services:
  primary:
    image: postgres:15
    container_name: primary
    volumes:
      - ./primary/init:/docker-entrypoint-initdb.d
      - postgresPrimaryData:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: statelessCommerce
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
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
        condition: service_healthy
    volumes:
      - postgresReplicaData:/var/lib/postgresql/data
      - postgresPrimaryData:/primary_data:ro
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "${REPLICA_HOST_PORT}:5432"
    networks:
      - postgresnet
      - clientnet

  python_client:
    build:
      context: ./python_client
    container_name: python_client
    working_dir: /app
    volumes:
      - ./solutions:/solutions
    command: tail -f /dev/null
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
  postgresPrimaryData:
    name: statelessCommercePrimaryData
  postgresReplicaData:
    name: statelessCommerceReplicaData

networks:
  postgresnet:
    driver: bridge
  clientnet:
    driver: bridge
```
</details>

<details>
<summary><code>primary/init/00-init-permissions.sh</code></summary>

```sh
#!/bin/bash
set -e

# This script runs once as the postgres user during database initialization.

# 1. Create a subdirectory for WAL files inside the main data volume.
# This avoids host permission issues, especially in rootless Docker environments.
mkdir -p /var/lib/postgresql/data/wal-archive

# 2. Append replication rules to the default pg_hba.conf generated by initdb.
echo "host replication admin 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

# 3. Append necessary parameters to the default postgresql.conf.
cat >> "$PGDATA/postgresql.conf" <<EOF
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/data/wal-archive/%f'
max_wal_senders = 10
hot_standby = on
EOF

echo "Initialization complete: pg_hba.conf and postgresql.conf configured for replication."
```

</details>

<details>
<summary><code>primary/init/01-schema.sql</code></summary>

```sql
/* Schema for statelessCommerce */
CREATE TABLE customers (
    customerId SERIAL PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    registrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    productId SERIAL PRIMARY KEY,
    productName VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10, 2)
);

CREATE TABLE orders (
    orderId SERIAL PRIMARY KEY,
    customerId INT REFERENCES customers(customerId),
    orderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    totalAmount NUMERIC(10, 2)
);

CREATE TABLE orderItems (
    orderItemId SERIAL PRIMARY KEY,
    orderId INT REFERENCES orders(orderId),
    productId INT REFERENCES products(productId),
    quantity INT,
    pricePerUnit NUMERIC(10, 2)
);
```

</details>

<details>
<summary><code>primary/init/02-data.sql</code></summary>

```sql
/* Initial data for statelessCommerce */
INSERT INTO customers (firstName, lastName, email) VALUES
('Alice', 'Smith', 'alice.smith@example.com'),
('Bob', 'Johnson', 'bob.johnson@example.com');

INSERT INTO products (productName, category, price) VALUES
('Laptop Pro', 'Electronics', 1200.00),
('Wireless Mouse', 'Electronics', 25.50),
('Mechanical Keyboard', 'Electronics', 75.00),
('Data Engineering Essentials', 'Books', 49.99);

INSERT INTO orders (customerId, totalAmount) VALUES
(1, 1225.50),
(2, 124.99);

INSERT INTO orderItems (orderId, productId, quantity, pricePerUnit) VALUES
(1, 1, 1, 1200.00),
(1, 2, 1, 25.50),
(2, 4, 1, 49.99),
(2, 3, 1, 75.00);
```

</details>

<details>
<summary><code>replica/Dockerfile</code></summary>

```dockerfile
FROM postgres:15

# We copy our custom entrypoint and ensure it's executable.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# We override the default entrypoint to run our resilient script.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# The default CMD from the base image will be passed as arguments to our entrypoint.
CMD ["postgres"]
```

</details>

<details>
<summary><code>replica/entrypoint.sh</code></summary>

```sh
#!/bin/bash
set -e

# This script is the replica's entrypoint. It runs as root initially.
# We must ensure all postgres commands are executed as the 'postgres' user.

# Only run the backup/setup logic if the data directory is empty
if [ -z "$(ls -A "$PGDATA")" ]; then
    echo "Replica data directory is empty. Initializing..."

    # Ensure the postgres server is not running. The '|| true' handles cases where it's already stopped.
    # The command is run as the postgres user.
    su - postgres -c "pg_ctl -D \"$PGDATA\" -m fast -w stop || true"

    # Clean out any residual files from a failed previous attempt. Run as root.
    rm -rf "$PGDATA"/*

    echo "Starting base backup from primary..."

    # This entire block is executed as the 'postgres' user.
    su - postgres -c "
        # Create a temporary .pgpass file for non-interactive authentication.
        echo 'primary:5432:*:admin:$POSTGRES_PASSWORD' > ~/.pgpass
        chmod 0600 ~/.pgpass

        # Loop until the base backup succeeds. This handles the race condition where the
        # primary is 'healthy' but not yet fully configured for replication.
        until pg_basebackup --pgdata=\"$PGDATA\" --host=primary --username=admin -W --wal-method=stream --slot=replica_slot --create-slot
        do
          echo 'Waiting for primary to be fully ready for replication...'
          sleep 1s
        done

        # Clean up the password file immediately after use.
        rm ~/.pgpass
    "

    # Set correct directory permissions as root after backup.
    chmod 0700 "$PGDATA"

    # Create the standby signal file and postgresql.auto.conf.
    # These must be created as the postgres user.
    su - postgres -c "
        touch \"$PGDATA/standby.signal\"
        cat > \"$PGDATA/postgresql.auto.conf\" <<EOF
primary_conninfo = 'host=primary port=5432 user=admin password=$POSTGRES_PASSWORD'
restore_command = 'cp /primary_data/wal-archive/%f %p'
primary_slot_name = 'replica_slot'
EOF
    "

    echo "Replica setup complete. Starting PostgreSQL..."
else
    echo "Replica data directory already exists. Skipping initialization."
fi

# Finally, execute the original postgres entrypoint command, which will start the server.
# This script is smart enough to start the final server process as the 'postgres' user.
exec docker-entrypoint.sh "$@"
```

</details>

<details>
<summary><code>python_client/Dockerfile</code></summary>

```dockerfile
# python_client/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
```

</details>

<details>
<summary><code>python_client/requirements.txt</code></summary>

```txt
psycopg2-binary
```

</details>

<br>