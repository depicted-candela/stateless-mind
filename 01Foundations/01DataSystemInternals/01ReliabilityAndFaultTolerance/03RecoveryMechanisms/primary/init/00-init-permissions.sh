#!/bin/bash
set -e

# This script runs once as root when the database is first initialized.

# 1. Create a subdirectory within the data volume for WAL files.
mkdir -p /var/lib/postgresql/data/wal-archive

# 2. Change ownership of this NEW subdirectory to the postgres user.
# This works because this script runs as root before the server starts as postgres.
chown -R postgres:postgres /var/lib/postgresql/data/wal-archive

# 3. Append a rule to pg_hba.conf to allow the replica to connect.
echo "host replication all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "Initialization complete: pg_hba.conf updated and WAL archive directory prepared."