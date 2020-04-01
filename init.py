#!/usr/bin/env python

from stats        import Stats
from plugs.system import uptime
from plugs.todo   import todo

if __name__ == '__main__':
    while (True):
        Stats(
            f"Uptime: {uptime()}\n" +
            f"{todo()}",
            timeout=10
        )
