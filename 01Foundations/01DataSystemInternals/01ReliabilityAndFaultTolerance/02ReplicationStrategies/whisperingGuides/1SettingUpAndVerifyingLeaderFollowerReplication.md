To set up a leader-follower replication with Docker, you'll need to ensure you have PostgreSQL and Docker Desktop with Docker Compose installed.

Here's a breakdown of the necessary features and configurations:

**1. Directory Structure:**
   - Create a project directory with the following structure:
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

**2. Docker Installation:**
   - Install Docker Desktop with Docker Compose.
   - For rootless Docker, follow the instructions at [https://docs.docker.com/engine/security/rootless/](https://docs.docker.com/engine/security/rootless/) and run `export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock` in your terminal.

**3. Docker Compose Configuration (`docker-compose.yml`):**
   - This file defines the `leader` and `follower` services.
   - **Leader Service:**
     - `image: postgres:14`
     - `container_name: leader`, `hostname: leader`
     - `restart: always`
     - `ports: ["5433:5432"]` (maps host port 5433 to container port 5432)
     - `volumes:`
       - `./leader/postgresql.conf:/etc/postgresql/postgresql.conf` (mounts leader's config)
       - `./leader-data:/var/lib/postgresql/data` (mounts leader's data directory)
     - `command: postgres -c config_file=/etc/postgresql/postgresql.conf` (starts PostgreSQL with the specified config)
     - `environment:` (sets PostgreSQL user, password, and database name)
       - `POSTGRES_USER: postgres`
       - `POSTGRES_PASSWORD: postgres`
       - `POSTGRES_DB: appdb`
     - `networks: - replication-net`
   - **Follower Service:**
     - Similar configuration to the leader, but with `ports: ["5434:5432"]` to map to a different host port.
     - `depends_on: - leader` (ensures leader starts before follower)
     - `networks: - replication-net`
   - **Volumes:**
     - `leader-data:`
     - `follower-data:` (defines named volumes for persistent data)
   - **Networks:**
     - `replication-net:` (defines a bridge network for communication between containers)

**4. Leader Configuration (`leader/postgresql.conf`):**
   - `listen_addresses = '*'` (allows connections from any IP address)
   - `wal_level = replica` (enables WAL logging for replication)
   - `max_wal_senders = 10` (sets the maximum number of WAL sender processes)
   - `wal_keep_size = 256MB` (defines the minimum amount of WAL files to keep)
   - `hot_standby = on` (allows read-only queries on the follower)

**5. Follower Configuration (`follower/postgresql.conf`):**
   - `listen_addresses = '*'`
   - `hot_standby = on`

**6. Initial Dataset (`inventory` table):**
   - This table will be created on the leader and replicated to the follower.
   - SQL statements to create the table and insert initial data are provided in the exercise description.

**7. Starting the Environment:**
   - `docker compose up -d`: Starts the containers in detached mode.
   - `docker compose down -v`: Stops and removes the containers and volumes (useful for a clean start).
   - `sudo chown -R $(id -u):$(id -g) ./leader-data ./follower-data`: Fixes host directory ownership issues for Docker volumes.
   - `docker compose up -d leader`: Starts only the leader container, with a `sleep 5` command to allow it to initialize.

**8. Leader Setup for Replication:**
   - **Create replication user and slot:**
     ```bash
     docker exec -it --user postgres leader psql -U postgres -d appdb -c "CREATE USER replicator WITH REPLICATION PASSWORD 'replicatorpass';"
     docker exec -it --user postgres leader psql -U postgres -d appdb -c "SELECT * FROM pg_create_physical_replication_slot('follower_slot');"
     ```
     - `CREATE USER ... WITH REPLICATION PASSWORD ...`: Creates a user with replication privileges and sets a password.
     - `pg_create_physical_replication_slot()`: Creates a replication slot on the leader to ensure WAL logs are retained until the follower consumes them.

   - **Add replication user to `pg_hba.conf`:**
     ```bash
     echo "host replication replicator all md5" | docker exec -i leader tee -a /var/lib/postgresql/data/pg_hba.conf
     docker exec -it --user postgres leader pg_ctl reload
     ```
     - This command appends a rule to the `pg_hba.conf` file on the leader, allowing the `replicator` user to connect from any host with replication privileges using MD5 password authentication.
     - `pg_ctl reload`: Reloads the PostgreSQL configuration to apply the changes.

**9. Base Backup from Leader:**
   - `docker compose stop follower`: Stops the follower container.
   - `sudo rm -rf ./follower-data/*`: Clears the follower's data directory.
   - `docker run --rm ... postgres:14 pg_basebackup ...`: This command clones the leader's data to initialize the follower.
     - `-e PGPASSWORD=replicatorpass`: Sets the password for the replication user.
     - `-v $(pwd)/follower-data:/output`: Mounts the follower's data directory to `/output` in the run container.
     - `--network=solutions_replication-net`: Connects the run container to the replication network.
     - `pg_basebackup`: The PostgreSQL utility for taking a base backup.
       - `-h leader`: Specifies the leader host.
       - `-D /output`: Specifies the destination directory for the backup.
       - `-U replicator`: Specifies the replication user.
       - `-p 5432`: Specifies the port (PostgreSQL default is 5432).
       - `-vP`: Verbose output and progress.
       - `-R`: Automatically writes `standby.signal` and connection info to the follower's data directory.
       - `--slot=follower_slot`: Uses the created replication slot.

**10. Starting the Follower:**
    - `docker compose up -d follower`: Starts the follower container, which will now connect to the leader using the base backup information.

**11. Creating and Populating the `inventory` Table on the Leader:**
    - Use `docker exec` to connect to the leader and execute the SQL commands for creating the table and inserting data.

**12. Verifying Replication on the Follower:**
    - Use `docker exec` to connect to the follower and query the `inventory` table.
    - The expected output shows the data successfully replicated.

**Key Concepts and Configurations:**

*   **Replication User:** A dedicated PostgreSQL user with `REPLICATION` privileges is essential for the follower to connect to the leader and stream WAL data.
*   **Replication Slot:** A mechanism on the leader that ensures WAL data is not removed until it has been consumed by the follower, preventing data loss during replication.
*   **`pg_basebackup`:** A crucial utility for initializing a follower by taking a consistent base backup of the leader's data. The `-R` flag is key for automating the follower's configuration.
*   **`postgresql.conf`:** This configuration file is used on both leader and follower nodes to set parameters like `wal_level`, `max_wal_senders`, `hot_standby`, etc.
*   **`pg_hba.conf`:** This file controls client authentication. For replication to work, an entry must be added to allow the replication user to connect.
*   **Streaming Replication:** The process where WAL records are streamed directly from the leader to the follower.
*   **Hot Standby:** Allows read-only queries to be executed on the follower, enabling read scaling.
*   **`standby.signal`:** A file that, when present in the data directory, tells PostgreSQL to start in standby mode.