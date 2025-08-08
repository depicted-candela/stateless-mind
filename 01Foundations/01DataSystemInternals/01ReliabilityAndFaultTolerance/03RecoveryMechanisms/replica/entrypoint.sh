#!/bin/bash
set -e

pg_ctl -D "$PGDATA" -m fast -w stop
rm -rf "$PGDATA"/*

echo "Starting base backup from primary..."
echo "primary:5432:*:admin:password" > ~/.pgpass
chmod 0600 ~/.pgpass

until pg_basebackup --pgdata="$PGDATA" --host=primary --username=admin -W --wal-method=stream --slot=replica_slot --create-slot
do
  echo "Waiting for primary to connect to create base backup..."
  sleep 1s
done

rm ~/.pgpass
chmod 0700 "$PGDATA"
touch "$PGDATA/standby.signal"

# Create postgresql.auto.conf with the corrected restore_command path.
cat > "$PGDATA/postgresql.auto.conf" <<EOF
primary_conninfo = 'host=primary port=5432 user=admin password=password'
restore_command = 'cp /primary_data/wal-archive/%f %p'
primary_slot_name = 'replica_slot'
EOF

echo "Replica setup complete. The container will now start PostgreSQL..."