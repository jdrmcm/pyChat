import socket
from threading import Thread


server_host = "0.0.0.0"
server_port = 8392
separator_token = "<SEP>"


client_sockets = set()
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((server_host, server_port))
socket.listen(5)
print(f"[*] Listening as {server_host}:{server_port}")


def listen(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


while True:
    client_socket, client_address = socket.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen, args=(client_socket,))
    t.daemon = True
    t.start()


for cs in client_sockets:
    cs.close()
socket.close()
