import subprocess
import sys
import time
import os

def run_command(command, container):
    """Runs a command inside a specified docker container."""
    base_cmd = ["docker-compose", "exec", "-T", container]
    full_cmd = base_cmd + command
    print(f"Executing in {container}: {' '.join(command)}")
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
    print(result.stdout)
    return result

def main():
    recovery_target_time = input("Enter the recovery target timestamp (e.g., '2025-08-01 10:29:59 UTC'): ")
    if not recovery_target_time:
        print("Timestamp is required.")
        sys.exit(1)

    print("\n--- Starting Point-in-Time Recovery Simulation ---")

    print("\n[Step 1] Stopping the primary database server...")
    subprocess.run(["docker-compose", "stop", "primary"], check=True)

    print("\n[Step 2] Clearing the primary's data directory...")
    run_command(["rm", "-rf", "/var/lib/postgresql/data/*"], "primary")
    
    print("\n[Step 3] Restoring from base backup by copying from archive...")
    # In a real scenario, you'd restore from your backup storage (e.g., S3).
    # We simulate this by copying the archived data back.
    wal_archive_path = "/archive" # Path inside the container
    run_command(["pg_basebackup", "-D", "/var/lib/postgresql/data", "-h", os.environ['PRIMARY_HOST'], "-U", os.environ['DB_USER'], "-P", "-R"], "primary")


    print(f"\n[Step 4] Creating recovery signal with target time: {recovery_target_time}")
    recovery_conf = f"""
recovery_target_time = '{recovery_target_time}'
recovery_target_action = 'promote'
restore_command = 'cp {wal_archive_path}/%f %p'
"""
    run_command(["touch", "/var/lib/postgresql/data/recovery.signal"], "primary")
    run_command(["bash", "-c", f"echo \"{recovery_conf}\" >> /var/lib/postgresql/data/postgresql.auto.conf"], "primary")
    run_command(["chmod", "0700", "/var/lib/postgresql/data"], "primary")


    print("\n[Step 5] Restarting the primary server to initiate recovery...")
    subprocess.run(["docker-compose", "start", "primary"], check=True)

    print("\n[Step 6] Monitoring recovery. This may take a minute...")
    recovered = False
    for _ in range(30):
        result = run_command(["pg_isready", "-U", "admin"], "primary")
        if "accepting connections" in result.stdout:
            print("Recovery complete. Primary is back online.")
            recovered = True
            break
        time.sleep(2)
    
    if not recovered:
        print("Recovery monitoring timed out. Please check logs.")
        sys.exit(1)
    
    print("\n--- PITR Simulation Complete ---")
    print("Verify the data has been restored correctly.")


if __name__ == "__main__":
    main()