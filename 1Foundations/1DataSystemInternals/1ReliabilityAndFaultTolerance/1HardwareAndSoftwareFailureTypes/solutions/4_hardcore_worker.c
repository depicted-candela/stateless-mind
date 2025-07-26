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
#include <signal.h>
#include <unistd.h>

#define LOCKER "cworker.lock"

void handlesGracefulShutdown(int sign) {
    remove(LOCKER);
    if (sign == SIGSEGV) perror("SEGMENTATION FAULT\n");
    signal(sign, SIG_DFL);
    raise(sign);
}

int main() {
    signal(SIGTERM, handlesGracefulShutdown);
    signal(SIGSEGV, handlesGracefulShutdown);
    FILE *cworker = fopen(LOCKER, "w");
    if (!cworker) {
        perror("The lock file couldn't be created");
        return 1;
    }
    fprintf(cworker, "%d", getpid());
    fclose(cworker);
    setbuf(stdout, NULL); // Disable buffering for stdout
    setbuf(stderr, NULL); // Disable buffering for stderr
    char line[32];
    int converted_line;
    while (fgets(line, sizeof(line), stdin)) {
        converted_line = atoi(line);
        if (converted_line < 0) {
            fprintf(stderr, "Corrupted data {%d}\n", converted_line);
            fflush(stderr);
            continue;
        }
        if (converted_line == 0) {
            fprintf(stderr, "Recoverable software error: input 0\n");
            fflush(stderr);
            continue;
        }
        if (converted_line == 999) {
            raise(SIGSEGV);
        }
        long long squared_line = (long long)converted_line * converted_line;
        printf("%d,%lld\n", converted_line, squared_line);
        fflush(stdout);
    }
    remove(LOCKER);
    return 0;
}