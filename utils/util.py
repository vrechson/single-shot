#! /usr/bin/python3

lines = []
payload = '{newline}'
with open("req") as f:
    lines = f.read().splitlines()

print(payload.join(lines))
