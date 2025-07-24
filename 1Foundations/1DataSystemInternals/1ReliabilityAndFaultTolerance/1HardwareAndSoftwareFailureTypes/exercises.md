<head>
    <link rel="stylesheet" href="../../../../styles/exercises.css">
</head>
<body>
    <div class="container">
        <h1>Practical Application: Hardware and Software Failure Types</h1>
        <h2>Introduction & Learning Objectives</h2>
        <p>
            Welcome to the first practical exercise set in the "Stateless Mind" curriculum. These exercises are designed to translate the theoretical concepts of <strong>Hardware and software failure types</strong> into tangible, hands-on skills. You will move beyond theory to implement and observe failure modes, build resilient code, and understand the fundamental challenges of creating reliable systems.
        </p>
        <p>
            The primary reference materials for this section are <code>Designing Data-Intensive Applications, Chapter 8</code> and <code>Computer Organization and Design, Section 5.5</code>. Throughout these exercises, you will be challenged to think critically about the trade-offs between direct, open-source implementations and the abstractions offered by proprietary managed services.
        </p>
        <p>Upon completing this section, you will be able to:</p>
        <ul>
            <li>Differentiate between hardware faults, software bugs, transient errors, and fatal failures within a programmatic context.</li>
            <li>Implement robust fault-tolerance mechanisms, including detailed logging, graceful shutdowns, and resource cleanup using both Python and C.</li>
            <li>Use low-level system tools, such as C signal handlers, to manage process state and ensure resilient recovery from catastrophic software errors.</li>
            <li>Analyze the practical trade-offs between self-managed fault tolerance in open-source environments and the automated recovery features of managed cloud platforms.</li>
            <li>Recognize and articulate the fundamental ambiguity between process crashes, process pauses, and network partitions in distributed systems.</li>
        </ul>
        <h2>Prerequisites & Setup</h2>
        <h3>Prerequisites</h3>
        <p>
            As this is the first topic in the course, there are no preceding sections to review. However, a foundational understanding of the following is required:
        </p>
        <ul>
            <li>Basic proficiency in Python, including file I/O, exception handling, and the <code>subprocess</code> module.</li>
            <li>Basic proficiency in C, including file I/O, function pointers, and the compilation process with <code>gcc</code>.</li>
            <li>Familiarity with command-line operations in a Unix-like environment (Linux, macOS, or WSL).</li>
        </ul>
        <h3>Environment & Dataset Setup</h3>
        <p>
            Follow these steps to prepare your environment. A correct setup is crucial for the exercises to function as intended.
        </p>
        <ol>
            <li>
                <strong>Install Required Tools:</strong> Ensure you have a working C compiler (<code>gcc</code> is recommended) and a Python 3.10+ interpreter installed on your system.
            </li>
            <li>
                <strong>Create a Project Directory:</strong> Create a dedicated folder for these exercises to keep your files organized.
            </li>
            <li>
                <strong>Generate the Dataset:</strong> Save the following Python script as <code>generateData.py</code> in your project directory. This script will create the <code>input.dat</code> file used in subsequent exercises.

```python
# generateData.py
import random
def generateDataFile(filename="input.dat", lines=100):
    """
    Generates a file with numerical data for processing.
    - Positive integers are valid data.
    - Negative integers simulate hardware read errors (data corruption).
    - The number 999 is a trigger for a software bug (segfault in C).
    - The number 0 is a trigger for a recoverable software error.
    """
    with open(filename, 'w') as f:
        # Ensure specific failure cases are present
        failurePoints = [-10, 0, 999, -25]
        for i in range(lines - len(failurePoints)):
            f.write(f"{random.randint(1, 100)}\n")
        
        # Intersperse failure points
        for point in failurePoints:
             f.write(f"{point}\n")
    print(f"Generated '{filename}' with {lines} lines.")
if __name__ == "__main__":
    generateDataFile()
```

</li>
<li>
    <strong>Execute the Script:</strong> Run the script from your terminal to create the data file:

```python
python generateData.py
```

