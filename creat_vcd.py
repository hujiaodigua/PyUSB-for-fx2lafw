import sys
from vcd import VCDWriter
from array import array

with VCDWriter(sys.stdout, timescale='1 ns', date='today', comment='Acquisition with 8/8 channels at 20 kHz',version='libsigrok 0.5.1') as writer:
    counter_var1 = writer.register_var('libsigrok', 'D0', 'wire',size=1,init=1,ident='!')    # init�����var�ĳ�ʼֵ
    counter_var2 = writer.register_var('libsigrok', 'D1', 'wire', size=1,init=1,ident='#')   # init�����var�ĳ�ʼֵ
    # for timestamp, value in enumerate(range(0, 1, 1)):

    writer.change(counter_var1, 100, 0)    # writer.change(����,ʱ�����λ�ã�,��ת��ֵ��)��0����ǰ�涼��1��һλ��1��תΪ0
    writer.change(counter_var2, 100, 0)

    writer.change(counter_var1, 1000, 1)   # writer.change(����,ʱ�����λ�ã�,��ת)��1����ǰ�涼��0��һλ��1��תΪ1
    writer.change(counter_var2, 1000, 1)

    writer.change(counter_var1, 1500, 0)
    writer.change(counter_var2, 1500, 0)