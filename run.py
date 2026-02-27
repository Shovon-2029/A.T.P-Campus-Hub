import subprocess
import sys

# List of your scripts
scripts = ["server.py", "chat_ai.py", "complaint.py", "register.py"]
processes = []

print("Starting all services...")

# Launch each script
for script in scripts:
    # Use 'python' for Windows, 'python3' for Mac/Linux
    process = subprocess.Popen([sys.executable, script])
    processes.append(process)

try:
    # Keep the main script running to keep the background processes alive
    for process in processes:
        process.wait()
except KeyboardInterrupt:
    # If you press Ctrl+C, it will cleanly shut down all 3 scripts
    print("\nShutting down all services...")
    for process in processes:
        process.terminate()