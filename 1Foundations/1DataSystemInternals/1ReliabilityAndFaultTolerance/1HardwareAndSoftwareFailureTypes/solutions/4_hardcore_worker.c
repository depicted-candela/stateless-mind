//      C Worker (`hardcore_worker.c`):

//  Startup: Creates a lock file named cworker.lock containing its PID.
// Input: Reads integer values, one per line, from stdin.
//  Processing:
// For a positive integer n, it calculates n*n and prints n,n*n\n to stdout.
// Hardware Fault Simulation: If n is negative, it prints an error message ERROR: 
// Corrupted data {n}\n to stderr and continues to the next input line without 
// producing output to stdout.
// Software Bug: If n is 999, it immediately triggers a segmentation fault.
// Signal Handling:
// It must catch SIGTERM to perform a graceful shutdown (remove cworker.lock and 
//     exit).
// It must catch SIGSEGV to perform the same cleanup before the process dies.
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

#define WORKER_LOCK "cworker.lock"

void gracefulShutdown(int sig) {
    remove(WORKER_LOCK);
    if (sig == SIGSEGV) signal(sig, SIG_DFL);
    const char message[] = "The worker was sucessfully cleaned triggerd by signal.\n";
    write(STDERR_FILENO, message, sizeof(message) - 1);
    _exit(128 + sig);
}

int main() {
    signal(SIGTERM, gracefulShutdown);
    signal(SIGSEGV, gracefulShutdown);

    FILE *cworker = fopen(WORKER_LOCK, "w");
    if (cworker == NULL) { 
        fprintf(stderr, "%s could not be opened", WORKER_LOCK); 
    }
    fprintf(stdin, "%d", getpid());
    fclose(cworker);

    char processed_line[256];
    setvbuf(stdout, NULL, _IOLBF, 0);
    setvbuf(stderr, NULL, _IOLBF, 0);
    while (fgets(processed_line, sizeof(processed_line), stdin)) {
        int processed_number = atoi(processed_line);
        if (processed_number < 0) {
            fprintf(stderr, "Corrupted data {%d}\n", processed_number);
            continue;
        }
        if (processed_number == 999) {
            fprintf(stderr, "Triggering fatal software bug.\n");
            *(int*)NULL = 0;
        }
        long long squared_number = processed_number * processed_number;
        fprintf(stdout, "%d, %lld\n", processed_number, squared_number);
    }
    gracefulShutdown(0);
}