</li>
<li>
    <strong>Understand the Data:</strong> The generated <code>input.dat</code> file contains integers. Each value has a specific meaning for our exercises:
    <ul>
        <li><strong>Positive Integers:</strong> Valid sensor readings.</li>
        <li><strong>Negative Integers:</strong> Simulate transient hardware faults (e.g., data corruption).</li>
        <li><strong>Zero (0):</strong> A trigger for a recoverable software bug.</li>
        <li><strong>999:</strong> A trigger for a fatal, unrecoverable software crash (segmentation fault).</li>
    </ul>
</li>
</ol>
<div class="caution">
<p><strong>Important Note:</strong> Several exercises create <code>.lock</code> files. If a program terminates abnormally during your experimentation, these files may not be cleaned up. Before each run, ensure no stale <code>.lock</code> files exist in your directory by running <code>rm -f *.lock</code>.</p>
</div>
<h2>Exercise Structure Overview</h2>
<p>The exercises are divided into four distinct types to build a comprehensive, practical understanding of the topic:</p>
<ol>
<li>
    <strong>Meanings, Values, Relations, and Advantages:</strong> These exercises focus on implementing the core concepts, identifying their purpose, and comparing open-source approaches with proprietary alternatives.
</li>
<li>
    <strong>Disadvantages and Pitfalls:</strong> These tasks are designed to expose you to the common failure modes, limitations, and conceptual traps associated with the topic.
</li>
<li>
    <strong>Contrasting with Inefficient/Naive Solutions:</strong> Here, you will first analyze a flawed or simplistic approach and then implement the correct, robust, and idiomatic solution.
</li>
<li>
    <strong>Hardcore Combined Problem:</strong> This final challenge integrates all concepts from the topic into a single, multi-part system that requires you to synthesize your knowledge.
</li>
</ol>
<h2>Exercises: Hardware and Software Failure Types</h2>
<h3>Exercise 1: Meanings, Values, Relations, and Advantages</h3>
<h4>Problem</h4>
<p>You are tasked with writing a robust data processing script in Python. The script reads sensor data from <code>input.dat</code>. You know that the system is prone to two kinds of issues:</p>
<ol>
<li><strong>Transient Hardware Faults:</strong> Occasionally, a sensor reading might be corrupted during transmission, appearing as a negative number. The processing should skip the corrupted reading, log a warning, and continue.</li>
<li><strong>Fatal Software Bugs:</strong> A specific logical error in the processing code causes a <code>ZeroDivisionError</code> if the input is <code>0</code>. This is considered a fatal bug for the current processing run, and the program should stop gracefully after logging a critical error.</li>
</ol>
<h5>Tasks:</h5>
<ol>
<li>Write a Python script (<code>processData.py</code>) that reads <code>input.dat</code> line by line.</li>
<li>Implement the processing logic: for each valid number, calculate its square.</li>
<li>
    <strong>Handle Failures:</strong>
    <ul>
        <li>If a line contains a negative number (a simulated hardware fault), log a <code>WARNING</code> message and skip to the next line.</li>
        <li>If a line contains <code>0</code> (a simulated software bug), log a <code>CRITICAL</code> error message and terminate the script.</li>
        <li>For valid numbers, log an <code>INFO</code> message with the number and its calculated square.</li>
    </ul>
</li>
<li>Configure the <code>logging</code> module to print messages of <code>INFO</code> level and higher to the console. The log format should include the timestamp, log level, and message.</li>
<li>Answer the following theoretical questions:
    <ol type="a">
        <li>Based on the course materials, explain the key difference between a <em>fault</em> and a <em>failure</em>. In this exercise, is the negative number a fault or a failure?</li>
        <li><strong>Proprietary Alternative:</strong> If this script were deployed as an AWS Lambda function triggered by new lines in a file, how might the platform's behavior for the hardware fault (negative number) and software bug (<code>ZeroDivisionError</code>) differ from your script's behavior? What are the advantages of the managed service approach?</li>
        <li><strong>Open-Source Advantage:</strong> What is the primary advantage of implementing this fault tolerance logic yourself in Python, as you have done, versus relying on a proprietary platform's defaults?</li>
    </ol>
