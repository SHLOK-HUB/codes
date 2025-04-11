import time
import subprocess
from threading import Thread

# Function to start the Flask backend
def start_backend():
    subprocess.run(["python", "backend.py"])

# Function to start the Tkinter frontend
def start_frontend():
    subprocess.run(["python", "frontend.py"])

# Main function that runs both backend and frontend
def main():
    # Start backend in a separate thread
    backend_thread = Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait for the backend to initialize
    time.sleep(2)

    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main()
import subprocess
import sys
import time
import threading

def start_backend():
    """
    Start the Flask backend server in a subprocess.
    """
    subprocess.run([sys.executable, "backend.py"])

def start_frontend():
    """
    Start the PyQt frontend application.
    """
    subprocess.run([sys.executable, "frontend.py"])

if __name__ == "__main__":
    # Start the backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Give the backend some time to start
    time.sleep(2)

    # Start the frontend application
    start_frontend()
