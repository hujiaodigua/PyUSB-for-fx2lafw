import sys
from vcd import VCDWriter
from array import array

buf = array('B', [250, 250, 250, 250, 250, 250, 249, 249, 249, 250, 250, 250, 250, 250, 250, 250, 250, 251, 251, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250
, 250, 250, 250, 250])


# 变量就是之前定义的
# 位置就是buf[i]的i，就是索引
# 值buf[i]的每一个二进制位(对2取余的结果是0还是1)

buf_bin = []

for i in range(0,len(buf)):
    buf_bin.append(bin(buf[i]).replace('0b',''))

D0_init = int(buf_bin[0][7])
D1_init = int(buf_bin[0][6])

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

# data的结构： | timestamp | value_counter_var0 | value_counter_var1 |
# 然后data应该是一个二维list
# 这样就是先把所有的timestamp和对应的value全部统计出来，按顺序放在data里，然后直接写入，因为VCDWriter是按行写入的，已经写入的行是不可以再修改的

# 去重合并
D_timestamp = list(set(D0_timestamp + D1_timestamp))
# 正向排序
D_timestamp.sort()

# len(D_timestamp) * 3 的二维list(元素用None填充)
D_data = [[None] * 3 for row in range(len(D_timestamp))]

for i in range(0,len(D_timestamp)):
    D_data[i][0]= D_timestamp[i]

# 把D0_timestamp对应的value填入D_data中
for i in range(0,len(D0_timestamp)):
    # print(D_timestamp.index(D0_timestamp[i]))
    D_data[D_timestamp.index(D0_timestamp[i])][1] = D0_Value[i]

for i in range(0,len(D1_timestamp)):
    # print(D_timestamp.index(D1_timestamp[i]))
    D_data[D_timestamp.index(D1_timestamp[i])][2] = D1_Value[i]


'''D_data = [ [3,1,None],    # len(D0_data)算的是最外层[]的长度
           [6,0,1],
           [9,1,0],
           [18,0,1]]'''


with VCDWriter(sys.stdout, timescale='1 ns', date='today', comment='Acquisition with 8/8 channels at 20 kHz',version='libsigrok 0.5.1') as writer:  # timescale='1 ns'这里单位不对有问题
    counter_var0 = writer.register_var('libsigrok', 'D0', 'wire',size=1,init=D0_init,ident='#')    # init是这个var的初始值
    counter_var1 = writer.register_var('libsigrok', 'D1', 'wire', size=1,init=D1_init,ident='!')   # init是这个var的初始值

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

    '''writer.change(counter_var0, 100, 0)    # writer.change(变量,时间戳（位置）,翻转（值）)，0就是前面都是1这一位从1翻转为0
    writer.change(counter_var1, 100, 0)

    writer.change(counter_var0, 1000, 1)   # writer.change(变量,时间戳（位置）,翻转)，1就是前面都是0这一位从1翻转为1
    writer.change(counter_var1, 1000, 1)

    writer.change(counter_var0, 1500, 0)
    writer.change(counter_var1, 1500, 0)'''



print('ok')


