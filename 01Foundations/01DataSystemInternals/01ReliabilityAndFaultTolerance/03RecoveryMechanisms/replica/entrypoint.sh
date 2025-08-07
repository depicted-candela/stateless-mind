#!/bin/bash
set -e

# This script runs as the 'postgres' user inside the container.

# Stop the server that was auto-started by the base image to allow backup.
pg_ctl -D "$PGDATA" -m fast -w stop

# Clean out the existing data directory to ensure a fresh restore.
rm -rf "$PGDATA"/*

echo "Starting base backup from primary..."

# Use a temporary .pgpass file for credentials during backup to avoid interactive prompts.
echo "primary:5432:*:admin:password" > ~/.pgpass
chmod 0600 ~/.pgpass

# Loop until the primary is available and the base backup succeeds.
# --create-slot ensures the primary creates a durable replication slot.
until pg_basebackup --pgdata="$PGDATA" --host=primary --username=admin -W --wal-method=stream --slot=replica_slot --create-slot
do
  echo "Waiting for primary to connect to create base backup..."
  sleep 1s
done

# Clean up the temporary password file immediately after use.
rm ~/.pgpass

# Set correct permissions for the data directory after backup.
chmod 0700 "$PGDATA"

# Create the standby.signal file to indicate this is a replica.
touch "$PGDATA/standby.signal"

# Create postgresql.auto.conf with connection info and restore command.
cat > "$PGDATA/postgresql.auto.conf" <<EOF
primary_conninfo = 'host=primary port=5432 user=admin password=password'
restore_command = 'cp /archive/%f %p'
primary_slot_name = 'replica_slot'
EOF

echo "Replica setup complete. The container will now start PostgreSQL..."
# The script now finishes, allowing the original Docker entrypoint to start postgres.