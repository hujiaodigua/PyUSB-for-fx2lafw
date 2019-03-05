import sys
from vcd import VCDWriter
from array import array

with VCDWriter(sys.stdout, timescale='1 ns', date='today', comment='Acquisition with 8/8 channels at 20 kHz',version='libsigrok 0.5.1') as writer:
    counter_var1 = writer.register_var('libsigrok', 'D0', 'wire',size=1,init=1,ident='!')    # init是这个var的初始值
    counter_var2 = writer.register_var('libsigrok', 'D1', 'wire', size=1,init=1,ident='#')   # init是这个var的初始值
    # for timestamp, value in enumerate(range(0, 1, 1)):

    writer.change(counter_var1, 100, 0)    # writer.change(变量,时间戳（位置）,翻转（值）)，0就是前面都是1这一位从1翻转为0
    writer.change(counter_var2, 100, 0)

    writer.change(counter_var1, 1000, 1)   # writer.change(变量,时间戳（位置）,翻转)，1就是前面都是0这一位从1翻转为1
    writer.change(counter_var2, 1000, 1)

    writer.change(counter_var1, 1500, 0)
    writer.change(counter_var2, 1500, 0)