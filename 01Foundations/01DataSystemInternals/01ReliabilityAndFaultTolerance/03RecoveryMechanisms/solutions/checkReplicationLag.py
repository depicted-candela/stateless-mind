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

        if lag_bytes > 500: # Setting a threshold for significant lag
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