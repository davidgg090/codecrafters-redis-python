import logging
import socket
import threading


def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            decoded_data = data.decode().strip()
            logging.info("Received data: %s", decoded_data)

            if decoded_data.upper() == "PING":
                conn.send(b"+PONG\r\n")
            elif decoded_data.upper().startswith("ECHO "):
                res = decoded_data[5:] + "\r\n"
                conn.send(res.encode())
            else:
                res = "-ERR unknown command\r\n"
                conn.send(res.encode())
                print("Unknown command:", decoded_data)
                break
        except Exception as e:
            print("Error handling the command:", e)
            conn.close()
            break

    conn.close()
        

def main():
    while True:
        server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
        connection, _ = server_socket.accept()
        print("Connected", connection)
        print("Address", _)
        threading.Thread(target=handle_client, args=(connection,)).start()



if __name__ == "__main__":
    main()