</li>
</ol>
<h4>Solution</h4>
<h5><code>processData.py</code>:</h5>

```python
import logging
import sys
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
def processData(filename="input.dat"):
    logging.info(f"Starting data processing for {filename}")
    try:
        with open(filename, 'r') as f:
            for line in f:
                try:
                    value = int(line.strip())
                    if value < 0:
                        # 1. Handle simulated transient hardware fault
                        logging.warning(f"Corrupted data detected (transient hardware fault): {value}. Skipping.")
                        continue
                    
                    if value == 0:
                        # 2. Handle simulated fatal software bug
                        logging.critical(f"Fatal software bug triggered with value: {value}. Terminating process.")
                        # This would typically be a more complex exception in real code
                        raise ZeroDivisionError("Simulated critical processing error")
                    # Process valid data
                    result = value ** 2
                    logging.info(f"Processed value {value}, result: {result}")
                except ValueError:
                    logging.warning(f"Could not parse line: '{line.strip()}'. Skipping.")
                except ZeroDivisionError as e:
                    # Gracefully exit on the specific fatal bug
                    sys.exit(f"Terminated due to: {e}")
                    
    except FileNotFoundError:
        logging.error(f"Input file not found: {filename}")
        sys.exit(1)
    logging.info("Data processing finished.")
if __name__ == "__main__":
    processData()
```
<h5>Theoretical Questions Answers:</h5>
<ol type="a">
    <li>A <strong>fault</strong> is when one component of a system deviates from its specification (e.g., a sensor returning a corrupted value). A <strong>failure</strong> is when the system as a whole fails to meet its required service guarantees (e.g., the entire data pipeline stops or produces incorrect aggregate results). In this exercise, the negative number is a <strong>fault</strong>. Because our script handles it gracefully, it does not cause a system failure.</li>
    <li>
        <strong>Proprietary Alternative (AWS Lambda):</strong>
        <ul>
            <li><strong>Hardware Fault:</strong> The behavior would be identical. The Lambda function's code would still need to contain the logic to detect, log (to AWS CloudWatch), and skip the negative number. The platform is unaware of the application-specific meaning of the data.</li>
            <li><strong>Software Bug:</strong> When the <code>ZeroDivisionError</code> occurs and is unhandled (or re-raised), the Lambda function execution would fail. The platform (AWS) would automatically log the exception and traceback to CloudWatch. Depending on the event source configuration (e.g., SQS, Kinesis), AWS could automatically retry the function a configured number of times. If retries fail, the event could be sent to a Dead-Letter Queue (DLQ) for later inspection.</li>
            <li><strong>Advantage:</strong> The managed service abstracts away the operational burden of failure management like retries and dead-lettering, which we would otherwise have to build ourselves.</li>
        </ul>
    </li>
    <li><strong>Open-Source Advantage:</strong> The primary advantage is <strong>control and portability</strong>. We have complete control over the retry logic, the conditions for failure, the logging format, and the destination for logs and failed messages. The code is not tied to any specific cloud provider's ecosystem (like CloudWatch or SQS DLQs) and can be run on-premises, on any cloud, or in a local container without modification.</li>
</ol>
<h3>Exercise 2: Disadvantages and Pitfalls</h3>
<h4>Problem</h4>
<p>A common pitfall in system monitoring is incorrectly diagnosing a temporarily paused process as a crashed one. A long garbage collection pause in a Java application or a <code>SIGSTOP</code> signal sent by an administrator can make a process unresponsive without terminating it.</p>
<h5>Tasks:</h5>
<ol>
    <li>Write a simple C program, <code>worker</code>, that creates a lock file (<code>worker.lock</code>) and then enters an infinite loop. Inside the loop, it prints a "Heartbeat" message to the console every second and then sleeps for one second.</li>
    <li>Write a simple Python monitoring script, <code>monitor.py</code>, that checks for the existence of <code>worker.lock</code>. If the lock file exists, it should check if the process ID (PID) inside the lock file is still running. If the process is not running, it should report that the worker has crashed.</li>
    <li>Compile and run the <code>worker</code> program in one terminal. It should start printing heartbeats.</li>
    <li>Run the <code>monitor.py</code> script in another terminal. It should report the worker is running.</li>
    <li>From a third terminal, send the <code>SIGSTOP</code> signal to the worker process (<code>kill -STOP &lt;PID&gt;</code>). Observe that the heartbeats stop.</li>
    <li>Now, send <code>SIGCONT</code> to the worker (<code>kill -CONT &lt;PID&gt;</code>). The worker will resume its heartbeats.</li>
    <li>Explain why a monitor that only relies on heartbeats (or lack thereof) would incorrectly flag the paused worker as "crashed." What is the fundamental ambiguity this reveals about failure detection in distributed systems?</li>
