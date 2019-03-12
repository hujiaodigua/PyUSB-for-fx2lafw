import usb.core
import usb.util
import time
import sys
from vcd import VCDWriter

def OneBitFlip(bit):
    if bit == 0:
        return 1
    if bit == 1:
        return 0
    else:
        print('error in put')

def binary_search(lis, num):
    left = 0
    right = len(lis) - 1
    while left <= right:   #循环条件
        mid = (left + right) // 2   #获取中间位置，数字的索引（序列前提是有序的）
        if num < lis[mid]:  #如果查询数字比中间数字小，那就去二分后的左边找，
            right = mid - 1   #来到左边后，需要将右变的边界换为mid-1
        elif num > lis[mid]:   #如果查询数字比中间数字大，那么去二分后的右边找
            left = mid + 1    #来到右边后，需要将左边的边界换为mid+1
        else:
            return mid  #如果查询数字刚好为中间值，返回该值得索引
    return -1  #如果循环结束，左边大于了右边，代表没有找到

samplerate = 24000000 # 可设定的采样率

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

D0_timestamp = []
D0_Value = []
for i in range(1,len(buf_bin)):
    if buf_bin[i-1][7] != buf_bin[i][7]:
        D0_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
        D0_Value.append(int(buf_bin[i][7]))

D1_timestamp = []
D1_Value = []
for i in range(1,len(buf_bin)):
    if buf_bin[i-1][6] != buf_bin[i][6]:
        D1_timestamp.append(i)                           # 要注意timestamp为空的情况，说明这一个通道的信号全程一个值，就只有初始值就没有后面的writer.change过程
        D1_Value.append(int(buf_bin[i][6]))

D2_timestamp = []
D2_Value = []
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

# 查找索引
index_D0 = []
for i in range(0,len(D0_timestamp)):
    index_D0.append(binary_search(D_timestamp,D0_timestamp[i]))

index_D1 = []
for i in range(0,len(D1_timestamp)):
    index_D1.append(binary_search(D_timestamp,D1_timestamp[i]))

index_D2 = []
for i in range(0,len(D2_timestamp)):
    index_D2.append(binary_search(D_timestamp,D2_timestamp[i]))

# len(D_timestamp) * 4 的二维list(元素用None填充)
D_data = [[None] * 4 for row in range(len(D_timestamp))]

for i in range(0,len(D_timestamp)):
    D_data[i][0]= D_timestamp[i]

# 把D0_timestamp对应的value填入D_data中
'''for i in range(0,len(D0_timestamp)):
    # print(D_timestamp.index(D0_timestamp[i]))
    D_data[D_timestamp.index(D0_timestamp[i])][1] = D0_Value[i]'''
for i in range(0,len(index_D0)):
    D_data[index_D0[i]][1] = D0_Value[i]

# 把D1_timestamp对应的value填入D_data中
'''for i in range(0,len(D1_timestamp)):
    # print(D_timestamp.index(D1_timestamp[i]))
    D_data[D_timestamp.index(D1_timestamp[i])][2] = D1_Value[i]'''
for i in range(0,len(index_D1)):
    D_data[index_D1[i]][2] = D1_Value[i]

# 把D2_timestamp对应的value填入D_data中
'''for i in range(0,len(D2_timestamp)):
    # print(D_timestamp.index(D2_timestamp[i]))
    D_data[D_timestamp.index(D2_timestamp[i])][3] = D2_Value[i]'''
for i in range(0,len(index_D2)):
    D_data[index_D2[i]][3] = D2_Value[i]

del D_timestamp
del D0_Value
del D1_Value
del D2_Value


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

