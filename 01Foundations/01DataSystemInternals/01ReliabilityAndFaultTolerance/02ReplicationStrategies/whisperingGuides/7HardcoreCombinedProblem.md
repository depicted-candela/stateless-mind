The problem is to set up a resilient Python service that replicates data between PostgreSQL leader and follower nodes, monitors replication lag, and handles leader failure with failover.

Here's a breakdown of the necessary and sufficient features, configurations, and concepts:

### 1. Docker and Docker Compose Setup

*   **Prerequisites:** Docker Desktop with Docker Compose installed.
*   **Directory Structure:** A specific structure for `docker-compose.yml`, leader, and follower configurations.
*   **`docker-compose.yml`:** Defines `leader` and `follower` services with specified PostgreSQL image, ports, volumes, environment variables, and network.
*   **PostgreSQL Configuration:**
    *   `leader/postgresql.conf`: `listen_addresses = '*'`, `wal_level = replica`, `max_wal_senders = 10`, `wal_keep_size = 256MB`, `hot_standby = on`.
    *   `follower/postgresql.conf`: `listen_addresses = '*'`, `hot_standby = on`.
*   **Starting Containers:** `docker compose up -d`.
*   **Host Directory Ownership:** `sudo chown -R $(id -u):$(id -g) ./leader-data ./follower-data` to fix ownership issues.

### 2. Leader Configuration and Replication User

*   **Start Leader:** `docker compose up -d leader` followed by `sleep 5`.
*   **Create Replication User:** Connect to the leader and create a user with replication privileges:
    ```sql
    CREATE USER replicator WITH REPLICATION PASSWORD 'replicatorpass';
    ```
*   **Create Replication Slot:** Ensure the leader retains WAL logs until the follower consumes them:
    ```sql
    SELECT pg_create_physical_replication_slot('follower_slot');
    ```
*   **Configure `pg_hba.conf` on Leader:** Allow the replication user to connect:
    ```bash
    echo "host replication replicator all md5" | docker exec -i leader tee -a /var/lib/postgresql/data/pg_hba.conf
    ```
*   **Reload Leader Configuration:** `docker exec -it --user postgres leader pg_ctl reload`.

### 3. Base Backup and Follower Initialization

*   **Stop Follower:** `docker compose stop follower`.
*   **Clear Follower Data:** `sudo rm -rf ./follower-data/*`.
*   **Take Base Backup:** Use `pg_basebackup` to clone the leader's data. The `-R` flag automatically creates `standby.signal` and connection info.
    ```bash
    docker run --rm \
        -e PGPASSWORD=replicatorpass \
        -v $(pwd)/follower-data:/output \
        --network=solutions_replication-net \
        postgres:14 \
        pg_basebackup -h leader -D /output -U replicator -p 5432 -vP -R --slot=follower_slot
    ```
*   **Start Follower:** `docker compose up -d follower`.

### 4. Data Setup and Verification

*   **Create Table on Leader:**
    ```sql
    CREATE TABLE inventory (
        productId INT PRIMARY KEY,
        productName VARCHAR(255) NOT NULL,
        quantity INT,
        lastUpdated TIMESTAMP
    );
    ```
*   **Insert Initial Data on Leader:**
    ```bash
    docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (101, 'QuantumWidget', 100, NOW()), (102, 'HyperSpanner', 75, NOW()), (103, 'FluxCapacitor', 50, NOW());"
    ```
*   **Verify Replication on Follower:**
    ```bash
    docker exec -it follower psql -U postgres -d appdb -c "SELECT * FROM inventory;"
    ```

### 5. Python Script (`resilientService.py`) for Monitoring and Failover

*   **Install `psycopg2`:** `pip install "psycopg2-binary"`
*   **Connection Parameters:** Global `config` dictionary for leader and follower connections, and `roles` dictionary for identifying nodes.
*   **`getConnection(role)`:** Function to establish a database connection, returning `None` if the role is not configured or connection fails.
*   **`updateInventory(productId, quantity)`:** Writes to the leader. Handles leader down scenario.
*   **`readInventory(productId)`:** Reads from the follower. Handles follower down or non-existent scenarios.
*   **`healthCheck()`:**
    *   Checks connectivity to leader and follower.
    *   Calculates replication lag in bytes using `pg_current_wal_lsn()` from the leader and `pg_last_wal_replay_lsn()` from the follower.
    *   Handles cases where LSNs might not be retrieved.
*   **`main()` execution flow:**
    1.  Initial health check, update, and read.
    2.  Simulate leader failure (`docker rm -f leader`).
    3.  Re-run health check (leader down, write fails).
    4.  Manually promote follower (`docker exec -it follower pg_ctl promote`).
    5.  Reconfigure service connections (`config["leader"] = config["follower"]`, update `roles`, pop follower).
    6.  Perform health check on the new configuration.
    7.  Perform update and read operations against the new leader.

### 6. Concepts and Guarantees

*   **Replication:** Keeping a copy of data on multiple machines for high availability, scalability, and reduced latency.
*   **Leader-Follower (Master-Slave):** One node accepts writes, others replicate. Followers are read-only.
*   **Streaming Replication:** Standby servers receive WAL records as they're generated, minimizing lag.
*   **Replication Lag:** Delay between a write on the leader and its application on the follower. Measured in bytes. A significant lag can lead to data loss if the leader fails.
*   **Replication Slots:** Ensure the leader retains WAL segments until the follower consumes them.
*   **`pg_basebackup`:** Tool to create a base backup for initializing a follower.
*   **Asynchronous vs. Synchronous Replication:** Asynchronous allows the leader to process writes without waiting for follower confirmation (potential data loss on leader failure). Synchronous ensures data is written to the follower before confirming the write (higher durability but potential for increased latency and blocking on follower failure).
*   **Failover:** The process of promoting a follower to become the new leader when the current leader fails.
*   **Split Brain:** A situation in a multi-leader or automatically failover system where two nodes believe they are the leader simultaneously, leading to data inconsistency.
*   **Fencing (STONITH):** A mechanism to prevent split brain by ensuring the old leader is definitively offline before a new one takes over.
*   **Read-after-Write Consistency:** Guarantee that a user sees their own submitted updates immediately.
*   **Monotonic Reads:** Guarantee that a user never sees older data after having seen newer data.
*   **Consistent Prefix Reads:** Guarantee that if a sequence of writes happens in a certain order, then any subsequent reads will see them in the same order.
*   **Total Order Broadcast:** A protocol that ensures messages are delivered reliably, in the same order, to all nodes, even in the presence of network failures. This is crucial for leader election and distributed consensus.
*   **Consensus:** A fundamental problem in distributed systems where nodes need to agree on a value or decision. Algorithms like Paxos, Raft, and ZooKeeper's Zab are used to achieve this.
*   **`pg_stat_activity`:** A PostgreSQL view providing information about currently executing server processes.
*   **`pg_stat_replication`:** A PostgreSQL view providing statistics about replication to standby servers.
*   **`pg_current_wal_lsn()` and `pg_last_wal_replay_lsn()`:** PostgreSQL functions used to retrieve WAL locations for calculating replication lag.

This comprehensive set of features, configurations, and concepts covers the requirements of the "Hardcore Combined Problem" for setting up a resilient, replicated PostgreSQL system with monitoring and failover capabilities.