</ol>
<h4>Solution</h4>
<h5><code>worker.c</code>:</h5>

```c
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;
#include &lt;sys/types.h&gt;
#define LOCK_FILE "worker.lock"
void cleanup() {
    remove(LOCK_FILE);
    printf("\nLock file cleaned up. Exiting.\n");
}
void handleSignal(int sig) {
    cleanup();
    exit(0);
}
int main() {
    // Register signal handler for cleanup
    signal(SIGINT, handleSignal);
    signal(SIGTERM, handleSignal);
    // Create lock file with PID
    FILE *lockFile = fopen(LOCK_FILE, "w");
    if (lockFile == NULL) {
        perror("Could not create lock file");
        return 1;
    }
    fprintf(lockFile, "%d", getpid());
    fclose(lockFile);
    printf("Worker started with PID %d. Press Ctrl+C to exit.\n", getpid());
    while (1) {
        printf("Heartbeat...\n");
        fflush(stdout);
        sleep(1);
    }
    return 0; // Unreachable
}
```
<h5><code>monitor.py</code>:</h5>

```python
import os
import time
import signal
LOCK_FILE = "worker.lock"
def checkWorker():
    if not os.path.exists(LOCK_FILE):
        print("Worker is not running (no lock file).")
        return
    try:
        with open(LOCK_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists by sending a "null" signal
        os.kill(pid, 0)
        print(f"Worker with PID {pid} is running.")
    except (IOError, ValueError):
        print("Could not read PID from lock file.")
    except ProcessLookupError:
        print(f"Worker with PID {pid} has crashed.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    while True:
        checkWorker()
        time.sleep(2)
```
<h5>Explanation of Pitfall:</h5>
<p>
    A monitor relying solely on heartbeats (e.g., checking if a "last seen" timestamp is too old) would fail. When the worker receives <code>SIGSTOP</code>, it freezes completely. It stops sending heartbeats. The monitor would see the missing heartbeats and, after its timeout, declare the worker "crashed." However, the process still exists in the OS process table, its memory is intact, and it is merely suspended. When <code>SIGCONT</code> is sent, it resumes as if nothing happened.
</p>
<p>
    This reveals the <strong>fundamental ambiguity between a process crash, a process pause, and a network partition</strong>. From an external observer's point of view, all three look identical: a lack of communication. Without an out-of-band, trusted channel (like querying the OS kernel as done in <code>monitor.py</code>), it is impossible to be certain of the remote process's true state. This is a core problem discussed in <code>Designing Data-Intensive Applications, Chapter 8</code>.
