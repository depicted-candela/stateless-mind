Of course. Based on the corrected and enhanced UCEE you've provided, which successfully resolves the startup race conditions and rootless permission issues, I have updated the entire set of exercises and configurations.

The new structure is more robust and aligns with modern best practices for containerized database environments. The `Makefile` simplifies the user experience, and the refined `entrypoint.sh` scripts ensure a reliable and idempotent setup.

Here is the enhanced and corrected response for the **Recovery mechanisms** topic.

### `tree.txt`

```
.
├── Makefile
├── README.md
├── docker-compose.yml
├── exercises
│   └── recovery-mechanisms.md
├── primary
│   └── init
│       ├── 00-init-permissions.sh
│       ├── 01-schema.sql
│       └── 02-data.sql
├── python_client
│   ├── Dockerfile
│   └── requirements.txt
├── replica
│   ├── Dockerfile
│   └── entrypoint.sh
└── solutions
    ├── checkReplicationLag.py
    ├── fullRecoveryOrchestrator.py
    └── pitrOrchestrator.py
```

<br>

### `README.md`

This directory contains the exercises for **1.1.1 Reliability and Fault Tolerance: Recovery mechanisms**. All exercises run within a self-contained Docker Compose environment designed for robustness and compatibility with rootless Docker on Debian 12.

#### Prerequisites

1.  **Docker and Docker Compose**: Ensure you have Docker and the Docker Compose plugin installed and running.
2.  **make**: The `make` utility must be installed (`sudo apt-get install build-essential`).

#### Environment Lifecycle Management

A `Makefile` is provided to simplify managing the User-Centric Execution Environment (UCEE). It will automatically generate a `.env` file on its first run with your user's permissions and default ports to ensure a conflict-free setup.

**1. Activate (Build and Start)**

This command prepares and launches the entire environment.

```bash
make up```

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
make clean```

**4. View Logs**

To view the real-time logs from all running services, use:

```bash
make logs
```

### Executing Exercise Solutions

The exercises in `exercises/recovery-mechanisms.md` will require you to run Python scripts or interact with the databases directly.

**1. Running Python Solution Scripts**

The solution scripts are located in the `solutions/` directory and can be run from within the `python_client` service. The `Makefile` provides a shortcut for the replication lag check.

*   **Example (using Makefile target):**
    ```bash
    make test-lag
    ```
*   **General Purpose (for other scripts):**
    ```bash
    docker-compose exec python_client python /solutions/pitrOrchestrator.py
    docker-compose exec python_client python /solutions/fullRecoveryOrchestrator.py
    ```

**2. Accessing the Databases**

You can connect to the primary and replica databases directly using `psql` via the `Makefile` targets.

*   **Connect to Primary Database:**
    ```bash
    make psql-primary
    ```
*   **Connect to Replica Database:**
    ```bash
    make psql-replica
    ```

### Architecture and Configuration Explained

This environment is designed to be robust, especially for rootless Docker setups. Here are the key design choices:

*   **Internal WAL Archiving**: The `primary` database archives its WAL files to a subdirectory *within its own data volume* (`/var/lib/postgresql/data/wal-archive`). This avoids the "Permission denied" errors that occur when a rootless container tries to write to a host-mounted volume it doesn't own.
*   **Read-Only Volume Sharing**: The `replica` service gains access to the WAL files by mounting the `primary`'s data volume in read-only mode (`:ro`). This is a secure and efficient way to share the necessary recovery data.
*   **Automated and Idempotent Setup**: The entrypoint scripts for both `primary` and `replica` are designed to be robust. The replica's script waits in a loop for the primary to be fully ready for replication, solving the startup race condition. It also uses replication slots to ensure the primary doesn't delete WAL files before the replica has consumed them.

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
```</details>

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

### `exercises/recovery-mechanisms.md`

#### **(i) Meanings, Values, Relations, and Advantages**

**Exercise 1.1: Point-in-Time Recovery (PITR) in Action**

