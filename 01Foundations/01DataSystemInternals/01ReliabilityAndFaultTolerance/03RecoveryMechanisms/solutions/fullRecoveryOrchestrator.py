import subprocess
import sys
import time
import os

def run_host_command(command):
    """Runs a command on the host machine."""
    print(f"Executing on host: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def main():
    recovery_target_time = input("Enter the recovery target timestamp (BEFORE the TRUNCATE): ")
    if not recovery_target_time:
        print("Timestamp is required.")
        sys.exit(1)

    print("\n--- Starting Full Disaster Recovery Drill ---")

    print("\n[Step 1] Tearing down the compromised environment...")
    run_host_command(["docker-compose", "down", "--volumes"])

    print("\n[Step 2] Re-creating volumes for the new environment...")
    run_host_command(["docker", "volume", "create", "statelessCommercePrimaryData"])
    run_host_command(["docker", "volume", "create", "statelessCommerceWalArchive"])

    print("\n[Step 3] Starting a temporary primary to create a 'base backup'...")
    run_host_command(["docker-compose", "up", "-d", "--no-deps", "primary"])

    print("\n[Step 4] Stopping the temporary primary...")
    run_host_command(["docker-compose", "stop", "primary"])
    
    print("\n[Step 5] Simulating restore: Re-initializing primary and configuring PITR...")
    # Get the absolute path to the WAL archive on the host
    wal_volume_path = run_host_command(["docker", "volume", "inspect", "-f", "{{.Mountpoint}}", "statelessCommerceWalArchive"]).stdout.strip()
    
    # We must run these next commands inside a temporary container with the volumes mounted
    # to manipulate the files correctly.
    data_volume = "statelessCommercePrimaryData"
    archive_volume = "statelessCommerceWalArchive"
    
    # 1. Clean the data directory
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "rm", "-rf", "/data/*"])
    
    # 2. Run pg_basebackup to restore from the WAL archive (this is a conceptual step)
    # A real backup would be on S3. Here, we just re-init and will rely on WAL replay.
    # We re-create the data dir from scratch, then apply WALs.
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "-v", f"{archive_volume}:/archive", "postgres:15", "pg_basebackup", "-D", "/data", "-R", "--wal-method=fetch"])


    print(f"\n[Step 6] Creating recovery.signal and setting recovery target...")
    recovery_conf = f"restore_command = 'cp /archive/%f %p'\nrecovery_target_time = '{recovery_target_time}'\nrecovery_target_action = 'promote'\n"
    
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "touch", "/data/recovery.signal"])
    run_host_command(["docker", "run", "--rm", "-v", f"{data_volume}:/data", "busybox", "sh", "-c", f"echo '{recovery_conf}' >> /data/postgresql.conf"])

    print("\n[Step 7] Starting the restored primary server...")
    run_host_command(["docker-compose", "up", "-d", "primary"])

    print("\n[Step 8] Monitoring recovery...")
    recovered = False
    for _ in range(60): # Increase timeout for recovery
        result = subprocess.run(["docker-compose", "exec", "primary", "pg_isready", "-U", "admin"], capture_output=True, text=True)
        if "accepting connections" in result.stdout:
            print("Recovery complete. New primary is online.")
            recovered = True
            break
        time.sleep(2)

    if not recovered:
        print("Recovery monitoring timed out. Please check container logs.")
        sys.exit(1)
        
    print("\n--- Full Recovery Drill Complete ---")
    print("Verify that the 'products' table and its data have been restored.")

if __name__ == "__main__":
    main()