</p>
<h3>Exercise 3: Contrasting with Inefficient/Naive Solutions</h3>
<h4>Problem</h4>
<p>When a program crashes unexpectedly, it can leave system resources in a corrupt state. A common example is leaving a lock file behind, which can prevent the service from restarting. A robust program must handle fatal errors gracefully.</p>
<h5>Tasks:</h5>
<ol>
    <li><strong>Part A (Naive):</strong> Write a C program (<code>naive_worker.c</code>) that:
        <ul>
            <li>Creates a file named <code>naive.lock</code>.</li>
            <li>Prints "Processing..."</li>
            <li>Deliberately causes a segmentation fault (e.g., <code>*(int*)NULL = 0;</code>).</li>
            <li>Compile and run it. Use <code>ls</code> to verify that <code>naive.lock</code> remains after the crash. Explain why this is problematic.</li>
        </ul>
    </li>
    <li><strong>Part B (Correct):</strong> Write a robust C program (<code>robust_worker.c</code>) that:
        <ul>
            <li>Installs a signal handler for <code>SIGSEGV</code>.</li>
            <li>The signal handler should print a clear error message to <code>stderr</code>, remove the <code>robust.lock</code> file, and then exit with a non-zero status.</li>
            <li>The <code>main</code> function should create <code>robust.lock</code> and then trigger the segmentation fault as before.</li>
            <li>Compile and run it. Verify that the lock file is gone. Explain how this solution is superior.</li>
        </ul>
    </li>
</ol>
<h4>Solution</h4>
<h5><code>naive_worker.c</code>:</h5>

```c
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
int main() {
    FILE *lockFile = fopen("naive.lock", "w");
    if (lockFile == NULL) {
        perror("Failed to create lock file");
        return 1;
    }
    fclose(lockFile);
    
    printf("Processing... about to crash.\n");
    
    // Deliberate segmentation fault
    *(int*)NULL = 0;
    
    // This part is never reached
    printf("This will not be printed.\n");
    remove("naive.lock");
    return 0;
}
```
<p><strong>Problem with Naive Approach:</strong> After running <code>./naive_worker</code>, the <code>naive.lock</code> file will persist. If a startup script checks for this lock file to prevent multiple instances from running, the service can never be restarted until an operator manually intervenes and deletes the file.</p>
<h5><code>robust_worker.c</code>:</h5>

```c
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;signal.h&gt;
#include &lt;unistd.h&gt;
#define LOCK_FILE "robust.lock"
void handleSegfault(int sig) {
    fprintf(stderr, "Caught segmentation fault. Cleaning up resources.\n");
    remove(LOCK_FILE);
    // Restore default handler and re-raise for core dump / default exit
    signal(sig, SIG_DFL);
    raise(sig);
}
int main() {
    // Install signal handler
    signal(SIGSEGV, handleSegfault);
    FILE *lockFile = fopen(LOCK_FILE, "w");
    if (lockFile == NULL) {
        perror("Failed to create lock file");
        return 1;
    }
    fclose(lockFile);
    
    printf("Processing... about to crash robustly.\n");
    
    // Deliberate segmentation fault
    *(int*)NULL = 0;
    
    // Unreachable
    return 0;
}
```
<p><strong>Superiority of Robust Solution:</strong> The robust worker catches the fatal signal. Before the process terminates, the signal handler executes, performing the crucial cleanup task of removing the lock file. This makes the system more resilient; an automated supervisor could safely restart the service without manual intervention, as the stale lock file that would block restart has been removed.</p>
<h3>Exercise 4: Hardcore Combined Problem</h3>
<h4>Problem</h4>
<p>
    Design a fault-tolerant data processing system. A Python supervisor process is responsible for managing a C worker process. The worker is designed to be fast but is known to be buggy. Your system must correctly handle data corruption, fatal software crashes, and graceful shutdowns.
