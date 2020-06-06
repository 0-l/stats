from os import path

directory = '~/Documents/Programming'
filename = 'todo.org'

def todo():
    with open(f"{path.expanduser(directory)}/{filename}", 'r') as f:
        return f.read()
