#!/usr/bin/env python3
# coding=utf-8

import usb

'''
| 数据方向 | bmRequest | bRequest |
|上传至芯片|   0x40    |   0xa0   |
|从芯片下载|   0xc0    |   0xa0   |
'''

'''RAM导出函数'''
def dump_ram(offset,lenth):
    data=handle.controlMsg(requestType=0xc0,request=0xa0,value=offset,index=0x00,buffer=lenth,timeout=100)
    print(data)

'''RAM写入函数'''
def write_ram(offset,buf):
    handle.controlMsg(requestType=0x40,request=0xa0,value=offset,index=0x00,buffer=buf,timeout=100)

'''导出与写入批量传输函数'''
def bulk(dendp,lenthl,wendp,buf): # *endp 为端点号实数
    # 初始化 USB 配置
    handle.detachKernelDriver(0) # 获得 Linux 底层的设备控制权
    if dendp !=" ": # 为导出模式时
        data=handle.bulkRead(dendp,lenthl,100)
    if wendp !=" ": # 为写入模式时
        handle.bulkWrite(wendp,buf,1000)

# VID与PID编号
vendor_id = 0x0925
product_id = 0x3881
# 搜索并加载
busses = usb.busses()
dev=""    # 强制制定dev的类型为字符
for bus in busses:    # 遍历所有USB组
    devices = bus.devices
    for d in devices:    # 遍历所有此组上的设备
        if (d.idVendor == vendor_id) and (d.idProduct == product_id):
            dev = d    # 若PID与VID均符合,将此设备传给字符变量dev,供后面调用
            print("PID与VID符合")
            break
handle=dev.open()    # 打开设备

# 进行操作

handle.releaseInterface() # 释放接口
# dev.close() # 关闭设备