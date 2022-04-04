import socket
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back


init()


client_color = Fore.WHITE


colors = {
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "yellow": Fore.YELLOW,
    "cyan": Fore.CYAN,
    "pink": Fore.LIGHTMAGENTA_EX
}


server_host = input("Enter server address: ")
server_port = 8392
separator_token = "<SEP>"

socket = socket.socket()
print(f"[*] Connecting to {server_host}:{server_port}")
try:
    socket.connect((server_host, server_port))
except Exception as e:
    print(f"[!] Error: {e}")
    exit()
print("[+] Connected.")


name = input("Enter a name: ")

while True:
    color_input = input("Enter a color: ").lower()
    if color_input in colors:
        client_color = colors.get(color_input)
        break
    else:
        print("Invalid color!")
        continue


def listen():
    while True:
        message = socket.recv(1024).decode()
        print("\n" + message)


t = Thread(target=listen)
t.daemon = True
t.start()


while True:
    to_send = input("> ")
    if to_send.lower() == "quit":
        break
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    socket.send(to_send.encode())

socket.close()
