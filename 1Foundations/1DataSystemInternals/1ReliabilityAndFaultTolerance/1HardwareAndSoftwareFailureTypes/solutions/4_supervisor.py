#     Setup: Runs generateData.py to ensure input.dat exists.

#   Lifecycle Management:
# Launches the compiled C worker as a subprocess, redirecting its stdin, stdout, and stderr.
# Writes all numbers from input.dat to the worker's stdin.
# Continuously and non-blockingly monitors the worker's stdout and stderr streams, and its 
# process status.
#   Fault Tolerance Logic:
# If a "Corrupted data" message appears on the worker's stderr, the supervisor must log a 
# warning and continue feeding data.
# If the worker process terminates unexpectedly (with a non-zero exit code), the supervisor must
# log a critical error, check that the cworker.lock file was properly removed, and attempt to
# restart the worker process once.
# After successfully processing all data, the supervisor must gracefully shut down the worker by 
# sending it a SIGTERM signal.

from time import sleep
import os, logging, sys, subprocess, select

from generateData import generateDataFile

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(levelname)s - %(message)s',
    stream=sys.stdout
)

DATA = "input.dat"
LOCKER = "cworker.lock"
STARTING_COMMAND = "./4_hardcore_worker"

def usesHardcoreWorker(starting_step=0):
    if not os.path.exists(STARTING_COMMAND):
        logging.error(f"The executable {STARTING_COMMAND} does not exist")
        sys.exit(1)
    if not os.path.exists(DATA):
        logging.error(f"The file {DATA} does not exist")
        sys.exit(1)
    if starting_step == 0:
        logging.info("First batch")
    else:
        logging.info(f"Batch started again at position {starting_step}")
    hard_worker = subprocess.Popen(
        [STARTING_COMMAND],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffering
    )
    try:
        processed_lines = starting_step
        with open(DATA, "r") as f:
            # Skip lines if resuming
            for _ in range(starting_step): f.readline()
            # Process input and output concurrently
            inputs = f.readlines()  # Read all remaining lines
            remaining_inputs = len(inputs)
            input_index = 0
            poller = select.poll()
            poller.register(hard_worker.stdout.fileno(), select.POLLIN)
            poller.register(hard_worker.stderr.fileno(), select.POLLIN)
            while input_index < len(inputs) or hard_worker.poll() is None:
                if input_index < len(inputs) and hard_worker.poll() is None:
                    hard_worker.stdin.write(inputs[input_index])
                    hard_worker.stdin.flush()
                    input_index += 1
                    sleep(0.01)  # Reduced delay for faster processing
                # Check for output
                for fd, _ in poller.poll(100):  # Timeout after 100ms
                    if fd == hard_worker.stdout.fileno():
                        processed_line = hard_worker.stdout.readline()
                        if processed_line:
                            logging.info(f"Line as: {processed_line.strip()}")
                            processed_lines += 1
                    elif fd == hard_worker.stderr.fileno():
                        error_catcher = hard_worker.stderr.readline()
                        if "Corrupted data" in error_catcher or "Recoverable software error" in error_catcher:
                            logging.warning(error_catcher.strip())
                if hard_worker.poll() is not None:
                    break
        # Check for remaining output after input is exhausted
        while hard_worker.poll() is None:
            for fd, _ in poller.poll(100):
                if fd == hard_worker.stdout.fileno():
                    processed_line = hard_worker.stdout.readline()
                    if processed_line:
                        logging.info(f"Line as: {processed_line.strip()}")
                        processed_lines += 1
                elif fd == hard_worker.stderr.fileno():
                    error_catcher = hard_worker.stderr.readline()
                    if "Corrupted data" in error_catcher or "Recoverable software error" in error_catcher:
                        logging.warning(error_catcher.strip())
        # Handle worker termination
        if hard_worker.poll() is None:
            hard_worker.terminate()  # Send SIGTERM
            hard_worker.wait(timeout=1)  # Wait for graceful shutdown
            logging.info("Worker terminated gracefully")
        if hard_worker.returncode is not None and hard_worker.returncode != 0:
            logging.warning(f"Critical error, probably a segmentation fault (exit code {hard_worker.returncode})")
            if os.path.exists(LOCKER): os.remove(LOCKER)
            usesHardcoreWorker(processed_lines + 1) if remaining_inputs > 2 else logging.error("All lines processed and error overcomed, exiting")
        else: logging.info("All lines processed successfully")
    except Exception as e:
        logging.error(f"Process aborted because of {e} exception")
        if hard_worker.poll() is None:
            hard_worker.terminate()
            hard_worker.wait(timeout=1)
    finally:
        if hard_worker.poll() is None:
            hard_worker.terminate()
            hard_worker.wait(timeout=1)
        exit(0)
    return

if __name__ == "__main__":
    generateDataFile()
    usesHardcoreWorker()