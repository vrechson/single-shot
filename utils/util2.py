#! /usr/bin/python3

lines = []

with open("shellshock-payloads.txt") as f:
    lines = f.read().splitlines()

with open('payloads.txt', 'w') as w:
    for idx, line in enumerate(lines):
        w.write('"payload{}": {}\n'.format(idx, line))