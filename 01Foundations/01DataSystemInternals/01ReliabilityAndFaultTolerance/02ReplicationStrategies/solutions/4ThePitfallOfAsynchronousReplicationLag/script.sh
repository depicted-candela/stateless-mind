## Problem: The primary disadvantage of asynchronous replication is data 
# loss on leader failure. If the leader fails before writes are sent to the 
# follower, that data is gone. Simulate this scenario to observe the data 
# loss directly.

docker network disconnect network replication-net leader

docker exec -it leader psql -U postgres -d appdb -c "INSERT INTO inventory (productId, productName, quantity, lastUpdated) VALUES (201, 'IsolatedPhoton', 10, NOW());"
docker exec -it leader psql -U postgres -d appdb -c "SELECT * FROM inventory WHERE productId = 201;"

docker rm -f leader

docker exec -it leader touch standby.signal && docker compose restart follower
docker exec -it --user postgres follower pg_ctl promote


docker exec -it follower psql -U postgres -d appdb -c "SELECT * FROM inventory WHERE productId=201;"