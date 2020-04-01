from os import path

def todo():
    with open(f"{path.expanduser('~/Documents')}/todo.org", 'r') as f:
        return f.read()
