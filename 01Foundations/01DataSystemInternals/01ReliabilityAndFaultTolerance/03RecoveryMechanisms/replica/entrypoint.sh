#!/bin/bash
set -e

# Stop the server that was auto-started by the base image.
pg_ctl -D "$PGDATA" -m fast -w stop

# Clean out the existing data directory.
rm -rf "$PGDATA"/*

echo "Starting base backup from primary..."
# Use a temporary .pgpass file for credentials.
echo "primary:5432:*:admin:password" > ~/.pgpass
chmod 0600 ~/.pgpass

# Loop until the base backup succeeds.
until pg_basebackup --pgdata="$PGDATA" --host=primary --username=admin -W --wal-method=stream --slot=replica_slot --create-slot
do
  echo "Waiting for primary to connect..."
  sleep 1s
done

rm ~/.pgpass
chmod 0700 "$PGDATA"
touch "$PGDATA/standby.signal"

# Create postgresql.auto.conf with the corrected restore_command.
cat > "$PGDATA/postgresql.auto.conf" <<EOF
primary_conninfo = 'host=primary port=5432 user=admin password=password'
restore_command = 'cp /primary_data/wal-archive/%f %p'
primary_slot_name = 'replica_slot'
EOF

echo "Replica setup complete."