#!/usr/bin/env python
from socket import *
def sockconn():
    try:
        s=socket(AF_INET, SOCK_STREAM)
        s.connect(('127.0.0.1', 7070))
        return s
    except Except, e:
        print e
def main():
    input = ''
    smain = sockconn()
    while(1):
        input=raw_input("enter message > ")
        if (input == "/conn"):
            smain=sockconn()
        elif (input == "/close"):
            smain.close()
        elif (input == "/q"):
            break
        else:
            smain.send(input)
    smain.close()
if __name__ == "__main__": main() 