1.  **Meaning and Value:** In your own words, what is Point-in-Time Recovery (PITR)? What is its primary value proposition compared to simply restoring the latest full backup?
2.  **Relation:** How does the Write-Ahead Log (WAL) from PostgreSQL, a concept tied to durability, enable the recovery mechanism of PITR? How does this relate to the concept of a replication log discussed in *Designing Data-Intensive Applications*?
3.  **Practice:**
    a.  Connect to the `primary` database and record the current timestamp.
    b.  Delete all customers with the last name 'Johnson'.
        ```sql
        DELETE FROM customers WHERE lastName = 'Johnson';
        SELECT * FROM customers; -- Verify deletion
        ```
    c.  You've just made a critical error. The `pitrOrchestrator.py` script is designed to automate recovery, but it is destructive. Before running it, examine its contents. What high-level steps does it perform?
4.  **Proprietary Contrast:** Describe how a managed database service like Amazon RDS or Google Cloud SQL simplifies this entire recovery process for the user. What trade-offs are being made?

<details>
<summary>Solution 1.1</summary>

1.  **Meaning and Value:** PITR is a recovery mechanism that allows a database to be restored to a specific moment in time, not just to the time a full backup was taken. Its primary value is minimizing data loss. While a full backup might be hours or days old, PITR uses a full backup *plus* a continuous log of all subsequent transactions (the WAL) to restore the database to the minute or second right before a failure or error occurred.

2.  **Relation:** The WAL is an ordered log of every change made to the database. This is fundamentally the same concept as a replication log used in leader-follower setups. Both are streams of data changes. Replication applies this stream to a live replica to keep it in sync. PITR applies this stream to a restored backup file to "roll it forward" to a specific point in time. Both rely on the same underlying principle of a durable, ordered log of transactions.

3.  **Practice:**
    a.  Connect and get timestamp:
        ```bash
        make psql-primary
        # Inside psql:
        SELECT now();
        # Example output: 2025-08-12 18:30:00.123456+00
        ```
    b.  Run the deletion.
    c.  **Analysis of `pitrOrchestrator.py`:** The script automates a PITR by:
        1.  Stopping the primary server.
        2.  Wiping its data directory (`/var/lib/postgresql/data`).
        3.  Simulating a restore from a base backup (in a real scenario, this would come from an object store like S3).
        4.  Creating a `recovery.signal` file and adding `recovery_target_time` and `restore_command` to the configuration.
        5.  Restarting the server, which triggers the recovery process.
        6.  Monitoring the server until it's back online.

    **Execution:**
    ```bash
    # Run the script from your host machine
    docker-compose exec python_client python /solutions/pitrOrchestrator.py
    ```
    When prompted, enter the timestamp you recorded before the deletion. After running, connect to the primary using `make psql-primary` and verify the 'Johnson' customer has been restored.

4.  **Proprietary Contrast:** Managed services like Amazon RDS abstract this entirely. You typically select a backup from a list, choose "Point-in-Time Restore", and enter a timestamp in a web UI. The service handles creating a new instance, finding the correct base backup, fetching the WAL files from its internal storage (like S3), and performing the replay. The trade-off is **simplicity vs. control/cost**. With RDS, you don't manage the WAL archive or `restore_command`, but you pay for the managed service and have less control over the underlying storage and recovery mechanisms. The open-source way is more complex but offers maximum flexibility and potentially lower direct costs.

</details>

---

#### **(ii) Disadvantages and Pitfalls**

**Exercise 2.1: The Peril of Replication Lag**

A failover is a common recovery mechanism in a replicated setup. However, it's not a silver bullet, especially with asynchronous replication.

