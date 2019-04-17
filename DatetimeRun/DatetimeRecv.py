#!/usr/bin/env python3
# coding=utf-8

import time
import subprocess
import sys
import os
import shutil
import socket


def DatetimeRecv(Server_IP_address, Port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((Server_IP_address, Port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    
    data_from_service = s.recv(64)
    print(data_from_service)

    b_str_Sec = s.recv(64)
    # print(bytes.decode(b_str_Sec))
    return bytes.decode(b_str_Sec)
    


def DatetimeRun(str_Sec):
    Command = './Datetime_GPIO_Interrupt ' + 'timestamp.txt ' + str_Sec
    os.system(Command)

if __name__ == "__main__":
    str_Sec = DatetimeRecv('192.168.0.106', 10000)
    DatetimeRun(str_Sec)
