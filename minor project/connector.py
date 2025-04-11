import socket

def start_connector():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5000))
    server.listen(5)

    print("[Connector] Waiting for requests...")

    while True:
        client_socket, addr = server.accept()
        data = client_socket.recv(4096).decode()
        
        if "::" in data:
            language, prompt = data.split("::", 1)
            print(f"[Connector] Received prompt for {language}: {prompt}")

            # Send to backend
            backend_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_client.connect(("localhost", 6000))
            backend_client.send(data.encode())

            # Receive response
            generated_code = backend_client.recv(4096).decode()
            backend_client.close()

            # Send back to frontend
            client_socket.send(generated_code.encode())

        client_socket.close()

if __name__ == "_main_":
    start_connector()
