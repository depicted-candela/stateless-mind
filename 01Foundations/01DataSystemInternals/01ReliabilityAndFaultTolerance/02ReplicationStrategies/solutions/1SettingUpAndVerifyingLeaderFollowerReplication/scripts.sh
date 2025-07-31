docker compose up -d
docker compose down -v
docker compose up -d leader
docker exec -it leader psql -U postgres -d appdb -c "CREATE USER replicator WITH REPLICATION PASSWORD 'replicatorpass';"
docker exec -it leader psql -U postgres -d appdb -c "SELECT * FROM pg_create_physical_replication_slot('follower_slot');"
echo "host replication replicator all md5" | docker exec -i leader tee -a /var/lib/postgresql/data/pg_hba.conf
docker exec -it --user postgres leader pg_ctl reload
docker compose stop follower
sudo rm -rf ./follower-data/*
docker run --rm \
    -e PGPASSWORD=replicatorpass \
    -v $(pwd)/follower-data:/output \
    --network=solutions_replication-net \
    postgres:14 \
    pg_basebackup -h leader -D /output -U replicator -p 5432 -vP -R --slot=follower_slot
docker compose up -d follower
docker exec -it leader psql -U postgres -d appdb -c "CREATE TABLE inventory (productId INT PRIMARY KEY, productName VARCHAR(255) NOT NULL, quantity INT, lastUpdated TIMESTAMP);"
docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (101, 'QuantumWidget', 100, NOW()), (102, 'HyperSpanner', 75, NOW()), (103, 'FluxCapacitor', 50, NOW());"