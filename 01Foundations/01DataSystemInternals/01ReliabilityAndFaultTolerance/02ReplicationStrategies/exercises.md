# Topic: Replication strategies (e.g., leader-follower, multi-leader)
## Section: 1.1 Data System Internals - *Phase: 1: Foundations*

# Dataset and Environment Setup

For these exercises, you will use Docker to create a PostgreSQL leader-follower replication setup. Thus you must have postgresql and docker desktop with docker compose already installed. This provides a consistent and isolated environment.

**1. Directory Structure:**

Create the following directory structure for your project:

```
solutions/
├── docker-compose.yml
├── leader/
│   ├── postgresql.conf
│   └── setup-leader.sh
└── follower/
    ├── postgresql.conf
    └── setup-follower.sh
```

**2. Install `Docker Desktop` with `Docker compose`

**3. Docker Compose (`docker-compose.yml`):**

This file defines the leader and follower services.

```yaml
services:
  leader:
    image: postgres:14
    container_name: leader
    hostname: leader
    restart: always
    ports:
      - "5433:5433"
    volumes:
      - ./leader/postgresql.conf:/etc/postgresql/postgresql.conf
      - ./leader-data:/var/lib/postgresql/data
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=appdb
    networks:
      - replication-net

  follower:
    image: postgres:14
    container_name: follower
    hostname: follower
    restart: always
    ports:
      - "5434:5433"
    depends_on:
      - leader
    volumes:
      - ./follower/postgresql.conf:/etc/postgresql/postgresql.conf
      - ./follower-data:/var/lib/postgresql/data
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=appdb
    networks:
      - replication-net

volumes:
  leader-data:
  follower-data:

networks:
  replication-net:
    driver: bridge
```

**3. Leader Configuration (`leader/postgresql.conf`):**

This configures the leader node for replication.

```ini
listen_addresses = '*'
wal_level = replica
max_wal_senders = 10
wal_keep_size = 256MB
hot_standby = on
```

**4. Follower Configuration (`follower/postgresql.conf`):**

This configures the follower node.

```ini
listen_addresses = '*'
hot_standby = on
```

**5. Initial Dataset (`inventory` table):**

You will create this table on the leader node after it starts.

```sql
CREATE TABLE inventory (
    productId INT PRIMARY KEY,
    productName VARCHAR(255) NOT NULL,
    quantity INT,
    lastUpdated TIMESTAMP
);

INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES
(101, 'QuantumWidget', 100, NOW()),
(102, 'HyperSpanner', 75, NOW()),
(103, 'FluxCapacitor', 50, NOW());
```

**To Start the Environment:**
See the state of docker with `sudo systemctl status docker`, and restart it with `sudo systemctl restart docker` as necessary where `sudo systemctl enable docker` starts docker as the machine is turned on

