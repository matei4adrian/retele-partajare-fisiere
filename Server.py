import os
import socket
import threading
import shutil

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_FILES = "server_data"

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connection.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = connection.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        command = data[0]
        if command == "LIST":
            files = os.listdir(SERVER_FILES)
            dataSent = "OK@"
            if len(files) == 0:
                dataSent += "The server directory doesn't contain files."
            else:
                dataSent += "\n".join(f for f in files)
            connection.send(dataSent.encode(FORMAT))
        elif command == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_FILES, name)
            with open(filepath, "w+") as f:
                f.write(text)
            dataSent = "OK@File uploaded with success."
            connection.send(dataSent.encode(FORMAT))
        elif command == "DELETE":
            files = os.listdir(SERVER_FILES)
            dataSent = "OK@"
            filename = data[1]
            if len(files) == 0:
                dataSent += "The server directory doesn't contain files"
            else:
                if filename in files:
                    # shutil.rmtree(f"{SERVER_DATA_PATH}/{filename}")
                    os.remove(f"{SERVER_FILES}/{filename}")
                    dataSent += "File deleted with success. "
                else:
                    dataSent += "File not found."
            connection.send(dataSent.encode(FORMAT))
        elif command == "LOGOUT":
            break
        elif command == "HELP":
            data = "OK@"
            data += "LIST: Show files saved on the server.\n"
            data += "UPLOAD <path>: Upload a file to server.\n"
            data += "DELETE <filename>: Delete a file saved on the server.\n"
            data += "LOGOUT: Leave server.\n"
            data += "HELP: Show commands list."
            connection.send(data.encode(FORMAT))
    print(f"[DISCONNECTED] {address} disconnected")
    connection.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()