# **(i) Meanings, Values, Relations, and Advantages**

**Exercise 1.1: Point-in-Time Recovery (PITR) in Action**

1.  **Meaning and Value:** In your own words, what is Point-in-Time Recovery (PITR)? What is its primary value proposition compared to simply restoring the latest full backup?
2.  **Relation:** How does the Write-Ahead Log (WAL) from PostgreSQL, a concept tied to durability, enable the recovery mechanism of PITR? How does this relate to the concept of a replication log discussed in the previous section?
3.  **Practice:**
    a.  Connect to the `primary` database and record the current timestamp.
    b.  Delete all customers with the last name 'Johnson'.
        ```sql
        DELETE FROM customers WHERE lastName = 'Johnson';
        SELECT * FROM customers; -- Verify deletion
        ```
    c.  You've just made a critical error. Use the provided Python script `pitrOrchestrator.py` to perform a PITR. The script automates the process of stopping the primary, clearing its data, and replaying WAL files up to the timestamp you recorded.
4.  **Proprietary Contrast:** Describe how a managed database service like Amazon RDS or Google Cloud SQL simplifies this entire recovery process for the user. What trade-offs are being made?

<details>
<summary>Solution 1.1</summary>

1.  **Meaning and Value:** PITR is a recovery mechanism that allows a database to be restored to a specific moment in time, not just to the time a full backup was taken. Its primary value is minimizing data loss. While a full backup might be hours or days old, PITR uses a full backup *plus* a continuous log of all subsequent transactions (the WAL) to restore the database to the minute or second right before a failure or error occurred.

2.  **Relation:** The WAL is an ordered log of every change made to the database. This is fundamentally the same concept as a replication log used in leader-follower setups. Both are streams of data changes. Replication applies this stream to a live replica to keep it in sync. PITR applies this stream to a restored backup file to "roll it forward" to a specific point in time. Both rely on the same underlying principle of a durable, ordered log of transactions.

3.  **Practice:**
    a.  Connect and get timestamp:
        ```bash
        docker-compose exec primary psql -U admin -d statelessCommerce -c "SELECT now();"
         Example output: 2025-08-01 10:30:00.123456+00
        ```
    b.  Run the deletion.
    c.  The solution involves orchestrating a recovery.

    <details>
    <summary><code>solutions/pitrOrchestrator.py</code></summary>

    ```python
    import subprocess
    import sys
    import time
    import os

    def run_command(command, container):
        """Runs a command inside a specified docker container."""
        base_cmd = ["docker-compose", "exec", "-T", container]
        full_cmd = base_cmd + command
        print(f"Executing in {container}: {' '.join(command)}")
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error executing command: {result.stderr}")
        print(result.stdout)
        return result

    def main():
        recovery_target_time = input("Enter the recovery target timestamp (e.g., '2025-08-01 10:29:59 UTC'): ")
        if not recovery_target_time:
            print("Timestamp is required.")
            sys.exit(1)

        print("\n--- Starting Point-in-Time Recovery Simulation ---")

        print("\n[Step 1] Stopping the primary database server...")
        subprocess.run(["docker-compose", "stop", "primary"], check=True)

        print("\n[Step 2] Clearing the primary's data directory...")
        run_command(["rm", "-rf", "/var/lib/postgresql/data/*"], "primary")
        
        print("\n[Step 3] Restoring from base backup by copying from archive...")
         In a real scenario, you'd restore from your backup storage (e.g., S3).
         We simulate this by copying the archived data back.
        wal_archive_path = "/archive"  Path inside the container
        run_command(["pg_basebackup", "-D", "/var/lib/postgresql/data", "-h", os.environ['PRIMARY_HOST'], "-U", os.environ['DB_USER'], "-P", "-R"], "primary")


        print(f"\n[Step 4] Creating recovery signal with target time: {recovery_target_time}")
        recovery_conf = f"""
    recovery_target_time = '{recovery_target_time}'
    recovery_target_action = 'promote'
    restore_command = 'cp {wal_archive_path}/%f %p'
    """
        run_command(["touch", "/var/lib/postgresql/data/recovery.signal"], "primary")
        run_command(["bash", "-c", f"echo \"{recovery_conf}\" >> /var/lib/postgresql/data/postgresql.auto.conf"], "primary")
        run_command(["chmod", "0700", "/var/lib/postgresql/data"], "primary")


        print("\n[Step 5] Restarting the primary server to initiate recovery...")
        subprocess.run(["docker-compose", "start", "primary"], check=True)

        print("\n[Step 6] Monitoring recovery. This may take a minute...")
        recovered = False
        for _ in range(30):
            result = run_command(["pg_isready", "-U", "admin"], "primary")
            if "accepting connections" in result.stdout:
                print("Recovery complete. Primary is back online.")
                recovered = True
                break
            time.sleep(2)
        
        if not recovered:
            print("Recovery monitoring timed out. Please check logs.")
            sys.exit(1)
        
        print("\n--- PITR Simulation Complete ---")
        print("Verify the data has been restored correctly.")


    if __name__ == "__main__":
        main()
    ```
    </details>
    
    **Execution:**
    ```bash
     Get the timestamp, then delete the data in psql
     Then run the script:
    docker-compose exec pythonClient python /solutions/pitrOrchestrator.py
     When prompted, enter the timestamp you recorded before the deletion.
    ```
    After running, connect to the primary and verify the 'Johnson' customer has been restored.

