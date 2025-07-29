// Part B (Correct): Write a robust C program (robust_worker.c) that:
// Installs a signal handler for SIGSEGV.
// The signal handler should print a clear error message to stderr, remove the 
// robust.lock file, and then exit with a non-zero status.
// The main function should create robust.lock and then trigger the segmentation 
// fault as before.
// Compile and run it. Verify that the lock file is gone. Explain how this solution 
// is superior.
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#define WORKER "robust.lock"

void handlesSegmentationFault(int sig) {
    remove(WORKER);
    fprintf(stderr, "A segmentation error broke %s, thus the process was stopped by ", WORKER);
    signal(sig, SIG_DFL); // Like an exception well ordered
    raise(sig);          // to be raised informing the OS
}

int main() {
    signal(SIGSEGV, handlesSegmentationFault);
    FILE *robust_worker = fopen(WORKER, "w");
    if (robust_worker == NULL) {
        perror("Failed to create the lock file for the robus worker");
        return 1;
    }
    fprintf(stdout, "Created %s", WORKER);
    fclose(robust_worker);
    fprintf(stdout, "Closed %s", WORKER);
    *(int*)NULL = 0;
}