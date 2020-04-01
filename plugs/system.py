from os import popen

def uptime():
    return popen('uptime -p').read().replace('up ', '')