4.  **Proprietary Contrast:** Managed services like Amazon RDS abstract this entirely. You typically select a backup from a list, choose "Point-in-Time Restore", and enter a timestamp in a web UI. The service handles creating a new instance, finding the correct base backup, fetching the WAL files from its internal storage (like S3), and performing the replay. The trade-off is **simplicity vs. control/cost**. With RDS, you don't manage the WAL archive or `restore_command`, but you pay for the managed service and have less control over the underlying storage and recovery mechanisms. The open-source way is more complex but offers maximum flexibility and potentially lower direct costs.

</details>

---

# **(ii) Disadvantages and Pitfalls**

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
    c.  Now, simulate a primary failure by stopping the container.
        ```bash
        docker-compose stop primary
        ```
    d.  "Failover" by promoting the replica. Un-pause it and promote it.
        ```bash
        docker-compose unpause replica
        docker-compose exec replica pg_ctl promote
        ```
    e.  Connect to the now-promoted replica (running on the host port specified by `REPLICA_HOST_PORT`) and check for the critical customer 'Charlie Davis'. Is the record there?
2.  **Explanation:** Why is the record missing? What fundamental trade-off of distributed systems does this demonstrate?

<details>
<summary>Solution 2.1</summary>

1.  After completing the steps, you will find that the customer 'Charlie Davis' is **not** on the newly promoted primary. The `INSERT` transaction was lost.

2.  **Explanation:** This demonstrates the major pitfall of failover with **asynchronous replication**.
    *   When we paused the replica, streaming replication stopped.
    *   The `INSERT` on the primary was committed locally and its WAL record was written, but it was never sent to the replica.
    *   When the primary "failed" and we promoted the replica, the replica only had the data it had received *before* the network partition.
    *   This is a classic example of the trade-offs described in the **CAP theorem**. We chose **Availability** (the primary could still accept writes even when the replica was disconnected) over strong **Consistency** (the replica was not guaranteed to be in sync). The result of this choice during a failure is potential data loss. A synchronous replication strategy would have prevented this, but the primary would have blocked on the `INSERT` until the replica acknowledged it, which would have been impossible during the network partition.

</details>

---

# **(iii) Contrasting with Inefficient/Naive Solutions**

**Exercise 3.1: The Filesystem Copy Disaster**

A junior engineer suggests that for backups, we can just use `docker cp` to copy the live `PGDATA` directory (`/var/lib/postgresql/data`) to a backup location. They argue it's much simpler than dealing with WALs and base backups.

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
    d.  Check the logs of the primary container. Does it start correctly? If not, why?
        ```bash
        docker-compose logs primary
        ```
2.  **The Correct Approach:** Describe why the naive approach fails. What makes a tool like `pg_basebackup` fundamentally different and correct?

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

    When you restore from this backup, PostgreSQL knows it's starting from a "fuzzy" but consistent state and uses the included WAL files to perform crash recovery, bringing the database to a perfectly consistent state. This is the only safe way to take a filesystem-level backup of a live database.

</details>

---

# **(iv) Hardcore Combined Problem**

**Exercise 4.1: The Full Disaster Recovery Drill**

**Scenario:** You are the lead data engineer for `statelessCommerce`.
1.  A network switch is failing, causing your hot standby **replica** to have intermittent connection issues, leading to significant replication lag.
2.  While you are investigating the network, a developer runs a faulty script on the **primary** that accidentally executes `TRUNCATE TABLE products CASCADE;`. All products and their related order items are now gone.
3.  Your C-level executives want the site back online with minimal data loss.