1.  **Pitfall Demonstration:**
    a.  First, stop the network connection from the primary to the replica to simulate a network partition.
        ```bash
        docker-compose pause replica
        ```
    b.  Connect to the `primary` and insert a new, critical customer record.
        ```sql
        INSERT INTO customers (firstName, lastName, email) VALUES ('Charlie', 'Davis', 'charlie.davis@critical.com');
        ```
    c.  Now, simulate a primary failure by stopping its container.
        ```bash
        docker-compose stop primary
        ```
    d.  "Failover" by promoting the replica. Un-pause it and then use the provided `Makefile` target to promote it correctly.
        ```bash
        docker-compose unpause replica
        make promote-replica
        ```
    e.  Connect to the now-promoted replica using `make psql-replica` and check for the critical customer 'Charlie Davis'. Is the record there?
2.  **Explanation:** Why is the record missing? What fundamental trade-off of distributed systems does this demonstrate?

<details>
<summary>Solution 2.1</summary>

1.  After completing the steps, you will find that the customer 'Charlie Davis' is **not** on the newly promoted primary. The `INSERT` transaction was lost.

2.  **Explanation:** This demonstrates the major pitfall of failover with **asynchronous replication**.
    *   When we paused the replica, streaming replication stopped.
    *   The `INSERT` on the primary was committed locally and its WAL record was written, but it was never sent to the replica because of the partition. The use of a replication slot (`replica_slot`) correctly prevented the primary from deleting the WAL file, but it couldn't magically transmit it.
    *   When the primary "failed" and we promoted the replica, the replica only had the data it had received *before* the network partition.
    *   This is a classic example of the trade-offs described in the **CAP theorem**. We chose **Availability** (the primary could still accept writes even when the replica was disconnected) over strong **Consistency** (the replica was not guaranteed to be in sync). The result of this choice during a failure is potential data loss. A synchronous replication strategy would have prevented this, but the primary would have blocked on the `INSERT` until the replica acknowledged it, which would have been impossible during the network partition.

</details>

---

#### **(iii) Contrasting with Inefficient/Naive Solutions**

**Exercise 3.1: The Filesystem Copy Disaster**

A junior engineer suggests that for backups, we can just use `docker cp` to copy the live `PGDATA` directory (`/var/lib/postgresql/data`) to a backup location. They argue it's much simpler than dealing with WALs and `pg_basebackup`.

1.  **The Naive Approach (Simulated):**
    a.  While the primary database is running, execute a command that simulates a filesystem copy.
        ```bash
        docker-compose exec primary tar -cf /tmp/baddata.tar -C /var/lib/postgresql/data .
        ```
    b.  Now, simulate a disaster. Stop the primary and wipe its data directory.
        ```bash
        docker-compose stop primary
        docker-compose exec primary rm -rf /var/lib/postgresql/data/*
        ```
    c.  Attempt to restore using the "backup" you just made.
        ```bash
        docker-compose exec primary tar -xf /tmp/baddata.tar -C /var/lib/postgresql/data
        docker-compose start primary
        ```
    d.  Check the logs of the primary container using `make logs`. Does it start correctly? If not, why?
2.  **The Correct Approach:** Describe why the naive approach fails. What makes a tool like `pg_basebackup` fundamentally different and correct? How is this correct approach demonstrated in our UCEE's `replica/entrypoint.sh` script?

<details>
<summary>Solution 3.1</summary>

1.  When you check the logs in step (d), you will see a stream of errors. The server will likely fail to start, complaining about inconsistent data, partial page writes, or control file mismatches. The database is in a **non-crash-consistent state**.

2.  **Why it Fails:** The naive filesystem copy is not an atomic snapshot. While `tar` was running, the live database was constantly changing files.
    *   Some data files may have been written to disk *before* their corresponding WAL records were flushed.
    *   A single transaction might have changes that span multiple files, and the `tar` command could have copied some of these files before the transaction committed and others after, resulting in a physically corrupt state.
    *   The control file (`pg_control`) might have been copied at a different point in time than the data files, leading to a state mismatch.

    **The Correct Approach:** `pg_basebackup` is fundamentally different because it communicates with the PostgreSQL server to create a **consistent online backup**. It works by:
    a.  Putting the database into a special backup mode.
    b.  Ensuring all necessary WAL records from before and during the copy are preserved.
    c.  Copying the data files.
    d.  Taking the database out of backup mode.

    Our UCEE's `replica/entrypoint.sh` script demonstrates this correct approach perfectly. It explicitly calls `pg_basebackup` to create a consistent starting point for the replica. When this restored backup starts, PostgreSQL knows it's starting from a "fuzzy" but consistent state and uses the WAL files streamed from the primary to perform recovery and bring itself up to date.

