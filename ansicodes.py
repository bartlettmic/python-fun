#!/usr/bin/python3
import sys, tty
tty.setraw(sys.stdin)
while True:
    char = sys.stdin.read(1)
    if ord(char) == 3:
        break
    print(ord(char))
    sys.stdout.write(u"\u001b[1000D")
        
