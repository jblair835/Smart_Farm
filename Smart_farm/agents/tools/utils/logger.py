#-----------------------
# Logger
#-----------------------
"""Simple timestamped logger for Smart Farm project."""

import datetime

def log(message):
    """Print a timestamped log message."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
