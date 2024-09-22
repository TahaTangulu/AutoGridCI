import requests
import subprocess
import sys
import time

def check_grid_health():
    url = "http://localhost:4444/status"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json()['value']['ready']:
            print("Selenium Grid is up and ready!")
            return True
        else:
            print("Selenium Grid is not ready yet.")
            return False
    except Exception as e:
        print(f"Error checking grid health: {e}")
        return False

def run_tests(node_count):
    if check_grid_health():
        print(f"Running tests with {node_count} node(s)...")
        subprocess.run(["docker-compose", "up", "--scale", f"chrome={node_count}", "--abort-on-container-exit"])
        subprocess.run(["docker-compose", "down"])
    else:
        print("Cannot run tests as Selenium Grid is not ready.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_tests.py <node_count>")
        sys.exit(1)
    try:
        node_count = int(sys.argv[1])
        if not 1 <= node_count <= 5:
            raise ValueError
    except ValueError:
        print("node_count must be an integer between 1 and 5.")
        sys.exit(1)
    run_tests(node_count)