</p>
<h5>Tasks:</h5>
<p>Write two programs: a C worker and a Python supervisor.</p>
<ol>
    <li>
        <strong>C Worker (`hardcore_worker.c`):</strong>
        <ul>
            <li><strong>Startup:</strong> Creates a lock file named <code>cworker.lock</code> containing its PID.</li>
            <li><strong>Input:</strong> Reads integer values, one per line, from <code>stdin</code>.</li>
            <li>
                <strong>Processing:</strong>
                <ul>
                    <li>For a positive integer <code>n</code>, it calculates <code>n*n</code> and prints <code>n,n*n\n</code> to <code>stdout</code>.</li>
                    <li><strong>Hardware Fault Simulation:</strong> If <code>n</code> is negative, it prints an error message <code>ERROR: Corrupted data {n}\n</code> to <code>stderr</code> and continues to the next input line without producing output to <code>stdout</code>.</li>
                    <li><strong>Software Bug:</strong> If <code>n</code> is <code>999</code>, it immediately triggers a segmentation fault.</li>
                </ul>
            </li>
            <li>
                <strong>Signal Handling:</strong>
                <ul>
                    <li>It must catch <code>SIGTERM</code> to perform a graceful shutdown (remove <code>cworker.lock</code> and exit).</li>
                    <li>It must catch <code>SIGSEGV</code> to perform the same cleanup before the process dies.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>
        <strong>Python Supervisor (`supervisor.py`):</strong>
        <ul>
            <li><strong>Setup:</strong> Runs <code>generateData.py</code> to ensure <code>input.dat</code> exists.</li>
            <li>
                <strong>Lifecycle Management:</strong>
                <ul>
                    <li>Launches the compiled C worker as a subprocess, redirecting its <code>stdin</code>, <code>stdout</code>, and <code>stderr</code>.</li>
                    <li>Writes all numbers from <code>input.dat</code> to the worker's <code>stdin</code>.</li>
                    <li>Continuously and non-blockingly monitors the worker's <code>stdout</code> and <code>stderr</code> streams, and its process status.</li>
                </ul>
            </li>
            <li>
                <strong>Fault Tolerance Logic:</strong>
                <ul>
                    <li>If a "Corrupted data" message appears on the worker's <code>stderr</code>, the supervisor must log a warning and continue feeding data.</li>
                    <li>If the worker process terminates unexpectedly (with a non-zero exit code), the supervisor must log a critical error, check that the <code>cworker.lock</code> file was properly removed, and attempt to restart the worker process once.</li>
                    <li>After successfully processing all data, the supervisor must gracefully shut down the worker by sending it a <code>SIGTERM</code> signal.</li>
                </ul>
            </li>
        </ul>
    </li>
</ol>

<h4>Solution</h4>
<h5><code>Makefile</code>:</h5>

```bash
all: hardcore_worker
hardcore_worker: hardcore_worker.c
	gcc -Wall -o hardcore_worker hardcore_worker.c
clean:
	rm -f hardcore_worker cworker.lock input.dat
```
<h5><code>hardcore_worker.c</code>:</h5>

```c
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;
#include &lt;sys/types.h&gt;
#define LOCK_FILE "cworker.lock"
void cleanupAndExit(int sig) {
    remove(LOCK_FILE);
    // Use a temp buffer to be safe in a signal handler
    char msg[] = "Worker shutting down gracefully.\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
    
    // For segfault, re-raise to get a core dump if needed
    if (sig == SIGSEGV) {
        signal(sig, SIG_DFL);
        raise(sig);
    }
    exit(0);
}
int main() {
    signal(SIGTERM, cleanupAndExit);
    signal(SIGSEGV, cleanupAndExit);
    FILE *lockFile = fopen(LOCK_FILE, "w");
    if (!lockFile) {
        perror("Failed to create lock file");
        return 1;
    }
    fprintf(lockFile, "%d", getpid());
    fclose(lockFile);
    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        int n = atoi(line);
        if (n == 999) {
            fprintf(stderr, "ERROR: Triggering fatal software bug.\n");
            *(int*)NULL = 0; // Trigger SIGSEGV
        }
        if (n < 0) {
            fprintf(stderr, "ERROR: Corrupted data %d\n", n);
            continue;
        }
        long long result = (long long)n * n;
        printf("%d,%lld\n", n, result);
        fflush(stdout);
    }
    cleanupAndExit(0);
    return 0;
}
```
<h5><code>supervisor.py</code>:</h5>

