import time
import os
import csv
import psutil
from datetime import datetime

# Configuration
LOG_FILE = "system_stats.csv"
INTERVAL = 2  # Collect stats every N seconds

def initialize_csv(filepath: str):
    """Creates the CSV file with headers if it doesn't already exist."""
    if not os.path.exists(filepath):
        with open(filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp",
                "CPU_Usage_Pct",
                "RAM_Usage_Pct",
                "RAM_Used_MB",
                "Disk_Usage_Pct",
                "Bytes_Sent",
                "Bytes_Recv"
            ])

def get_system_stats() -> dict:
    """Collects current system metrics."""
    cpu_pct = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_pct": cpu_pct,
        "ram_pct": mem.percent,
        "ram_used_mb": round(mem.used / (1024 * 1024), 1),
        "disk_pct": disk.percent,
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
    }

def log_to_csv(filepath: str, stats: dict):
    """Appends a single snapshot of stats to CSV."""
    with open(filepath, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            stats["timestamp"],
            stats["cpu_pct"],
            stats["ram_pct"],
            stats["ram_used_mb"],
            stats["disk_pct"],
            stats["bytes_sent"],
            stats["bytes_recv"]
        ])

def display_dashboard(stats: dict):
    """Clears terminal and prints a clean, real-time dashboard."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Format bytes to human-readable strings
    sent_mb = round(stats["bytes_sent"] / (1024 * 1024), 2)
    recv_mb = round(stats["bytes_recv"] / (1024 * 1024), 2)

    print("==========================================")
    print("      PYTHON SYSTEM STATS COLLECTOR       ")
    print("==========================================")
    print(f" Timestamp  : {stats['timestamp']}")
    print(f" CPU Load   : [{stats['cpu_pct']:>5.1f}% ]")
    print(f" RAM Usage  : [{stats['ram_pct']:>5.1f}% ] ({stats['ram_used_mb']} MB)")
    print(f" Disk Usage : [{stats['disk_pct']:>5.1f}% ]")
    print("------------------------------------------")
    print(f" Net Sent   : {sent_mb:>8.2f} MB")
    print(f" Net Recv   : {recv_mb:>8.2f} MB")
    print("==========================================")
    print(f" Logging data to: {LOG_FILE}")
    print(" Press Ctrl+C to exit.")

def main():
    initialize_csv(LOG_FILE)
    
    # Initial call to prime psutil.cpu_percent
    psutil.cpu_percent(interval=None)
    time.sleep(1)

    print("Starting stats collector...")
    
    try:
        while True:
            stats = get_system_stats()
            log_to_csv(LOG_FILE, stats)
            display_dashboard(stats)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nCollector stopped gracefully.")

if __name__ == "__main__":
    main()
