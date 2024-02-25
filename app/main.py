import socket
import threading


def parse_resp_command(data):
    lines = data.split('\r\n')
    if lines[0].startswith('*'):
        num_elements = int(lines[0][1:])
        if lines[2] == 'ping':
            return 'PING'
    return None

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        decoded_data = data.decode().strip()
        command = parse_resp_command(decoded_data)
        if command == 'PING':
            conn.send(b"+PONG\r\n")

        elif not data.decode():
            conn.close()
            break

def main():
    while True:
        server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
        connection, _ = server_socket.accept()
        print("Connected", connection)
        print("Address", _)
        threading.Thread(target=handle_client, args=(connection,)).start()



if __name__ == "__main__":
    main()
