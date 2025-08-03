import psycopg2
import time

# Global connection details, matching docker-compose.yml
config = {
    "leader": "dbname=appdb user=postgres password=postgres host=localhost port=5433",
    "follower": "dbname=appdb user=postgres password=postgres host=localhost port=5434"
}

# Store the connection string part that identifies the node for clear health checks
# We will update this after failover
roles = {
    "leader": "port=5433",
    "follower": "port=5434"
}

def getConnection(role):
    """Gets a connection to the database for a given role ('leader' or 'follower')."""
    # Check if the role (e.g., "follower") even exists in the config anymore
    if role not in config or not config[role]:
        return None
    try:
        conn = psycopg2.connect(config[role])
        return conn
    except psycopg2.OperationalError:
        return None

def updateInventory(productId, quantity):
    """Connects to the LEADER and performs a write operation."""
    print(f"\n--> Attempting write to LEADER ({roles['leader']})")
    conn = getConnection("leader")
    if not conn:
        print("Write failed: Leader is down.")
        return
    try:
        # Use a `with` block to ensure the transaction is managed and connection is closed
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE inventory SET quantity = %s, lastUpdated = NOW() WHERE productId = %s",
                    (quantity, productId)
                )
        print(f"Successfully updated productId {productId} to quantity {quantity}.")
    except psycopg2.Error as e:
        print(f"Write failed: {e}")
    finally:
        if conn:
            conn.close()

def readInventory(productId):
    """Connects to the FOLLOWER and performs a read operation."""
    # The .get() method safely handles the case where 'follower' no longer exists in roles
    print(f"\n--> Attempting read from FOLLOWER ({roles.get('follower', 'N/A')})")
    conn = getConnection("follower")
    if not conn:
        print("Read failed: Follower is down or does not exist.")
        return None
    try:
        with conn:
            conn.set_session(readonly=True) # Ensure session is read-only on follower
            with conn.cursor() as cur:
                cur.execute("SELECT productName, quantity FROM inventory WHERE productId = %s", (productId,))
                result = cur.fetchone()
                print(f"Read from follower: {result}")
                return result
    finally:
        if conn:
            conn.close()

def healthCheck():
    """Checks connectivity and replication lag."""
    print("\n--- HEALTH CHECK ---")
    leaderConn = getConnection("leader")
    followerConn = getConnection("follower")

    print(f"Leader ({roles.get('leader', 'N/A')}): {'UP' if leaderConn else 'DOWN'}")
    print(f"Follower ({roles.get('follower', 'N/A')}): {'UP' if followerConn else 'DOWN'}")

    # Only attempt to check lag if both databases are connectable
    if leaderConn and followerConn:
        try:
            with leaderConn.cursor() as lcur, followerConn.cursor() as fcur:
                lcur.execute("SELECT pg_current_wal_lsn();")
                # fetchone() returns a tuple, e.g., ('0/1A833D0',), so we get the first element
                leader_result = lcur.fetchone()
                leaderLsn_str = leader_result[0] if leader_result else None

                fcur.execute("SELECT pg_last_wal_replay_lsn();")
                follower_result = fcur.fetchone()
                followerLsn_str = follower_result[0] if follower_result else None

                # *** THE FIX IS HERE ***
                # Check if both LSNs were successfully retrieved before doing calculations.
                if leaderLsn_str and followerLsn_str:
                    # Convert LSN from hex string (e.g., '0/1A833D0') to an integer for comparison
                    leaderLsn = int(leaderLsn_str.split('/')[0], 16) << 32 | int(leaderLsn_str.split('/')[1], 16)
                    followerLsn = int(followerLsn_str.split('/')[0], 16) << 32 | int(followerLsn_str.split('/')[1], 16)
                    
                    lagBytes = leaderLsn - followerLsn
                    print(f"Replication Lag: {lagBytes} bytes")
                else:
                    # This handles the case where the follower is up but hasn't replayed anything yet.
                    print("Replication Lag: Initializing...")
        except psycopg2.Error as e:
            print(f"Could not check replication lag: {e}")
        finally:
            if leaderConn: leaderConn.close()
            if followerConn: followerConn.close()
    print("--------------------")

# --- Main execution loop ---
def main():
    """Main execution flow for the service simulation."""
    input("Please ensure your environment is running ('docker compose up -d'). Press Enter to start...")

    print("\nService running with initial configuration.")
    healthCheck()
    updateInventory(101, 88)
    time.sleep(2)  # Give time for replication
    readInventory(101)
    healthCheck()

    input("\nSUCCESS! Now, in a separate terminal, run 'docker rm -f leader' and then press Enter...")

    print("\nRe-running health check after simulated failure...")
    healthCheck()
    updateInventory(102, 66)  # This will fail

    input("\nLeader is down. Now, in a separate terminal, run 'docker exec -it --user postgres follower pg_ctl promote' and then press Enter...")

    # --- Manual Failover and Reconfiguration ---
    print("\nFollower promoted. Reconfiguring service...")
    # The old follower is the new leader
    config["leader"] = config["follower"]
    roles["leader"] = roles["follower"]
    # There is no follower anymore, so we remove it
    config.pop("follower")
    roles.pop("follower")

    print(f"Service reconfigured. New leader is on {roles['leader']}.")
    healthCheck()

    # Writes now go to the new leader
    updateInventory(102, 66)

    # Reads must also go to the new leader
    print(f"\n--> Attempting read from new LEADER ({roles['leader']})")
    conn = getConnection("leader")
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT productName, quantity FROM inventory WHERE productId = %s", (102,))
                result = cur.fetchone()
                print(f"Read from new leader: {result}")
        finally:
            conn.close()

    print("\nRecovery successful!")

if __name__ == "__main__":
    main()