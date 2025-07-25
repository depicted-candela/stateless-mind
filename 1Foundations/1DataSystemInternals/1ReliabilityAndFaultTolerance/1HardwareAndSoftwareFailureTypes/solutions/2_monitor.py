import os, logging, sys
from time import sleep

WORKERFILE = 'worker.lock'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(levelname)s - %(message)s',
    stream=sys.stdout
)

def checkWorkerExistance():
    if not os.path.exists(WORKERFILE): logging.warning(f"The worker does not have lock as {WORKERFILE} storing its pid")
    try:
        with open(WORKERFILE, "r") as r:
            pid = r.read().strip()
        os.kill(int(pid), 0)
        logging.info(f"The worker locked at {WORKERFILE} is actively creating singals with pid {pid}")
    except Exception as e:
        logging.warning(f"Becuase {e} the observation wasn't successfull")

if __name__ == '__main__':
    while True:
        checkWorkerExistance()
        sleep(1)