Your task is to orchestrate a full recovery. Simply failing over to the replica is unacceptable because of the replication lag—you would lose all orders placed since the lag began.

**Your Plan:**
1.  **Assess the Damage (Connects to Replication):** Write and use a Python script (`checkReplicationLag.py`) to connect to both the primary and replica to determine the exact amount of replication lag. This will prove why a simple failover is not an option.
2.  **Formulate Recovery Plan (Connects to Recovery Mechanisms):** Decide on the correct recovery strategy. You must use PITR. Since the primary's data is corrupt and the replica is stale, you must build a *new* server.
3.  **Execute the Recovery (Connects to Automation & Systems):** Write a Python orchestrator script (`fullRecoveryOrchestrator.py`) that simulates the following steps:
    a.  Stops and removes the old (corrupted) primary and stale replica containers.
    b.  Creates a *new* primary container (`primaryNew`).
    c.  On the new primary, simulates a restore from the last known good base backup.
    d.  Configures the new primary for PITR to a timestamp *just before* the `TRUNCATE` command was run.
    e.  Starts the new primary and lets it recover.
    f.  Verifies the `products` table is restored.

<details>
<summary>Solution 4.1</summary>

**1. Assess the Damage**

First, we simulate the network lag by pausing the replica, and then run the damaging command on the primary.

```bash
 In one terminal, pause the replica
docker-compose pause replica

 In another terminal, connect to primary and run TRUNCATE
 First, get the current time!
docker-compose exec primary psql -U admin -d statelessCommerce -c "SELECT now();"
 RECORD THIS TIMESTAMP! e.g., '2025-08-01 11:00:00 UTC'
docker-compose exec primary psql -U admin -d statelessCommerce -c "TRUNCATE TABLE products CASCADE;"
docker-compose exec primary psql -U admin -d statelessCommerce -c "SELECT COUNT(*) FROM products;" -- Should be 0
```

Now, unpause the replica and run the lag check script.

```bash
docker-compose unpause replica
 Wait a few seconds for it to reconnect
docker-compose exec pythonClient python /solutions/checkReplicationLag.py
```

<details>
<summary><code>solutions/checkReplicationLag.py</code></summary>

```python
import psycopg2
import os
import time

def get_db_connection(host):
    return psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=host,
        port=5432
    )

def get_current_wal_lsn(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT pg_current_wal_lsn()")
        return cur.fetchone()[0]

def get_last_replay_lsn(conn):
    with conn.cursor() as cur:
        time.sleep(5)
        cur.execute("SELECT pg_last_wal_replay_lsn()")
        return cur.fetchone()[0]

def lsn_to_bytes(lsn):
    parts = lsn.split('/')
    return int(parts[0], 16) * 16**8 + int(parts[1], 16)

def main():
    try:
        primary_conn = get_db_connection(os.environ['PRIMARY_HOST'])
        replica_conn = get_db_connection(os.environ['REPLICA_HOST'])

        primary_lsn_str = get_current_wal_lsn(primary_conn)
        replica_lsn_str = get_last_replay_lsn(replica_conn)

        primary_bytes = lsn_to_bytes(primary_lsn_str)
        replica_bytes = lsn_to_bytes(replica_lsn_str)

        lag_bytes = primary_bytes - replica_bytes

        print(f"Primary LSN: {primary_lsn_str} ({primary_bytes} bytes)")
        print(f"Replica LSN: {replica_lsn_str} ({replica_bytes} bytes)")
        print(f"Replication Lag: {lag_bytes / 1024:.2f} KB")

        if lag_bytes > 500:  Setting a threshold for significant lag
            print("\nWARNING: Replica is significantly lagging. Direct failover would result in data loss.")
        else:
            print("\nReplica is in sync or has minimal lag.")

    except psycopg2.OperationalError as e:
        print(f"Could not connect to database: {e}")
    finally:
        if 'primary_conn' in locals() and primary_conn:
            primary_conn.close()
        if 'replica_conn' in locals() and replica_conn:
            replica_conn.close()

if __name__ == "__main__":
    main()
```
</details>

You will see a significant lag reported, confirming that failing over would lose data.

**2. Formulate Recovery Plan**

