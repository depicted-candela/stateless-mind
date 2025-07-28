#     Setup: Runs generateData.py to ensure input.dat exists.

#   Lifecycle Management:
# Launches the compiled C worker as a subprocess, redirecting its stdin, stdout, 
# and stderr. Writes all numbers from input.dat to the worker's stdin.
# Continuously and non-blockingly monitors the worker's stdout and stderr 
# streams, and its process status.
#   Fault Tolerance Logic:
# If a "Corrupted data" message appears on the worker's stderr, the supervisor 
# must log a warning and continue feeding data.
# If the worker process terminates unexpectedly (with a non-zero exit code), the 
# supervisor must log a critical error, check that the cworker.lock file was 
# properly removed, and attempt to restart the worker process once.
# After successfully processing all data, the supervisor must gracefully shut 
# down the worker by sending it a SIGTERM signal.
import subprocess, select, generateData, logging, sys, os

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)

EXECUTABLE = ["./4_hardcore_worker"]
LOCK_WORKER = "cworker.lock"
data_file = "input.dat"



def observes_worker(starting_line = 0):

    if not os.path.exists(EXECUTABLE[0]):
        logging.warning(f"The executable <{EXECUTABLE[0]}> for the expected c worker does not exists")
        return

    hardcore_worker = subprocess.Popen(
        EXECUTABLE,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    maximum_step = 0
    batch_size = 0

    try:
        lines = []
        with open(data_file, "r") as f:
            for _ in range(starting_line):
                f.readline()
            lines = f.readlines()
        
        batch_size = len(lines)

        worker_buffer = select.poll()
        worker_buffer.register(hardcore_worker.stdout.fileno(), select.POLLIN)
        worker_buffer.register(hardcore_worker.stderr.fileno(), select.POLLIN)
        while maximum_step < batch_size or hardcore_worker.poll() is None:
            line = lines[maximum_step]
            hardcore_worker.stdin.write(line)
            hardcore_worker.stdin.flush()
            for fd, _ in worker_buffer.poll(10):
                if fd == hardcore_worker.stdout.fileno():
                    processed_line = hardcore_worker.stdout.readline()
                    if processed_line: logging.info(f"Line successfully readed as: {processed_line}")
                    maximum_step += 1
                if fd == hardcore_worker.stderr.fileno():
                    error_line = hardcore_worker.stderr.readline()
                    if "Corrupted data" in error_line: 
                        logging.warning(f"{error_line}")
                        maximum_step += 1
                    elif "Triggering fatal" in error_line:
                        logging.warning(f"FATAL: {error_line}")
                        maximum_step += 1
                        hardcore_worker.terminate()
                    else: logging.warning(f"FATAL: {error_line}")
            if maximum_step == batch_size: break

        if batch_size > 1: observes_worker(starting_line + maximum_step - 1)

    except Exception as e:
        logging.warning(f"With exception <{e}> the worker struggled")
        if batch_size == maximum_step: hardcore_worker.terminate()
        
    finally: 
        if batch_size == maximum_step and os.path.exists(LOCK_WORKER): 
            hardcore_worker.terminate()
            os.remove(LOCK_WORKER)

if __name__ == "__main__":
    generateData.generateDataFile()
    if os.path.exists(LOCK_WORKER):
        logging.warning(f"The locker <{LOCK_WORKER}> currently exists")
        os.remove(LOCK_WORKER)
    observes_worker()