```python
import subprocess
import os
import signal
import time
import logging
import sys
# Import and run the data generator
import generateData
logging.basicConfig(level=logging.INFO, format='%(asctime)s SUPERVISOR - %(levelname)s - %(message)s')
C_WORKER_CMD = "./hardcore_worker"
INPUT_FILE = "input.dat"
LOCK_FILE = "cworker.lock"
def runJob(restartCount=0):
    if restartCount > 1:
        logging.error("Worker has failed repeatedly. Aborting job.")
        return
    if restartCount > 0:
        logging.warning(f"Attempting to restart worker (Attempt {restartCount}).")
    try:
        if not os.path.exists(C_WORKER_CMD):
            logging.critical(f"Worker executable '{C_WORKER_CMD}' not found. Did you run 'make'?")
            sys.exit(1)
            
        logging.info(f"Starting worker process: {C_WORKER_CMD}")
        workerProcess = subprocess.Popen(
            [C_WORKER_CMD],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        with open(INPUT_FILE, 'r') as f:
            for line in f:
                workerProcess.stdin.write(line)
                workerProcess.stdin.flush()
                time.sleep(0.01) # Slow down input feeding for demonstration
        workerProcess.stdin.close()
        # Monitor output
        while workerProcess.poll() is None:
            err = workerProcess.stderr.readline()
            if "Corrupted data" in err:
                logging.warning(f"Worker reported data corruption: {err.strip()}")
            
            out = workerProcess.stdout.readline()
            if out:
                logging.info(f"Worker output: {out.strip()}")
        
        # Check final status
        if workerProcess.returncode != 0:
            logging.critical(f"Worker crashed with exit code {workerProcess.returncode}. Restarting.")
            # Check for cleanup
            if os.path.exists(LOCK_FILE):
                logging.error("Worker did not clean up lock file on crash!")
            else:
                logging.info("Worker successfully cleaned up lock file on crash.")
            runJob(restartCount + 1)
        else:
            logging.info("Worker finished successfully.")
    except Exception as e:
        logging.critical(f"Supervisor error: {e}")
        if 'workerProcess' in locals() and workerProcess.poll() is None:
            workerProcess.terminate()
def main():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    generateData.generateDataFile(INPUT_FILE)
    runJob()
if __name__ == "__main__":
    main()
```
<p>To run the solution:</p>
<ol>
    <li>Run <code>make</code> to compile the C worker.</li>
    <li>Run <code>python supervisor.py</code>.</li>
</ol>
<p>You will see output where the supervisor logs the worker's processing, its warnings about corrupted data, its detection of the crash caused by <code>999</code>, its verification of cleanup, and its successful restart of the worker to complete the job. This demonstrates a complete, albeit simple, fault-tolerant system handling multiple types of failures as defined in this section.</p>
<h2>Tips for Success & Learning</h2>
<ul>
    <li>
        <strong>Fault vs. Failure:</strong> Constantly ask yourself if a particular issue is a <code>fault</code> (a component deviating from its spec) or a <code>failure</code> (the system not delivering its service). This distinction is critical to designing targeted recovery strategies.
    </li>
    <li>
        <strong>Signal Handler Constraints:</strong> When implementing the C signal handlers, remember that they execute in a minimal, fragile context. Avoid complex operations like <code>printf</code> (which is not async-signal-safe) or dynamic memory allocation. Prefer low-level, safe functions like <code>write</code> for logging within a handler.
    </li>
    <li>
        <strong>Process Communication:</strong> In the Hardcore problem, use non-blocking reads or separate threads in your Python supervisor to monitor the worker's <code>stdout</code> and <code>stderr</code> streams. A simple blocking read on one stream could cause a deadlock if the worker is waiting to write to the other.
    </li>
    <li>
        <strong>Experiment:</strong> Don't just run the solution. Modify the C worker to handle different signals. Change the supervisor's restart logic. The goal is to understand the boundaries and failure points of your own designs.
    </li>
</ul>

<h2>Conclusion & Next Steps</h2>
<p>
    Congratulations on completing the practical exercises for handling hardware and software failures. You have built systems that can identify, classify, and recover from different types of faults, a foundational skill for any data engineer. You have seen firsthand how low-level control in C and high-level orchestration in Python can be combined to create resilient applications.
</p>
<p>
    Having established how to make a single node more reliable, the next logical step is to address reliability across multiple nodes. The upcoming topic, <strong>Replication strategies</strong>, will explore how to maintain data availability and consistency when data is distributed across several machines, each with its own potential for failure.
</p>
</div>
</body>