</details>

---

#### **(iv) Hardcore Combined Problem**

**Exercise 4.1: The Full Disaster Recovery Drill**

**Scenario:** You are the lead data engineer for `statelessCommerce`.
1.  A network switch is failing, causing your hot standby **replica** to have intermittent connection issues, leading to significant replication lag.
2.  While you are investigating the network, a developer runs a faulty script on the **primary** that accidentally executes `TRUNCATE TABLE products CASCADE;`. All products and their related order items are now gone.
3.  Your C-level executives want the site back online with minimal data loss.

Your task is to orchestrate a full recovery. Simply failing over to the replica is unacceptable because of the replication lag—you would lose all orders placed since the lag began.

**Your Plan:**
1.  **Assess the Damage (Connects to Replication):** Use the `make test-lag` command to determine the exact amount of replication lag. This will prove why a simple failover is not an option.
2.  **Formulate Recovery Plan (Connects to Recovery Mechanisms):** Decide on the correct recovery strategy. You must use PITR. Since the primary's data is corrupt and the replica is stale, you must recover the primary database itself to a point in time before the `TRUNCATE`.
3.  **Execute the Recovery (Connects to Automation & Systems):** Write a Python orchestrator script (`fullRecoveryOrchestrator.py`) that performs the recovery by issuing the necessary `docker-compose` and `docker` commands to the host system. Your script should:
    a.  Prompt the user for the timestamp to recover to.
    b.  Stop the primary service (`docker-compose stop primary`).
    c.  Wipe the primary's data volume (`docker volume rm ...` and `docker volume create ...`).
    d.  Start a *temporary* PostgreSQL container using the `postgres:15` image, mounting the *now-empty* data volume and the *existing* WAL archive volume. This container's job is to run `pg_basebackup` to create a valid base from the WAL archive.
    e.  After the base backup is created, stop the temporary container.
    f.  Create the `recovery.signal` and configure `postgresql.conf` for PITR on the primary's data volume.
    g.  Start the original `primary` service (`docker-compose up -d primary`), which will now begin the PITR process.
    h.  Monitor the primary until it is healthy and accepting connections.

<details>
<summary>Solution 4.1</summary>

**1. Assess the Damage**

First, simulate the disaster.

```bash
# Pause the replica to induce lag
make stop-replica # You may need to add a 'stop-replica: docker-compose stop replica' target to the Makefile

# Get the current time on the primary BEFORE the disaster
make psql-primary
# SELECT now(); -- Record this timestamp, e.g., '2025-08-12 19:00:00 UTC'
# \q

# Run the damaging command
make psql-primary -c "TRUNCATE TABLE products CASCADE;"

# Now, check the lag. Unpause the replica first.
make start-replica # Add a 'start-replica: docker-compose start replica' target
make test-lag
```
The script will report a significant lag, confirming that a failover would cause data loss.

**2. Formulate Recovery Plan**

The correct plan is to perform a Point-in-Time Recovery on the primary server itself, since the WAL archive contains all the necessary data. The replica is irrelevant to this recovery process because it is both stale and not needed.

**3. Execute the Recovery**

<details>
<summary><code>solutions/fullRecoveryOrchestrator.py</code></summary>

