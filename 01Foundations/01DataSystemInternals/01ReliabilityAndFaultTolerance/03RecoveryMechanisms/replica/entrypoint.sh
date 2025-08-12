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