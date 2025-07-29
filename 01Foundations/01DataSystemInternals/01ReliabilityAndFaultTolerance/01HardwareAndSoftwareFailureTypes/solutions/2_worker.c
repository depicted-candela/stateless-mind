// Exercise 2: Disadvantages and Pitfalls
//     Problem
// A common pitfall in system monitoring is incorrectly diagnosing a 
// temporarily paused process as a crashed one. A long garbage collection 
// pause in a Java application or a SIGSTOP signal sent by an administrator 
// can make a process unresponsive without terminating it.

//     Tasks:
// Write a simple C program, worker, that creates a lock file (worker.lock) 
// and then enters an infinite loop. Inside the loop, it prints a "Heartbeat" 
// message to the console every second and then sleeps for one second.
// Write a simple Python monitoring script, monitor.py, that checks for the 
// existence of worker.lock. If the lock file exists, it should check if the 
// process ID (PID) inside the lock file is still running. If the process is 
// not running, it should report that the worker has crashed.
// Compile and run the worker program in one terminal. It should start 
// printing heartbeats.
// Run the monitor.py script in another terminal. It should report the worker 
// is running.
// From a third terminal, send the SIGSTOP signal to the worker process 
// (kill -STOP <PID>). Observe that the heartbeats stop.
// Now, send SIGCONT to the worker (kill -CONT <PID>). The worker will resume 
// its heartbeats.
// Explain why a monitor that only relies on heartbeats (or lack thereof) 
// would incorrectly flag the paused worker as "crashed." What is the 
// fundamental ambiguity this reveals about failure detection in distributed systems?
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

#define LOCK_FILE "worker.lock"

void cleanup() {
    remove(LOCK_FILE);
    printf("The %s file was successfully deleted\n");
}

void handleSignal() {
    cleanup();
    exit(0);
}

int main() {
    signal(SIGINT, handleSignal);
    signal(SIGTERM, handleSignal);
    
    FILE *lock_file = fopen(LOCK_FILE, "w");
    if (lock_file == NULL) {
        printf("The %s file can't be opened");
        return 0;
    }
    fprintf(lock_file, "%d", getpid());
    fclose(lock_file);

    while (1) {
        printf("\nHeartbeat");
        fflush(stdout);
        sleep(1);
    }
}