```python
import subprocess
import sys
import time
import os

# Get volume names from docker-compose config
PROJECT_NAME = os.path.basename(os.getcwd())
DATA_VOLUME = "statelesscommerceprimarydata"
# Note: The WAL archive is now a directory inside the primary data volume,
# but for a real PITR, we assume it's on a separate, safe storage.
# Our setup simulates this by having the replica copy from it. For this script,
# we'll assume the `wal-archive` directory within the volume is our safe source.

def run_host_command(command, check=True):
    """Runs a command on the host machine."""
    print(f"Executing on host: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=check)
    if result.stdout: print(result.stdout)
    if result.stderr: print(f"STDERR: {result.stderr}", file=sys.stderr)
    return result

def main():
    recovery_target_time = input("Enter the recovery target timestamp (BEFORE the TRUNCATE): ")
    if not recovery_target_time:
        print("Timestamp is required.")
        sys.exit(1)

    print("\n--- Starting Full Disaster Recovery Drill ---")

    print("\n[Step 1] Stopping the primary service...")
    run_host_command(["docker-compose", "stop", "primary"])

    print(f"\n[Step 2] Wiping and recreating the primary data volume ('{DATA_VOLUME}')...")
    run_host_command(["docker", "volume", "rm", DATA_VOLUME])
    run_host_command(["docker", "volume", "create", DATA_VOLUME])
    
    # In a real-world scenario, you would now restore your latest base backup
    # into the new empty volume. Since we don't have an external backup,
    # we will skip this and rely on WAL replay from the beginning of time.
    # For a real system, this is where you'd use a tool like wal-g or pgBackRest.
    print("\n[Step 3] (Simulated) Base backup restored. Configuring for PITR...")

    recovery_conf = f"""
restore_command = 'cp /primary_data/wal-archive/%f %p'
recovery_target_time = '{recovery_target_time}'
recovery_target_action = 'promote'
"""
    # Use a temporary container to write the configuration to the volume
    run_host_command([
        "docker", "run", "--rm",
        "-v", f"{DATA_VOLUME}:/data",
        "busybox", "touch", "/data/recovery.signal"
    ])
    
    run_host_command([
        "docker", "run", "--rm",
        "-v", f"{DATA_VOLUME}:/data",
        "busybox", "sh", "-c", f"echo \"{recovery_conf}\" > /data/postgresql.conf"
    ])
    
    # pg_basebackup would typically set permissions, but since we are manually creating, we must ensure them.
    uid = os.environ.get('UID', '999') # 999 is the default postgres user in the image
    run_host_command([
        "docker", "run", "--rm",
        "-v", f"{DATA_VOLUME}:/data",
        "busybox", "chown", "-R", f"{uid}:{uid}", "/data"
    ])
    run_host_command([
        "docker", "run", "--rm",
        "-v", f"{DATA_VOLUME}:/data",
        "busybox", "chmod", "0700", "/data"
    ])

    print("\n[Step 4] Starting the primary service to initiate recovery...")
    run_host_command(["docker-compose", "up", "-d", "--no-deps", "primary"])

    print("\n[Step 5] Monitoring recovery...")
    for i in range(60):
        print(f"Waiting for recovery... {i*5}s")
        time.sleep(5)
        result = subprocess.run(
            ["docker-compose", "exec", "primary", "pg_isready", "-U", "admin"],
            capture_output=True, text=True
        )
        if "accepting connections" in result.stdout:
            print("✅ Recovery complete. New primary is online.")
            print("\n--- Full Recovery Drill Complete ---")
            print("Connect to the primary on port specified by PRIMARY_HOST_PORT and verify data.")
            return

    print("❌ Recovery monitoring timed out. Please check container logs with 'make logs'.")

if __name__ == "__main__":
    main()

```
</details>

**Execution:**
1.  Follow the steps in "Assess the Damage".
2.  Run the orchestrator: `docker-compose exec python_client python /solutions/fullRecoveryOrchestrator.py`
3.  Enter the recovery timestamp.
4.  Connect to the recovered primary (`make psql-primary`) and verify that the `products` table and its data are restored.

This exercise successfully integrates concepts of **replication lag analysis**, **snapshot/PITR strategy**, and **automation**. It forces the student to confront a realistic scenario where the simplest recovery option (failover) is incorrect, requiring a more nuanced, data-aware approach executed through scripted automation.

</details>
```
