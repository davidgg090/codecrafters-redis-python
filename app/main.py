import socket
import threading


def parse_resp_command(data):
    lines = data.split('\r\n')
    command = None
    arguments = []
    if lines[0].startswith('*'):
        num_elements = int(lines[0][1:])
        for i in range(1, num_elements * 2, 2):
            if lines[i].startswith('$'):
                arguments.append(lines[i + 1])
        if arguments:
            command = arguments[0].upper()
            arguments = arguments[1:]
    return command, arguments

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        decoded_data = data.decode().strip()
        command, arguments = parse_resp_command(decoded_data)
        if command == 'PING':
            conn.send(b"+PONG\r\n")
        elif command == 'ECHO' and arguments:
            message = arguments[0]
            response = f"${len(message)}\r\n{message}\r\n"
            conn.send(response.encode())
        elif command == 'SET' and arguments:
            key = arguments[0]
            value = arguments[1]
            conn.send(b"+OK\r\n")
        elif command == 'GET' and arguments:
            key = arguments[0]
            value = "Hello"
            response = f"${len(value)}\r\n{value}\r\n"
            conn.send(response.encode())
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
