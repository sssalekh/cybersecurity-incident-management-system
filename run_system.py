import subprocess
import sys
import time

processes = []

try:
    processes.append(subprocess.Popen([sys.executable, "event_generator.py"]))
    processes.append(subprocess.Popen([sys.executable, "main.py"]))
    processes.append(subprocess.Popen([sys.executable, "app.py"]))

    print("System running... CTRL+C to stop")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    for p in processes:
        p.terminate()