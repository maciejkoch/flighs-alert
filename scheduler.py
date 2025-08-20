#!/usr/bin/env python3
"""
Scheduler script for Railway cron jobs.
This script is designed to be executed by Railway's scheduler.
"""
import sys
from datetime import datetime


def main():
    """Main function that executes the scheduled job."""
    print("Job is working")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("Scheduler script executed successfully")


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"Error in scheduler: {e}")
        sys.exit(1)
