#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# set -e

# --- Self-location and Directory Change Logic ---
# This is the magic part. It ensures the script always runs from the 'solutions' directory.
#
# "$0" is the path to this script itself.
# dirname "$0" gets the directory part of that path (e.g., ./1SettingUpAndVerifyingLeaderFollowerReplication)
# The 'cd' command then changes the current working directory to the parent ('..') of that directory.
# This forces the script's context to be the 'solutions' folder.
cd "$(dirname "$0")/.."

# Optional: Verify the new working directory.
echo "Forcing execution context to: $(pwd)"
# --- End of Self-location Logic ---


# --- Introduction and Password Prompt ---
echo "--- PostgreSQL Replication Setup Script ---"
echo "This script will reset the environment and set up leader-follower replication."
echo "You will be prompted for your sudo password once at the beginning."

# 'Prime the pump' for sudo. This will ask for the password upfront and cache it.
sudo -v

# --- 1. Clean Up Existing Environment ---
echo ""
echo "--- Step 1: Cleaning up previous Docker environment... ---"
# Use '|| true' to prevent script exit if containers don't exist
docker compose down -v || true 
sudo rm -rf ./follower-data/* ./leader-data/*
echo "Environment cleaned."

# --- 2. Set Permissions and Start Leader ---
echo ""
echo "--- Step 2: Setting data directory permissions and starting leader... ---"
sudo chown -R $(id -u):$(id -g) ./leader-data ./follower-data
docker compose up -d leader
echo "Waiting 5 seconds for leader to initialize..."
sleep 5
echo "Leader started."

# --- 3. Configure Replication on Leader ---
echo ""
echo "--- Step 3: Creating replication user and slot on the leader... ---"
docker exec -it --user postgres leader psql -U postgres -d appdb -c "CREATE USER replicator WITH REPLICATION PASSWORD 'replicatorpass';"
docker exec -it --user postgres leader psql -U postgres -d appdb -c "SELECT * FROM pg_create_physical_replication_slot('follower_slot');"
echo "host replication replicator all md5" | docker exec -i leader tee -a /var/lib/postgresql/data/pg_hba.conf
docker exec -it --user postgres leader pg_ctl reload
echo "Leader replication configured."

# --- 4. Initialize Follower from Base Backup ---
echo ""
echo "--- Step 4: Taking base backup from leader to initialize follower... ---"
# Stop the follower container if it's running from a previous attempt
docker compose stop follower || true
sudo rm -rf ./follower-data/* # Clear again to be safe
docker run --rm \
    -e PGPASSWORD=replicatorpass \
    -v $(pwd)/follower-data:/output \
    --network=solutions_replication-net \
    postgres:15 \
    pg_basebackup -h leader -D /output -U replicator -p 5432 -vP -R --slot=follower_slot
echo "Base backup complete."

# --- 5. Start Follower and Verify ---
echo ""
echo "--- Step 5: Starting the follower... ---"
docker compose up -d follower
echo "Follower started. Waiting 5 seconds for it to sync..."
sleep 5

echo ""
echo "--- Step 6: Creating initial data on the leader... ---"
docker exec -it leader psql -U postgres -d appdb -c "CREATE TABLE inventory (productId INT PRIMARY KEY, productName VARCHAR(255) NOT NULL, quantity INT, lastUpdated TIMESTAMP);"
docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (101, 'QuantumWidget', 100, NOW()), (102, 'HyperSpanner', 75, NOW()), (103, 'FluxCapacitor', 50, NOW());"
echo "Initial data inserted on leader."

echo ""
echo "--- Step 7: Verifying data on the follower... ---"
docker exec -it follower psql -U postgres -d appdb -c "SELECT * FROM inventory;"

echo ""
echo "--- Setup Complete! ---"
echo "Leader is running on port 5433, follower on port 5434."