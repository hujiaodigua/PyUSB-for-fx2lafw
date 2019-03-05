import usb.core
import usb.util
import time
import sys
from vcd import VCDWriter
from array import array

from array import array

# 先开pulseview保证fx2有固件

# find our device
dev = usb.core.find(idVendor=0x0925, idProduct=0x3881)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()
# print('===============================')
# print(dev)

# get an endpoint instance
cfg = dev.get_active_configuration()
# print('===============================')
# print(cfg)

intf = cfg[(0,0)]
# print('===============================')
# print(intf)

ret = dev.ctrl_transfer(0xc0,0xb0,0,0,0x02,0x00)
# print(ret)

# time.sleep(1)
ret = dev.ctrl_transfer(0xc0,0xb2,0,0,0x01,0x00)
# print(ret)

# time.sleep(1)

Setdata = [0x00,0x05,0xdb]
ret = dev.ctrl_transfer(0x40,0xb1,0,0,Setdata,0x0300)
# print(ret)

# 读取数据
buf = intf[0].read(512)

'''############'''
'''按vcd格式保存'''
'''############'''

buf_bin = []

for i in range(0,len(buf)):
    buf_bin.append(bin(buf[i]).replace('0b',''))

D0_init = int(buf_bin[0][7])
D1_init = int(buf_bin[0][6])
D2_init = int(buf_bin[0][5])

D0_timestamp = []
D0_Value = []
for i in range(1,len(buf)):
    if buf_bin[i-1][7] != buf_bin[i][7]:
        D0_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
        D0_Value.append(int(buf_bin[i][7]))

D1_timestamp = []
D1_Value = []
for i in range(1,len(buf)):
    if buf_bin[i-1][6] != buf_bin[i][6]:
        D1_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
        D1_Value.append(int(buf_bin[i][6]))

D2_timestamp = []
D2_Value = []
for i in range(1,len(buf)):
    if buf_bin[i-1][5] != buf_bin[i][5]:
        D2_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
        D2_Value.append(int(buf_bin[i][5]))

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

# 把D0_timestamp对应的value填入D_data中
for i in range(0,len(D0_timestamp)):
    # print(D_timestamp.index(D0_timestamp[i]))
    D_data[D_timestamp.index(D0_timestamp[i])][1] = D0_Value[i]

# 把D1_timestamp对应的value填入D_data中
for i in range(0,len(D1_timestamp)):
    # print(D_timestamp.index(D1_timestamp[i]))
    D_data[D_timestamp.index(D1_timestamp[i])][2] = D1_Value[i]

# 把D2_timestamp对应的value填入D_data中
for i in range(0,len(D2_timestamp)):
    # print(D_timestamp.index(D2_timestamp[i]))
    D_data[D_timestamp.index(D2_timestamp[i])][3] = D2_Value[i]


'''D_data = [ [3,1,None],    # len(D0_data)算的是最外层[]的长度
           [6,0,1],
           [9,1,0],
           [18,0,1]]'''


# 注意timescale在writer.py中值只能设置为TIMESCALE_NUMS = [1, 10, 100]，需要其他间隔值和采样频率对上的话，在TIMESCALE_NUMS把间隔值添加进去即可
with VCDWriter(sys.stdout, timescale='50 us', date='today', comment='Acquisition with 8/8 channels at 20 kHz',version='libsigrok 0.5.1') as writer:  # timescale='1 ns'这里单位不对有问题
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

    '''writer.change(counter_var0, 100, 0)    # writer.change(变量,时间戳（位置）,翻转（值）)，0就是前面都是1这一位从1翻转为0
    writer.change(counter_var1, 100, 0)

    writer.change(counter_var0, 1000, 1)   # writer.change(变量,时间戳（位置）,翻转)，1就是前面都是0这一位从1翻转为1
    writer.change(counter_var1, 1000, 1)

    writer.change(counter_var0, 1500, 0)
    writer.change(counter_var1, 1500, 0)'''



# print('ok')


# rdata = array('H')
# rdata.fromlist([0]*128)
# dev.bulk_read(0x82,rdata)

# time.sleep(1)




'''# if dev is None:
    # do something
# get the configuration
cfg = dev.get_active_configuration()

intface = cfg[(0,1)]
ep = intface[6]

# get interface 0
intface_01 = cfg[(0,1)]
intface_02 = cfg[(0,2)]
intface_03 = cfg[(0,3)]

print(intface_01[6])

# get endpoint,下面这几个point，显示实体不存在，01的6应该是control out，但是这个EndPoint是非法的，会报错，
# 现在只要能找到正确的输入/输出Endpoint，问题就解决了
endpoint_0x2_BulkOut = intface_01[2]
endpoint_0x81_BulkIn = intface_01[1]

endpoint_0x2_InterruptOut = intface_02[2]
endpoint_0x81_InterruptIn = intface_02[1]

GetFwVersion = [0xc0,0xb0,0x00,0x00,0x00,0x00,0x02,0x00]

GetFwVersion = [0x40,0xb1,0x00,0x00,0x00,0x00,0x03 ,0x00]

bytes_writed = intface_01[1].write(GetFwVersion)

# buffer = endpoint_0x2_BulkOut.read(32)

print('123')'''