import socket
import time
from pyhive import hive
import yaml

# Load Hive Configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

HIVE_HOST = config["hive"]["host"]
HIVE_PORT = config["hive"]["port"]
HIVE_DATABASE = config["hive"]["database"]
TABLE_NAME = config["hive"]["metadata_table"]

def check_hive_server():
    """Check if HiveServer2 is running by attempting a socket connection."""
    try:
        with socket.create_connection((HIVE_HOST, int(HIVE_PORT)), timeout=5):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def get_hive_connection():
    """Establish connection to HiveServer2."""
    if not check_hive_server():
        raise ConnectionError(f"HiveServer2 is not running on {HIVE_HOST}:{HIVE_PORT}")

    return hive.Connection(host=HIVE_HOST, port=int(HIVE_PORT), database=HIVE_DATABASE)

def read_metadata():
    """Execute a Hive SQL query and return the results."""
    query = f"SELECT hdfs_path, format, description, domain, keywords FROM {TABLE_NAME}"
    try:
        with get_hive_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error reading metadata from Hive: {e}")
        return []
