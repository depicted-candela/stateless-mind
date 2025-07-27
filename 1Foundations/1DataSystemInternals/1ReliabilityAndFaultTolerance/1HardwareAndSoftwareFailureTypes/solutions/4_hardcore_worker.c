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
