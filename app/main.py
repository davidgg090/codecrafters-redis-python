import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, address = server_socket.accept()
    connection.send(b"+PONG\r\n")
    while True:
        data = connection.recv(1024)
        if not data:
            break
        connection.send(b"+PONG\r\n")


if __name__ == "__main__":
    main()
