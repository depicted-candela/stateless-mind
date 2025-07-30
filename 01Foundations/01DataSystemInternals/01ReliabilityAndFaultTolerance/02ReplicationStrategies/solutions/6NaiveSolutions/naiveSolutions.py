import psycopg2
import random

LEADERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5433"
FOLLOWERPARAMS = "dbname=appdb user=postgres password=postgres host=localhost port=5434"
READENDPOINTS = [LEADERPARAMS, FOLLOWERPARAMS]

## WRITES always go to the leader
def updateProductQuantity(productId, newQuantity):
    with psycopg2.connect(LEADERPARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE inventory SET quantity = %s, lastUpdated = NOW() WHERE productId = %s",
                (newQuantity, productId)
            )
    print(f"Updated productId {productId} on LEADER.")

## READS can go to any endpoint
def getProductQuantity(productId):
    connString = random.choice(READENDPOINTS)
    port = connString.split('port=')[1]
    with psycopg2.connect(connString) as conn:
        #  The follower will be read-only
        conn.set_session(readonly=True)
        with conn.cursor() as cur:
            cur.execute("SELECT quantity FROM inventory WHERE productId = %s", (productId,))
            quantity = cur.fetchone()[0]
            print(f"Read quantity for productId {productId} from endpoint on port {port}: {quantity}")
            return quantity

updateProductQuantity(101, 99)
## Give a moment for replication
import time
time.sleep(1)
getProductQuantity(101)
getProductQuantity(101)