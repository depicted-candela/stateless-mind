#!/bin/bash
set -e

# This script runs once as root when the database is first initialized.

# Append a rule to pg_hba.conf to allow the replica to connect for replication.
echo "host replication all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "Initialization complete: pg_hba.conf updated for replication."