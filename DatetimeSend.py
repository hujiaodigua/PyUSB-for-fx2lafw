#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import socket
import os
import sys
import time

def DatetimeSend(My_IP_address, My_Port, b_str_Sec):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((My_IP_address,My_Port))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('waiting connection...')


    conn, addr = s.accept()
    print('Accept new connection from {0}'.format(addr))
    conn.send(b'Hi, Welcome to the server!\n')
    conn.send(b_str_Sec)


if __name__ == '__main__':
    b_str_Sec = bytes(str(int(time.time()) + 10), encoding = 'utf8')
    DatetimeSend('192.168.0.101', 10000, b_str_Sec)