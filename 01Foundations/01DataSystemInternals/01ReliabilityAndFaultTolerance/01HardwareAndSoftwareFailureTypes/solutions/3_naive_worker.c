// Part A (Naive): Write a C program (naive_worker.c) that:
// Creates a file named naive.lock.
// Prints "Processing..."
// Deliberately causes a segmentation fault (e.g., *(int*)NULL = 0;).
// Compile and run it. Use ls to verify that naive.lock remains after the crash. 
// Explain why this is problematic.
#include <stdio.h>
#define NAIVE_WORKER "naiver.lock"

void main() {
    FILE *naive_woker = fopen(NAIVE_WORKER, "w");
    fclose(naive_woker);
    printf("Processing...\n");
    fflush(stdout);
    *(int*)NULL = 0;
}

// With `ls` the file remains and that means the pointer was not closed, very
// problematic if the memory or computing resources running there were expensive