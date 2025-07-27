// C Worker (`hardcore_worker.c`):

// Startup: Creates a lock file named cworker.lock containing its PID.
// Input: Reads integer values, one per line, from stdin.
// Processing:
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
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

#define LOCK_FILE "cworker.lock"

// A signal-safe handler for cleanup.
// Using write() is safer than printf() inside a signal handler.
// _exit() is used for immediate termination without calling other handlers.
void cleanupOnSignal(int sig) {
    remove(LOCK_FILE);
    const char msg[] = "Worker terminated by signal, cleaning up lock file.\n";
    write(STDERR_FILENO, msg, sizeof(msg) - 1);
    _exit(128 + sig); // Exit with a code indicating the signal
}

int main() {
    // Register signal handlers for graceful shutdown and crashes.
    signal(SIGTERM, cleanupOnSignal);
    signal(SIGSEGV, cleanupOnSignal);

    // Create a lock file with the process ID.
    FILE *lockFile = fopen(LOCK_FILE, "w");
    if (!lockFile) {
        perror("Failed to create lock file");
        return 1;
    }
    fprintf(lockFile, "%d", getpid());
    fclose(lockFile);

    // Set line buffering for stdout and stderr to ensure the supervisor
    // receives messages as they are produced, line by line.
    setvbuf(stdout, NULL, _IOLBF, 0);
    setvbuf(stderr, NULL, _IOLBF, 0);

    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        int n = atoi(line);

        if (n == 999) {
            // Trigger a segmentation fault to test the SIGSEGV handler.
            fprintf(stderr, "ERROR: Triggering fatal software bug.\n");
            *(int*)NULL = 0;
        } else if (n < 0) {
            // Handle simulated hardware fault.
            fprintf(stderr, "ERROR: Corrupted data %d\n", n);
            continue;
        } else {
            // Process valid data.
            long long result = (long long)n * n;
            printf("%d,%lld\n", n, result);
        }
    }

    // Clean up the lock file on normal exit.
    remove(LOCK_FILE);
    return 0;
}