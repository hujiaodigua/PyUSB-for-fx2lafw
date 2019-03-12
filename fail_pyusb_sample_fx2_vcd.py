import usb.core
import usb.util
import time
import sys
from vcd import VCDWriter
import multiprocessing
import os

def OneBitFlip(bit):
    if bit == 0:
        return 1
    if bit == 1:
        return 0
    else:
        print('error in put')

def read_task(D_timestamp,D0_timestamp,D1_timestamp,D2_timestamp,D_data,D0_Value,D1_Value,D2_Value,flag):

    filename = 'mailbox_samples.txt'
    file_object = open(filename,'r')

    buf_bin = []

    buf_bin = file_object.readlines()

    for i in range(0,len(buf_bin)):
        buf_bin[i] = buf_bin[i].replace('\n','')
    file_object.close()

    '''############'''
    '''按vcd格式保存'''
    '''############'''

    D0_init = int(buf_bin[0][7])
    D1_init = int(buf_bin[0][6])
    D2_init = int(buf_bin[0][5])

    # D0_timestamp = []
    # D0_Value = []
    for i in range(1,len(buf_bin)):
        if buf_bin[i-1][7] != buf_bin[i][7]:
            D0_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
            D0_Value.append(int(buf_bin[i][7]))

    # D1_timestamp = []
    # D1_Value = []
    for i in range(1,len(buf_bin)):
        if buf_bin[i-1][6] != buf_bin[i][6]:
            D1_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
            D1_Value.append(int(buf_bin[i][6]))

    # D2_timestamp = []
    # D2_Value = []
    for i in range(1,len(buf_bin)):
        if buf_bin[i-1][5] != buf_bin[i][5]:
            D2_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
            D2_Value.append(int(buf_bin[i][5]))
    del buf_bin


    # data的结构： | timestamp | value_counter_var0 | value_counter_var1 |
    # 然后data应该是一个二维list
    # 这样就是先把所有的timestamp和对应的value全部统计出来，按顺序放在data里，然后直接写入，因为VCDWriter是按行写入的，已经写入的行是不可以再修改的

    # 去重合并
    D_timestamp = list(set(D0_timestamp + D1_timestamp + D2_timestamp))
    # 正向排序
    D_timestamp.sort()

    # len(D_timestamp) * 4 的二维list(元素用None填充)
    D_data = [[None] * 4 for row in range(len(D_timestamp))]

    for i in range(0,len(D_timestamp)):
        D_data[i][0]= D_timestamp[i]

    flag = 1

'''
index_D0_timestamp = []
for i in range(0,len(D0_timestamp)):
    index_D0_timestamp.append(D_timestamp.index(D0_timestamp[i]))
'''

def D0_Value_fill(self):
    # 把D0_timestamp对应的value填入D_data中
    for i in range(0,len(D0_timestamp)):
        # print(D_timestamp.index(D0_timestamp[i]))
        D_data[D_timestamp.index(D0_timestamp[i])][1] = D0_Value[i]

def D1_Value_fill(self):
    # 把D1_timestamp对应的value填入D_data中
    for i in range(0,len(D1_timestamp)):
        # print(D_timestamp.index(D1_timestamp[i]))
        D_data[D_timestamp.index(D1_timestamp[i])][2] = D1_Value[i]

def D2_Value_fill():
    # 把D2_timestamp对应的value填入D_data中
    for i in range(0,len(D2_timestamp)):
        # print(D_timestamp.index(D2_timestamp[i]))
        D_data[D_timestamp.index(D2_timestamp[i])][3] = D2_Value[i]


def vcd_task(self):
    del D_timestamp
    del D0_Value
    del D1_Value
    del D2_Value

    samplerate = 24000000  # 可设定的采样率

    '''D_data = [ [3,1,None],    # len(D0_data)算的是最外层[]的长度
               [6,0,1],
               [9,1,0],
               [18,0,1]]'''


    # 注意timescale在writer.py中值只能设置为TIMESCALE_NUMS = [1, 10, 100]，需要其他间隔值和采样频率对上的话，在TIMESCALE_NUMS把间隔值添加进去即可
    if samplerate == 24000000:
        timescale_unit = '41666667 fs'

    if samplerate == 20000:
        timescale_unit = '50 us'

    with VCDWriter(sys.stdout, timescale=timescale_unit, date='today', comment='Acquisition with 8/8 channels at 24 MHz',version='libsigrok 0.5.1') as writer:  # timescale='1 ns'这里单位不对有问题
        counter_var0 = writer.register_var('libsigrok', 'D0', 'wire',size=1,init=D0_init,ident='#')    # init是这个var的初始值
        counter_var1 = writer.register_var('libsigrok', 'D1', 'wire', size=1,init=D1_init,ident='!')   # init是这个var的初始值
        counter_var2 = writer.register_var('libsigrok', 'D2', 'wire', size=1, init=D2_init, ident='$')  # init是这个var的初始值

        # for i in range(0, len(D0_timestamp)):
        '''for i in range(0,len(D0_timestamp)):
            writer.change(counter_var0, D0_timestamp[i], D0_Value[i])
            # for j in range(0,len(D1_timestamp)):
            writer.change(counter_var1, D1_timestamp[j], D1_Value[j])'''

        #for i in range(0, len(D1_timestamp)):
        #    writer.change(counter_var1, D1_timestamp[i], int(buf_bin[(D1_timestamp[i])][6]))

        for i in range(0,len(D_data)):
            if D_data[i][1] != None:
                writer.change(counter_var0, D_data[i][0], D_data[i][1])
            if D_data[i][2] != None:
                writer.change(counter_var1, D_data[i][0], D_data[i][2])
            if D_data[i][3] != None:
                writer.change(counter_var2, D_data[i][0], D_data[i][3])
        del D_data

    flag = -1

if __name__=="__main__":
    with multiprocessing.Manager() as MG:
        D_timestamp = multiprocessing.Manager().list()
        D0_timestamp = multiprocessing.Manager().list()
        D1_timestamp = multiprocessing.Manager().list()
        D2_timestamp = multiprocessing.Manager().list()
        D_data = multiprocessing.Manager().list()
        D0_Value = multiprocessing.Manager().list()
        D1_Value = multiprocessing.Manager().list()
        D2_Value = multiprocessing.Manager().list()
    flag = multiprocessing.Value("d", 0)

    P_read = multiprocessing.Process(target=read_task, args=(D_timestamp,D0_timestamp,D1_timestamp,D2_timestamp,D_data,D0_Value,D1_Value,D2_Value,flag))
    P_read.start()
    P_read.join()

    if flag == 1:
        P0 = multiprocessing.Process(target=D0_Value_fill, args=('test',))
        P1 = multiprocessing.Process(target=D1_Value_fill, args=('test',))
        P2 = multiprocessing.Process(target=D2_Value_fill, args=('test',))
        P0.start()
        P0.join()
        P1.start()
        P1.join()
        P2.start()
        P2.join()

    if flag == -1:
        P_vcd= multiprocessing.Process(target=vcd_task, args=('test',))
        P_vcd.start()
        P_vcd.join()