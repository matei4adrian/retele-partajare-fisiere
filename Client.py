import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENTS = set()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    CLIENTS.add(client)

    while True:
        response = client.recv(SIZE).decode(FORMAT)
        command, message = response.split("@")
        if command == "DISCONNECTED":
            print(f"[SERVER]: {message}")
            break
        elif command == "OK":
            print(f"{message}")
        response = input("> ")
        response = response.split(" ")
        command = response[0]
        if command == "HELP":
            client.send(command.encode(FORMAT))
        elif command == "LOGOUT":
            client.send(command.encode(FORMAT))
            break
        elif command == "LIST":
            client.send(command.encode(FORMAT))
        elif command == "DELETE":
            #client.send(f"{command}@{response[1]}".encode(FORMAT))
            for c in CLIENTS:
                c.sendall(f"{command}@{response[1]}".encode(FORMAT))
        elif command == "UPLOAD":
            path = response[1]
            with open(f"{path}", "a+") as f:
                text = f.read()
            filename = path.split("/")[-1]
            dataSent = f"{command}@{filename}@{text}"
            client.send(dataSent.encode(FORMAT))

    print("The client was disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()