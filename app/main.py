import socket
import threading


def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            break
        decoded_data = data.decode()

        if decoded_data.startswith("ECHO "):
            argument = decoded_data[5:].strip()
            response = f"${len(argument)}\r\n{argument}\r\n"
            conn.send(response.encode())
        elif data == b"*1\r\n$4\r\nping\r\n":
            res = "+PONG\r\n"
            conn.send(res.encode())
        

def main():
    while True:
        server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
        connection, _ = server_socket.accept()
        print("Connected", connection)
        print("Address", _)
        threading.Thread(target=handle_client, args=(connection,)).start()



if __name__ == "__main__":
    main()
