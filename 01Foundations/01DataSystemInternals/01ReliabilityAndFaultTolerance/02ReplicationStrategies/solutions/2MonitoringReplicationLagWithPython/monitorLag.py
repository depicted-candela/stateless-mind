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

        #  On leader, get the current WAL write location
        leaderCursor.execute("SELECT pg_current_wal_lsn();")
        leaderLsn = leaderCursor.fetchone()[0]

        #  On follower, get the last WAL location replayed
        followerCursor.execute("SELECT pg_last_wal_replay_lsn();")
        followerLsn = followerCursor.fetchone()[0]

        #  Convert LSNs from hex string format to integers for subtraction
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