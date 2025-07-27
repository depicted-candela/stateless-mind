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
