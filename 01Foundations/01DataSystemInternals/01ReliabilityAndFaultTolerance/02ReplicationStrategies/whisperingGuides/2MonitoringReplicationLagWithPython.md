To monitor replication lag using Python and psycopg2, you'll need to:

1.  **Install psycopg2:**
    This library allows Python to interact with PostgreSQL databases.
    ```bash
    pip install "psycopg2-binary"
    ```

2.  **Establish Database Connections:**
    You'll need to connect to both the leader and follower PostgreSQL instances. The provided script uses connection strings that specify the database name, user, password, host, and port.

    ```python
    LEADERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5433"
    FOLLOWERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5434"

    def getPgConnection(connString):
        try:
            return psycopg2.connect(connString)
        except psycopg2.OperationalError as e:
            print(f"Could not connect to database: {e}")
            return None
    ```

3.  **Retrieve Replication Information:**
    To calculate the lag, you need to query specific PostgreSQL system functions:
    *   On the leader, use `pg_current_wal_lsn()` to get the current Write-Ahead Log (WAL) write location.
    *   On the follower, use `pg_last_wal_replay_lsn()` to get the last WAL location that has been replayed.

    ```python
    # On leader, get the current WAL write location
    leaderCursor.execute("SELECT pg_current_wal_lsn();")
    leaderLsn = leaderCursor.fetchone()[0]

    # On follower, get the last WAL location replayed
    followerCursor.execute("SELECT pg_last_wal_replay_lsn();")
    followerLsn = followerCursor.fetchone()[0]
    ```

4.  **Calculate Replication Lag:**
    The LSN (Log Sequence Number) is returned as a hexadecimal string (e.g., '0/1A833D0'). You need to convert these into integers to calculate the difference, which represents the lag in bytes.

    ```python
    # Convert LSNs from hex string format to integers for subtraction
    leaderLsnInt = int(leaderLsn.split('/')[0], 16) * 16**8 + int(leaderLsn.split('/')[1], 16)
    followerLsnInt = int(followerLsn.split('/')[0], 16) * 16**8 + int(followerLsn.split('/')[1], 16)

    lagBytes = leaderLsnInt - followerLsnInt
    print(f"Current replication lag: {lagBytes} bytes")
    ```

5.  **Loop and Report:**
    The script runs in an infinite loop, checking and printing the replication lag every 2 seconds.

    ```python
    if __name__ == "__main__":
        while True:
            checkReplicationLag()
            time.sleep(2)
    ```

This script demonstrates how to access and interpret PostgreSQL's replication status for monitoring purposes, a key advantage of open-source technologies.