The correct plan is:
-   Do not use the stale replica.
-   Do not try to fix the corrupted primary.
-   Create a new instance, restore it from the most recent base backup (which our Docker setup creates on init), and perform Point-in-Time Recovery using the archived WAL files to the moment *before* the `TRUNCATE` command was run.

**3. Execute the Recovery**

This conceptual orchestrator script uses Docker commands to achieve the recovery steps.

<details>
<summary><code>solutions/fullRecoveryOrchestrator.py</code> (Conceptual Implementation)</summary>

```python
import subprocess
import sys
import time
import os

def run_host_command(command):
    """Runs a command on the host machine."""
    print(f"Executing on host: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def main():
    recovery_target_time = input("Enter the recovery target timestamp (BEFORE the TRUNCATE): ")
    if not recovery_target_time:
        print("Timestamp is required.")
        sys.exit(1)

    print("\n--- Starting Full Disaster Recovery Drill ---")

    print("\n[Step 1] Tearing down the compromised environment...")
    run_host_command(["docker-compose", "down", "--volumes"])

    print("\n[Step 2] Re-creating volumes for the new environment...")
    run_host_command(["docker", "volume", "create", "statelessCommercePrimaryData"])
    run_host_command(["docker", "volume", "create", "statelessCommerceWalArchive"])

    print("\n[Step 3] Starting a temporary primary to create a 'base backup'...")
    run_host_command(["docker-compose", "up", "-d", "--no-deps", "primary"])

    print("\n[Step 4] Stopping the temporary primary...")
    run_host_command(["docker-compose", "stop", "primary"])
    
    print("\n[Step 5] Simulating restore: Re-initializing primary and configuring PITR...")
     Get the absolute path to the WAL archive on the host
    wal_volume_path = run_host_command(["docker", "volume", "inspect", "-f", "{{.Mountpoint}}", "statelessCommerceWalArchive"]).stdout.strip()
    
     We must run these next commands inside a temporary container with the volumes mounted
     to manipulate the files correctly.
    data_volume = "statelessCommercePrimaryData"
    archive_volume = "statelessCommerceWalArchive"
    
     1. Clean the data directory
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "rm", "-rf", "/data/*"])
    
     2. Run pg_basebackup to restore from the WAL archive (this is a conceptual step)
     A real backup would be on S3. Here, we just re-init and will rely on WAL replay.
     We re-create the data dir from scratch, then apply WALs.
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "-v", f"{archive_volume}:/archive", "postgres:15", "pg_basebackup", "-D", "/data", "-R", "--wal-method=fetch"])


    print(f"\n[Step 6] Creating recovery.signal and setting recovery target...")
    recovery_conf = f"restore_command = 'cp /archive/%f %p'\nrecovery_target_time = '{recovery_target_time}'\nrecovery_target_action = 'promote'\n"
    
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "touch", "/data/recovery.signal"])
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "sh", "-c", f"echo '{recovery_conf}' >> /data/postgresql.conf"])

    print("\n[Step 7] Starting the restored primary server...")
    run_host_command(["docker-compose", "up", "-d", "primary"])

    print("\n[Step 8] Monitoring recovery...")
    recovered = False
    for _ in range(60):  Increase timeout for recovery
        result = subprocess.run(["docker-compose", "exec", "primary", "pg_isready", "-U", "admin"], capture_output=True, text=True)
        if "accepting connections" in result.stdout:
            print("Recovery complete. New primary is online.")
            recovered = True
            break
        time.sleep(2)

    if not recovered:
        print("Recovery monitoring timed out. Please check container logs.")
        sys.exit(1)
        
    print("\n--- Full Recovery Drill Complete ---")
    print("Verify that the 'products' table and its data have been restored.")

if __name__ == "__main__":
    main()

```
</details>

**Execution:**
1.  Follow the steps in "Assess the Damage" to create a disaster scenario. Make sure you have the timestamp right before the `TRUNCATE`.
2.  Run the orchestrator: `python3 solutions/fullRecoveryOrchestrator.py`
3.  Enter the recovery timestamp when prompted.
4.  The script will tear down the old environment and bring up a new primary container.
5.  Connect to the new `primary` container and verify that the `products` and `orderItems` tables have been restored to their original state.

This exercise integrates understanding of replication lag, the mechanics of PITR, and the necessity of automation to execute a complex, multi-step recovery plan that prioritizes data integrity over simple availability.

</details>