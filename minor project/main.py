import subprocess
import time

# Start Backend
backend_process = subprocess.Popen(["python", "backend.py"])
time.sleep(2)  # Give backend time to start

# Start Connector
connector_process = subprocess.Popen(["python", "connector.py"])
time.sleep(2)  # Give connector time to start

# Start Frontend
frontend_process = subprocess.Popen(["python", "frontend.py"])

# Wait for frontend to close, then terminate everything
frontend_process.wait()

# When frontend is closed, kill backend and connector
backend_process.terminate()
connector_process.terminate()

print("[Main] Application closed.")
