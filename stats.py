#!/usr/bin/env python

import requests
import json
import datetime

from time   import sleep
from typing import Dict

class Config:
    Config = Dict[str, str]

    def __init__(self, path):
        self.path = path
        self.config = {}

    def setup(self) -> Config:
        try:
            with open(self.path) as f:
                self.config = json.load(f)
        except OSError:
            print("{0} was not found or the file is corrupted."
                  .format(self.path))
        return self.config

class Gist:
    ISSUES_URL = "https://github.com/0-l/stats/issues/new"

    RESPONSES = {
        200: 'Gist successfully updated.',
        401: 'Invalid content.',
        404: 'Filename not found.',
        500: "\n".join(
            ["Something broke :(", "Report this bug at: {0}"
                .format(ISSUES_URL)]
        )
    }

    def __init__(self):
        self.config = Config('./config.json').setup()
        self.base_url = 'https://api.github.com/gists/' + self.config['hash']

    def handle_status(self, status: int):
        if status != 200:
            raise SystemExit(self.RESPONSES[status])
        print("-> " + self.RESPONSES[status])

    def get_files(self):
        try:
            request = requests.get(
                self.base_url,
                auth=(self.config['user'], self.config['token'])
            )
            files = request.json()['files']

            return next(iter(files.values()))
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def update(self, content: str):
        files = self.get_files()
        payload = {
            'files': {
                files['filename']: {
                    'content': content
                }
            }
        }

        response = requests.post(
            self.base_url,
            data=json.dumps(payload),
            auth=(self.config['user'], self.config['token'])
        )
        self.handle_status(response.status_code)

class Stats:
    def __init__(self, content, timeout = 5):
        self.banner()
        self.content = content
        self.timeout = timeout
        self.gist = Gist()
        self.start()

    def banner(self):
        print('-' * 20)
        print('>> STARTING')

    def start(self):
        while (True):
            self.gist.update(str(self.content))
            sleep(60 * self.timeout)