Follow this [instructions](https://docs.docker.com/engine/security/rootless/)

Run `docker compose up -d` in the `solutions` directory. The containers will start, but replication is not yet configured. The exercises will guide you through the full setup.

---

# (i) Meanings, Values, Relations, and Advantages

These exercises focus on the fundamental purpose and benefits of replication strategies using the specified open-source technology (PostgreSQL and Python).

## Exercise 1: Setting Up and Verifying Leader-Follower Replication

**Problem:**
A core principle of reliable systems, as discussed in DDIA Chapter 5, is ensuring data is not lost if a single node fails. Leader-follower replication is the most common pattern to achieve this.

Your task is to finalize the configuration of the Docker environment to establish a streaming replication link from the `leader` to the `follower`. Then, create the `inventory` table on the leader, insert the initial data, and verify that the data is successfully replicated to the follower.

**Solution:**

1.  **Stop running containers if they exist:**
    ```bash
    docker compose down -v
    ```

2.  **Start the leader node:**
    ```bash
    docker compose up -d leader
    ```

3.  **Create the replication user and slot on the leader:** Connect to the leader and create a user with replication privileges. A replication slot ensures the leader retains WAL logs until the follower has consumed them.
    ```bash
    docker exec -it leader psql -U postgres -d appdb -c "CREATE USER replicator WITH REPLICATION PASSWORD 'replicatorpass';"
    docker exec -it leader psql -U postgres -d appdb -c "SELECT * FROM pg_create_physical_replication_slot('follower_slot');"
    ```

4.  **Add replication user to `pg_hba.conf` on the leader:**
    ```bash
    echo "host replication replicator all md5" | docker exec -i leader tee -a /var/lib/postgresql/data/pg_hba.conf
    docker exec -it --user postgres leader pg_ctl reload
    ```

5.  **Take a base backup from the leader:** This command stops the follower, clears its data directory, and uses `pg_basebackup` to clone the leader's data. This is the standard procedure for initializing a follower.
    ```bash
    docker compose stop follower
    sudo rm -rf ./follower-data/*  # Clear previous data
    docker run --rm \
        -e PGPASSWORD=replicatorpass \
        -v $(pwd)/follower-data:/output \
        --network=solutions_replication-net \
        postgres:14 \
        pg_basebackup -h leader -D /output -U replicator -p 5432 -vP -R --slot=follower_slot
    ```
    *Note: The `-R` flag automatically writes the `standby.signal` file and connection info into the follower's data directory.*

6.  **Start the follower:**
    ```bash
    docker compose up -d follower
    ```

7.  **Create and populate the `inventory` table on the leader:**
    ```bash
    docker exec -it leader psql -U postgres -d appdb -c "CREATE TABLE inventory (productId INT PRIMARY KEY, productName VARCHAR(255) NOT NULL, quantity INT, lastUpdated TIMESTAMP);"
    docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (101, 'QuantumWidget', 100, NOW()), (102, 'HyperSpanner', 75, NOW()), (103, 'FluxCapacitor', 50, NOW());"
    ```

8.  **Verify replication on the follower:** The follower is read-only. A successful query confirms that replication is working.
    ```bash
    docker exec -it follower psql -U postgres -d appdb -c "SELECT * FROM inventory;"
     Expected output:
      productId |  productName  | quantity |         lastUpdated
     -----------+---------------+----------+----------------------------
            101 | QuantumWidget |      100 | 2025-07-22 23:41:34.123456
            102 | HyperSpanner  |       75 | 2025-07-22 23:41:34.123456
            103 | FluxCapacitor |       50 | 2025-07-22 23:41:34.123456
    ```

## Exercise 2: Monitoring Replication Lag with Python

**Problem:**
Asynchronous replication introduces a delay known as replication lag. This concept relates to the "Hardware and software failure types" topic because a large lag can lead to significant data loss if the leader fails. Your task is to write a Python script using `psycopg2` to connect to both the leader and follower and report the replication lag in bytes.

**Solution:**

1.  **Install psycopg2:**
    ```bash
    pip install "psycopg2-binary"
    ```
2.  **Create the Python script `monitorLag.py`:**
    ```python
    import psycopg2
    import time

    LEADERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5433"
    FOLLOWERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5434"

    def getPgConnection(connString):
        try:
            return psycopg2.connect(connString)
        except psycopg2.OperationalError as e:
            print(f"Could not connect to database: {e}")
            return None

    def checkReplicationLag():
        leaderConn = getPgConnection(LEADERPARAMS)
        followerConn = getPgConnection(FOLLOWERPARAMS)

        if not leaderConn or not followerConn:
            return

        try:
            leaderCursor = leaderConn.cursor()
            followerCursor = followerConn.cursor()

             On leader, get the current WAL write location
            leaderCursor.execute("SELECT pg_current_wal_lsn();")
            leaderLsn = leaderCursor.fetchone()[0]

             On follower, get the last WAL location replayed
            followerCursor.execute("SELECT pg_last_wal_replay_lsn();")
            followerLsn = followerCursor.fetchone()[0]

             Convert LSNs from hex string format to integers for subtraction
            leaderLsnInt = int(leaderLsn.split('/')[0], 16) * 16**8 + int(leaderLsn.split('/')[1], 16)
            followerLsnInt = int(followerLsn.split('/')[0], 16) * 16**8 + int(followerLsn.split('/')[1], 16)

            lagBytes = leaderLsnInt - followerLsnInt
            print(f"Current replication lag: {lagBytes} bytes")

        finally:
            if leaderConn:
                leaderConn.close()
            if followerConn:
                followerConn.close()

    if __name__ == "__main__":
        while True:
            checkReplicationLag()
            time.sleep(2)
    ```
3.  **Run the script:**
    ```bash
    python monitorLag.py
    ```
    You will see the replication lag reported every two seconds. It should be close to 0 bytes when the system is idle. This script demonstrates a key advantage of open-source: direct, granular access to internal system metrics.

## Exercise 3: Contrasting with Proprietary/Managed Alternatives

**Problem:**
Setting up replication manually requires understanding WALs, replication slots, and `pg_basebackup`. How does a managed database service like **Amazon RDS** or **Google Cloud SQL** alter the approach to creating a read replica (a follower)? What are the primary advantages and disadvantages of using the managed service for this task compared to your manual setup?

**Solution (Conceptual):**

*   **How it's Altered/Simplified:**
    *   **Abstraction:** Managed services abstract away the entire setup process. Creating a read replica is typically done with a few clicks in a web console or a single API call/CLI command (e.g., `gcloud sql replicas create ...`).
    *   **No Manual Configuration:** You do not need to edit `postgresql.conf` or `pg_hba.conf`, create replication users, or run `pg_basebackup`. The service handles all of this automatically in the background.
    *   **Integrated Monitoring:** Replication lag is usually exposed as a pre-configured metric (e.g., in AWS CloudWatch or Google Cloud Monitoring) with built-in alerting, removing the need for custom scripts.
    *   **Failover:** Managed services offer automated, push-button failover to promote a replica to a new leader, which is a complex process to implement reliably from scratch.

*   **Advantages of Managed Service:**
    *   **Simplicity and Speed:** A replica can be provisioned in minutes with minimal database expertise.
    *   **Reduced Operational Overhead:** The cloud provider manages patching, backups, monitoring, and failover mechanisms for the replication infrastructure.
    *   **Reliability:** The replication and failover processes are battle-tested by the cloud provider across thousands of customers.

*   **Disadvantages (Trade-offs):**
    *   **Less Control:** You lose fine-grained control over replication parameters (e.g., specific WAL settings, replication slot management). This is the key benefit of the open-source approach you just practiced.
    *   **Cost:** Managed services have a higher cost than running the same on a self-managed virtual machine, as you are paying for the management layer.
    *   **Vendor Lock-in:** The APIs and tools for managing replication are specific to the cloud provider, making it harder to migrate to another provider or back to a self-hosted environment.

---

# (ii) Disadvantages and Pitfalls

These exercises highlight the operational complexities and potential failure modes of replication.

## Exercise 4: The Pitfall of Asynchronous Replication Lag

**Problem:**
The primary disadvantage of asynchronous replication is data loss on leader failure. If the leader fails before writes are sent to the follower, that data is gone. Simulate this scenario to observe the data loss directly.

**Solution:**

1.  **Ensure replication is running.**
2.  **Stop network connectivity from the leader to the follower:** The easiest way to do this without stopping the container is to disconnect the `leader` from the network.
    ```bash
    docker network disconnect solutions_replication-net leader
    ```
3.  **Perform a write on the leader:** Since the leader is disconnected, this write will *not* be replicated.
    ```bash
    docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (201, 'IsolatedPhoton', 10, NOW());" ## Verify the write on the leader
    docker exec -it leader psql -U postgres -d appdb -c "SELECT * FROM inventory WHERE productId=201;"
    ```
4.  **Simulate a catastrophic leader failure:** We simply remove the leader container. In a real-world scenario, this would be a server crash.
    ```bash
    docker rm -f leader
    ```
5.  **Promote the follower:** The follower now becomes the new leader, but it never received the last write.
    ```bash
    docker exec -it follower touch standby.signal && docker compose restart follower ## The presence of standby.signal makes it a follower, removing it (or promoting) makes it a primary. Let's assume we would promote it with pg_ctl promote
    docker exec -it --user postgres follower pg_ctl promote
    ```
6.  **Check for the "lost" data on the new leader (the old follower):**
    ```bash
    docker exec -it follower psql -U postgres -d appdb -c "SELECT * FROM inventory WHERE productId=201;"
     Expected output:
     (0 rows)
    ```
    This demonstrates the classic pitfall: the write was confirmed to the client by the old leader but is now lost forever.

## Exercise 5: Understanding Split-Brain in Multi-Leader Replication

**Problem:**
This is a conceptual question based on DDIA Chapter 5. While our setup is leader-follower, it's crucial to understand the primary danger of multi-leader replication. Describe what "split brain" is in a multi-leader context. Why is it a significant problem, and what is the fundamental mechanism used to prevent it?

**Solution (Conceptual):**

*   **What is Split Brain?** In a multi-leader (or any distributed system requiring a single leader, like with automatic failover), split brain occurs when a network partition causes two or more nodes to believe they are the leader simultaneously. For example, if two leaders, A and B, cannot communicate, A might think B is down, and B might think A is down. Both might then be promoted to leader by clients in their respective network partitions.

*   **Why is it a problem?** Each self-proclaimed leader will independently accept writes. This leads to two divergent histories of the data that cannot be easily merged. When the network partition heals, you have two conflicting "sources of truth." Resolving these conflicts often requires manual intervention and almost always results in data loss. For instance, if user 1 updates their password on node A and user 2 updates it on node B, which password is correct?

*   **Prevention Mechanism:** The fundamental mechanism to prevent split brain is **fencing**, often implemented with a technique called **STONITH** (Shoot The Other Node In The Head). Before a new leader is allowed to become active, it must ensure the old leader is definitively offline and can no longer accept writes. This is often done through an external channel, like a power controller that reboots the old leader, or a network switch that blocks its traffic. This guarantees that only one node can be the active leader at any given time.

---

# (iii) Contrasting with Inefficient/Naive Solutions

## Exercise 6: Naive Solutions

This exercise contrasts the correct replication pattern with a common but flawed alternative.

**Problem:**
A developer is tasked with building a system that can handle high read traffic and survive the failure of a single database server. Their naive solution is to have the application layer write to two independent PostgreSQL servers simultaneously in a `try...except` block. Reads are then randomly distributed between the two servers.

Identify at least three critical flaws with this "dual-write" application-layer approach and then implement the correct, robust solution using the provided Docker environment.

**Solution:**

**Flaws in the Naive "Dual-Write" Approach:**

1.  **No Consistency Guarantee:** A write could succeed on Server A but fail on Server B (due to a network glitch, disk full, etc.). The application might retry, leading to duplicate data on Server A, or give up, leaving the databases permanently inconsistent. There is no source of truth.
2.  **No Failover Logic for Writes:** If Server A fails, the application can write to B. But what happens when A comes back online? It has missed writes and is now stale. The application logic would need to handle this complex "catch-up" process, which is exactly what database replication is designed for.
3.  **Read Inconsistency (Stale Reads):** A user could write data (which succeeds on both servers) and immediately issue a read that lands on a server that is momentarily lagging for some other reason (e.g., higher load), resulting in a stale read. This is similar to replication lag but without any formal mechanism to manage or measure it.
4.  **Operational Complexity:** The application becomes responsible for data consistency, a task databases are built to handle. This logic is difficult to get right, error-prone, and makes the application fragile.

**Correct Implementation (using the configured replication setup):**

The correct solution is the leader-follower setup from Exercise (i).
1.  **Set up Leader-Follower Replication:** Complete all steps from Exercise (i)-1 to establish robust, database-native replication.
2.  **Application Logic:** The application logic becomes vastly simpler:
    *   **Writes:** All write operations (`INSERT`, `UPDATE`, `DELETE`) are **always** sent to the leader's address (`localhost:5432`).
    *   **Reads:** All read operations (`SELECT`) can be load-balanced between the leader (`localhost:5432`) and the follower (`localhost:5433`).
3.  **Demonstrate the correct read/write pattern with Python:**
    `naiveSolution.py`
    ```python
    import psycopg2
    import random

    LEADERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5432"
    FOLLOWERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5433"
    READENDPOINTS = [LEADERPARAMS, FOLLOWERPARAMS]

    ## WRITES always go to the leader
    def updateProductQuantity(productId, newQuantity):
        with psycopg2.connect(LEADERPARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE inventory SET quantity = %s, lastUpdated = NOW() WHERE productId = %s",
                    (newQuantity, productId)
                )
        print(f"Updated productId {productId} on LEADER.")

    ## READS can go to any endpoint
    def getProductQuantity(productId):
        connString = random.choice(READENDPOINTS)
        port = connString.split('port=')[1]
        with psycopg2.connect(connString) as conn:
             The follower will be read-only
            conn.set_session(readonly=True)
            with conn.cursor() as cur:
                cur.execute("SELECT quantity FROM inventory WHERE productId = %s", (productId,))
                quantity = cur.fetchone()[0]
                print(f"Read quantity for productId {productId} from endpoint on port {port}: {quantity}")
                return quantity

    updateProductQuantity(101, 99)
    ## Give a moment for replication
    import time
    time.sleep(1)
    getProductQuantity(101)
    getProductQuantity(101)
    ```
    This code demonstrates the correct, simplified application logic. The database handles the complexity of data propagation and consistency.

---

# (iv) Hardcore Combined Problem

This problem integrates the current topic with all preceding concepts in the syllabus.

**Problem:**
You are tasked with building a fault-tolerant Python service that provides a simple API for an `inventory` system. The service must ensure data durability against a single server crash and provide a way to check system health.

**Requirements:**
1.  Use the PostgreSQL leader-follower setup from Exercise (i).
2.  Create a Python script `resilientService.py` that does the following:
    *   It maintains a connection to both the leader (`localhost:5432`) and the follower (`localhost:5433`).
    *   It includes a function `updateInventory(productId, quantity)` that **always writes to the leader**.
    *   It includes a function `readInventory(productId)` that **always reads from the follower** to simulate read scaling.
    *   It includes a `healthCheck()` function that reports:
        *   If the leader is connectable.
        *   If the follower is connectable.
        *   The current replication lag in bytes (from Exercise (i)-2).
3.  Simulate a **hardware failure** on the leader node by stopping the `leader` container.
4.  Your script's `healthCheck` function should detect the failure.
5.  Manually perform a failover by promoting the `follower` to become the new leader.
6.  Modify your Python script's connection logic `on-the-fly` (or by restarting it with new parameters) to treat the old follower at port `5433` as the new leader for both reads and writes, demonstrating recovery from the failure.

**Solution:**

1.  **Start with a fresh, working replication setup** from Exercise (i).
2.  **Create `resilientService.py`:**
    ```python
    import psycopg2
    import time
    import sys

     Global connection details, can be updated during runtime
    config = {
        "leader": "dbname=appdb user=postgres password=postgres host=localhost port=5432",
        "follower": "dbname=appdb user=postgres password=postgres host=localhost port=5433"
    }

    def getConnection(role):
        try:
            conn = psycopg2.connect(config[role])
            return conn
        except psycopg2.OperationalError:
            return None

    def updateInventory(productId, quantity):
        print(f"\n--> Attempting write to LEADER ({config['leader']})")
        conn = getConnection("leader")
        if not conn:
            print("Write failed: Leader is down.")
            return
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE inventory SET quantity = %s, lastUpdated = NOW() WHERE productId = %s",
                    (quantity, productId)
                )
        print(f"Successfully updated productId {productId} to quantity {quantity}.")
        conn.close()

    def readInventory(productId):
        print(f"\n--> Attempting read from FOLLOWER ({config['follower']})")
        conn = getConnection("follower")
        if not conn:
            print("Read failed: Follower is down.")
            return None
        with conn:
            conn.set_session(readonly=True)
            with conn.cursor() as cur:
                cur.execute("SELECT productName, quantity FROM inventory WHERE productId = %s", (productId,))
                result = cur.fetchone()
                print(f"Read from follower: {result}")
                return result
        conn.close()


    def healthCheck():
        print("\n--- HEALTH CHECK ---")
        leaderConn = getConnection("leader")
        followerConn = getConnection("follower")

        print(f"Leader ({config['leader']}): {'UP' if leaderConn else 'DOWN'}")
        print(f"Follower ({config['follower']}): {'UP' if followerConn else 'DOWN'}")

        if leaderConn and followerConn:
            try:
                lcur = leaderConn.cursor()
                fcur = followerConn.cursor()

                lcur.execute("SELECT pg_current_wal_lsn();")
                leaderLsn = lcur.fetchone()[0]
                fcur.execute("SELECT pg_last_wal_replay_lsn();")
                followerLsn = fcur.fetchone()[0]

                leaderLsnInt = int(leaderLsn.split('/')[0], 16) * 16**8 + int(leaderLsn.split('/')[1], 16)
                followerLsnInt = int(followerLsn.split('/')[0], 16) * 16**8 + int(followerLsn.split('/')[1], 16)

                lagBytes = leaderLsnInt - followerLsnInt
                print(f"Replication Lag: {lagBytes} bytes")
            finally:
                leaderConn.close()
                followerConn.close()
        print("--------------------")

     --- Main execution loop ---
    print("Service running with initial configuration.")
    healthCheck()
    updateInventory(101, 88)
    time.sleep(2)
    readInventory(101)
    healthCheck()

    input("\nPress Enter to simulate leader failure (docker rm -f leader)...")
     In a separate terminal, run: docker rm -f leader

    print("\nRe-running health check after simulated failure...")
    healthCheck()
    updateInventory(102, 66)  This will fail

    input("\nLeader is down. Press Enter to promote follower and reconfigure service...")

     --- Manual Failover and Reconfiguration ---
     In a separate terminal: docker exec -it follower pg_ctl promote
    print("Follower promoted. Reconfiguring service...")
    config["leader"] = "dbname=appdb user=postgres password=postgres host=localhost port=5433"
    config["follower"] = None  No follower exists anymore

    print("Service reconfigured. New leader is at port 5433.")
    healthCheck()  Follower will show as down because config is None
    
     Writes now go to the new leader
    updateInventory(102, 66)
    
     We can also read from the new leader now
    print(f"\n--> Attempting read from new LEADER ({config['leader']})")
    conn = getConnection("leader")
    with conn.cursor() as cur:
        cur.execute("SELECT productName, quantity FROM inventory WHERE productId = %s", (102,))
        result = cur.fetchone()
        print(f"Read from new leader: {result}")
    conn.close()
    ```

3.  **Execution Steps:**
    1.  Run the Python script: `python resilientService.py`. It will perform an initial health check, an update, and a read.
    2.  The script will pause. In another terminal, simulate the leader failure: `docker rm -f leader`.
    3.  Return to the Python script and press Enter. The health check will now show the leader is `DOWN` and the write operation will fail.
    4.  The script will pause again. In the other terminal, promote the follower: `docker exec -it follower pg_ctl promote`.
    5.  Return to the Python script and press Enter. The script reconfigures itself, routing all traffic to the newly promoted leader on port 5433. The subsequent `updateInventory` and `readInventory` calls will now succeed against the new leader, demonstrating a successful (though manual) recovery from a catastrophic node failure. This exercise integrates replication setup, failure simulation, monitoring, and recovery logic.